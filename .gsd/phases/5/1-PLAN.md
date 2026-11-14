---
phase: 5
plan: 1
wave: 1
depends_on: []
files_modified:
  - scraped_data_global/pipeline/scraper_worker.py
  - scraped_data_global/pipeline/run_parallel_scrapers.py
  - scraped_data_global/pipeline/merge_and_sync_all_datasets.py
  - scraped_data_global/raw/myrobi_global.csv
  - scraped_data_global/classified/myrobi_classified_global.csv
  - scraped_data_global/pipeline/sync_post_classification.py
  - scraped_data_global/classified/all_operators_classified_global.csv
  - scraped_data_global/classified/all_operators_common_duration_classified.csv
  - scraped_data_global/classified/common_duration_summary.json
  - scraped_data_global/classified/yearly_intelligence_trends.json
  - scraped_data_global/classified/global_multi_year_intelligence_report.md
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "Scraper worker preserves all 12 raw columns, parameterizes language/country, and guards against null reviewId"
    - "Parallel scraper launcher resolves Python interpreter dynamically via sys.executable"
    - "merge_and_sync_all_datasets.py preserves 12 raw columns, prevents duplicate dropping of distinct review_ids, and computes 3,713 inclusive days"
    - "Row 72102 in myrobi_global.csv and myrobi_classified_global.csv has non-null deterministic ID ro_missing_72102 with zero row count shift"
    - "sync_post_classification.py enforces the canonical 2016-08-01 boundary and regenerates all telemetry datasets (N=655,649, 3,713 days) with 2016 counts 438/126/744"
  artifacts:
    - "scraped_data_global/classified/all_operators_common_duration_classified.csv with 655,649 rows and 0 null review_ids"
    - "scraped_data_global/classified/common_duration_summary.json with total_reviews=655649 and common_duration_days=3713"
    - "scraped_data_global/classified/yearly_intelligence_trends.json with total sum 655,649 and 2016 operator counts 438/126/744"
    - "scraped_data_global/classified/global_multi_year_intelligence_report.md reporting N=655,649 and 3,713 shared days"
---

# Plan 5.1: Pipeline Scripts, Review ID Hygiene & Telemetry JSONs Regeneration

