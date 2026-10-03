"""
Classify all reviews in the common duration dataset (2025-08-24 to 2026-09-30)
using the PRE-TRAINED ML and DL models saved from the earlier training run.

Models used:
  1. ml/models/ensemble_voting_classifier.joblib  (Soft-Voting Ensemble)
  2. ml/models/primary_logistic_regression.joblib (Balanced Logistic Regression)
  3. ml/models/challenger_linearsvc.joblib        (Calibrated LinearSVC)
  4. dl/models/bilstm_attention_model.pt          (Hybrid BiLSTM + Attention)
  5. dl/models/minilm_transformer_head.pt         (Pretrained Multilingual MiniLM)
"""

import sys
import time
from pathlib import Path
import re
import numpy as np
import pandas as pd
import joblib
import torch
import torch.nn.functional as F

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent if SCRIPT_DIR.name == "pipeline" else SCRIPT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

COMMON_DIR = REPO_ROOT / "scraped_data_2020" / "common_duration"
INPUT_CSV = COMMON_DIR / "all_operators_common_duration.csv"
OUTPUT_ALL = COMMON_DIR / "classified_all_operators_pretrained.csv"
OUTPUT_GP = COMMON_DIR / "mygp_classified_pretrained.csv"
OUTPUT_BL = COMMON_DIR / "mybl_classified_pretrained.csv"
OUTPUT_ROBI = COMMON_DIR / "myrobi_classified_pretrained.csv"
SUMMARY_TXT = COMMON_DIR / "classification_summary_pretrained.txt"

MODELS_ML_DIR = REPO_ROOT / "ml" / "models"
MODELS_DL_DIR = REPO_ROOT / "dl" / "models"


def clean_text(text: str) -> str:
    text = str(text).strip()
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower()


