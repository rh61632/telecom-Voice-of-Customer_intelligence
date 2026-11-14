---
phase: 1
plan: 1
wave: 1
depends_on: []
files_modified:
  - .gsd/phases/1/evidence/01_scraping_and_raw_schema_audit.md
  - .gsd/phases/1/evidence/01_merge_sync_telemetry_audit.md
  - .gsd/phases/1/1-SUMMARY.md
autonomous: true
user_setup: []

must_haves:
  truths:
    - "Raw CSV schemas across all 3 operators and column-preservation behavior in scrapers are empirically verified"
    - "Common-window boundary logic (2016-08-01 vs 2016-07-28), row counts (655,649 vs 655,670), and summary JSON schemas are reconciled"
    - "NSS telemetry analytics, CLT floor (N>=30), and 35 significant monthly shocks are verified against live classified outputs"
  artifacts:
    - ".gsd/phases/1/evidence/01_scraping_and_raw_schema_audit.md"
    - ".gsd/phases/1/evidence/01_merge_sync_telemetry_audit.md"
    - ".gsd/phases/1/1-SUMMARY.md"
  key_links:
    - "Scraping column exports link to downstream feature requirements in scripts/check_version_bias.py"
    - "Common-window duration logic links to all_operators_common_duration_classified.csv and common_duration_summary.json"
---

# Plan 1.1: Scraping, Merge, Common-Window & Telemetry Pipeline Audit

<objective>
Audit the end-to-end data acquisition, synchronization, classification, and telemetry pipeline scripts in `scraped_data_global/` against actual raw and classified datasets on disk. Specifically identify schema-dropping overwrite risks, common-window boundary drift (`2016-08-01` vs `2016-07-28`), duplicate model logic, and NSS shock metrics without modifying any project or data files outside `.gsd/`.
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- .gsd/ARCHITECTURE.md
- .gsd/DECISIONS.md
- scraped_data_global/pipeline/run_parallel_scrapers.py
- scraped_data_global/pipeline/scraper_worker.py
- scraped_data_global/pipeline/merge_and_sync_all_datasets.py
- scraped_data_global/pipeline/classify_global_dataset.py
- scraped_data_global/pipeline/sync_post_classification.py
- scraped_data_global/pipeline/evaluate_nss_stability_and_shocks.py
- scraped_data_global/classified/common_duration_summary.json
</context>

<tasks>

<task type="auto">
  <name>Audit Google Play scraping scripts, raw CSV schemas, and pipeline column preservation</name>
  <files>
    scraped_data_global/pipeline/run_parallel_scrapers.py
    scraped_data_global/pipeline/scraper_worker.py
    scraped_data_global/raw/mygp_global.csv
    scraped_data_global/raw/myrobi_global.csv
    scraped_data_global/raw/mybl_global.csv
    scraped_data_global/raw/progress_gp.json
    scraped_data_global/raw/progress_robi.json
    scraped_data_global/raw/progress_bl.json
    .gsd/phases/1/evidence/01_scraping_and_raw_schema_audit.md
  </files>
  <action>
    Perform a strict read-only audit of the review scraping scripts and raw CSV datasets:
    1. Inspect header columns and row counts for `mygp_global.csv`, `myrobi_global.csv`, and `mybl_global.csv`. Document column counts and exact names for each file (e.g., GP has 12 columns including app_version, user_image, developer_reply, developer_reply_date, is_enriched, whereas Robi/BL may have different column counts).
    2. Audit `scraper_worker.py` (lines 49-57, 163-170) and `merge_and_sync_all_datasets.py` (line 272) for column-dropping risks: check if hardcoded 7-column saving (`review_id, user_name, rating, review_date, review_text, thumbs_up, operator`) drops `app_version` and metadata required downstream by `scripts/check_version_bias.py`.
    3. Audit `run_parallel_scrapers.py:22` for cross-platform interpreter invocation (`dl/.venv/bin/python` vs Windows `Scripts/python.exe` or `sys.executable`).
    4. Audit scraping query parameters (`country="us"`, `lang="en"`, `Sort.NEWEST`, `count=199`, incremental logic) and progress JSON state tracking (`progress_gp.json`, etc.).
    5. Save structured empirical evidence, tables of column comparisons, row counts, and line citations to `.gsd/phases/1/evidence/01_scraping_and_raw_schema_audit.md`.

    AVOID: Modifying any CSV or Python files outside `.gsd/`. Do NOT re-run active scrapers. Do NOT load full 1.2 GB CSVs into memory at once (use `pd.read_csv(..., nrows=5)` for schema and line counting for total rows).
    USE: Read-only Python scripts or PowerShell commands that output markdown tables into `.gsd/phases/1/evidence/01_scraping_and_raw_schema_audit.md`.
  </action>
  <verify>
    python -c "import os; assert os.path.exists('.gsd/phases/1/evidence/01_scraping_and_raw_schema_audit.md'), 'Evidence file missing'; print('Scraping audit evidence successfully verified')"
  </verify>
  <done>
    `.gsd/phases/1/evidence/01_scraping_and_raw_schema_audit.md` exists and contains exact column schemas for all 3 raw CSVs, row counts, date ranges, file:line evidence of schema-dropping overwrite risks, and runtime path compatibility findings.
  </done>
