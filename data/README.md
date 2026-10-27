# 📊 Telecom VoC Ground Truth & Human Validation Datasets

This directory serves as the canonical home for all labeled datasets used for model training, benchmarking, and empirical human verification.

---

## 1. Curated Training Seed Dataset (`data/processed/`, $N = 4,500$)

The multi-operator seed dataset used across all Classical Machine Learning (`ml/`) and Deep Learning (`dl/`) training pipelines:
- `data/processed/mygp_classified_reviews.csv` (1,500 reviews)
- `data/processed/myrobi_classified_reviews.csv` (1,500 reviews)
- `data/processed/mybl_classified_reviews.csv` (1,500 reviews)

Each review contains dual annotations:
1. **Sentiment**: `Positive`, `Neutral`, `Negative`
2. **Operational Category**: `Offers & Data Packs`, `App Login & Technical Bugs`, `Network Speed & 4G Latency`, `Billing & Airtime Deductions`, `General Appreciation / Other`

---

## 2. Verified Human Gold Standard (`data/gold_set/`)

Dual-annotator zero-leakage human ground truth used for empirical inter-annotator reliability and production model auditing:
- `data/gold_set/blind_annotation_300_ratul.csv` (Primary blind human review, $N = 300$)
- `data/gold_set/blind_annotation_200_friend.csv` (Overlapping independent secondary review, $N = 200$)
- `data/gold_set/calculate_agreement.py` (Cohen's Kappa evaluator: $\kappa = 0.7694$ Substantial Agreement)
- `data/gold_set/ANNOTATION_RULEBOOK.md` (Taxonomy annotation protocol & edge cases)
- `data/gold_set/gold_standard_evaluation_report.md` (Scientific evaluation report)
- `data/gold_set/comprehensive_benchmark_table.md` (Multi-model benchmark table against human consensus)

To compute inter-annotator reliability:
```bash
python data/gold_set/calculate_agreement.py
```

---

> ℹ️ **Note**: The master multi-year corpus ($N = 434,803$, 2020–2026) and the 1,072-day common window benchmark ($N = 285,111$) are maintained in [`scraped_data_global_2020_2026/`](../scraped_data_global_2020_2026/).
