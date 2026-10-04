#!/usr/bin/env python3
"""
Script: merge_and_sync_all_datasets.py
Purpose:
1. Merges raw reviews from US global scrape and BD archive scrape across Grameenphone, Robi, and Banglalink.
2. Strictly deduplicates records: exact same operator, timestamp, text, and user.
3. Reuses existing classifications for already processed reviews and runs the full model suite on any new reviews.
4. Saves the complete multi-year master classified dataset (N=398,193).
5. Isolates the common temporal duration where ALL THREE operators have simultaneous reviews (Oct 24, 2023 to Sep 30, 2026, N=248,507).
"""

import sys
import time
import json
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
import torch
import torch.nn as nn

warnings.filterwarnings("ignore", category=UserWarning)

# Define PyTorch architectures matching the pickled models
class Vocabulary:
    def __init__(self, min_freq=2):
        self.min_freq = min_freq
        self.word2idx = {"<pad>": 0, "<unk>": 1}
        self.idx2word = {0: "<pad>", 1: "<unk>"}

    def transform(self, text, max_len=40):
        words = str(text).lower().split()[:max_len]
        seq = [self.word2idx.get(w, 1) for w in words]
        return seq + [0] * (max_len - len(seq))


class BahdanauAttention(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.w = nn.Linear(hidden_dim, hidden_dim)
        self.v = nn.Linear(hidden_dim, 1, bias=False)

    def forward(self, rnn_outputs):
        energy = torch.tanh(self.w(rnn_outputs))
        weights = torch.softmax(self.v(energy), dim=1)
        context = torch.sum(weights * rnn_outputs, dim=1)
        return context, weights


class HybridBiLSTMAttention(nn.Module):
    def __init__(self, vocab_size, num_classes, embed_dim=128, hidden_dim=128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.bilstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.attention = BahdanauAttention(hidden_dim * 2)
        self.fc = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(hidden_dim * 2, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        embedded = self.embedding(x)
        outputs, _ = self.bilstm(embedded)
        context, _ = self.attention(outputs)
        return self.fc(context)


def load_all_models(repo_root: Path):
    ml_dir = repo_root / "ml" / "models"
    dl_dir = repo_root / "dl" / "models"

    print("Loading classification model suite...")
    sent_ensemble = joblib.load(ml_dir / "sentiment_voting_classifier.joblib")
    cat_ensemble = joblib.load(ml_dir / "category_voting_classifier.joblib")
    sent_lr = joblib.load(ml_dir / "primary_logistic_regression.joblib")
    sent_svc = joblib.load(ml_dir / "challenger_linearsvc.joblib")
    cat_lr = joblib.load(ml_dir / "category_logistic_regression.joblib")
    cat_svc = joblib.load(ml_dir / "category_linearsvc.joblib")

    vocab = joblib.load(dl_dir / "bilstm_vocab.joblib")
    sent_le = joblib.load(dl_dir / "sent_le.joblib")
    cat_le = joblib.load(dl_dir / "cat_le.joblib")

    bilstm_sent = HybridBiLSTMAttention(len(vocab.word2idx), len(sent_le.classes_))
    bilstm_sent.load_state_dict(torch.load(dl_dir / "bilstm_sentiment_model.pt", map_location="cpu"))
    bilstm_sent.eval()

    bilstm_cat = HybridBiLSTMAttention(len(vocab.word2idx), len(cat_le.classes_))
    bilstm_cat.load_state_dict(torch.load(dl_dir / "bilstm_category_model.pt", map_location="cpu"))
    bilstm_cat.eval()

    return {
        "sent_ensemble": sent_ensemble,
        "cat_ensemble": cat_ensemble,
        "sent_lr": sent_lr,
        "sent_svc": sent_svc,
        "cat_lr": cat_lr,
        "cat_svc": cat_svc,
        "vocab": vocab,
        "sent_le": sent_le,
        "cat_le": cat_le,
        "bilstm_sent": bilstm_sent,
        "bilstm_cat": bilstm_cat,
    }


def classify_subset(df: pd.DataFrame, models: dict, batch_size: int = 10000):
    total = len(df)
    if total == 0:
        return df

    texts = df["review_text"].fillna(" ").astype(str).str.strip().tolist()
    safe_texts = [t if len(t) > 0 else " " for t in texts]

    sent_ens_preds, sent_ens_confs = [], []
    cat_ens_preds, cat_ens_confs = [], []
    sent_lr_preds, sent_svc_preds = [], []
    cat_lr_preds, cat_svc_preds = [], []
    bilstm_sent_preds, bilstm_cat_preds = [], []

    vocab = models["vocab"]
    sent_le = models["sent_le"]
    cat_le = models["cat_le"]

    num_batches = (total + batch_size - 1) // batch_size
    t0 = time.time()

    for b_idx in range(num_batches):
        start = b_idx * batch_size
        end = min(start + batch_size, total)
        chunk = safe_texts[start:end]

        # 1. Classical Ensemble
        sent_probs = models["sent_ensemble"].predict_proba(chunk)
        sent_preds = models["sent_ensemble"].classes_[np.argmax(sent_probs, axis=1)]
        sent_confs = np.max(sent_probs, axis=1)

        cat_probs = models["cat_ensemble"].predict_proba(chunk)
        cat_preds = models["cat_ensemble"].classes_[np.argmax(cat_probs, axis=1)]
        cat_confs = np.max(cat_probs, axis=1)

        sent_ens_preds.extend(sent_preds)
        sent_ens_confs.extend(np.round(sent_confs, 4))
        cat_ens_preds.extend(cat_preds)
        cat_ens_confs.extend(np.round(cat_confs, 4))

        # 2. Components
        sent_lr_preds.extend(models["sent_lr"].predict(chunk))
        sent_svc_preds.extend(models["sent_svc"].predict(chunk))
        cat_lr_preds.extend(models["cat_lr"].predict(chunk))
        cat_svc_preds.extend(models["cat_svc"].predict(chunk))

        # 3. BiLSTM
        seqs = torch.tensor([vocab.transform(t) for t in chunk], dtype=torch.long)
        with torch.no_grad():
            b_s_out = models["bilstm_sent"](seqs)
            b_c_out = models["bilstm_cat"](seqs)
            b_s_idx = b_s_out.argmax(dim=1).numpy()
            b_c_idx = b_c_out.argmax(dim=1).numpy()

        bilstm_sent_preds.extend(sent_le.inverse_transform(b_s_idx))
        bilstm_cat_preds.extend(cat_le.inverse_transform(b_c_idx))

    df["predicted_sentiment"] = sent_ens_preds
    df["sentiment_confidence"] = sent_ens_confs
    df["predicted_category"] = cat_ens_preds
    df["category_confidence"] = cat_ens_confs
    df["sentiment_logistic"] = sent_lr_preds
    df["sentiment_linearsvc"] = sent_svc_preds
    df["sentiment_bilstm"] = bilstm_sent_preds
    df["category_logistic"] = cat_lr_preds
    df["category_linearsvc"] = cat_svc_preds
    df["category_bilstm"] = bilstm_cat_preds
    return df


def main():
    repo_root = Path(__file__).resolve().parent.parent.parent
    raw_glob_dir = repo_root / "scraped_data_global_2020_2026" / "raw"
    raw_arch_dir = repo_root / "archive" / "scraped_data_2020" / "raw"
    cls_dir = repo_root / "scraped_data_global_2020_2026" / "classified"
    cls_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 75)
    print("MERGING & DEDUPLICATING US AND BD REGIONAL DATASETS")
    print("=" * 75)

    operator_files = [
        ("Grameenphone", raw_arch_dir / "mygp_scraped_2020_to_sep2026.csv", raw_glob_dir / "mygp_global_2020_to_sep2026.csv"),
        ("Robi", raw_arch_dir / "myrobi_scraped_2020_to_sep2026.csv", raw_glob_dir / "myrobi_global_2020_to_sep2026.csv"),
        ("Banglalink", raw_arch_dir / "mybl_scraped_2020_to_sep2026.csv", raw_glob_dir / "mybl_global_2020_to_sep2026.csv"),
    ]

    # Load existing classified dataset to reuse predictions
    existing_cls_file = cls_dir / "all_operators_classified_global_2020_2026.csv"
    if existing_cls_file.exists():
        print(f"Loading existing classified dataset ({existing_cls_file.name})...")
        existing_cls = pd.read_csv(existing_cls_file, low_memory=False)
        existing_cls["review_date"] = pd.to_datetime(existing_cls["review_date"], errors="coerce")
        existing_cls["review_text"] = existing_cls["review_text"].fillna("").astype(str).str.strip()
        existing_cls["user_name"] = existing_cls["user_name"].fillna("").astype(str).str.strip()
    else:
        existing_cls = None

    merged_operator_dfs = []
    models = None

    for op_name, f_bd, f_us in operator_files:
        print(f"\nProcessing {op_name}...")
        df_bd = pd.read_csv(f_bd, low_memory=False)
        df_us = pd.read_csv(f_us, low_memory=False)

        # Standardize fields
        for df in [df_bd, df_us]:
            df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
            df["review_text"] = df["review_text"].fillna("").astype(str).str.strip()
            df["user_name"] = df["user_name"].fillna("").astype(str).str.strip()
            df["operator"] = op_name
            if "review_id" not in df.columns:
                df["review_id"] = [f"{op_name[:2].lower()}_bd_{i}" for i in range(len(df))]

        combined = pd.concat([df_us, df_bd], ignore_index=True)
        raw_len = len(combined)

        # Strict deduplication: exact operator, review_date, review_text, user_name
        dedup = combined.drop_duplicates(subset=["operator", "review_date", "review_text", "user_name"]).copy()
        dedup_len = len(dedup)
        print(f"  Raw: {raw_len:,d} -> Deduplicated: {dedup_len:,d} (Dropped {raw_len - dedup_len:,d} exact duplicates)")
        print(f"  Range: {dedup['review_date'].min()} to {dedup['review_date'].max()}")

        # Check existing classifications
        if existing_cls is not None:
            op_existing = existing_cls[existing_cls["operator"] == op_name]
            cls_cols = [
                "predicted_sentiment", "sentiment_confidence", "predicted_category", "category_confidence",
                "sentiment_logistic", "sentiment_linearsvc", "sentiment_bilstm",
                "category_logistic", "category_linearsvc", "category_bilstm"
            ]
            
            merged = dedup.merge(
                op_existing[["review_date", "review_text", "user_name"] + cls_cols],
                on=["review_date", "review_text", "user_name"],
                how="left"
            )
            
            unclassified_mask = merged["predicted_sentiment"].isna()
            num_unclassified = unclassified_mask.sum()
            print(f"  Matched {len(merged) - num_unclassified:,d} existing predictions. Unclassified: {num_unclassified:,d}")

            if num_unclassified > 0:
                if models is None:
                    models = load_all_models(repo_root)
                unclassified_df = merged[unclassified_mask].copy()
                classified_unclass = classify_subset(unclassified_df, models)
                for col in cls_cols:
                    merged.loc[unclassified_mask, col] = classified_unclass[col]
            
            op_final = merged
        else:
            if models is None:
                models = load_all_models(repo_root)
            op_final = classify_subset(dedup, models)

        # Save operator raw and classified
        file_key = "mygp" if op_name == "Grameenphone" else "myrobi" if op_name == "Robi" else "mybl"
        raw_out = raw_glob_dir / f"{file_key}_global_2020_to_sep2026.csv"
        cls_out = cls_dir / f"{file_key}_classified_global_2020_2026.csv"

        dedup[["review_id", "user_name", "rating", "review_date", "review_text", "thumbs_up", "operator"]].to_csv(raw_out, index=False)
        op_final.to_csv(cls_out, index=False)
        merged_operator_dfs.append(op_final)

    # Master complete dataset
    master_df = pd.concat(merged_operator_dfs, ignore_index=True)
    master_file = cls_dir / "all_operators_classified_global_2020_2026.csv"
    master_df.to_csv(master_file, index=False)
    print(f"\n🎉 Saved Master Classified Dataset: {len(master_df):,d} records to {master_file.name}")

    # =========================================================================
    # COMMON PERIOD EXTRACTION (STRICT COMMON PERIOD WHERE ALL 3 BRANDS COEXIST)
    # =========================================================================
    print("\n" + "=" * 75)
    print("EXTRACTING COMMON DURATION PERIOD (WHERE ALL 3 OPERATORS OVERLAP)")
    print("=" * 75)

    start_common = max(master_df[master_df["operator"] == op]["review_date"].min() for op in ["Grameenphone", "Robi", "Banglalink"])
    end_common = min(master_df[master_df["operator"] == op]["review_date"].max() for op in ["Grameenphone", "Robi", "Banglalink"])

    common_df = master_df[(master_df["review_date"] >= start_common) & (master_df["review_date"] <= end_common)].copy()
    days = (end_common - start_common).days

    common_file = cls_dir / "all_operators_common_duration_classified.csv"
    common_df.to_csv(common_file, index=False)

    print(f"Common Window: {start_common} to {end_common} ({days:,d} days)")
    print(f"Total reviews in Common Window: {len(common_df):,d}")
    
    summary = {
        "common_window_start": str(start_common),
        "common_window_end": str(end_common),
        "common_duration_days": days,
        "total_reviews": len(common_df),
        "operators": {}
    }

    for op in ["Grameenphone", "Robi", "Banglalink"]:
        sub = common_df[common_df["operator"] == op]
        pos = (sub["predicted_sentiment"] == "Positive").sum()
        neu = (sub["predicted_sentiment"] == "Neutral").sum()
        neg = (sub["predicted_sentiment"] == "Negative").sum()
        nss = ((pos - neg) / len(sub)) * 100 if len(sub) > 0 else 0
        print(f"  {op:13s}: {len(sub):6,d} reviews ({len(sub)/len(common_df)*100:4.1f}%) | Pos: {pos/len(sub)*100:4.1f}% | Neu: {neu/len(sub)*100:4.1f}% | Neg: {neg/len(sub)*100:4.1f}% | NSS: {nss:+5.1f}%")
        summary["operators"][op] = {
            "total_reviews": len(sub),
            "share_percent": round(len(sub) / len(common_df) * 100, 2),
            "positive_percent": round(pos / len(sub) * 100, 2),
            "neutral_percent": round(neu / len(sub) * 100, 2),
            "negative_percent": round(neg / len(sub) * 100, 2),
            "net_sentiment_score": round(nss, 2),
        }

    with open(cls_dir / "common_duration_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n✓ Saved common duration summary to: common_duration_summary.json")


if __name__ == "__main__":
    main()
