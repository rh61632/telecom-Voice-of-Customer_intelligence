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
- `data/gold_set/blind_annotation_300_annotator1.csv` (Primary blind human review, $N = 300$, Annotator 1)
- `data/gold_set/blind_annotation_200_annotator2.csv` (Overlapping independent secondary review, $N = 200$, Annotator 2)
- `data/gold_set/calculate_agreement.py` (Cohen's Kappa evaluator: Sentiment $\kappa = 0.5762$, Category $\kappa = 0.7694$)
- `data/gold_set/ANNOTATION_RULEBOOK.md` (Taxonomy annotation protocol & edge cases)
- `data/gold_set/gold_standard_evaluation_report.md` (Scientific evaluation report)
- `data/gold_set/comprehensive_benchmark_table.md` (Multi-model benchmark table against human consensus)

To compute inter-annotator reliability:
```bash
python data/gold_set/calculate_agreement.py
```

---

> ℹ️ **Note**: The master multi-year corpus ($N = 661,160$, 2014–2026) and the 3,713-day common window benchmark ($N = 655,649$, August 2016 – September 2026) are maintained in [`scraped_data_global/`](../scraped_data_global/).
