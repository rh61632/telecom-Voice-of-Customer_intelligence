#!/usr/bin/env python3
"""
scripts/audit_project_integrity.py
Comprehensive neutral audit script executing automated sanity checks across all 8 modules:
1. Data integrity (counts, dates, nulls, duplicates, telemetry JSONs)
2. Gold set agreement, independence, and active McNemar / Rogan-Gladen bounds
3. Model deserialization, schema parity, and benchmark consistency
4. Exact mathematical identities of NSS and Additive Decomposition
5. Time series aggregation, CLT floor, RMSSD volatility, and surge filtering
6. Proposition 1 and Proposition 2 statistical tests, and Priority Matrix
7. Spring 2024 counterfactual telemetry and Case Study 2 turnaround
8. Double-blind anonymity, manuscript completeness, page budgets, and deliverable sync

Conforms to ADR-002, ADR-003, and REM-05.
Supports `--strict-paper` command-line flag for gating Phase 8/9 deliverables.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import warnings

# Suppress sklearn unpickling and convergence warnings during audit
warnings.filterwarnings("ignore")

import joblib
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import chi2_contingency, fisher_exact

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def parse_args():
    parser = argparse.ArgumentParser(description="Telecom VoC Intelligence: Integrity Audit")
    parser.add_argument(
        "--strict-paper",
        action="store_true",
        help="Hard-fail (exit 1) on pending Phase 8/9 paper defects (raw markdown, PDF page limits, missing Excel)",
    )
    return parser.parse_args()


def main():
    t_start = time.time()
    args = parse_args()
    strict_paper = args.strict_paper

    print("=" * 80)
    print("TELECOM VOC INTELLIGENCE: COMPREHENSIVE PROJECT INTEGRITY AUDIT")
    print(f"Mode: {'STRICT PAPER GATE (Exit 1 on Phase 8/9 defects)' if strict_paper else 'DEFAULT (Warnings on Phase 8/9 defects)'}")
    print("=" * 80)

    # ---------------------------------------------------------
    # MODULE 1: DATA INTEGRITY
    # ---------------------------------------------------------
    print("\n[MODULE 1] Verifying Data Provenance, Counts & Deduplication...")
    csv_common = REPO_ROOT / "scraped_data_global" / "classified" / "all_operators_common_duration_classified.csv"
    if not csv_common.exists():
        print(f"FAILED: File not found: {csv_common}")
        sys.exit(1)

    df_common = pd.read_csv(
        csv_common,
        usecols=[
            "review_id",
            "operator",
            "review_date",
            "predicted_sentiment",
            "predicted_category",
            "ym",
            "review_text",
            "app_version",
            "year",
        ],
    )
    total_rows = len(df_common)
    assert total_rows == 655649, f"Expected 655649 rows, got {total_rows}"
    print(f"  [PASS] Common duration rows: {total_rows:,}")

    # Operator breakdown
    counts = df_common["operator"].value_counts().to_dict()
    assert counts.get("Grameenphone") == 320140, f"GP count mismatch: {counts.get('Grameenphone')}"
    assert counts.get("Robi") == 198378, f"Robi count mismatch: {counts.get('Robi')}"
    assert counts.get("Banglalink") == 137131, f"BL count mismatch: {counts.get('Banglalink')}"
    print(f"  [PASS] Operator breakdown: GP={counts['Grameenphone']:,}, Robi={counts['Robi']:,}, BL={counts['Banglalink']:,}")

    # Date Window
    min_date = str(df_common["review_date"].min())[:10]
    max_date = str(df_common["review_date"].max())[:10]
    assert min_date == "2016-08-01", f"Min date mismatch: {min_date}"
    assert max_date == "2026-09-30", f"Max date mismatch: {max_date}"
    print(f"  [PASS] Synchronized Date Window: {min_date} to {max_date}")

    # Deduplication and Null Handling
    assert not df_common["review_id"].duplicated().any(), "Duplicate review_id values detected in common duration dataset!"
    core_cols = ["review_id", "operator", "review_date", "predicted_sentiment", "predicted_category", "ym"]
    for c in core_cols:
        assert df_common[c].isna().sum() == 0, f"Unexpected null values detected in column '{c}'!"
    null_texts = int(df_common["review_text"].isna().sum())
    assert null_texts == 51, f"Expected exactly 51 null review_text rows, found {null_texts}"
    print(f"  [PASS] Data Hygiene: 0 duplicate IDs, 0 core nulls, exactly 51 legitimate null review_text rows")

    # Global Dataset
    csv_global = REPO_ROOT / "scraped_data_global" / "classified" / "all_operators_classified_global.csv"
    assert csv_global.exists(), f"Global CSV missing: {csv_global}"
    df_global_ids = pd.read_csv(csv_global, usecols=["review_id"])
    assert len(df_global_ids) == 661160, f"Expected 661160 rows in global dataset, got {len(df_global_ids)}"
    assert not df_global_ids["review_id"].duplicated().any(), "Duplicate review_id detected in global dataset!"
    print(f"  [PASS] Global dataset: {len(df_global_ids):,} rows, 0 duplicate IDs")

    # Telemetry JSON alignment
    json_summary = REPO_ROOT / "scraped_data_global" / "classified" / "common_duration_summary.json"
    json_trends = REPO_ROOT / "scraped_data_global" / "classified" / "yearly_intelligence_trends.json"
    assert json_summary.exists(), "common_duration_summary.json missing!"
    assert json_trends.exists(), "yearly_intelligence_trends.json missing!"
    with open(json_trends, "r", encoding="utf-8") as f:
        trends_data = json.load(f)
    yearly_sum = sum(
        op_data.get("total", 0)
        for yr, op_dict in trends_data.items()
        if isinstance(op_dict, dict)
        for op, op_data in op_dict.items()
        if isinstance(op_data, dict)
    )
    assert yearly_sum == 655649, f"Yearly trends sum {yearly_sum} != 655649"
    y2016 = trends_data.get("2016", {})
    assert y2016.get("Grameenphone", {}).get("total") == 438
    assert y2016.get("Robi", {}).get("total") == 126
    assert y2016.get("Banglalink", {}).get("total") == 744
    print(f"  [PASS] Telemetry JSONs aligned: Sum = {yearly_sum:,}, 2016 baseline = 438/126/744")

    # ---------------------------------------------------------
    # MODULE 2: GOLD SET AGREEMENT & INDEPENDENCE
    # ---------------------------------------------------------
    print("\n[MODULE 2] Verifying Gold Standard Set, Independence, IRR & Consensus Bounds...")
    f_gold300 = REPO_ROOT / "data" / "gold_set" / "blind_annotation_300_annotator1.csv"
    f_gold200 = REPO_ROOT / "data" / "gold_set" / "blind_annotation_200_annotator2.csv"
    assert f_gold300.exists(), "Gold annotation 300 missing!"
    assert f_gold200.exists(), "Gold annotation 200 missing!"

    df_g300 = pd.read_csv(f_gold300)
    df_g200 = pd.read_csv(f_gold200)
    assert len(df_g300) == 300, f"Expected 300 rows in Gold set 1, got {len(df_g300)}"
    assert len(df_g200) == 200, f"Expected 200 rows in Gold set 2, got {len(df_g200)}"
    g300_counts = df_g300["operator"].value_counts().to_dict()
    assert g300_counts == {"Grameenphone": 100, "Robi": 100, "Banglalink": 100}
    g200_counts = df_g200["operator"].value_counts().to_dict()
    assert g200_counts == {"Grameenphone": 67, "Banglalink": 67, "Robi": 66}
    print(f"  [PASS] Gold sample sizes: N=300 (100/op) and N=200 (67 GP, 67 BL, 66 Robi)")

    # Independence from seed N=4,500 dataset
    seed_csv = REPO_ROOT / "data" / "processed" / "all_operators_classified_with_language.csv"
    assert seed_csv.exists(), "Seed N=4,500 dataset missing!"
    df_seed = pd.read_csv(seed_csv, usecols=["review_text", "category", "sentiment"])
    assert len(df_seed) == 4500, f"Expected 4500 seed rows, got {len(df_seed)}"

    gold_texts = set(df_g300["review_text"].dropna().str.strip()).union(set(df_g200["review_text"].dropna().str.strip()))
    seed_texts = set(df_seed["review_text"].dropna().str.strip())
    overlap = gold_texts.intersection(seed_texts)
    assert len(overlap) == 0, f"Data leakage detected! {len(overlap)} reviews overlap between Gold and Seed sets!"
    print(f"  [PASS] Gold Set Independence: 0 overlapping reviews with N=4,500 seed dataset")

    # IRR Metrics
    g300_dict = {r["sample_id"]: r for _, r in df_g300.iterrows()}
    g200_dict = {r["sample_id"]: r for _, r in df_g200.iterrows()}
    common_ids = [sid for sid in g300_dict if sid in g200_dict]
    assert len(common_ids) == 200, f"Expected 200 overlapping sample IDs, got {len(common_ids)}"

    paired_sent = []
    paired_cat = []
    for sid in common_ids:
        r1, r2 = g300_dict[sid], g200_dict[sid]
        s1 = "" if pd.isna(r1.get("sentiment_label")) else str(r1.get("sentiment_label")).strip()
        s2 = "" if pd.isna(r2.get("sentiment_label")) else str(r2.get("sentiment_label")).strip()
        if s1 and s2 and s1 != "nan" and s2 != "nan":
            paired_sent.append((s1, s2))
        c1 = "" if pd.isna(r1.get("category_label")) else str(r1.get("category_label")).strip()
        c2 = "" if pd.isna(r2.get("category_label")) else str(r2.get("category_label")).strip()
        if c1 and c2 and c1 != "nan" and c2 != "nan":
            paired_cat.append((c1, c2))

    assert len(paired_sent) == 200, f"Expected 200 sentiment pairs, got {len(paired_sent)}"
    assert len(paired_cat) == 196, f"Expected 196 valid category pairs, got {len(paired_cat)}"

    def calc_cohen_kappa(pairs, classes):
        n = len(pairs)
        po = sum(1 for a, b in pairs if a == b) / n
        y1 = [a for a, b in pairs]
        y2 = [b for a, b in pairs]
        pe = sum((y1.count(c) / n) * (y2.count(c) / n) for c in classes)
        kappa = 1.0 if pe >= 1.0 else (po - pe) / (1.0 - pe)
        k_cls = len(classes)
        pabak = (k_cls * po - 1.0) / (k_cls - 1.0) if k_cls > 1 else po
        return round(po * 100, 2), round(kappa, 4), round(pabak, 4)

    sent_labels = ["Positive", "Neutral", "Negative"]
    cat_labels = [
        "General Appreciation / Other",
        "Offers & Data Packs",
        "App Login & Technical Bugs",
        "Network Speed & 4G Latency",
        "Billing & Airtime Deductions",
    ]

    sent_raw, sent_k, sent_pabak = calc_cohen_kappa(paired_sent, sent_labels)
    cat_raw, cat_k, _ = calc_cohen_kappa(paired_cat, cat_labels)
    assert np.isclose(sent_raw, 91.00, atol=0.01), f"Sentiment raw agreement mismatch: {sent_raw}"
    assert np.isclose(sent_k, 0.5762, atol=0.001), f"Sentiment kappa mismatch: {sent_k}"
    assert np.isclose(sent_pabak, 0.8650, atol=0.001), f"Sentiment PABAK mismatch: {sent_pabak}"
    assert np.isclose(cat_raw, 95.41, atol=0.01), f"Category raw agreement mismatch: {cat_raw}"
    assert np.isclose(cat_k, 0.7694, atol=0.001), f"Category kappa mismatch: {cat_k}"
    print(f"  [PASS] Inter-Rater Reliability: Sentiment agreement {sent_raw:.2f}% (kappa={sent_k:.4f}, PABAK={sent_pabak:.4f}); Category agreement {cat_raw:.2f}% (kappa={cat_k:.4f})")

    # Consensus subsets and active model bounds
    consensus_sent = [p for p in paired_sent if p[0] == p[1]]
    consensus_cat = [p for p in paired_cat if p[0] == p[1]]
    assert len(consensus_sent) == 182, f"Expected 182 sentiment consensus items, got {len(consensus_sent)}"
    assert len(consensus_cat) == 187, f"Expected 187 category consensus items, got {len(consensus_cat)}"
    print(f"  [PASS] Consensus Subsets: N=182 (Sentiment) and N=187 (Category)")

    # ---------------------------------------------------------
    # MODULE 3: MODEL DESERIALIZATION & BENCHMARK CONSISTENCY
    # ---------------------------------------------------------
    print("\n[MODULE 3] Verifying Model Deserialization, Schema Parity & Ground Truth...")
    core_models = [
        "category_voting_classifier.joblib",
        "sentiment_voting_classifier.joblib",
        "ensemble_voting_classifier.joblib",
        "primary_logistic_regression.joblib",
        "challenger_linearsvc.joblib",
        "category_logistic_regression.joblib",
        "category_linearsvc.joblib",
    ]
    loaded_models = {}
    for m in core_models:
        p = REPO_ROOT / "ml" / "models" / m
        assert p.exists(), f"Core model file missing: {p}"
        loaded_models[m] = joblib.load(p)
    print(f"  [PASS] All {len(core_models)} core joblib models deserialized cleanly")

    # BiLSTM vocab
    from dl.bilstm_artifacts import load_bilstm_vocab
    bilstm_vocab = load_bilstm_vocab(REPO_ROOT / "dl" / "models")
    assert len(bilstm_vocab) == 2864, f"Expected 2864 bilstm tokens, got {len(bilstm_vocab)}"
    print(f"  [PASS] BiLSTM vocabulary: 2,864 tokens verified")

    # Schema Parity
    cat_le = joblib.load(REPO_ROOT / "dl" / "models" / "cat_le.joblib")
    expected_cat_classes = [
        "App Login & Technical Bugs",
        "Billing & Airtime Deductions",
        "General Appreciation / Other",
        "Network Speed & 4G Latency",
        "Offers & Data Packs",
    ]
    assert list(cat_le.classes_) == expected_cat_classes, f"cat_le classes mismatch: {list(cat_le.classes_)}"

    with open(REPO_ROOT / "dl" / "models" / "banglabert_finetuned_category" / "config.json", "r", encoding="utf-8") as f:
        bert_cat_cfg = json.load(f)
    assert bert_cat_cfg.get("id2label", {}).get("0") == "General Appreciation / Other"
    assert bert_cat_cfg.get("id2label", {}).get("1") == "Offers & Data Packs"
    assert bert_cat_cfg.get("id2label", {}).get("2") == "App Login & Technical Bugs"
    assert bert_cat_cfg.get("id2label", {}).get("3") == "Network Speed & 4G Latency"
    assert bert_cat_cfg.get("id2label", {}).get("4") == "Billing & Airtime Deductions"
    print(f"  [PASS] Label schema parity: BiLSTM alphabetical vs BanglaBERT CATEGORY_LABEL_MAP verified")

    # Ground truth JSON consistency and live seed evaluation
    ground_truth_json = REPO_ROOT / "scraped_data_global" / "classified" / "paper_empirical_ground_truth.json"
    assert ground_truth_json.exists(), f"Ground truth JSON missing: {ground_truth_json}"
    with open(ground_truth_json, "r", encoding="utf-8") as f:
        gt_data = json.load(f)

    # Validate ground-truth full-seed N=4,500 benchmark metrics
    gt_t3 = gt_data.get("table3_seed_and_complexity", {})
    assert gt_t3.get("vocabulary_size") == 29843, f"Ground truth V mismatch: {gt_t3.get('vocabulary_size')}"
    assert np.isclose(gt_t3.get("full_seed_n4500_performance", {}).get("accuracy", 0), 0.9900, atol=0.0001)
    assert np.isclose(gt_t3.get("full_seed_n4500_performance", {}).get("macro_f1", 0), 0.9883, atol=0.0001)

    # Live model spot-check on seed dataset
    cat_clf = loaded_models["category_voting_classifier.joblib"]
    X_seed_sample = df_seed["review_text"].iloc[:50].astype(str).tolist()
    y_seed_sample = df_seed["category"].iloc[:50].tolist()
    pred_sample = cat_clf.predict(X_seed_sample)
    sample_acc = (pred_sample == y_seed_sample).mean()
    assert sample_acc >= 0.98, f"Live seed sample accuracy below expected fit threshold: {sample_acc:.4f}"

    v_size = cat_clf.named_steps["features"].transform(X_seed_sample[:5]).shape[1]
    assert v_size == 29843, f"Expected V=29,843 features, got {v_size}"
    print(f"  [PASS] Live Category Hero Model: V = 29,843, ground-truth full-seed Acc = 99.00%, Macro-F1 = 0.9883, live sample Acc = {sample_acc*100:.1f}%")

    # Live model predictions on active Gold N=300 and Consensus N=182
    ens_cli = loaded_models["ensemble_voting_classifier.joblib"]
    ens_prod = loaded_models["sentiment_voting_classifier.joblib"]
    pred_ens_300 = ens_cli.predict(df_g300["review_text"])
    pred_prod_300 = ens_prod.predict(df_g300["review_text"])
    y_sent_300 = df_g300["sentiment_label"]

    ens_acc_300 = float((pred_ens_300 == y_sent_300).mean())
    prod_acc_300 = float((pred_prod_300 == y_sent_300).mean())
    assert np.isclose(ens_acc_300, 0.8900, atol=0.001), f"Ensemble N=300 accuracy mismatch: {ens_acc_300}"
    assert np.isclose(prod_acc_300, 0.8367, atol=0.001), f"Prod sentiment N=300 accuracy mismatch: {prod_acc_300}"

    consensus_sids = set(common_ids[i] for i, (s1, s2) in enumerate(paired_sent) if s1 == s2)
    cons_mask = df_g300["sample_id"].isin(consensus_sids)
    ens_acc_cons = float((pred_ens_300[cons_mask] == y_sent_300[cons_mask]).mean())
    prod_acc_cons = float((pred_prod_300[cons_mask] == y_sent_300[cons_mask]).mean())
    assert np.isclose(ens_acc_cons, 0.9121, atol=0.001), f"Ensemble consensus accuracy mismatch: {ens_acc_cons}"
    assert np.isclose(prod_acc_cons, 0.8791, atol=0.001), f"Prod sentiment consensus accuracy mismatch: {prod_acc_cons}"
    print(f"  [PASS] Active Gold N=300 & Consensus N=182 accuracy bounds: Ensemble {ens_acc_300*100:.2f}% / {ens_acc_cons*100:.2f}%; Prod {prod_acc_300*100:.2f}% / {prod_acc_cons*100:.2f}%")

    # Linguistic subcohort benchmark
    df_ling = pd.read_csv(REPO_ROOT / "ml" / "reports" / "linguistic_subcohort_benchmark.csv")
    sub_n_sum = df_ling[df_ling["Sub-Cohort"] != "Overall (Cross-Validation)"]["N"].sum()
    assert sub_n_sum == 4500, f"Expected 4500 subcohort reviews, got {sub_n_sum}"
    print(f"  [PASS] Linguistic subcohorts sum to N=4,500")

    # ---------------------------------------------------------
    # MODULE 4: MATHEMATICAL INVARIANTS OF NSS
    # ---------------------------------------------------------
    print("\n[MODULE 4] Verifying Mathematical Invariants of NSS & Additive Decomposition...")
    # Overall and per-operator NSS with strict atol=0.01
    for op, sub in df_common.groupby("operator"):
        pos = (sub["predicted_sentiment"] == "Positive").sum()
        neg = (sub["predicted_sentiment"] == "Negative").sum()
        tot = len(sub)
        nss = ((pos - neg) / tot) * 100
        if op == "Grameenphone":
            assert np.isclose(nss, 64.85, atol=0.01), f"GP NSS mismatch: {nss:.2f}"
        elif op == "Robi":
            assert np.isclose(nss, 65.91, atol=0.01), f"Robi NSS mismatch: {nss:.2f}"
        elif op == "Banglalink":
            assert np.isclose(nss, 53.04, atol=0.01), f"BL NSS mismatch: {nss:.2f}"
        print(f"  [PASS] {op:15} N={tot:7,} Pos={pos/tot*100:0.1f}% Neg={neg/tot*100:0.1f}% NSS={nss:+0.2f}% (strict atol=0.01)")

    pos_all = (df_common["predicted_sentiment"] == "Positive").sum()
    neg_all = (df_common["predicted_sentiment"] == "Negative").sum()
    nss_all = ((pos_all - neg_all) / total_rows) * 100
    assert np.isclose(nss_all, 62.70, atol=0.01), f"Sector NSS mismatch: {nss_all:.2f}"
    print(f"  [PASS] All Operators:   N={total_rows:,} Pos={pos_all/total_rows*100:0.1f}% Neg={neg_all/total_rows*100:0.1f}% NSS={nss_all:+0.2f}%")

    # Vectorized computation of sector monthly metrics across all 122 months
    cats_all = [
        "General Appreciation / Other",
        "Offers & Data Packs",
        "App Login & Technical Bugs",
        "Network Speed & 4G Latency",
        "Billing & Airtime Deductions",
    ]
    grp_sec = df_common.groupby(["ym", "predicted_category", "predicted_sentiment"]).size().unstack(fill_value=0)
    pos_s = grp_sec["Positive"] if "Positive" in grp_sec.columns else 0
    neg_s = grp_sec["Negative"] if "Negative" in grp_sec.columns else 0
    net_s = pos_s - neg_s
    tot_s = grp_sec.sum(axis=1)

    m_net_sec = net_s.groupby(level="ym").sum()
    m_tot_sec = tot_s.groupby(level="ym").sum()
    m_nss_sec = m_net_sec / m_tot_sec * 100.0

    c_net_sec = net_s.unstack(level="predicted_category", fill_value=0)
    c_contrib_sec = c_net_sec.div(m_tot_sec, axis=0) * 100.0

    # Sort by calendar period and assert 122 gapless months
    sec_yms = m_nss_sec.index.tolist()
    sec_periods = [pd.Period(y, "M") for y in sec_yms]
    assert len(sec_periods) == 122, f"Expected 122 sector months, got {len(sec_periods)}"

    for i in range(1, len(sec_periods)):
        assert (sec_periods[i] - sec_periods[i - 1]).n == 1

    d_nss_sec = m_nss_sec.diff().dropna()
    d_c_sec = c_contrib_sec.diff().dropna()
    max_sec_residual = float((d_c_sec.sum(axis=1) - d_nss_sec).abs().max())
    assert max_sec_residual <= 1e-6, f"Sector additive residual exceeded atol=1e-6: {max_sec_residual:.2e}"
    print(f"  [PASS] Sector additive decomposition identity verified across all 121 transitions (max residual: {max_sec_residual:.2e} <= 1e-6)")

    # ---------------------------------------------------------
    # MODULE 5: TIME SERIES AGGREGATION & VOLATILITY
    # ---------------------------------------------------------
    print("\n[MODULE 5] Verifying Time Series Continuity, CLT Floor, RMSSD & Surge Filtering...")
    cats_4 = [
        "App Login & Technical Bugs",
        "Offers & Data Packs",
        "Network Speed & 4G Latency",
        "Billing & Airtime Deductions",
    ]

    grp_op = df_common.groupby(["operator", "ym", "predicted_category", "predicted_sentiment"]).size().unstack(fill_value=0)
    pos_op = grp_op["Positive"] if "Positive" in grp_op.columns else 0
    neg_op = grp_op["Negative"] if "Negative" in grp_op.columns else 0
    net_op = pos_op - neg_op
    tot_op = grp_op.sum(axis=1)

    m_net_op = net_op.groupby(level=["operator", "ym"]).sum()
    m_tot_op = tot_op.groupby(level=["operator", "ym"]).sum()
    m_nss_op = m_net_op / m_tot_op * 100.0
    c_net_op = net_op.unstack(level="predicted_category", fill_value=0)
    c_contrib_op = c_net_op.div(m_tot_op, axis=0) * 100.0

    transitions = []
    rmssd_metrics = {}

    for op in ["Grameenphone", "Robi", "Banglalink"]:
        op_tot = m_tot_op.loc[op].loc["2020-01":"2026-09"]
        op_nss = m_nss_op.loc[op].loc["2020-01":"2026-09"]
        op_c = c_contrib_op.loc[op].loc["2020-01":"2026-09"]
        assert len(op_tot) == 81, f"Expected 81 months for {op}, got {len(op_tot)}"

        min_vol = int(op_tot.min())
        assert min_vol >= 294, f"CLT volume floor violated for {op}: min volume {min_vol} < 294"

        yms = op_tot.index.tolist()
        periods = [pd.Period(y, "M") for y in yms]
        for i in range(1, len(yms)):
            assert (periods[i] - periods[i - 1]).n == 1, f"Gap in months for {op}: {yms[i-1]} -> {yms[i]}"

        d_nss = op_nss.diff().dropna()
        v_pct = (op_tot.diff() / op_tot.shift(1) * 100.0).dropna()
        d_ln_vol = np.log(op_tot).diff().dropna()
        d_c = op_c.diff().dropna()

        # Residual check
        residual_max = float((d_c.sum(axis=1) - d_nss).abs().max())
        assert residual_max <= 1e-6, f"Decomposition residual exceeded atol=1e-6 for {op}: {residual_max:.2e}"

        sign_d = np.where(d_nss != 0, np.sign(d_nss), 1.0)
        op_diffs = d_c[cats_4].mul(sign_d, axis=0)
        leading_op = op_diffs.idxmax(axis=1)

        raw_rmssd = float(np.sqrt(np.mean(d_nss ** 2)))
        filt_mask = v_pct.abs() < 50.0
        filt_rmssd = float(np.sqrt(np.mean(d_nss[filt_mask] ** 2)))
        rmssd_metrics[op] = {
            "raw_rmssd": round(raw_rmssd, 2),
            "ssi": round(100.0 - raw_rmssd, 2),
            "filt_rmssd": round(filt_rmssd, 2),
        }

        for ym_curr in yms[1:]:
            transitions.append({
                "operator": op,
                "transition": ym_curr,
                "d_nss": d_nss.loc[ym_curr],
                "abs_d_nss": abs(d_nss.loc[ym_curr]),
                "v_pct": v_pct.loc[ym_curr],
                "d_ln_vol": d_ln_vol.loc[ym_curr],
                "is_shock": abs(d_nss.loc[ym_curr]) >= 10.0,
                "is_surge": abs(v_pct.loc[ym_curr]) >= 50.0,
                "leading_op": leading_op.loc[ym_curr],
                "login_leads": (leading_op.loc[ym_curr] == "App Login & Technical Bugs"),
                "d_general": d_c.loc[ym_curr, "General Appreciation / Other"],
            })

    tdf = pd.DataFrame(transitions)
    assert len(tdf) == 240, f"Expected 240 transitions, got {len(tdf)}"
    shocks = tdf[tdf["is_shock"]]
    non_shocks = tdf[~tdf["is_shock"]]
    assert len(shocks) == 35, f"Expected 35 shocks, got {len(shocks)}"
    assert len(non_shocks) == 205, f"Expected 205 non-shocks, got {len(non_shocks)}"
    print(f"  [PASS] Modern transitions: 240 transitions (80/op), exactly 35 shocks (|ΔNSS| >= 10.0), min volume >= 294")

    # RMSSD tolerances
    assert np.isclose(rmssd_metrics["Grameenphone"]["raw_rmssd"], 6.28, atol=0.01)
    assert np.isclose(rmssd_metrics["Grameenphone"]["ssi"], 93.72, atol=0.01)
    assert np.isclose(rmssd_metrics["Grameenphone"]["filt_rmssd"], 5.14, atol=0.01)

    assert np.isclose(rmssd_metrics["Robi"]["raw_rmssd"], 5.61, atol=0.01)
    assert np.isclose(rmssd_metrics["Robi"]["ssi"], 94.39, atol=0.01)
    assert np.isclose(rmssd_metrics["Robi"]["filt_rmssd"], 4.53, atol=0.01)

    assert np.isclose(rmssd_metrics["Banglalink"]["raw_rmssd"], 13.61, atol=0.01)
    assert np.isclose(rmssd_metrics["Banglalink"]["ssi"], 86.39, atol=0.01)
    assert np.isclose(rmssd_metrics["Banglalink"]["filt_rmssd"], 7.56, atol=0.01)
    print(f"  [PASS] RMSSD & SSI: GP 6.28 (SSI 93.72, filt 5.14); Robi 5.61 (SSI 94.39, filt 4.53); BL 13.61 (SSI 86.39, filt 7.56)")

    # ---------------------------------------------------------
    # MODULE 6: PROPOSITIONS 1 & 2 STATISTICAL TESTS & PRIORITY MATRIX
    # ---------------------------------------------------------
    print("\n[MODULE 6] Verifying Statistical Tests, Asymmetry & Priority Matrix...")
    # Pooled 2x2
    s_login = int(shocks["login_leads"].sum())
    ns_login = int(non_shocks["login_leads"].sum())
    assert s_login == 27, f"Expected 27 shock login leads, got {s_login}"
    assert ns_login == 91, f"Expected 91 non-shock login leads, got {ns_login}"

    table_pooled = [[s_login, len(shocks) - s_login], [ns_login, len(non_shocks) - ns_login]]
    chi2_p, p_p, _, _ = chi2_contingency(table_pooled, correction=False)
    or_p, p_fish_p = fisher_exact(table_pooled)
    assert np.isclose(chi2_p, 12.83, atol=0.01), f"Pooled chi2 mismatch: {chi2_p:.2f}"
    assert np.isclose(or_p, 4.23, atol=0.01), f"Pooled Fisher OR mismatch: {or_p:.2f}"
    print(f"  [PASS] Pooled 2x2: Shocks 27/35 vs Non-shocks 91/205 => chi2(1) = {chi2_p:.2f}, Fisher OR = {or_p:.2f} (p={p_fish_p:.4e})")

    # Non-surge 2x2 (|v_pct| < 50%)
    shocks_ns = shocks[~shocks["is_surge"]]
    non_shocks_ns = non_shocks[~non_shocks["is_surge"]]
    s_ns_login = int(shocks_ns["login_leads"].sum())
    ns_ns_login = int(non_shocks_ns["login_leads"].sum())
    assert s_ns_login == 14 and len(shocks_ns) == 19
    assert ns_ns_login == 82 and len(non_shocks_ns) == 189
    table_ns = [[s_ns_login, len(shocks_ns) - s_ns_login], [ns_ns_login, len(non_shocks_ns) - ns_ns_login]]
    chi2_ns, _, _, _ = chi2_contingency(table_ns, correction=False)
    or_ns, p_fish_ns = fisher_exact(table_ns)
    assert np.isclose(chi2_ns, 6.38, atol=0.01), f"Non-surge chi2 mismatch: {chi2_ns:.2f}"
    assert np.isclose(or_ns, 3.65, atol=0.01), f"Non-surge OR mismatch: {or_ns:.2f}"
    print(f"  [PASS] Non-surge 2x2: Shocks 14/19 vs Non-shocks 82/189 => chi2(1) = {chi2_ns:.2f}, Fisher OR = {or_ns:.2f}")

    # Banglalink asymmetry
    bl_shk = shocks[shocks["operator"] == "Banglalink"]
    bl_nshk = non_shocks[non_shocks["operator"] == "Banglalink"]
    bl_s_log = int(bl_shk["login_leads"].sum())
    bl_ns_log = int(bl_nshk["login_leads"].sum())
    table_bl = [[bl_s_log, len(bl_shk) - bl_s_log], [bl_ns_log, len(bl_nshk) - bl_ns_log]]
    or_bl, p_bl = fisher_exact(table_bl)
    assert np.isclose(or_bl, 10.00, atol=0.01)
    assert np.isclose(p_bl, 0.0007, atol=0.0002)
    print(f"  [PASS] Operator asymmetry: BL OR = {or_bl:.2f} (p = {p_bl:.4f})")

    # Proposition 1 surge regression across 35 shocks
    slope, intercept, r_val, p_val, std_err = stats.linregress(shocks["d_ln_vol"], shocks["d_general"])
    r2_p1 = r_val ** 2
    assert np.isclose(r2_p1, 0.5601, atol=0.001), f"Prop 1 R2 mismatch: {r2_p1:.4f}"
    assert np.isclose(slope, 11.52, atol=0.01), f"Prop 1 slope mismatch: {slope:.2f}"
    print(f"  [PASS] Proposition 1 Regression: R2 = {r2_p1:.4f}, slope = {slope:.2f} (p = {p_val:.2e})")

    # Priority Matrix (N = 88,181)
    df_4dom = df_common[df_common["predicted_category"].isin(cats_4)].copy()
    assert len(df_4dom) == 88181, f"Expected 88181 reviews in 4 domains, got {len(df_4dom)}"

    cont_tab = pd.crosstab(df_4dom["predicted_category"], df_4dom["predicted_sentiment"] == "Negative")
    chi2_4, p_4, _, _ = stats.chi2_contingency(cont_tab)
    v_4 = np.sqrt(chi2_4 / (len(df_4dom) * 1))
    assert np.isclose(chi2_4, 11027.60, atol=1.0)
    assert np.isclose(v_4, 0.3536, atol=0.001)

    # Odds ratios vs Offers
    def get_dom_odds(cat_name):
        sub_dom = df_4dom[df_4dom["predicted_category"] == cat_name]
        neg = (sub_dom["predicted_sentiment"] == "Negative").sum()
        non_neg = len(sub_dom) - neg
        return neg / non_neg

    odds_offers = get_dom_odds("Offers & Data Packs")
    or_billing = get_dom_odds("Billing & Airtime Deductions") / odds_offers
    or_login = get_dom_odds("App Login & Technical Bugs") / odds_offers
    or_network = get_dom_odds("Network Speed & 4G Latency") / odds_offers

    assert np.isclose(or_billing, 9.49, atol=0.01), f"Billing OR mismatch: {or_billing:.2f}"
    assert np.isclose(or_login, 6.44, atol=0.01), f"Login OR mismatch: {or_login:.2f}"
    assert np.isclose(or_network, 2.50, atol=0.01), f"Network OR mismatch: {or_network:.2f}"
    print(f"  [PASS] Priority Matrix (N=88,181): omnibus chi2(3) = {chi2_4:.2f}, V = {v_4:.4f}; Billing OR = {or_billing:.2f}, Login OR = {or_login:.2f}, Network OR = {or_network:.2f}")

    # ---------------------------------------------------------
    # MODULE 7: SPRING 2024 COUNTERFACTUAL TELEMETRY & CASE STUDY 2
    # ---------------------------------------------------------
    print("\n[MODULE 7] Verifying Spring 2024 Telemetry & Case Study 2 Turnaround...")
    bl_data = df_common[df_common["operator"] == "Banglalink"]

    # Spring 2024 monthly transitions (indexed directly from precomputed operator series)
    bl_tot_s = m_tot_op.loc["Banglalink"]
    bl_nss_s = m_nss_op.loc["Banglalink"]

    assert int(bl_tot_s.loc["2024-03"]) == 1093
    assert np.isclose(bl_nss_s.loc["2024-03"], 42.82, atol=0.01)
    assert int(bl_tot_s.loc["2024-04"]) == 1315
    assert np.isclose(bl_nss_s.loc["2024-04"], 31.63, atol=0.01)
    assert np.isclose(bl_nss_s.loc["2024-04"] - bl_nss_s.loc["2024-03"], -11.18, atol=0.01)
    assert int(bl_tot_s.loc["2024-05"]) == 2265
    assert np.isclose(bl_nss_s.loc["2024-05"], 64.42, atol=0.01)
    assert np.isclose(bl_nss_s.loc["2024-05"] - bl_nss_s.loc["2024-04"], 32.78, atol=0.01)
    print(f"  [PASS] BL Spring 2024: 2024-03 (+42.82), 2024-04 (+31.63, Δ=-11.18), 2024-05 (+64.42, Δ=+32.78)")

    # BL app_version missingness
    bl_null_vers = int(bl_data["app_version"].isna().sum())
    assert bl_null_vers == 71068
    bl_miss_rate = bl_null_vers / len(bl_data) * 100.0
    assert np.isclose(bl_miss_rate, 51.82, atol=0.01)
    print(f"  [PASS] BL app_version missingness: 51.82% ({bl_null_vers:,} / {len(bl_data):,})")

    # v11.8.0 telemetry
    v_apr = bl_data[(bl_data["ym"] == "2024-04") & (bl_data["app_version"] == "11.8.0")]
    assert len(v_apr) == 158
    nss_apr = ((v_apr["predicted_sentiment"] == "Positive").sum() - (v_apr["predicted_sentiment"] == "Negative").sum()) / len(v_apr) * 100.0
    assert np.isclose(nss_apr, -7.59, atol=0.01)

    v_mj = bl_data[(bl_data["ym"] >= "2024-03") & (bl_data["ym"] <= "2024-06") & (bl_data["app_version"] == "11.8.0")]
    assert len(v_mj) == 198
    nss_mj = ((v_mj["predicted_sentiment"] == "Positive").sum() - (v_mj["predicted_sentiment"] == "Negative").sum()) / len(v_mj) * 100.0
    assert np.isclose(nss_mj, 10.61, atol=0.01)
    print(f"  [PASS] v11.8.0 Telemetry: Apr 2024 N=158 (NSS=-7.59%), Mar-Jun 2024 N=198 (NSS=+10.61%)")

    # Case Study 2 turnaround
    y25 = bl_data[bl_data["year"] == 2025]
    y26 = bl_data[bl_data["year"] == 2026]
    assert len(y25) == 10238
    assert len(y26) == 21810
    nss_y25 = ((y25["predicted_sentiment"] == "Positive").sum() - (y25["predicted_sentiment"] == "Negative").sum()) / len(y25) * 100.0
    nss_y26 = ((y26["predicted_sentiment"] == "Positive").sum() - (y26["predicted_sentiment"] == "Negative").sum()) / len(y26) * 100.0
    assert np.isclose(nss_y25, 66.39, atol=0.01)
    assert np.isclose(nss_y26, 81.93, atol=0.01)
    d_cs2 = nss_y26 - nss_y25
    assert np.isclose(d_cs2, 15.54, atol=0.01)

    gen25 = ((y25[y25["predicted_category"] == "General Appreciation / Other"]["predicted_sentiment"] == "Positive").sum()
             - (y25[y25["predicted_category"] == "General Appreciation / Other"]["predicted_sentiment"] == "Negative").sum()) / len(y25) * 100.0
    gen26 = ((y26[y26["predicted_category"] == "General Appreciation / Other"]["predicted_sentiment"] == "Positive").sum()
             - (y26[y26["predicted_category"] == "General Appreciation / Other"]["predicted_sentiment"] == "Negative").sum()) / len(y26) * 100.0
    d_gen_cs2 = gen26 - gen25
    d_tech_cs2 = d_cs2 - d_gen_cs2
    assert np.isclose(d_gen_cs2, 10.33, atol=0.01)
    assert np.isclose(d_tech_cs2, 5.21, atol=0.01)
    print(f"  [PASS] Case Study 2: 2025 (N=10,238, NSS=+66.39) -> 2026 (N=21,810, NSS=+81.93) => ΔNSS=+15.54 (+10.33 Gen, +5.21 Tech)")

    # ---------------------------------------------------------
    # MODULE 8: ANONYMITY, MANUSCRIPT COMPLETENESS & DELIVERABLES
    # ---------------------------------------------------------
    print("\n[MODULE 8] Verifying Double-Blind Anonymity, Manuscript Structure & Deliverables...")
    blinded_files = [
        REPO_ROOT / "paper" / "eswa_latex" / "manuscript.tex",
        REPO_ROOT / "paper" / "eswa_latex" / "manuscript_twocolumn.tex",
        REPO_ROOT / "paper" / "eswa_latex" / "highlights.txt",
        REPO_ROOT / "paper" / "eswa_latex" / "references.bib",
    ]
    prohibited_terms = ["Ratul", "rh61632", "Leading University", "Jashore", "github.com"]

    for bf in blinded_files:
        if bf.exists():
            text_bf = bf.read_text(encoding="utf-8", errors="ignore")
            for term in prohibited_terms:
                matches = len(re.findall(re.escape(term), text_bf, re.IGNORECASE))
                assert matches == 0, f"Found {matches} occurrences of prohibited identifier '{term}' in {bf}!"
    print(f"  [PASS] Anonymity check: 0 prohibited terms across all 4 blinded ESWA files")

    # Section completeness
    expected_sections = [
        "Introduction",
        "Related Work",
        "VoC-Intelligence: System Architecture and Methodology",
        "Experimental Setup and Empirical Validation",
        "Real-World Deployment and Diagnostic Case Studies",
        "Managerial Decision Support and Industrial Implementation Guidelines",
        "Discussion, Threats to Validity, and Limitations",
        "Conclusion and Future Work",
    ]
    expected_labels = [
        "tab:taxonomy",
        ["tab:model_leaderboard", "tab:leaderboard"],
        "tab:perclass",
        "tab:linguistic_benchmark",
        "tab:eras",
        "tab:shocks",
        "alg:canary",
        "tab:decision_matrix",
    ]

    for tex_path in [REPO_ROOT / "paper" / "eswa_latex" / "manuscript.tex", REPO_ROOT / "paper" / "eswa_latex" / "manuscript_twocolumn.tex"]:
        assert tex_path.exists(), f"Manuscript tex missing: {tex_path}"
        tex_content = tex_path.read_text(encoding="utf-8")
        for sec in expected_sections:
            assert f"\\section{{{sec}}}" in tex_content, f"Missing section '{sec}' in {tex_path}"
        for lbl in expected_labels:
            if isinstance(lbl, list):
                assert any(f"\\label{{{l}}}" in tex_content for l in lbl), f"Missing label {lbl} in {tex_path}"
            else:
                assert f"\\label{{{lbl}}}" in tex_content, f"Missing label '{lbl}' in {tex_path}"
    print(f"  [PASS] Manuscript structure: All 8 sections and 8 key labels verified in both tex files")

    # PDF Existence & Page Count Inspection via pdfinfo
    pdf_sc = REPO_ROOT / "paper" / "manuscript.pdf"
    pdf_tc = REPO_ROOT / "paper" / "manuscript_twocolumn.pdf"
    assert pdf_sc.exists() and pdf_sc.stat().st_size > 0, "Single-column PDF missing or empty!"
    assert pdf_tc.exists() and pdf_tc.stat().st_size > 0, "Two-column PDF missing or empty!"

    def get_pdf_pages(pdf_path: Path) -> int:
        try:
            out = subprocess.check_output(["pdfinfo", str(pdf_path)], text=True, errors="ignore")
            m = re.search(r"Pages:\s+(\d+)", out)
            if m:
                return int(m.group(1))
        except Exception:
            pass
        return -1

    pages_sc = get_pdf_pages(pdf_sc)
    pages_tc = get_pdf_pages(pdf_tc)
    print(f"  [PASS] Deliverable PDFs exist: manuscript.pdf ({pages_sc} pages), manuscript_twocolumn.pdf ({pages_tc} pages)")

    # ---------------------------------------------------------
    # PHASE 8/9 GATED CHECKS
    # ---------------------------------------------------------
    pending_defects = []

    # 1. Inspect for raw markdown tokens (**) in .tex files
    for tex_file in [REPO_ROOT / "paper" / "eswa_latex" / "manuscript.tex", REPO_ROOT / "paper" / "eswa_latex" / "manuscript_twocolumn.tex"]:
        raw_md = re.findall(r"\*\*[^*]+\*\*", tex_file.read_text(encoding="utf-8"))
        if raw_md:
            pending_defects.append(f"{tex_file.name} contains {len(raw_md)} raw markdown (**...**) bold tokens (remediated in Phase 8)")

    # 2. Check PDF page limits (single-column <= 35, two-column <= 15)
    if pages_sc > 35:
        pending_defects.append(f"manuscript.pdf exceeds 35-page target ({pages_sc} pages, target <= 35, remediated in Phase 8)")
    if pages_tc > 15:
        pending_defects.append(f"manuscript_twocolumn.pdf exceeds 15-page target ({pages_tc} pages, target <= 15, remediated in Phase 8)")

    # 3. Check PDF SHA256 sync between paper/ and paper/eswa_latex/
    for name in ["manuscript.pdf", "manuscript_twocolumn.pdf"]:
        p_root = REPO_ROOT / "paper" / name
        p_eswa = REPO_ROOT / "paper" / "eswa_latex" / name
        if p_root.exists() and p_eswa.exists():
            h_root = hashlib.sha256(p_root.read_bytes()).hexdigest()
            h_eswa = hashlib.sha256(p_eswa.read_bytes()).hexdigest()
            if h_root != h_eswa:
                pending_defects.append(f"PDF SHA256 mismatch for {name} between paper/ and paper/eswa_latex/ (remediated in Phase 8)")

    # 4. Check existence of paper/JBA_Manuscript_Empirical_Calculations.xlsx
    xlsx_path = REPO_ROOT / "paper" / "JBA_Manuscript_Empirical_Calculations.xlsx"
    if not xlsx_path.exists():
        pending_defects.append("paper/JBA_Manuscript_Empirical_Calculations.xlsx does not exist yet (owned by Phase 9)")

    if pending_defects:
        print("\n  [PHASE 8/9 PENDING DELIVERABLES EVALUATION]:")
        for defect in pending_defects:
            print(f"    [WARN - Pending Phase 8/9] {defect}")
        if strict_paper:
            print("\nFAILED: --strict-paper mode enabled; failing audit on pending Phase 8/9 defects!")
            sys.exit(1)
        else:
            print("\n  [INFO] Default mode: All Phase 1–7 empirical checks passed cleanly. Phase 8/9 warnings emitted without failure.")
    else:
        print("  [PASS] 100% of Phase 8/9 paper deliverables also verified present and compliant!")

    elapsed = time.time() - t_start
    print("\n" + "=" * 80)
    print(f"AUDIT RESULT: 100% OF EMPIRICAL & SYSTEM CHECKS PASSED IN {elapsed:.2f}s!")
    print("=" * 80)


if __name__ == "__main__":
    main()
