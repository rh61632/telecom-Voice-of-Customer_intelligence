# 📊 Curated Training Dataset ($N = 4,500$)

This directory contains the curated ground-truth training dataset used across all Classical Machine Learning (`ml/`) and Deep Learning (`dl/`) pipelines:

- `data/processed/mygp_classified_reviews.csv` (1,500 reviews)
- `data/processed/myrobi_classified_reviews.csv` (1,500 reviews)
- `data/processed/mybl_classified_reviews.csv` (1,500 reviews)

Each review contains dual annotations:
1. **Sentiment**: `Positive`, `Neutral`, `Negative`
2. **Operational Category**:
   - `Offers & Data Packs`
   - `App Login & Technical Bugs`
   - `Network Speed & 4G Latency`
   - `Billing & Airtime Deductions`
   - `General Appreciation / Other`

> ℹ️ **Note**: The master multi-year corpus ($N = 398,193$, 2020–2026) and the 1,072-day common window benchmark ($N = 248,501$) are maintained in [`scraped_data_global_2020_2026/`](../scraped_data_global_2020_2026/).
