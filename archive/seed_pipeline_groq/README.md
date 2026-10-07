# 🗄️ Archived: Groq LLM Seed Pipeline (Phase 1)

> **Status: SUPERSEDED** — Archived as of October 2026.  
> The global production pipeline in [`scraped_data_global_2020_2026/pipeline/`](../../scraped_data_global_2020_2026/pipeline/) is the canonical source of truth for all classification and analysis.

---

## What This Was

This directory contains the **original Phase 1 seed pipeline** — the earliest version of the VoC classification system, which used **Groq Cloud API (`qwen/qwen3-8b-27b`)** to zero-shot classify a small sample of reviews per operator.

It served two key purposes:
1. **Bootstrapping the gold standard dataset** — LLM-labeled reviews were used as starting candidates for human annotation (the human-verified gold set lives in [`archive/scraped_data_2020/gold_set/`](../scraped_data_2020/gold_set/)).
2. **Proof-of-concept** — Validated the 5-category taxonomy (`Billing & Airtime Deductions`, `Network Speed & 4G Latency`, `App Login & Technical Bugs`, `Offers & Data Packs`, `General Appreciation / Other`) before committing to full ML training.

---

## Directory Contents

```
seed_pipeline_groq/
├── src/                          # Original per-operator scrape + Groq classify scripts
│   ├── 01_scrape_mybl.py         # Scrape ~2,000 Banglalink reviews (BD store)
│   ├── 01_scrape_mygp.py         # Scrape ~2,000 Grameenphone reviews (BD store)
│   ├── 01_scrape_myrobi.py       # Scrape ~2,000 Robi reviews (BD store)
│   ├── 02_classify_reviews_mybl.py   # Groq API classification (Banglalink)
│   ├── 02_classify_reviews_mygp.py   # Groq API classification (Grameenphone)
│   └── 02_classify_reviews_myrobi.py # Groq API classification (Robi)
│
└── data/                         # Small-scale (~2k reviews/operator) seed datasets
    ├── raw/                      # Raw scraped reviews (no operator label, no review_id)
    │   ├── mybl_raw_reviews.csv
    │   ├── mygp_raw_reviews.csv
    │   └── myrobi_raw_reviews.csv
    └── processed/                # Groq-classified reviews (category + sentiment + english_summary)
        ├── mybl_classified_reviews.csv
        ├── mygp_classified_reviews.csv
        └── myrobi_classified_reviews.csv
```

---

## Why It Was Superseded

| Aspect | Seed Pipeline (this dir) | Global Pipeline |
|---|---|---|
| Scale | ~2,000 reviews/operator | 81k–161k reviews/operator |
| Classification | Groq LLM API (zero-shot) | Trained ML Ensemble (87.5% CV Acc) |
| Speed | ~2.1s/review (API throttle) | ~18,200 reviews/second |
| Cost | Groq API credits | Free (local inference) |
| Coverage | 2026 only (most recent) | 2020 – September 2026 |
| Schema | No `review_id`, no `operator` col in raw | Full UUID + operator label |

The trained ensemble models (`ml/models/sentiment_voting_classifier.joblib`, `category_voting_classifier.joblib`) replaced the Groq API as the production classifier after being calibrated on the human-annotated gold standard.

---

## To Re-Run (if needed)

```bash
# Requires: GROQ_API_KEY environment variable
export GROQ_API_KEY="your_key_here"

# Step 1: Scrape fresh reviews
python archive/seed_pipeline_groq/src/01_scrape_mygp.py
python archive/seed_pipeline_groq/src/01_scrape_myrobi.py
python archive/seed_pipeline_groq/src/01_scrape_mybl.py

# Step 2: Classify via Groq API
python archive/seed_pipeline_groq/src/02_classify_reviews_mygp.py
python archive/seed_pipeline_groq/src/02_classify_reviews_myrobi.py
python archive/seed_pipeline_groq/src/02_classify_reviews_mybl.py
```

> ⚠️ Output writes to `archive/seed_pipeline_groq/data/` — does **not** affect the global production dataset.

