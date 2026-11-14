---
phase: 5
verified: 2026-11-11T13:46:00+06:00
status: passed
score: 20/20 must-haves verified
is_re_verification: false
---

# Phase 5 Verification Report

**Target Phase:** Phase 5 — Data Pipeline, Telemetry JSONs, Demo UI & Dependencies Remediation  
**Milestone:** v2.0.0 (Remediation)  
**Requirements Addressed:** `REM-01`, `REM-02`  
**Discrepancies Verified Closed:** `DISC-CRIT-08`, `DISC-MAJ-03`, `DISC-MAJ-08`, `DISC-MAJ-16`, `DISC-MIN-06`, `DISC-MIN-14`, `DISC-MIN-15`, `DISC-MIN-16`, `DISC-MIN-17`, `DISC-HYG-01`, `DISC-HYG-02`, `DISC-HYG-03`, `DISC-HYG-05`  
**Git Commit Enforcement:** 0 unsolicited git commits created (`ADR-003`)  
**Overall Verdict:** **PASSED (20/20 Must-Haves Verified)**

---

## 1. Executive Summary

Phase 5 was verified independently against the repository files on disk, ensuring that all data pipeline scripts, datasets, telemetry JSONs, demo UI callbacks, dependencies manifests, and documentation scorecards strictly satisfy requirements `REM-01` and `REM-02`. Every must-have was tested empirically by executing live AST parsers, DataFrame row counters, JSON deserializers, runtime model inference checks, and git tree diagnostics.

Key empirical findings:
1. **Pipeline Schema & Portability**: `scraper_worker.py` and `merge_and_sync_all_datasets.py` preserve all 12 canonical raw fields (`DISC-CRIT-08`). Scraper workers guard against empty `reviewId`s, parameterize language/country (`DISC-HYG-05`), and `run_parallel_scrapers.py` invokes `sys.executable` across platforms (`DISC-HYG-01`).
2. **Review ID Hygiene & Dataset Invariants**: Historical row `72102` in Robi raw and classified datasets was safely resolved with deterministic ID `ro_missing_72102`, achieving `0` null `review_id`s across all `200,652` Robi rows and all `661,160` master / `655,649` common duration rows without altering row counts (`DISC-HYG-05`).
3. **Telemetry JSONs & Canonical Boundary**: `sync_post_classification.py` strictly anchors the common window at `2016-08-01 00:00:00` with inclusive `3,713` days (`DISC-MAJ-16`, `DISC-MIN-06`). `yearly_intelligence_trends.json` sums to exactly `655,649` across all years and records `438` (GP), `126` (Robi), and `744` (BL) for 2016. `common_duration_summary.json` reflects `655,649` reviews and `3,713` days.
4. **Gradio UI & Model Inference**: `demo/app.py` correctly wires `out_cat` into the Gradio UI callback and outputs, returning full 6-element tuples across empty, whitespace, and valid review branches (`DISC-MAJ-08`). The training volume banner cites `4,500` seed reviews and `655,649` evaluation reviews (`DISC-MIN-14`), and the title is aligned with the formal ESWA manuscript title (`DISC-HYG-01`). Live model inference was executed end-to-end for native Bengali, Romanized Banglish, and English inputs, returning valid sentiment and category classifications with triage notes.
5. **Dependency Alignment**: `demo/requirements.txt`, `ml/requirements.txt`, `dl/requirements.txt`, and root `requirements.txt` are synchronized: unused heavy libraries (`torchvision`, `torchaudio`) were removed, and missing runtime libraries (`nltk>=3.8.1`, `gradio>=4.0.0`, `python-docx>=1.1.0`, etc.) were declared (`DISC-MAJ-03`, `DISC-HYG-02`, `DISC-HYG-03`).
6. **Documentation Scorecards**: `README.md` features dual Cohen's Kappa badges (Sentiment $\kappa = 0.58$, Category $\kappa = 0.77$), Banglalink common period NSS at `+53.0%`, canonical 2016 `(Aug–Dec)` counts `438/126/744`, `122 Months` / `41 Months` duration spans, complete directory trees, and zero academic paper references per commit `4d5aaad`. `TODO.txt` fixes the model archive filename, anonymizes annotator filenames, corrects seed count to $N=4,500$, updates corpus volumes to `655.6k` / `661.2k`, and marks the Gradio web demo as completed locally.
7. **Policy Compliance**: Zero git commits were made (`ADR-003`).