</task>

<task type="auto">
  <name>Audit merge, global classification, common-window synchronization, and NSS telemetry analytics</name>
  <files>
    scraped_data_global/pipeline/merge_and_sync_all_datasets.py
    scraped_data_global/pipeline/classify_global_dataset.py
    scraped_data_global/pipeline/sync_post_classification.py
    scraped_data_global/pipeline/evaluate_nss_stability_and_shocks.py
    scraped_data_global/classified/all_operators_classified_global.csv
    scraped_data_global/classified/all_operators_common_duration_classified.csv
    scraped_data_global/classified/common_duration_summary.json
    scraped_data_global/classified/yearly_intelligence_trends.json
    scraped_data_global/classified/global_voc_intelligence_report.json
    scraped_data_global/classified/nss_stability_and_shocks_summary.json
    scraped_data_global/classified/nss_significant_shocks.csv
    scraped_data_global/classified/global_multi_year_intelligence_report.md
    .gsd/phases/1/evidence/01_merge_sync_telemetry_audit.md
  </files>
  <action>
    Perform a strict read-only audit of dataset merging, global classification, common-window filtering, and telemetry computation:
    1. Audit common-window boundary drift: compare `merge_and_sync_all_datasets.py:290` (hardcoded `2016-08-01` to `2026-09-30`, `3,713` days) with `sync_post_classification.py:58` (`start_common = max(...)` yielding `2016-07-28`, `3,716` days). Verify exact row count on disk in `all_operators_common_duration_classified.csv` (`655,649` vs legacy `655,670`).
    2. Audit schema discrepancies in summary JSON files: check `common_duration_summary.json` against `merge_and_sync_all_datasets.py:317-324` (omits sentiment breakdown) and `sync_post_classification.py:86-96` (includes `positive_count`, `neutral_count`, `negative_count`).
    3. Audit model loading and PyTorch class duplication: verify copy-pasted `BahdanauAttention`, `Vocabulary`, and `HybridBiLSTMAttention` across `classify_global_dataset.py:24-67` and `merge_and_sync_all_datasets.py:26-69`. Check model filename divergence: `classify_global_dataset.py:78` loading `sentiment_voting_classifier.joblib` vs `ml/predict.py:21` loading `ensemble_voting_classifier.joblib`.
    4. Audit NSS shock calculations and invariants: inspect `evaluate_nss_stability_and_shocks.py` for CLT floor (`N >= 30`), shock threshold (`|Delta NSS| >= 10.0` pp), total shock count in `nss_significant_shocks.csv` (reconcile against the 35 shocks claim), and additive category decomposition math.
    5. Save structured audit findings with exact line numbers, JSON snippet diffs, and count comparisons to `.gsd/phases/1/evidence/01_merge_sync_telemetry_audit.md`.

    AVOID: Re-running classification or rewriting classified CSVs. Do NOT modify any source scripts.
    USE: Read-only Python checks reading summary JSONs, CSV headers/row counts, and inspecting source code lines.
  </action>
  <verify>
    python -c "import os; assert os.path.exists('.gsd/phases/1/evidence/01_merge_sync_telemetry_audit.md'), 'Evidence file missing'; print('Merge and telemetry audit evidence successfully verified')"
  </verify>
  <done>
    `.gsd/phases/1/evidence/01_merge_sync_telemetry_audit.md` exists and contains empirical verification of the 2016-08-01 vs 2016-07-28 window cutoff, summary JSON schema divergence, duplicated PyTorch definitions, model checkpoint naming drift, and verification of the 35 shocks count.
  </done>
</task>

</tasks>

<verification>
After all tasks complete, verify:
- [ ] `.gsd/phases/1/evidence/01_scraping_and_raw_schema_audit.md` exists and documents raw CSV column schemas, scraper column dropping, and path portability.
- [ ] `.gsd/phases/1/evidence/01_merge_sync_telemetry_audit.md` exists and documents common-window dates/counts, summary JSON schemas, duplicated model architectures, and 35 shocks telemetry.
- [ ] `.gsd/phases/1/1-SUMMARY.md` is generated summarizing all Task 1 and Task 2 findings and discrepancies.
</verification>

<success_criteria>
- [ ] All tasks verified passing with exit code 0
- [ ] No project source, data, or paper files outside `.gsd/` were modified
- [ ] No git commands (`git add`, `git commit`) were executed
</success_criteria>