## Objective
Remediate the raw Google Play data scrapers and dataset merge logic to preserve all 12 raw metadata columns, make worker execution cross-platform, resolve the single historical null `review_id` in Robi datasets without altering row count invariants (`N=661,160` / `N=655,649`), and safely regenerate downstream telemetry JSONs and intelligence reports enforcing the canonical `2016-08-01` boundary (`3,713` days).

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/DECISIONS.md` (`ADR-002`, `ADR-003`)
- `.gsd/phases/5/RESEARCH.md`
- `scraped_data_global/pipeline/scraper_worker.py`
- `scraped_data_global/pipeline/run_parallel_scrapers.py`
- `scraped_data_global/pipeline/merge_and_sync_all_datasets.py`
- `scraped_data_global/pipeline/sync_post_classification.py`

## Tasks

<task type="auto">
  <name>Update scraper workers and parallel runner for 12-column preservation and cross-platform execution</name>
  <files>
    scraped_data_global/pipeline/scraper_worker.py
    scraped_data_global/pipeline/run_parallel_scrapers.py
  </files>
  <action>
    1. In `scraped_data_global/pipeline/scraper_worker.py`:
       - Expand `FIELDNAMES` (lines 49-57) to include all 12 canonical raw fields (`DISC-CRIT-08`):
         ```python
         FIELDNAMES = [
             "review_id", "user_name", "rating", "review_date", "review_text",
             "thumbs_up", "operator", "app_version", "user_image",
             "developer_reply", "developer_reply_date", "is_enriched",
         ]
         ```
       - Parameterize `run_scraper(operator_key: str, incremental: bool = False, lang: str = "en", country: str = "us")` and add `--lang` (default `"en"`) and `--country` (default `"us"`) to `argparse` at lines 265-275 (`DISC-HYG-05`). Pass `lang=lang, country=country` into `reviews(...)` at lines 165-166.
       - In `run_scraper` row construction (lines 203-211), populate all 12 fields from element review dict `r`:
         - Guard empty reviewId: `rev_id = str(r.get("reviewId") or "").strip()`. If not `rev_id`: `continue` (`DISC-HYG-05`).
         - Extract `replied_at = r.get("repliedAt")`, `reply_text = r.get("replyContent")`, and `app_ver = r.get("appVersion") or r.get("reviewCreatedVersion")`.
         - Map `app_version` (strip string if present else `None`), `user_image` (strip string if present else `None`), `developer_reply` (strip string if present else `None`), `developer_reply_date` (`replied_at.strftime("%Y-%m-%d %H:%M:%S")` if replied_at else `None`), and `is_enriched = True`.
       - In incremental append (lines 238-248), ensure `new_df = pd.DataFrame(new_rows, columns=FIELDNAMES)` and verify column alignment against existing CSV columns before appending.
    2. In `scraped_data_global/pipeline/run_parallel_scrapers.py`:
       - Replace hardcoded POSIX interpreter path `PROJECT_ROOT / "dl" / ".venv" / "bin" / "python"` (lines 22-25) with dynamic cross-platform interpreter resolution using `sys.executable` (`DISC-HYG-01`).
       - Add optional `--lang` and `--country` argument forwarding to worker invocations.
       - In the completion loop (lines 61-66), inspect `p.returncode` for all worker processes and report any non-zero exit code.
    
    AVOID: Keeping `FIELDNAMES` at 7 columns because re-running the scraper permanently strips metadata columns and breaks `scripts/check_version_bias.py` with `KeyError: 'app_version'` (`DISC-CRIT-08`).
    USE: Exact 12-column canonical raw schema matching disk CSVs.
  </action>
  <verify>
    python -c "import ast; ast.parse(open('scraped_data_global/pipeline/scraper_worker.py', encoding='utf-8').read()); ast.parse(open('scraped_data_global/pipeline/run_parallel_scrapers.py', encoding='utf-8').read()); from scraped_data_global.pipeline.scraper_worker import FIELDNAMES; assert len(FIELDNAMES) == 12; assert 'app_version' in FIELDNAMES and 'is_enriched' in FIELDNAMES; runner = open('scraped_data_global/pipeline/run_parallel_scrapers.py', encoding='utf-8').read(); assert 'dl/.venv/bin/python' not in runner; assert 'sys.executable' in runner; print('Task 1 verified: 12 raw columns and cross-platform runner confirmed.')"
  </verify>
  <done>
    `scraper_worker.py` exports all 12 raw fields, drops empty review IDs, parameterizes language/country; `run_parallel_scrapers.py` uses `sys.executable`.
  </done>
</task>

<task type="auto">
  <name>Harden merge script and resolve null review_id in raw and classified Robi datasets</name>
  <files>
    scraped_data_global/pipeline/merge_and_sync_all_datasets.py
    scraped_data_global/raw/myrobi_global.csv
    scraped_data_global/classified/myrobi_classified_global.csv
  </files>
  <action>
    1. In `scraped_data_global/pipeline/merge_and_sync_all_datasets.py`:
       - Define `RAW_COLUMNS = ["review_id", "user_name", "rating", "review_date", "review_text", "thumbs_up", "operator", "app_version", "user_image", "developer_reply", "developer_reply_date", "is_enriched"]` (`DISC-CRIT-08`).
       - Replace the 7-column slice at line 272 `dedup[["review_id", ...]].to_csv(raw_out, index=False)` with `dedup[RAW_COLUMNS].to_csv(raw_out, index=False)`.
       - Fix the deduplication and merge trap (lines 225-261):
         - In `combined.drop_duplicates(...)`, do NOT drop rows that possess unique non-null `review_id`s (the historical dataset contains 44,303 pairs sharing the 4-tuple but possessing distinct `_bd_` vs UUID `review_id`s). Deduplicate strictly by non-null `review_id` when present, or only drop duplicate 4-tuples where `review_id` is identical or missing.
         - At lines 243-247, join `dedup` against `op_existing` primarily on `review_id` for non-null IDs, and deduplicate `op_existing` on `["review_date", "review_text", "user_name"]` before any fallback 4-tuple merge (`validate="many_to_one"`), preventing many-to-many row expansion.
       - Fix line 294 inclusive days calculation (`DISC-MIN-06`):
         `days = (end_common.normalize() - start_common.normalize()).days + 1` (evaluates to 3713 days, not truncated 3712).
       - Align `common_duration_summary.json` operator metrics (lines 317-324) to include `"positive_count": int(pos)`, `"neutral_count": int(neu)`, `"negative_count": int(neg)` matching `sync_post_classification.py`.
    2. In `scraped_data_global/raw/myrobi_global.csv` and `scraped_data_global/classified/myrobi_classified_global.csv` (`DISC-HYG-05`):
       - Locate the single row with null `review_id` (DataFrame index `72102`, 1-based data row `72,103`, review date `'2024-09-17 08:15:53'`, `user_name == "Shahidul Islam"`, `review_text == "nice"`).
       - Assign it deterministic synthetic ID `"ro_missing_72102"`.
       - Verify that both `myrobi_global.csv` and `myrobi_classified_global.csv` preserve exactly `200,652` rows, with zero null `review_id`s remaining.
    
    AVOID: Deleting row `72102` because dropping it reduces Robi rows from `200,652` to `200,651` and common duration rows from `655,649` to `655,648`, violating `SPEC.md:18` invariants and failing `audit_project_integrity.py`.
    AVOID: Running `merge_and_sync_all_datasets.py` against disk files in this task.
    USE: Deterministic non-colliding ID `"ro_missing_72102"` assigned directly in pandas.
  </action>
  <verify>
    python -c "import pandas as pd; df_raw = pd.read_csv('scraped_data_global/raw/myrobi_global.csv', low_memory=False); df_cls = pd.read_csv('scraped_data_global/classified/myrobi_classified_global.csv', low_memory=False); assert len(df_raw) == 200652, f'Expected 200652 raw, got {len(df_raw)}'; assert len(df_cls) == 200652, f'Expected 200652 cls, got {len(df_cls)}'; assert df_raw['review_id'].isna().sum() == 0, 'Found null review_id in raw'; assert df_cls['review_id'].isna().sum() == 0, 'Found null review_id in cls'; assert df_raw.loc[72102, 'review_id'] == 'ro_missing_72102'; assert df_cls.loc[72102, 'review_id'] == 'ro_missing_72102'; print('Task 2 verified: Robi raw and classified verified at N=200,652 with zero null IDs.')"
  </verify>
  <done>
    `merge_and_sync_all_datasets.py` preserves 12 raw columns, prevents 44,303 row drops, calculates 3,713 days; row 72102 has ID `"ro_missing_72102"`, leaving 0 null IDs across `200,652` Robi rows.
  </done>
</task>

<task type="auto">
  <name>Update sync_post_classification.py and safely regenerate telemetry JSONs and markdown report</name>
  <files>
    scraped_data_global/pipeline/sync_post_classification.py
    scraped_data_global/classified/all_operators_classified_global.csv
    scraped_data_global/classified/all_operators_common_duration_classified.csv
    scraped_data_global/classified/common_duration_summary.json
    scraped_data_global/classified/yearly_intelligence_trends.json
    scraped_data_global/classified/global_multi_year_intelligence_report.md
  </files>
  <action>
    1. In `scraped_data_global/pipeline/sync_post_classification.py`:
       - Standardize line 58 common duration start to August 1, 2016 (`DISC-MAJ-16`):
         ```python
         # Align to start of first complete calendar month (August 1, 2016)
         start_common = pd.Timestamp("2016-08-01 00:00:00")
         ```
       - Fix line 62 inclusive days calculation (`DISC-MIN-06`):
         ```python
         days = (end_common.normalize() - start_common.normalize()).days + 1
         ```
         (evaluates to `3,713` days, resolving truncation to 3712).
    2. Safely execute `python scraped_data_global/pipeline/sync_post_classification.py`.
       This reads `scraped_data_global/classified/my{bl,gp,robi}_classified_global.csv` (`139,134 + 321,374 + 200,652 = 661,160` rows, with the updated `ro_missing_72102` ID) and regenerates:
       - `all_operators_classified_global.csv`: `661,160` rows, `0` null `review_id`s, `24` columns.
       - `all_operators_common_duration_classified.csv`: `655,649` rows (`GP=320,140`, `Robi=198,378`, `BL=137,131`), `0` null `review_id`s, span `2016-08-01 22:52:08` to `2026-09-30 23:16:00`.
       - `common_duration_summary.json`: `total_reviews: 655649`, `common_duration_days: 3713`, operator metrics matching the common scorecard.
       - `yearly_intelligence_trends.json`: Year 2016 sums to `438 + 126 + 744 = 1,308` (`GP=438`, `Robi=126`, `BL=744`), eliminating the 21 July 2016 reviews; all years sum to exact `655,649` (`DISC-MAJ-16`).
       - `global_multi_year_intelligence_report.md`: Sections 1, 2, and 3 fully synchronized to `655,649` reviews and `3,713` shared days.
    
    AVOID: Running `merge_and_sync_all_datasets.py` to regenerate these files. Always use `sync_post_classification.py` which operates strictly on classified datasets without touching raw duplicate pairs.
    USE: Single-command execution of `sync_post_classification.py`.
  </action>
  <verify>
    python -c "import json, pandas as pd; df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv', low_memory=False); assert len(df) == 655649, f'Expected 655649 rows, got {len(df)}'; assert df['review_id'].isna().sum() == 0, 'Found null review_id in common dataset'; with open('scraped_data_global/classified/common_duration_summary.json') as f: s = json.load(f); assert s['total_reviews'] == 655649 and s['common_duration_days'] == 3713, f'Summary mismatch: {s}'; with open('scraped_data_global/classified/yearly_intelligence_trends.json') as f: y = json.load(f); tot = sum(op_data['total'] for yr in y.values() for op_data in yr.values()); assert tot == 655649, f'Yearly trends sum={tot} != 655649'; assert y['2016']['Grameenphone']['total'] == 438 and y['2016']['Robi']['total'] == 126 and y['2016']['Banglalink']['total'] == 744, f'2016 counts mismatch: {y[\"2016\"]}'; print('Task 3 verified: Common duration classified, summary JSON, and yearly trends verified at N=655,649!')"
  </verify>
  <done>
    `sync_post_classification.py` enforces `2016-08-01` boundary; all generated telemetry CSVs, JSONs, and markdown reports reflect `N=655,649`, `3,713` days, and zero null `review_id`s.
  </done>
</task>

</tasks>

## Must-Haves
After all tasks complete, verify:
- [ ] All 12 raw columns preserved in `scraper_worker.py` and `merge_and_sync_all_datasets.py`
- [ ] `myrobi_global.csv`, `myrobi_classified_global.csv`, and all generated classified CSVs have `0` null `review_id`s
- [ ] `all_operators_common_duration_classified.csv` contains exactly `655,649` rows
- [ ] `common_duration_summary.json` has `total_reviews: 655649` and `common_duration_days: 3713`
- [ ] `yearly_intelligence_trends.json` sums to `655,649` across all years and records `438/126/744` for 2016

## Success Criteria
- [ ] All 3 tasks verified passing with single-command PowerShell checks
- [ ] Must-haves confirmed
- [ ] Zero unsolicited git commits generated (`ADR-003`)