---

## 2. Must-Haves Verification Matrix

### 2.1 Observable Truths

| # | Stated Truth | Status | Empirical Evidence |
|---|---|---|---|
| 1 | `scraper_worker.py` preserves 12 raw columns, parameterizes language/country, and guards against null `reviewId` | **PASSED** | Inspected AST and imported `FIELDNAMES`: length is 12 (`app_version`, `user_image`, `developer_reply`, `developer_reply_date`, `is_enriched` present). Guard `if not rev_id: continue` verified in AST. `--lang` and `--country` present in `argparse`. |
| 2 | `run_parallel_scrapers.py` dynamically resolves Python interpreter via `sys.executable` | **PASSED** | AST verified: `sys.executable` used to launch workers; hardcoded `dl/.venv/bin/python` completely removed. |
| 3 | `merge_and_sync_all_datasets.py` preserves 12 raw columns, prevents duplicate dropping of distinct review IDs, and computes 3,713 inclusive days | **PASSED** | Source verified: `RAW_COLUMNS` has 12 fields; deduplication guards against dropping unique `review_id`s; join uses `op_existing` primary `review_id` join; days formula is `(end - start).days + 1` = 3,713; JSON schema includes `positive_count`, `neutral_count`, `negative_count`. |
| 4 | Row 72102 in `myrobi_global.csv` and `myrobi_classified_global.csv` has deterministic ID `ro_missing_72102` with 0 row count shift | **PASSED** | Read both CSVs via pandas: exactly 200,652 rows each; 0 null `review_id`s in both; row index 72102 has ID `ro_missing_72102`. |
| 5 | `sync_post_classification.py` enforces `2016-08-01` start and `3,713` inclusive days | **PASSED** | Source verified: `start_common = pd.Timestamp("2016-08-01 00:00:00")` and `days = (end.normalize() - start.normalize()).days + 1`. |
| 6 | `all_operators_classified_global.csv` contains exactly 661,160 rows and 0 null review IDs | **PASSED** | Loaded in pandas: `len == 661,160`, `df['review_id'].isna().sum() == 0`, 24 columns. |
| 7 | `all_operators_common_duration_classified.csv` contains exactly 655,649 rows and 0 null review IDs | **PASSED** | Loaded in pandas: `len == 655,649`, `df['review_id'].isna().sum() == 0` (GP=320,140, Robi=198,378, BL=137,131). |
| 8 | `common_duration_summary.json` records 655,649 reviews, 3,713 days, and full operator metrics | **PASSED** | Deserialized JSON: `total_reviews=655649`, `common_duration_days=3713`, `common_window_start="2016-08-01 00:00:00"`, `common_window_end="2026-09-30 23:16:00"`, `positive_count`/`neutral_count`/`negative_count` present across all 3 operators. |
| 9 | `yearly_intelligence_trends.json` sums to 655,649 across all years and reports 438/126/744 for 2016 | **PASSED** | Calculated total: sum across all years is 655,649; Year 2016 reports GP=438, Robi=126, BL=744 (sum=1,308). |
| 10 | `global_multi_year_intelligence_report.md` synchronizes with 655,649 reviews, 3,713 days, and August 2016 | **PASSED** | Text parsed: Sections 1–3 report $N=655,649$, 3,713 Shared Days, August 01, 2016 start, and 2016 table row counts 438, 126, 744. |
| 11 | `demo/app.py` wires `out_cat` in callback outputs and returns 6-tuples matching layout | **PASSED** | AST confirmed `outputs=[out_lang, out_sent, out_cat, out_sent_probs, out_cat_probs, out_diag]` and both return statements return 6-element tuples with `category_label` at index 2. |
| 12 | `demo/app.py` executes end-to-end model inference on native Bangla, Banglish, and English reviews | **PASSED** | Executed `test_demo_runtime.py`: empty review returns 6-tuple `("N/A", "N/A", "N/A", {}, {}, ...)`; native Bangla correctly classified as Negative / Network Speed & 4G Latency; Banglish classified as Negative / App Login & Technical Bugs; English classified as Positive / General Appreciation. |
| 13 | `demo/app.py` banner cites models trained on 4,500 seed reviews and evaluated on 655,649 reviews | **PASSED** | Verified text: `*Demonstrating models trained on 4,500 expert/LLM-labeled seed reviews and evaluated across 655,649 longitudinal customer reviews...*` |
| 14 | `demo/app.py` unifies paper title to formal ESWA manuscript title without informal prefix | **PASSED** | Verified text: `**Research Paper:** *“An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling”*`; `"With Great Reviews Comes Great Responsibility:"` is completely absent. |
| 15 | `demo/requirements.txt` includes scikit-learn>=1.4.0, nltk>=3.8.1, and pandas>=2.0.0 | **PASSED** | Read manifest: `scikit-learn>=1.4.0`, `nltk>=3.8.1`, `pandas>=2.0.0`, `gradio>=4.0.0`, `joblib>=1.3.0` declared. |
| 16 | `ml/requirements.txt`, `dl/requirements.txt`, and root `requirements.txt` reconciled | **PASSED** | `ml/requirements.txt` has `nltk>=3.8.1`; `dl/` and root manifests stripped of `torchvision`/`torchaudio`; root declares `nltk`, `gradio`, `python-docx`, `openpyxl`, `Pillow`, `huggingface-hub`. |
| 17 | `README.md` features dual Cohen's Kappa badges (Sentiment 0.58, Category 0.77) | **PASSED** | Verified badge lines: `Sentiment%20Kappa-%CE%BA%20%3D%200.58%20(Moderate)` and `Category%20Kappa-%CE%BA%20%3D%200.77%20(Substantial)`. |
| 18 | `README.md` reports Banglalink Common Period NSS as +53.0% and 2016 Aug–Dec counts 438/126/744 | **PASSED** | Verified lines 52, 120, 416: `+53.0%` (stale `+53.1%` absent); 2016 table row reports `*(Aug–Dec)*` with `(438)`, `(126)`, `(744)` (stale 441 and 762 absent); month counts are `122 Months` and `41 Months`. |
| 19 | `README.md` strictly contains zero academic paper references per commit 4d5aaad | **PASSED** | Substring scan confirmed: `"Expert Systems with Applications"` not in file; `"ESWA"` not in file. |
| 20 | `TODO.txt` fixes zip filename, anonymizes annotators, updates seed count to 4,500, updates corpus to 655.6k/661.2k, and marks demo completed locally | **PASSED** | Scanned file: `banglabert_finetuned_models.zip` (no ` (1)` suffix); `blind_annotation_300_annotator1.csv` & `_annotator2.csv`; `N = 4,500`; `655.6k` & `661.2k`; Section 4 marked `[COMPLETED LOCALLY]`. |

