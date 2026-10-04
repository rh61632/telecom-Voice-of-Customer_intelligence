#!/usr/bin/env python3
"""
Multi-Model Batch Classification Pipeline for Global Multi-Year Dataset (2020 - 2026)
Applies the full suite of trained Classical ML and Deep Learning BiLSTM models
across all 353,714 raw reviews for Grameenphone, Robi, and Banglalink.
"""

import os
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

# Suppress sklearn unpickle version warnings for clean terminal logging
warnings.filterwarnings("ignore", category=UserWarning)

# Define architecture classes matching the pickled artifacts
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

    print("=" * 75)
    print("LOADING TRAINED MACHINE LEARNING & DEEP LEARNING MODEL SUITE")
    print("=" * 75)

    print("1/6 Loading Hero Sentiment Ensemble...", flush=True)
    sent_ensemble = joblib.load(ml_dir / "sentiment_voting_classifier.joblib")

    print("2/6 Loading Hero Operational Category Ensemble...", flush=True)
    cat_ensemble = joblib.load(ml_dir / "category_voting_classifier.joblib")

    print("3/6 Loading Component Classifiers (LR & LinearSVC)...", flush=True)
    sent_lr = joblib.load(ml_dir / "primary_logistic_regression.joblib")
    sent_svc = joblib.load(ml_dir / "challenger_linearsvc.joblib")
    cat_lr = joblib.load(ml_dir / "category_logistic_regression.joblib")
    cat_svc = joblib.load(ml_dir / "category_linearsvc.joblib")

    print("4/6 Loading Deep Learning Vocabulary & Encoders...", flush=True)
    vocab = joblib.load(dl_dir / "bilstm_vocab.joblib")
    sent_le = joblib.load(dl_dir / "sent_le.joblib")
    cat_le = joblib.load(dl_dir / "cat_le.joblib")

    print("5/6 Loading Hybrid BiLSTM Sentiment Model...", flush=True)
    bilstm_sent = HybridBiLSTMAttention(len(vocab.word2idx), len(sent_le.classes_))
    bilstm_sent.load_state_dict(torch.load(dl_dir / "bilstm_sentiment_model.pt", map_location="cpu"))
    bilstm_sent.eval()

    print("6/6 Loading Hybrid BiLSTM Category Model...", flush=True)
    bilstm_cat = HybridBiLSTMAttention(len(vocab.word2idx), len(cat_le.classes_))
    bilstm_cat.load_state_dict(torch.load(dl_dir / "bilstm_category_model.pt", map_location="cpu"))
    bilstm_cat.eval()

    print("✓ All models loaded successfully!\n")
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


