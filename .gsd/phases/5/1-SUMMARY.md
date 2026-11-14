# Phase 5 Plan 1: Pipeline Scripts, Review ID Hygiene & Telemetry JSONs Regeneration Summary

**Phase:** 5  
**Plan:** 1-PLAN.md  
**Status:** complete  
**Execution Mode:** `inherit` workspace, zero git commits (`ADR-003`)  
**Timestamp:** 2026-11-11  

---

## 1. Executive Summary

Plan 5.1 remediated the raw Google Play scraper worker, the parallel launcher, and the dataset merge script to enforce 12-column canonical metadata preservation, dynamic cross-platform interpreter resolution, and protection against dropping unique review IDs sharing identical 4-tuples. In addition, the single historical null `review_id` in Robi raw and classified datasets was resolved with a deterministic synthetic identifier (`ro_missing_72102`) preserving row counts exactly at $N = 200,652$. Finally, `sync_post_classification.py` was updated to enforce the canonical `2016-08-01` boundary and inclusive calendar duration ($3,713$ days), successfully regenerating all telemetry datasets, summary JSONs, and multi-year markdown reports.

---

## 2. Tasks Completed & Empirical Evidence

### Task 1: Update scraper workers and parallel runner for 12-column preservation and cross-platform execution
- **Files Modified:**
  - `scraped_data_global/pipeline/scraper_worker.py`
  - `scraped_data_global/pipeline/run_parallel_scrapers.py`
- **Actions Taken:**
  - Expanded `FIELDNAMES` in `scraper_worker.py` from 7 to all 12 canonical fields: `['review_id', 'user_name', 'rating', 'review_date', 'review_text', 'thumbs_up', 'operator', 'app_version', 'user_image', 'developer_reply', 'developer_reply_date', 'is_enriched']` (`DISC-CRIT-08`).
  - Parameterized `run_scraper(operator_key, incremental, lang="en", country="us")` and added `--lang` / `--country` CLI flags (`DISC-HYG-05`).
  - Added empty `reviewId` guard (`if not rev_id: continue`) and mapped all 12 fields from Google Play review elements.
  - Aligned incremental DataFrame construction and column reindexing against existing target CSV columns before appending.
  - Replaced hardcoded POSIX interpreter path in `run_parallel_scrapers.py` with `sys.executable` (`DISC-HYG-01`), forwarded `--lang`/`--country`, and verified worker exit codes.
- **Verification Command:**
  ```powershell
  python -c "import ast; ast.parse(open('scraped_data_global/pipeline/scraper_worker.py', encoding='utf-8').read()); ast.parse(open('scraped_data_global/pipeline/run_parallel_scrapers.py', encoding='utf-8').read()); from scraped_data_global.pipeline.scraper_worker import FIELDNAMES; assert len(FIELDNAMES) == 12; assert 'app_version' in FIELDNAMES and 'is_enriched' in FIELDNAMES; runner = open('scraped_data_global/pipeline/run_parallel_scrapers.py', encoding='utf-8').read(); assert 'dl/.venv/bin/python' not in runner; assert 'sys.executable' in runner; print('Task 1 verified: 12 raw columns and cross-platform runner confirmed.')"
  ```
- **Output:** `Task 1 verified: 12 raw columns and cross-platform runner confirmed.`

### Task 2: Harden merge script and resolve null review_id in raw and classified Robi datasets
- **Files Modified:**
  - `scraped_data_global/pipeline/merge_and_sync_all_datasets.py`
  - `scraped_data_global/raw/myrobi_global.csv`
  - `scraped_data_global/classified/myrobi_classified_global.csv`
- **Actions Taken:**
  - Defined `RAW_COLUMNS` (12 fields) in `merge_and_sync_all_datasets.py` and replaced 7-column slice at CSV write with `RAW_COLUMNS`.
  - Re-architected deduplication to preserve distinct non-null `review_id`s, preventing the unintended deletion of 44,303 historical overlap pairs.
  - Hardened merge against `op_existing` to join primarily on `review_id` and deduplicate on the 4-tuple prior to fallback joining, eliminating many-to-many row expansion.
  - Fixed inclusive days formula to `(end_common.normalize() - start_common.normalize()).days + 1` ($3,713$ days) (`DISC-MIN-06`).
  - Added `positive_count`, `neutral_count`, `negative_count` to summary JSON schema.
  - In `myrobi_global.csv` and `myrobi_classified_global.csv`, located index `72102` (`Shahidul Islam`, `2024-09-17 08:15:53`, `nice`) and assigned deterministic ID `ro_missing_72102` without row deletion (`DISC-HYG-05`).
- **Verification Command:**
  ```powershell
  python -c "import pandas as pd; df_raw = pd.read_csv('scraped_data_global/raw/myrobi_global.csv', low_memory=False); df_cls = pd.read_csv('scraped_data_global/classified/myrobi_classified_global.csv', low_memory=False); assert len(df_raw) == 200652, f'Expected 200652 raw, got {len(df_raw)}'; assert len(df_cls) == 200652, f'Expected 200652 cls, got {len(df_cls)}'; assert df_raw['review_id'].isna().sum() == 0, 'Found null review_id in raw'; assert df_cls['review_id'].isna().sum() == 0, 'Found null review_id in cls'; assert df_raw.loc[72102, 'review_id'] == 'ro_missing_72102'; assert df_cls.loc[72102, 'review_id'] == 'ro_missing_72102'; print('Task 2 verified: Robi raw and classified verified at N=200,652 with zero null IDs.')"
  ```