---

### 2.2 Artifacts Verification (3-Level Check)

| Path | Level 1: Exists | Level 2: Substantive | Level 3: Wired | Status |
|---|:---:|:---:|:---:|:---:|
| `scraped_data_global/pipeline/scraper_worker.py` | ✓ | ✓ | ✓ | **PASSED** |
| `scraped_data_global/pipeline/run_parallel_scrapers.py` | ✓ | ✓ | ✓ | **PASSED** |
| `scraped_data_global/pipeline/merge_and_sync_all_datasets.py` | ✓ | ✓ | ✓ | **PASSED** |
| `scraped_data_global/pipeline/sync_post_classification.py` | ✓ | ✓ | ✓ | **PASSED** |
| `scraped_data_global/raw/myrobi_global.csv` | ✓ | ✓ | ✓ | **PASSED** |
| `scraped_data_global/classified/myrobi_classified_global.csv` | ✓ | ✓ | ✓ | **PASSED** |
| `scraped_data_global/classified/all_operators_classified_global.csv` | ✓ | ✓ | ✓ | **PASSED** |
| `scraped_data_global/classified/all_operators_common_duration_classified.csv` | ✓ | ✓ | ✓ | **PASSED** |
| `scraped_data_global/classified/common_duration_summary.json` | ✓ | ✓ | ✓ | **PASSED** |
| `scraped_data_global/classified/yearly_intelligence_trends.json` | ✓ | ✓ | ✓ | **PASSED** |
| `scraped_data_global/classified/global_multi_year_intelligence_report.md` | ✓ | ✓ | ✓ | **PASSED** |
| `demo/app.py` | ✓ | ✓ | ✓ | **PASSED** |
| `demo/requirements.txt` | ✓ | ✓ | ✓ | **PASSED** |
| `ml/requirements.txt` | ✓ | ✓ | ✓ | **PASSED** |
| `dl/requirements.txt` | ✓ | ✓ | ✓ | **PASSED** |
| `requirements.txt` | ✓ | ✓ | ✓ | **PASSED** |
| `README.md` | ✓ | ✓ | ✓ | **PASSED** |
| `TODO.txt` | ✓ | ✓ | ✓ | **PASSED** |