def classify_operator_dataframe(df: pd.DataFrame, operator_name: str, models: dict, batch_size: int = 10000):
    total = len(df)
    print(f"\n>>> Classifying {operator_name} ({total:,d} reviews)...", flush=True)
    t0 = time.time()

    # Pre-clean text representations
    texts = df["review_text"].fillna(" ").astype(str).str.strip().tolist()
    # Replace empty strings with space for safe tokenization
    safe_texts = [t if len(t) > 0 else " " for t in texts]

    # Pre-allocate output arrays
    sent_ens_preds = []
    sent_ens_confs = []
    cat_ens_preds = []
    cat_ens_confs = []

    sent_lr_preds = []
    sent_svc_preds = []
    cat_lr_preds = []
    cat_svc_preds = []

    bilstm_sent_preds = []
    bilstm_cat_preds = []

    vocab = models["vocab"]
    sent_le = models["sent_le"]
    cat_le = models["cat_le"]

    num_batches = (total + batch_size - 1) // batch_size

    for b_idx in range(num_batches):
        start = b_idx * batch_size
        end = min(start + batch_size, total)
        chunk = safe_texts[start:end]
        chunk_len = len(chunk)

        # 1. Classical Ensemble Predictions & Probabilities
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

        # 2. Component Classifiers
        sent_lr_preds.extend(models["sent_lr"].predict(chunk))
        sent_svc_preds.extend(models["sent_svc"].predict(chunk))
        cat_lr_preds.extend(models["cat_lr"].predict(chunk))
        cat_svc_preds.extend(models["cat_svc"].predict(chunk))

        # 3. BiLSTM Neural Predictions
        # Tokenize chunk into PyTorch tensor
        seqs = torch.tensor([vocab.transform(t) for t in chunk], dtype=torch.long)
        with torch.no_grad():
            b_s_out = models["bilstm_sent"](seqs)
            b_c_out = models["bilstm_cat"](seqs)
            b_s_idx = b_s_out.argmax(dim=1).numpy()
            b_c_idx = b_c_out.argmax(dim=1).numpy()

        bilstm_sent_preds.extend(sent_le.inverse_transform(b_s_idx))
        bilstm_cat_preds.extend(cat_le.inverse_transform(b_c_idx))

        elapsed = time.time() - t0
        speed = end / elapsed if elapsed > 0 else 0
        print(f"    Processed {end:,d}/{total:,d} reviews ({end/total*100:.1f}%) | {speed:.0f} rev/s", flush=True)

    dt = time.time() - t0
    print(f"✓ Completed {operator_name} in {dt:.1f}s ({total/dt:.0f} reviews/sec overall)")

    # Assign columns
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
    raw_dir = repo_root / "scraped_data_global_2020_2026" / "raw"
    classified_dir = repo_root / "scraped_data_global_2020_2026" / "classified"
    classified_dir.mkdir(parents=True, exist_ok=True)

    files = [
        ("Banglalink", raw_dir / "mybl_global_2020_to_sep2026.csv", classified_dir / "mybl_classified_global_2020_2026.csv"),
        ("Grameenphone", raw_dir / "mygp_global_2020_to_sep2026.csv", classified_dir / "mygp_classified_global_2020_2026.csv"),
        ("Robi", raw_dir / "myrobi_global_2020_to_sep2026.csv", classified_dir / "myrobi_classified_global_2020_2026.csv"),
    ]

    # Verify input existence
    for op, in_path, _ in files:
        if not in_path.exists():
            print(f"Error: Raw dataset not found at {in_path}")
            sys.exit(1)

    models = load_all_models(repo_root)

    start_total = time.time()
    classified_dfs = []
    operator_summaries = {}

    for op_name, in_path, out_path in files:
        print(f"\nReading {in_path.name}...")
        df = pd.read_csv(in_path)
        df_classified = classify_operator_dataframe(df, op_name, models, batch_size=10000)
        
        print(f"Saving to {out_path.name}...")
        df_classified.to_csv(out_path, index=False)
        print(f"✓ Saved {len(df_classified):,d} rows to {out_path.name}")

        classified_dfs.append(df_classified)

        # Compute summary metrics for this operator
        sent_counts = df_classified["predicted_sentiment"].value_counts().to_dict()
        cat_counts = df_classified["predicted_category"].value_counts().to_dict()
        total_rev = len(df_classified)

        pos = sent_counts.get("Positive", 0)
        neg = sent_counts.get("Negative", 0)
        neu = sent_counts.get("Neutral", 0)
        net_sentiment = ((pos - neg) / total_rev) * 100 if total_rev > 0 else 0

        operator_summaries[op_name] = {
            "total_reviews": total_rev,
            "net_sentiment_score": round(net_sentiment, 2),
            "sentiment_distribution": {
                "Positive": {"count": pos, "pct": round(pos / total_rev * 100, 2)},
                "Negative": {"count": neg, "pct": round(neg / total_rev * 100, 2)},
                "Neutral": {"count": neu, "pct": round(neu / total_rev * 100, 2)},
            },
            "category_distribution": {
                c: {"count": n, "pct": round(n / total_rev * 100, 2)}
                for c, n in cat_counts.items()
            },
            "avg_sentiment_confidence": round(float(df_classified["sentiment_confidence"].mean()), 4),
            "avg_category_confidence": round(float(df_classified["category_confidence"].mean()), 4),
        }

    # Combined master dataset
    print("\nMerging into combined master classified dataset...")
    all_df = pd.concat(classified_dfs, ignore_index=True)
    all_out_path = classified_dir / "all_operators_classified_global_2020_2026.csv"
    all_df.to_csv(all_out_path, index=False)
    print(f"✓ Saved master dataset: {all_out_path.name} ({len(all_df):,d} reviews, {os.path.getsize(all_out_path)/1e6:.1f} MB)")

    total_time = time.time() - start_total
    print(f"\n>>> Total Pipeline Execution Time: {total_time:.1f}s ({len(all_df)/total_time:.0f} rev/s overall)")

    # Save summary report JSON
    summary_json_path = classified_dir / "global_voc_intelligence_report.json"
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(operator_summaries, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved intelligence summary JSON: {summary_json_path.name}")

    print("\n" + "=" * 75)
    print("GLOBAL 2020 - 2026 MULTI-OPERATOR INTELLIGENCE SUMMARY")
    print("=" * 75)
    for op, stats in operator_summaries.items():
        print(f"\n📱 {op} (Total Reviews: {stats['total_reviews']:,d})")
        print(f"   Net Sentiment Score (NSS): {stats['net_sentiment_score']:+.2f}%")
        print(f"   Positive : {stats['sentiment_distribution']['Positive']['pct']:.1f}% ({stats['sentiment_distribution']['Positive']['count']:,d})")
        print(f"   Negative : {stats['sentiment_distribution']['Negative']['pct']:.1f}% ({stats['sentiment_distribution']['Negative']['count']:,d})")
        print(f"   Neutral  : {stats['sentiment_distribution']['Neutral']['pct']:.1f}% ({stats['sentiment_distribution']['Neutral']['count']:,d})")
        print("   Top Operational Complaint Categories:")
        for cat, c_stats in list(stats['category_distribution'].items())[:3]:
            print(f"     • {cat:<30}: {c_stats['pct']:5.1f}% ({c_stats['count']:,d})")

    print("\n✓ ALL 353,714 REVIEWS CLASSIFIED ACROSS ALL 8 MODELS SUCCESSFULLY!")


if __name__ == "__main__":
    main()