def main():
    print("=" * 80, flush=True)
    print("CLASSIFYING COMMON DURATION DATASET WITH PRE-TRAINED MODELS", flush=True)
    print("Shared Window: 2025-08-24 to 2026-09-30 (83,417 Reviews)", flush=True)
    print("=" * 80, flush=True)

    if not INPUT_CSV.exists():
        print(f"Error: {INPUT_CSV} not found!", flush=True)
        sys.exit(1)

    print(f"Loading reviews from: {INPUT_CSV.name}...", flush=True)
    df = pd.read_csv(INPUT_CSV)
    df["review_text_clean"] = df["review_text"].fillna(" ").astype(str).apply(lambda t: t if len(t.strip()) > 0 else " ")
    print(f"Total reviews to classify: {len(df):,d}\n", flush=True)

    # -----------------------------------------------------------------------
    # 1. SOFT-VOTING ENSEMBLE (Pretrained ML)
    # -----------------------------------------------------------------------
    ensemble_path = MODELS_ML_DIR / "ensemble_voting_classifier.joblib"
    print(f">>> [Model 1/5] Loading Pretrained Ensemble Model: {ensemble_path.name}...", flush=True)
    ensemble_pipeline = joblib.load(ensemble_path)
    print("    Running batch inference on all 83,417 reviews...", flush=True)
    
    t0 = time.time()
    batch_size = 10000
    ensemble_preds = []
    ensemble_conf = []

    for i in range(0, len(df), batch_size):
        chunk = df["review_text_clean"].iloc[i : i + batch_size].tolist()
        preds = ensemble_pipeline.predict(chunk)
        probs = ensemble_pipeline.predict_proba(chunk)
        max_p = np.max(probs, axis=1)
        ensemble_preds.extend(preds)
        ensemble_conf.extend(np.round(max_p, 4))
        print(f"    [Ensemble] Classified {min(i + batch_size, len(df)):,d}/{len(df):,d} reviews...", flush=True)

    dt_ens = time.time() - t0
    df["pred_ensemble"] = ensemble_preds
    df["conf_ensemble"] = ensemble_conf
    print(f"    Completed in {dt_ens:.2f}s ({len(df)/dt_ens:.0f} reviews/sec)!\n", flush=True)

    # -----------------------------------------------------------------------
    # 2. BALANCED LOGISTIC REGRESSION (Pretrained ML)
    # -----------------------------------------------------------------------
    logreg_path = MODELS_ML_DIR / "primary_logistic_regression.joblib"
    print(f">>> [Model 2/5] Loading Pretrained Logistic Regression: {logreg_path.name}...", flush=True)
    logreg_pipeline = joblib.load(logreg_path)
    print("    Running batch inference on all 83,417 reviews...", flush=True)

    t0 = time.time()
    logreg_preds = []
    for i in range(0, len(df), batch_size):
        chunk = df["review_text_clean"].iloc[i : i + batch_size].tolist()
        preds = logreg_pipeline.predict(chunk)
        logreg_preds.extend(preds)
        print(f"    [Logistic] Classified {min(i + batch_size, len(df)):,d}/{len(df):,d} reviews...", flush=True)

    dt_lr = time.time() - t0
    df["pred_logistic"] = logreg_preds
    print(f"    Completed in {dt_lr:.2f}s ({len(df)/dt_lr:.0f} reviews/sec)!\n", flush=True)

    # -----------------------------------------------------------------------
    # 3. CALIBRATED LINEARSVC (Pretrained ML)
    # -----------------------------------------------------------------------
    linearsvc_path = MODELS_ML_DIR / "challenger_linearsvc.joblib"
    print(f">>> [Model 3/5] Loading Pretrained LinearSVC: {linearsvc_path.name}...", flush=True)
    svc_pipeline = joblib.load(linearsvc_path)
    print("    Running batch inference on all 83,417 reviews...", flush=True)

    t0 = time.time()
    svc_preds = []
    for i in range(0, len(df), batch_size):
        chunk = df["review_text_clean"].iloc[i : i + batch_size].tolist()
        preds = svc_pipeline.predict(chunk)
        svc_preds.extend(preds)
        print(f"    [LinearSVC] Classified {min(i + batch_size, len(df)):,d}/{len(df):,d} reviews...", flush=True)

    dt_svc = time.time() - t0
    df["pred_linearsvc"] = svc_preds
    print(f"    Completed in {dt_svc:.2f}s ({len(df)/dt_svc:.0f} reviews/sec)!\n", flush=True)

    # -----------------------------------------------------------------------
    # 4. HYBRID BiLSTM + ATTENTION (Pretrained DL)
    # -----------------------------------------------------------------------
    bilstm_path = MODELS_DL_DIR / "bilstm_attention_model.pt"
    print(f">>> [Model 4/5] Loading Pretrained BiLSTM Model: {bilstm_path.name}...", flush=True)
    from dl.predict_dl import load_bilstm, INV_LABEL_MAP
    b_model, b_vocab = load_bilstm()
    print("    Running batch inference on all 83,417 reviews...", flush=True)

    t0 = time.time()
    dl_batch_size = 2000
    bilstm_preds = []

    for i in range(0, len(df), dl_batch_size):
        chunk = df["review_text_clean"].iloc[i : i + dl_batch_size].tolist()
        w_list, c_list = [], []
        for text in chunk:
            w, c = b_vocab.encode(clean_text(text))
            w_list.append(w)
            c_list.append(c)

        w_tensor = torch.tensor(w_list, dtype=torch.long)
        c_tensor = torch.tensor(c_list, dtype=torch.long)
        with torch.no_grad():
            logits = b_model(w_tensor, c_tensor)
            p_idx = torch.argmax(logits, dim=-1).cpu().numpy()
            bilstm_preds.extend([INV_LABEL_MAP[idx] for idx in p_idx])

        print(f"    [BiLSTM] Classified {min(i + dl_batch_size, len(df)):,d}/{len(df):,d} reviews...", flush=True)

    dt_bilstm = time.time() - t0
    df["pred_bilstm"] = bilstm_preds
    print(f"    Completed in {dt_bilstm:.2f}s ({len(df)/dt_bilstm:.0f} reviews/sec)!\n", flush=True)

    # -----------------------------------------------------------------------
    # 5. PRETRAINED MULTILINGUAL MINILM TRANSFORMER (Sample Benchmark)
    # -----------------------------------------------------------------------
    print(f">>> [Model 5/5] Loading Pretrained MiniLM Transformer Head...", flush=True)
    from dl.predict_dl import load_transformer
    from dl.train_transformer import mean_pooling
    tokenizer, transformer, head = load_transformer()

    # Stratified sample of 1,500 reviews across the 3 operators (500 GP, 500 BL, 500 Robi)
    # for rapid CPU transformer evaluation without 45min blocking
    print("    Running MiniLM Transformer on stratified sample (1,500 reviews: 500 GP, 500 BL, 500 Robi)...", flush=True)
    sample_indices = []
    for op in ["Grameenphone", "Banglalink", "Robi"]:
        op_idx = df[df["operator"] == op].index
        chosen = np.random.RandomState(42).choice(op_idx, size=min(500, len(op_idx)), replace=False)
        sample_indices.extend(chosen)

    sample_texts = df.loc[sample_indices, "review_text_clean"].tolist()
    t0 = time.time()
    minilm_preds_sample = []
    for i in range(0, len(sample_texts), 64):
        b_txt = sample_texts[i : i + 64]
        encoded = tokenizer(b_txt, padding=True, truncation=True, max_length=64, return_tensors="pt")
        with torch.no_grad():
            out = transformer(**encoded)
            pooled = mean_pooling(out, encoded["attention_mask"])
            normed = F.normalize(pooled, p=2, dim=1)
            logits = head(normed)
            p_idx = torch.argmax(logits, dim=-1).cpu().numpy()
            minilm_preds_sample.extend([INV_LABEL_MAP[idx] for idx in p_idx])

    dt_tf = time.time() - t0
    df["pred_minilm_sample"] = None
    df.loc[sample_indices, "pred_minilm_sample"] = minilm_preds_sample
    print(f"    Completed sample in {dt_tf:.2f}s ({len(sample_texts)/dt_tf:.1f} reviews/sec)!\n", flush=True)

    # -----------------------------------------------------------------------
    # SAVE CLASSIFIED DATASETS
    # -----------------------------------------------------------------------
    df.drop(columns=["review_text_clean"], inplace=True)
    df.to_csv(OUTPUT_ALL, index=False)
    print(f"Master classified dataset saved to: {OUTPUT_ALL.name} ({len(df):,d} rows)", flush=True)

    # Save per-operator datasets
    for op, out_file in [("Grameenphone", OUTPUT_GP), ("Banglalink", OUTPUT_BL), ("Robi", OUTPUT_ROBI)]:
        op_df = df[df["operator"] == op]
        op_df.to_csv(out_file, index=False)
        print(f"Saved {op:13s} classified dataset to: {out_file.name} ({len(op_df):,d} rows)", flush=True)

    # -----------------------------------------------------------------------
    # PRODUCE BENCHMARK & COMPARISON REPORT
    # -----------------------------------------------------------------------
    print("\n" + "=" * 80, flush=True)
    print("VOICE-OF-CUSTOMER COMPARISON USING PRE-TRAINED MODELS (COMMON DURATION)", flush=True)
    print("=" * 80, flush=True)

    report_lines = [
        "================================================================================",
        "TELECOM VOICE-OF-CUSTOMER INTELLIGENCE: PRETRAINED MODEL CLASSIFICATION",
        "Common Duration Window: 2025-08-24 to 2026-09-30 (Total Reviews: 83,417)",
        "================================================================================",
        "",
        "1. CLASSIFICATION BREAKDOWN BY MODEL (OVERALL ACROSS ALL 83,417 REVIEWS):",
        "-" * 80,
    ]

    header_models = f"{'Model Architecture':<30} | {'Positive %':<11} | {'Neutral %':<10} | {'Negative %':<11}"
    print(header_models, flush=True)
    print("-" * 80, flush=True)
    report_lines.append(header_models)
    report_lines.append("-" * 80)

    for col, name in [
        ("pred_ensemble", "Soft-Voting Ensemble (ML)"),
        ("pred_logistic", "Balanced Logistic Regression"),
        ("pred_linearsvc", "Calibrated LinearSVC"),
        ("pred_bilstm", "Hybrid BiLSTM + Attention"),
    ]:
        pos = (df[col] == "Positive").sum() / len(df) * 100
        neu = (df[col] == "Neutral").sum() / len(df) * 100
        neg = (df[col] == "Negative").sum() / len(df) * 100
        row = f"{name:<30} | {pos:>9.1f}%  | {neu:>8.1f}%  | {neg:>9.1f}%"
        print(row, flush=True)
        report_lines.append(row)

    print("\n" + "=" * 80, flush=True)
    print("2. OPERATOR BENCHMARK (USING PRIMARY ENSEMBLE MODEL):", flush=True)
    print("=" * 80, flush=True)
    report_lines.extend([
        "",
        "2. OPERATOR BENCHMARK (USING PRIMARY ENSEMBLE MODEL):",
        "-" * 85,
    ])

    voc_header = f"{'Operator':<15} | {'Total Reviews':<13} | {'Positive %':<11} | {'Neutral %':<10} | {'Negative %':<11} | {'Net Sentiment (NSS)':<18}"
    print(voc_header, flush=True)
    print("-" * 85, flush=True)
    report_lines.append(voc_header)
    report_lines.append("-" * 85)

    for op in ["Grameenphone", "Banglalink", "Robi"]:
        op_data = df[df["operator"] == op]
        tot = len(op_data)
        pos = (op_data["pred_ensemble"] == "Positive").sum() / tot * 100
        neu = (op_data["pred_ensemble"] == "Neutral").sum() / tot * 100
        neg = (op_data["pred_ensemble"] == "Negative").sum() / tot * 100
        nss = pos - neg
        row = f"{op:<15} | {tot:<13,d} | {pos:>9.1f}%  | {neu:>8.1f}%  | {neg:>9.1f}%  | {nss:>+16.1f}%"
        print(row, flush=True)
        report_lines.append(row)

    # Cross-Model Agreement Rate with Ensemble
    report_lines.extend([
        "",
        "3. CROSS-MODEL AGREEMENT RATE WITH PRETRAINED ENSEMBLE:",
        "-" * 60,
    ])
    for col, name in [
        ("pred_logistic", "Logistic Regression"),
        ("pred_linearsvc", "LinearSVC"),
        ("pred_bilstm", "BiLSTM + Attention"),
    ]:
        agree = (df["pred_ensemble"] == df[col]).mean() * 100
        report_lines.append(f"- Agreement between Ensemble and {name:<25}: {agree:.2f}%")

    SUMMARY_TXT.write_text("\n".join(report_lines), encoding="utf-8")
    print("\n" + "=" * 80, flush=True)
    print(f"Summary report written to: {SUMMARY_TXT.name}", flush=True)
    print("=" * 80, flush=True)


if __name__ == "__main__":
    main()