---

### 2.3 Key Links & Wiring Verification

| From | To | Via | Status | Notes |
|---|---|---|---|---|
| `run_parallel_scrapers.py` | `scraper_worker.py` | `subprocess.Popen([sys.executable, str(SCRAPER_SCRIPT), ...])` | **WIRED** | Replaced hardcoded POSIX interpreter path with `sys.executable`. |
| `scraper_worker.py` | `google-play-scraper` | `reviews(...)` | **WIRED** | Populates all 12 canonical fields, drops null `reviewId`. |
| `sync_post_classification.py` | Classified CSVs | `pd.read_csv(...)` | **WIRED** | Concatenates GP (321,374), Robi (200,652), BL (139,134) into master ($N=661,160$). |
| `sync_post_classification.py` | Common dataset | `df[df['review_date'] >= '2016-08-01']` | **WIRED** | Filters to exactly $N=655,649$ reviews, calculating 3,713 days. |
| `demo/app.py` | `ml.predict` | `predict_sentiment(...)` | **WIRED** | Calls sentiment model, category model, and returns 6-tuple matching UI. |
| `demo/app.py` | Gradio UI components | `submit_btn.click(..., outputs=[..., out_cat, ...])` | **WIRED** | `out_cat` is explicitly registered in outputs and updated on every review submission. |

---

## 3. Detailed Empirical Verification Results

### 3.1 Pipeline Scripts Verification (Step 1)
Script executed: `C:\Users\user\.gemini\antigravity\brain\b9bfa747-f4c3-46a8-a84d-d569328ec6e5\scratch\verify_step1.py`
Command: `python verify_step1.py`
Output:
```text
=== STEP 1: VERIFYING PIPELINE SCRIPTS ===
[OK] scraper_worker.py: 12 fields, null reviewId guard, lang/country parameterization confirmed.
[OK] run_parallel_scrapers.py: sys.executable used, hardcoded POSIX python eliminated.
[OK] merge_and_sync_all_datasets.py: RAW_COLUMNS, 3,713 days inclusive formula, summary JSON schema confirmed.
[OK] sync_post_classification.py: 2016-08-01 start, 3,713 days inclusive formula confirmed.
STEP 1: ALL CHECKS PASSED.
```

