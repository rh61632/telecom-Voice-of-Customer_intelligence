# Plan 1.1 Summary: Scraping, Merge, Common-Window & Telemetry Pipeline Audit

**Phase:** 1 - Core Pipeline, Data, Demo & Documentation Audit  
**Plan:** `1-PLAN.md` (Plan 1 of 3)  
**Status:** Completed  
**Execution Mode:** Strictly Read-Only Audit (`ADR-001`)  
**Date:** 2026-11-11  

---

## 1. Executive Summary

Plan 1.1 conducted a comprehensive, strictly read-only empirical audit of the data acquisition, regional merge, global classification, common-window synchronization, and NSS telemetry analytics pipeline across `scraped_data_global/` and `scripts/`. 

All findings were established with non-destructive streaming analysis, exact row parsing, and code inspection without modifying any project, source, model, or paper files outside `.gsd/`, and without modifying git working-tree state in accordance with `ADR-001` and `ADR-002`.

---

## 2. Completed Tasks

| Task | Description | Evidence Artifact | Status |
|---|---|---|---|
| **Task 1** | Audit Google Play scraping scripts, raw CSV schemas, and pipeline column preservation | `.gsd/phases/1/evidence/01_scraping_and_raw_schema_audit.md` | **PASSED** |
| **Task 2** | Audit merge, global classification, common-window synchronization, and NSS telemetry analytics | `.gsd/phases/1/evidence/01_merge_sync_telemetry_audit.md` | **PASSED** |

---

## 3. Key Empirical Findings & Discrepancy Catalog

### 3.1 Raw CSV Schemas & Severe Overwrite / Column-Dropping Hazard
- **On-Disk Reality:** All three raw CSV files (`mygp_global.csv`, `myrobi_global.csv`, `mybl_global.csv`) contain **12 columns**:
  `['review_id', 'user_name', 'rating', 'review_date', 'review_text', 'thumbs_up', 'operator', 'app_version', 'user_image', 'developer_reply', 'developer_reply_date', 'is_enriched']`.
  - Parsed rows: GP: `321,374`, Robi: `200,652`, BL: `139,134` (Total: `661,160` parsed rows).
  - Physical text lines total `730,959` due to embedded newlines in review and reply texts.
- **Code Vulnerability 1 (`scraper_worker.py`):** Lines 49–57, 137–140, and 203–211 define and write only 7 hardcoded columns. Running `scraper_worker.py` in full mode overwrites raw CSVs and strips `app_version` and metadata. Running in incremental mode appends 7-column rows to 12-column CSVs, corrupting schema alignment.
- **Code Vulnerability 2 (`merge_and_sync_all_datasets.py`):** Line 272 explicitly filters `dedup` to 7 columns and overwrites `raw_out` (`my*_global.csv`). Running this script permanently wipes out `app_version`, `user_image`, `developer_reply`, `developer_reply_date`, and `is_enriched` from disk.
- **Downstream Breakage:** `scripts/check_version_bias.py` line 6 requires `df['has_version'] = df['app_version'].notna()`. Overwriting raw files breaks this downstream script with `KeyError: 'app_version'`.

### 3.2 Platform Portability Issue
- In `run_parallel_scrapers.py:22`, `PYTHON_BIN` is hardcoded as `PROJECT_ROOT / "dl" / ".venv" / "bin" / "python"` (POSIX layout). On Windows, virtual environments use `Scripts/python.exe`. As a result, the check fails on Windows and falls back to `sys.executable`, which fails if dependencies (`google_play_scraper`) are isolated within `dl/.venv`.

### 3.3 Common-Window Cutoff & 27-Row Discrepancy
- **Boundary Conflict:**
  - `merge_and_sync_all_datasets.py:290` hardcodes `2016-08-01 00:00:00` to align with the first complete calendar month (yielding **3,713 days** and **655,649 reviews**).
  - `sync_post_classification.py:58` uses `start_common = max(min_dates)` which yields Grameenphone's earliest review `2016-07-28 22:36:00` (yielding **3,716 days** and **655,676 reviews**).
- **On-Disk Truth:** `all_operators_common_duration_classified.csv` on disk contains **655,649 rows** (GP: 320,140, Robi: 198,378, BL: 137,131), strictly matching the `2016-08-01` calendar-month start date.
- **Overwriting Risk:** Running `sync_post_classification.py` would overwrite the common duration dataset with 655,676 rows and reintroduce a partial 4-day July 2016 month.

### 3.4 Summary JSON Schema Inconsistency
- In `merge_and_sync_all_datasets.py:317-324`, `common_duration_summary.json` is generated without count metrics (`positive_count`, `neutral_count`, `negative_count`).
- In `sync_post_classification.py:86-96`, those counts are preserved.
- The on-disk `common_duration_summary.json` has `total_reviews: 655,649` but includes the count fields from `sync_post_classification.py`.

### 3.5 Model Checkpoint & PyTorch Architecture Divergence
- **PyTorch Class Duplication:** `Vocabulary`, `BahdanauAttention`, and `HybridBiLSTMAttention` are verbatim duplicates across `classify_global_dataset.py:24-67` and `merge_and_sync_all_datasets.py:26-69`.
- **Architectural Disconnect:** `dl/predict_dl.py` uses `BiLSTMWithAttention` (with character embeddings, loading `bilstm_attention_model.pt`), whereas the pipeline scripts use `HybridBiLSTMAttention` (word-only, loading `bilstm_sentiment_model.pt`).
- **Classifier Divergence:** `classify_global_dataset.py` loads `sentiment_voting_classifier.joblib` (5.65 MB, FeatureUnion pipeline), whereas `ml/predict.py` loads `ensemble_voting_classifier.joblib` (3.98 MB, single TfidfVectorizer pipeline).

### 3.6 NSS Telemetry & Reconciliation of Shocks (35 vs 37 vs 98)
- In `evaluate_nss_stability_and_shocks.py`, CLT floor ($N \ge 30$) and shock threshold ($|\Delta\text{NSS}| \ge 10.0$ pp) are applied with exact additive category attribution math ($\Delta \text{NSS} = \sum_c \Delta \text{Contrib}_c$).
- **Reconciliation:**
  1. `nss_significant_shocks.csv` has **98 rows**, representing all qualifying shocks across the full 10-year common window (2016–2026).
  2. `nss_stability_and_shocks_summary.json` lists **37 recent shocks**, which includes the 2 cross-era boundary transitions from December 2019 to January 2020 (`Grameenphone 2019-12 -> 2020-01` and `Robi 2019-12 -> 2020-01`).
  3. `scripts/tally_35_shocks.py` and the **ESWA manuscript** evaluate strictly the 240 intra-era monthly transitions within the modern high-volume era (Jan 2020 to Sep 2026, 80 transitions per operator $\times$ 3 operators = 240 transitions). Across these 240 transitions, there are **EXACTLY 35 SHOCKS** (GP: 6, Robi: 7, BL: 22).
  4. App Login & Technical Bugs led in **27 of 35 shocks (77.1%)**, exactly matching the manuscript's core empirical proposition.

---

## 4. Verification Proof

- Task 1 Evidence: `.gsd/phases/1/evidence/01_scraping_and_raw_schema_audit.md` (created and verified)
- Task 2 Evidence: `.gsd/phases/1/evidence/01_merge_sync_telemetry_audit.md` (created and verified)
- Verified with PowerShell command execution (zero errors, exit code 0).
- Git state: Untouched (`ADR-001` strictly maintained, no `git add` or `git commit` performed).