- **Output:** `Task 2 verified: Robi raw and classified verified at N=200,652 with zero null IDs.`

### Task 3: Update sync_post_classification.py and safely regenerate telemetry JSONs and markdown report
- **Files Modified:**
  - `scraped_data_global/pipeline/sync_post_classification.py`
  - `scraped_data_global/classified/all_operators_classified_global.csv`
  - `scraped_data_global/classified/all_operators_common_duration_classified.csv`
  - `scraped_data_global/classified/common_duration_summary.json`
  - `scraped_data_global/classified/yearly_intelligence_trends.json`
  - `scraped_data_global/classified/global_multi_year_intelligence_report.md`
- **Actions Taken:**
  - Updated line 58 in `sync_post_classification.py` to enforce canonical `start_common = pd.Timestamp("2016-08-01 00:00:00")` (`DISC-MAJ-16`).
  - Fixed line 62 inclusive days calculation: `days = (end_common.normalize() - start_common.normalize()).days + 1` ($3,713$ days) (`DISC-MIN-06`).
  - Executed `python scraped_data_global/pipeline/sync_post_classification.py` which regenerated:
    - `all_operators_classified_global.csv`: $661,160$ rows, $0$ null `review_id`s, 24 columns.
    - `all_operators_common_duration_classified.csv`: $655,649$ rows (Grameenphone $320,140$, Robi $198,378$, Banglalink $137,131$), $0$ null `review_id`s.
    - `common_duration_summary.json`: `total_reviews: 655649`, `common_duration_days: 3713`.
    - `yearly_intelligence_trends.json`: Year 2016 totals $438$ (GP), $126$ (Robi), $744$ (Banglalink); overall sum across all years is exactly $655,649$ (eliminating the 21 July 2016 reviews).
    - `global_multi_year_intelligence_report.md`: Sections 1, 2, and 3 fully synchronized to $N = 655,649$ and $3,713$ shared days.
- **Verification Command:**
  ```powershell
  python -c "import json, pandas as pd; df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv', low_memory=False); assert len(df) == 655649, f'Expected 655649 rows, got {len(df)}'; assert df['review_id'].isna().sum() == 0, 'Found null review_id in common dataset'; s = json.load(open('scraped_data_global/classified/common_duration_summary.json')); assert s['total_reviews'] == 655649 and s['common_duration_days'] == 3713, f'Summary mismatch: {s}'; y = json.load(open('scraped_data_global/classified/yearly_intelligence_trends.json')); tot = sum(op_data['total'] for yr in y.values() for op_data in yr.values()); assert tot == 655649, f'Yearly trends sum={tot} != 655649'; y2016 = y['2016']; assert y2016['Grameenphone']['total'] == 438 and y2016['Robi']['total'] == 126 and y2016['Banglalink']['total'] == 744, f'2016 counts mismatch: {y2016}'; print('Task 3 verified: Common duration classified, summary JSON, and yearly trends verified at N=655,649!')"
  ```
- **Output:** `Task 3 verified: Common duration classified, summary JSON, and yearly trends verified at N=655,649!`

---

## 3. Discrepancy Invariants & Must-Haves Verification

| Invariant / Metric | Expected | Observed | Status |
|---|---|---|---|
| `scraped_data_global/raw/*.csv` Schema | 12 raw columns | 12 columns | PASS |
| `scraped_data_global/raw/myrobi_global.csv` Row Count | 200,652 | 200,652 | PASS |
| `scraped_data_global/raw/myrobi_global.csv` Null `review_id`s | 0 | 0 | PASS |
| `myrobi_classified_global.csv` Row Count | 200,652 | 200,652 | PASS |
| `myrobi_classified_global.csv` Null `review_id`s | 0 | 0 | PASS |
| `all_operators_classified_global.csv` Row Count | 661,160 | 661,160 | PASS |
| `all_operators_classified_global.csv` Null `review_id`s | 0 | 0 | PASS |
| `all_operators_common_duration_classified.csv` Row Count | 655,649 | 655,649 | PASS |
| Common Duration Start Boundary | 2016-08-01 00:00:00 | 2016-08-01 00:00:00 | PASS |
| Common Duration Days | 3,713 | 3,713 | PASS |
| `yearly_intelligence_trends.json` 2016 Operator Counts | 438 / 126 / 744 | 438 / 126 / 744 | PASS |
| `yearly_intelligence_trends.json` Total Sum Across Years | 655,649 | 655,649 | PASS |

---

## 4. Deviations & Deferred Work

- **Deviations:** None. All tasks strictly conformed to `1-PLAN.md`, `ADR-002`, and `ADR-003`.
- **Git Commits:** None (`commits: none (ADR-003)`). Working tree diffs are maintained for final user review.

---

## 5. Next Steps

- Proceed to **Plan 5.2** (`demo/` application runtime hardening, requirements manifests synchronization, and demo banner updates).