### 3.2 Dataset Counts & Telemetry Outputs Verification (Step 2)
Script executed: `C:\Users\user\.gemini\antigravity\brain\b9bfa747-f4c3-46a8-a84d-d569328ec6e5\scratch\verify_step2.py`
Command: `python verify_step2.py`
Output:
```text
=== STEP 2: VERIFYING CSV & JSON COUNTS AND TELEMETRY ===
[OK] myrobi_global.csv: N=200,652, 0 null review_ids, row 72102 is ro_missing_72102, 12 columns.
[OK] myrobi_classified_global.csv: N=200,652, 0 null review_ids, row 72102 is ro_missing_72102.
[OK] Operator classified totals: GP=321,374, Robi=200,652, BL=139,134 -> Sum = 661,160.
[OK] all_operators_classified_global.csv: N=661,160, 0 null review_ids, 24 columns.
[OK] all_operators_common_duration_classified.csv: N=655,649, 0 null review_ids (GP=320,140, Robi=198,378, BL=137,131).
[OK] common_duration_summary.json: total_reviews=655,649, days=3,713, start=2016-08-01, positive/neutral/negative counts present.
[OK] yearly_intelligence_trends.json: total sum=655,649, 2016 counts: GP=438, Robi=126, BL=744 (Sum=1,308).
[OK] global_multi_year_intelligence_report.md: verified references to 655,649 reviews, 3,713 days, and August 2016.
STEP 2: ALL CHECKS PASSED.
```

### 3.3 Demo UI AST, Manifests, README & TODO Verification (Step 3)
Script executed: `C:\Users\user\.gemini\antigravity\brain\b9bfa747-f4c3-46a8-a84d-d569328ec6e5\scratch\verify_step3.py`
Command: `python verify_step3.py`
Output:
```text
=== STEP 3: VERIFYING DEMO UI, REQUIREMENTS, README, AND TODO ===
[OK] demo/app.py: 6-tuple returns, out_cat wired in outputs, 4,500/655,649 banner, unified title confirmed.
[OK] demo/requirements.txt: scikit-learn>=1.4.0, nltk>=3.8.1, pandas>=2.0.0 confirmed.
[OK] ml/requirements.txt: nltk>=3.8.1 confirmed.
[OK] dl/requirements.txt: torchvision and torchaudio excluded.
[OK] requirements.txt: heavy libs removed, runtime dependencies declared.
[OK] README.md: dual badges, +53.0%, 2016 438/126/744, 122/41 months, tree, Gradio, no paper leaks confirmed.
[OK] TODO.txt: zip name, anonymized annotators, N=4,500, 655.6k/661.2k, COMPLETED LOCALLY confirmed.
STEP 3: ALL CHECKS PASSED.
```

### 3.4 Live End-to-End Model Inference in Demo UI (Step 4)
Script executed: `C:\Users\user\.gemini\antigravity\brain\b9bfa747-f4c3-46a8-a84d-d569328ec6e5\scratch\test_demo_runtime.py`
Command: `python test_demo_runtime.py`
Output:
```text
Loading VoC Intelligence models...
Models loaded successfully!
[OK] Empty input test passed: returns 6-tuple.
[OK] Whitespace input test passed: returns 6-tuple.
[OK] Bangla review inference:
  Detected Language: Bangla (Native Script) 
  Sentiment: Negative (79.0%)
  Category: Network Speed & 4G Latency (72.4%)
  Sentiment Probs: {'Negative': 0.79, 'Neutral': 0.1052, 'Positive': 0.1048}
  Category Probs: {'App Login & Technical Bugs': 0.15365510207951097, 'Billing & Airtime Deductions': 0.03332385015246269, 'General Appreciation / Other': 0.07736087133511237, 'Network Speed & 4G Latency': 0.7243846685562864, 'Offers & Data Packs': 0.011275507876627509}
  Diagnostic: **Decoupled Subsystem:** Core Telecommunications RAN (RF propagation, 4G/3G drops, video buffering, fiber cut)...
[OK] English review inference:
  Detected Language: English 
  Sentiment: Positive (70.8%)
  Category: General Appreciation / Other (56.9%)
[OK] Banglish review inference:
  Detected Language: Romanized Banglish (Code-Mixed)
  Sentiment: Negative (72.7%)
  Category: App Login & Technical Bugs (68.7%)
ALL RUNTIME MODEL INFERENCE CHECKS IN demo/app.py PASSED PERFECTLY!
```

### 3.5 Anti-Patterns & Codebase Hygiene Scan (Step 5)
Script executed: `C:\Users\user\.gemini\antigravity\brain\b9bfa747-f4c3-46a8-a84d-d569328ec6e5\scratch\scan_antipatterns.py`
Command: `python scan_antipatterns.py`
Output:
```text
=== ANTI-PATTERN SCAN ===
Anti-pattern scan completed. Found 1 potential issues:
 - scraped_data_global/pipeline/scraper_worker.py:80: Empty body/return None: pass
```
*Note on line 80:* Code inspection proves this is an intended defensive `try...except Exception: pass` block surrounding non-critical progress file writing. No code stubs, empty functions, or TODO comments were found in modified files.

### 3.6 Git Commits Verification (Step 6)
Command: `git log -1`
Output:
```text
commit 3d9f8897e7b1cb46f6499cd88e369b559af2c5db
Author: Ratul Hasan <rh61632@gmail.com>
Date:   Sun Nov 8 13:53:46 2026 +0600

    feat(ml): integrate automated language detector into inference CLI
```
`git status --short` confirms all changes are staged/unstaged in the live working tree without any commit creation, strictly satisfying `ADR-003`.

---

## 4. Discrepancy Closure Status

| Discrepancy ID | Description | Remediation Artifacts | Status |
|---|---|---|---|
| `DISC-CRIT-08` | Scraper & merge stripping metadata columns (7 vs 12) | `scraper_worker.py`, `merge_and_sync_all_datasets.py` | **CLOSED** |
| `DISC-MAJ-16` | 2016 review count inconsistency (441/126/762 vs 438/126/744) | `sync_post_classification.py`, `yearly_intelligence_trends.json`, `README.md` | **CLOSED** |
| `DISC-MIN-06` | Common duration days off-by-one (3,712 vs 3,713 inclusive) | `sync_post_classification.py`, `common_duration_summary.json`, `global_multi_year_intelligence_report.md` | **CLOSED** |
| `DISC-HYG-01` | Hardcoded POSIX python path in scraper runner; paper title prefix in demo | `run_parallel_scrapers.py`, `demo/app.py` | **CLOSED** |
| `DISC-HYG-05` | Null reviewId in scrapers and single null review_id in Robi dataset | `scraper_worker.py`, `myrobi_global.csv`, `myrobi_classified_global.csv` | **CLOSED** |
| `DISC-MAJ-08` | `demo/app.py` Gradio `out_cat` operational category disconnected | `demo/app.py` | **CLOSED** |
| `DISC-MIN-14` | Demo UI banner claiming 655k training volume instead of 4,500 | `demo/app.py` | **CLOSED** |
| `DISC-MAJ-03` | Incomplete dependencies in `demo/requirements.txt` and `ml/requirements.txt` | `demo/requirements.txt`, `ml/requirements.txt` | **CLOSED** |
| `DISC-HYG-02` | Unused heavy dependencies `torchvision` and `torchaudio` in manifests | `dl/requirements.txt`, `requirements.txt` | **CLOSED** |
| `DISC-HYG-03` | Dependency specifier mismatch (`scikit-learn>=1.3.0` vs `>=1.4.0`) | `demo/requirements.txt` | **CLOSED** |
| `DISC-MIN-15` | Banglalink NSS scorecard discrepancy (+53.1% vs +53.0%) | `README.md` | **CLOSED** |
| `DISC-MIN-16` | Single Cohen's Kappa badge in `README.md` missing Category Kappa | `README.md` | **CLOSED** |
| `DISC-MIN-17` | Browser duplicate suffix ` (1)` in `TODO.txt` checkpoint zip name | `TODO.txt` | **CLOSED** |

---

## 5. Verdict & Status

```
status: pass
phase: 5
report: .gsd/phases/5/VERIFICATION.md
must_haves: 20/20
failures: []
gap_plans: []
blocker: none
```

All empirical checks passed without a single failure. Phase 5 is fully certified and complete. Ready to proceed to Phase 6 (`ML/DL Models, Label Mappings, Gold Standard & Reports Remediation`).
