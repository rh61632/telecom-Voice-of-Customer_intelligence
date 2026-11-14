---
phase: 2
phase_name: "ML/DL Models, Gold Standard & Empirical Audit Scripts"
status: pass
verified_at: "2026-11-11T09:58:00+06:00"
must_haves_passed: 9
must_haves_total: 9
non_gsd_files_modified: 0
git_commits_created: 0
---

# Phase 2 Verification Report: ML/DL Models, Gold Standard & Empirical Audit Scripts

## 1. Executive Summary

Phase 2 verified and empirically audited all Machine Learning (`ml/`), Deep Learning (`dl/`), Gold Standard (`data/gold_set/` and `archive/.../archived_600_plan/`), and diagnostic/empirical scripts (`scripts/`) under the Telecom Voice-of-Customer (VoC) Intelligence repository.

An independent audit was conducted across all 9 must-haves specified in `.gsd/phases/2/*-PLAN.md` and `.gsd/ROADMAP.md` covering `REQ-03` and `REQ-04`. All reported discrepancies in `1-SUMMARY.md`, `2-SUMMARY.md`, `3-SUMMARY.md`, and the 7 underlying evidence files in `.gsd/phases/2/evidence/` were independently inspected, re-executed, and verified against the actual disk files and working tree state.

**Verdict: PASS (9/9 Must-Haves Verified with Concrete Empirical Proof)**
**Project File Safety: PASS (Zero non-`.gsd/` project/paper files modified, zero git commits created per `ADR-001`)**

---

## 2. Must-Have Empirical Verification Matrix

| Must-Have ID | Scope | Requirement / Observable Truth | Status | Empirical Evidence |
|:---:|:---|:---|:---:|:---|
| **MH-2.1** | Deep Learning Notebooks & Scripts | All 4 DL notebooks compared against local scripts, reports, `dl/README.md`, and HF metadata | **PASS** | 4/4 notebooks inspected; stale `results.txt` (commit `60cf0f4`, missing `colab_bilstm_attention.pt`); live misclassification at Cell 10; Char-CNN architecture mismatch; category 5-fold CV divergence (`0.7624` vs `0.8032`). |
| **MH-2.2** | BanglaBERT Diff & Zip Parity | Uncommitted `config.json` diff and byte-level parity with `banglabert_finetuned_models.zip` verified | **PASS** | `git diff dl/models/` verified; SHA256 hashes of `model.safetensors` match zip (`b566cc09e58f3649` sentiment, `dc85d60cf99eb9f8` category); label index misalignment hazard with `cat_le.joblib` proven. |
| **MH-2.3** | PyTorch & Joblib Deserialization | PyTorch `.pt` checkpoints, `bilstm_vocab.joblib` crash, and `predict_dl.py` CLI tested under Python 3.15.1 | **PASS** | Direct `joblib.load('dl/models/bilstm_vocab.joblib')` crashes with `AttributeError: module '__main__' has no attribute 'Vocabulary'`; `predict_dl.py --model bilstm` exits 0 (74.48% Pos); `--model transformer` exits 1 (`ModuleNotFoundError: No module named 'transformers'`). |
| **MH-2.4** | Classical ML Model Provenance | All 9 `.joblib` models deserialized with producer pipelines, sklearn versions, and vectorizers traced | **PASS** | Voting classifiers raise `InconsistentVersionWarning` (pickled under sklearn 1.6.1 vs runtime 1.9.1); `category_voting_classifier.joblib` proven to originate from Colab Cell 7 (`weights=[2.0, 2.5, 1.0]`, `LR C=2.5`), not `ml/train_category.py`. |
| **MH-2.5** | ML Seed Data, Scripts & Reports | Seed dataset counts ($N=4,500$ vs stale 4,499), script formatting bugs, and language detector thresholds documented | **PASS** | Ground-truth CSVs total exactly 4,500 rows (`2,774 Pos / 1,238 Neg / 488 Neu`); `train_category.py:247` mean macro-F1 duplication confirmed; `train_filtered_experiments.py:19` dead path confirmed; `language_detector.py` 60% fallthrough confirmed. |
| **MH-2.6** | Gold Standard Provenance Contradiction | Inter-annotator agreement reproduced and critical g600 benchmark leakage empirically demonstrated | **PASS** | `calculate_agreement.py` reproduces 91.00% ($\kappa = 0.5762$) and 95.41% ($\kappa = 0.7694$); model evaluation on archived `g600` matches `comprehensive_benchmark_table.md` exactly to 4 decimal places (82.00% / 0.6781), while active 300 ground-truth yields 89.00% / 0.6089. |
| **MH-2.7** | Scripts Directory Classification | All 88 scripts in `scripts/` categorized into 27 read-only Python, 19 read-only shell, and 42 mutating Python scripts | **PASS** | Exact count: 69 `.py` + 11 `.ps1` + 8 `.sh` = 88 total scripts; full classification mapped and verified in `03_scripts_classification_and_execution_audit.md`. |
| **MH-2.8** | Empirical / Econometric Execution | All safe read-only empirical/econometric scripts executed under Python 3.15.1, and broken path failures documented | **PASS** | `test_table_defs.py` (rc=0), `verify_html.py` (rc=0, 3,843 prose words), `audit_check.py` (rc=1, `FileNotFoundError`), `audit_docx.py` (rc=1, `PackageNotFoundError`), `find_tables.py` (rc=1, `PackageNotFoundError`). |
| **MH-2.9** | Integrity Script & Harness Validator Gaps | Structural gaps in `audit_project_integrity.py` and fragility gaps in `validate-all.ps1` empirically documented | **PASS** | `audit_project_integrity.py` omits Modules 2, 3, and 7; line 36 asserts 655,649 but prints "Expected 655670 rows"; `validate-skills.ps1` CWD fragility causes silent false-positive pass ("0 skills checked, 0 errors, All valid"); all 8 `.sh` files contain CRLF line endings. |

---

## 3. Detailed Empirical Verification Results

### 3.1 DL Notebooks, Scripts, and Checkpoint Audit (Plan 2.1)

#### 1. Notebook and Seed Dataset Class Distribution
- **Dataset Counts:**
  ```powershell
  python -c "import pandas as pd; df = pd.concat([pd.read_csv(f'data/processed/{f}') for f in ['mygp_classified_reviews.csv', 'mybl_classified_reviews.csv', 'myrobi_classified_reviews.csv']]); print('Total:', len(df)); print(df['sentiment'].value_counts().to_dict()); print(df['category'].value_counts().to_dict())"
  ```
  *Output:*
  ```text
  Total: 4500
  {'Positive': 2774, 'Negative': 1238, 'Neutral': 488}
  {'General Appreciation / Other': 2731, 'Offers & Data Packs': 788, 'App Login & Technical Bugs': 400, 'Network Speed & 4G Latency': 364, 'Billing & Airtime Deductions': 217}
  ```
- **Stale Report File (`dl/reports/results.txt`):**
  - Line 4: `Executed In : Google Colab (Commit: 60cf0f4)`
  - Lines 11-13: `Positive: 2,773 (61.62%)`, `Negative: 1,238 (27.51%)`, `Neutral: 489 (10.87%)`
  - Line 59: Points to `dl/models/colab_bilstm_attention.pt`.
  - Independent check: `Test-Path dl/models/colab_bilstm_attention.pt` returned `False`.
- **BanglaBERT Colab Misclassification:**
  - Cell 10 (`dl/telecom_voc_banglabert_finetuning_colab.ipynb:904-906`): Input review `"Onk shundor app shob offer e discount pai"` predicted as `Negative (94.7% confidence)`.
- **BanglaBERT Category Macro-F1 Inconsistency:**
  - `dl/README.md:76` and `master_unified_colab.ipynb:1095`: `85.27% CV Accuracy / 0.7624 Macro-F1`.
  - `scripts/upload_to_huggingface.py:145-147,164`: Hardcodes `85.27% CV Accuracy / 0.8032 Macro-F1`.
- **Architecture Discrepancy:**
  - `dl/README.md:12,62` advertises `Hybrid BiLSTM + Attention + Char-CNN`.
  - `master_unified_colab.ipynb:486-504` (`class HybridBiLSTMAttention`): Word embedding only; zero character embedding or Char-CNN logic.

#### 2. BanglaBERT Git Diff & Zip Parity
- **Uncommitted Diff (`git diff dl/models/`):**
  - Verified in-place edits in `banglabert_finetuned_{sentiment,category}/config.json` swapping `"LABEL_0.."` with human-readable labels.
- **Label Alignment Hazard:**
  - BanglaBERT `config.json` class order: `0: General`, `1: Offers`, `2: App Login`, `3: Network`, `4: Billing`.
  - Scikit-learn `cat_le.joblib` class order: `0: App Login`, `1: Billing`, `2: General`, `3: Network`, `4: Offers`.
  - Passing BanglaBERT logits into `cat_le.inverse_transform()` corrupts 80% (4 of 5) classes.
- **SHA256 Parity:**
  - `dl/models/banglabert_finetuned_sentiment/model.safetensors` SHA256 in zip vs disk: `b566cc09e58f3649` (`True`).
  - `dl/models/banglabert_finetuned_category/model.safetensors` SHA256 in zip vs disk: `dc85d60cf99eb9f8` (`True`).

#### 3. Deserialization & CLI Runtime Tests
- **Vocabulary Unpickling Crash:**
  ```powershell
  python -c "import joblib; joblib.load('dl/models/bilstm_vocab.joblib')"
  ```
  *Observed Exception:*
  ```text
  AttributeError: module '__main__' has no attribute 'Vocabulary'
  ```
- **CLI Inference:**
  - `python dl/predict_dl.py --model bilstm --text "valo service"`: Exited code 0; predicted Positive (74.48%).
  - `python dl/predict_dl.py --model transformer --text "valo service"`: Exited code 1; `ModuleNotFoundError: No module named 'transformers'`.

---

### 3.2 Classical ML Models, Provenance & Gold Standard Benchmark Audit (Plan 2.2)

#### 1. ML Model Deserialization & Scikit-Learn Versions
- Executed deserialization script across all 9 `ml/models/*.joblib` files.
- `category_voting_classifier.joblib` and `sentiment_voting_classifier.joblib` raised `InconsistentVersionWarning` (serialized with scikit-learn 1.6.1; runtime 1.9.1).
- Reflection inspection proved `category_voting_classifier.joblib` contains:
  - `char` n-grams, `min_df=2`, `max_features=25000`
  - `word` n-grams, `max_features=12000`
  - `LogisticRegression(C=2.5)`, `ComplementNB(norm=False, alpha=0.5)`
  - Soft voting weights `[2.0, 2.5, 1.0]`
  - This matches Google Colab Cell 7 (`dl/telecom_voc_master_unified_colab.ipynb:387-436`), proving the disk model was imported from Colab, not generated by `ml/train_category.py` (`char_wb`, `max_features=None`, `LR C=1.0`, weights `[2, 2, 1]`).

#### 2. ML Training Script Bugs & Documentation Drift
- **`ml/train_category.py:247` Formatting Bug:** Confirmed code prints `{m['mean_macro_f1']:.4f} ± {m['mean_macro_f1']:.4f}`, duplicating the mean instead of printing the standard deviation.
- **`ml/train_filtered_experiments.py:19` Dead Path:** Sets `GOLD_CSV` to `scraped_data_2020/gold_set/gold_set_verified.csv` (which does not exist), silently returning `0.0, 0.0`.
- **Ablation Study Internal Contradiction (`ml/reports/short_text_filtering_ablation_study.md`):**
  - Table line 12-13 reports Gold Set Macro-F1 rising from `0.6737` to `0.7318` (+5.81%).
  - Prose line 19 asserts a rise from `0.6781` to `0.7436` (+6.55% to +7.80%) with broken LaTeX `(≥ 3$ words)`.
- **Language Classifier Threshold Fallthrough (`ml/language_detector.py:149-153`):**
  - Line 149 tests `english_ratio >= self.dominance_threshold (0.70)`.
  - Line 153 falls through to `elif english_ratio >= 0.60: lang = "English"`, lowering the effective English threshold to 60%.

#### 3. Inter-Annotator Agreement & Gold Standard Provenance Contradiction
- **Execution of `data/gold_set/calculate_agreement.py`:**
  - Raw Percentage Agreement: **91.00%** (Sentiment), **95.41%** (Operational Category).
  - Cohen's Kappa: $\kappa = \mathbf{0.5762}$ (Sentiment), $\kappa = \mathbf{0.7694}$ (Category).
  - De-anonymization: Prints `"Ratul CSV"` and `"Friend CSV"`.
  - Rulebook Violation: `[BLIND_106]` categorized as `Billing & Airtime Deductions` on price complaint, violating `ANNOTATION_RULEBOOK.md:122`.
- **Empirical Demonstration of Benchmark Provenance Contradiction:**
  - Evaluation on archived 600-sample `archive/scraped_data_2020/gold_set/archived_600_plan/gold_set_verified.csv`:
    - `ensemble_voting_classifier.joblib`: **82.00% Accuracy / 0.6781 Macro-F1**
    - `challenger_linearsvc.joblib`: **79.33% Accuracy / 0.6305 Macro-F1**
    - `primary_logistic_regression.joblib`: **75.33% Accuracy / 0.6347 Macro-F1**
    *These match `data/gold_set/comprehensive_benchmark_table.md:30-36` and `data/gold_set/gold_standard_evaluation_report.md:18-58` EXACTLY.*
  - Evaluation on active 300-sample `data/gold_set/blind_annotation_300_annotator1.csv`:
    - `ensemble_voting_classifier.joblib`: **89.00% Accuracy / 0.6089 Macro-F1**
    - `challenger_linearsvc.joblib`: **89.00% Accuracy / 0.6330 Macro-F1**
    - `primary_logistic_regression.joblib`: **82.67% Accuracy / 0.5836 Macro-F1**
  - **Verdict:** Project reports publish metrics from the archived 600-sample dataset (which `archived_600_plan/README.md` claimed was "never executed"), masking the fact that on the active 300-sample ground truth, model Macro-F1 drops from 0.6781 to 0.6089.

---

### 3.3 Scripts Directory Classification, Execution & Validator Gaps (Plan 2.3)

#### 1. Scripts Classification (88 Total Files)
- Verified total file count in `scripts/`: **88 files** (`69` `.py`, `11` `.ps1`, `8` `.sh`).
- Group 1: 27 Read-Only Python Scripts (14 executed and passing `rc=0`, 3 broken path failures `rc=1`, 10 verified read-only by AST).
- Group 2: 19 Read-Only Shell/PowerShell Scripts (11 `.ps1`, 8 `.sh`).
- Group 3: 42 File-Mutating Python Scripts (quarantined under `ADR-001`).

#### 2. Runtime Execution of Safe Read-Only Scripts
- `python scripts/test_table_defs.py`: Exited 0 (printed lengths and labels for `TABLE1_NEW` through `TABLE8_NEW`).
- `python scripts/verify_html.py`: Exited 0 (prose count: 3,843 words, exceeding 3,200 guideline target by +20.1%).
- Confirmed path failure on `python scripts/audit_check.py`: Exited 1 with `FileNotFoundError: [Errno 2] No such file or directory: 'paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex'`.
- Confirmed path failure on `python scripts/audit_docx.py`: Exited 1 with `PackageNotFoundError: Package not found at 'paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx'`.
- Confirmed path failure on `python scripts/find_tables.py`: Exited 1 with `PackageNotFoundError: Package not found at 'paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx'`.

#### 3. Integrity Script & GSD Validator Gaps
- **`scripts/audit_project_integrity.py` Gaps:**
  - Docstring advertises 8 modules; code executes only Modules 1, 4, 5 & 6, and 8. **Modules 2 (Gold Set), 3 (Model Predictions), and 7 (Version Telemetry) are completely missing.**
  - Line 36 assertion error message: `"Expected 655670 rows"`, while code asserts `total_rows == 655649`.
  - Line 65 tolerance masking: `assert np.isclose(nss, 53.05, atol=0.05)` masks the fact that Banglalink NSS is 53.04%.
  - Omissions in econometric validation: Lacks $N \ge 30$ CLT volume floor, consecutive-month checks, RMSSD/SSI, and pre-2020 era.
- **Harness Validator Fragility:**
  - `validate-all.ps1` passes with 0 errors when run from root.
  - CWD Fragility: Running `validate-skills.ps1` from `scripts/` fails to find `.agents/skills`, evaluates 0 skills, and prints `✅ All skills valid!` with exit code 0.
  - CRLF in Bash Scripts: All 8 `scripts/*.sh` files contain Windows CRLF (`\r\n`) line endings, which cause syntax errors under POSIX bash; completely ignored by `validate-encoding.ps1` (which only inspects `*.ps1`).

---

## 4. Constraint Adherence & Git Working-Tree Verification

- **`ADR-001` (Read-Only & No Git Commits):**
  - `git log -n 1 --oneline` confirmed latest commit is `3d9f889` (pre-existing commit). Zero git commits were created.
  - `git status --porcelain` confirmed zero non-`.gsd/` project or paper files were modified during Phase 2 execution.
- **`ADR-002` (Sequential `inherit` Workspace Execution):**
  - Confirmed. Subagents executed in order within the parent workspace, preserving uncommitted working-tree fidelity.
- **PowerShell Shell Discipline:**
  - Confirmed. Single-command invocations used without `&&` or `||` operators.

---

## 5. Summary of Discrepancies Cataloged in Phase 2

Phase 2 identified, verified, and cataloged **32 distinct discrepancies** (DISC-P2-01 through DISC-P2-32):
- **DL Suite (DISC-P2-01 to DISC-P2-11):** 11 discrepancies (stale results report, 2-operator Colab artifact, positive review misclassification, F1 score contradictions, missing 5-fold CV persistence, Char-CNN advertising discrepancy, BanglaBERT config diff & label alignment hazard, zip SHA256 parity, PyTorch checkpoint shapes, vocabulary pickle coupling bug, CLI inference missing flags/dependencies).
- **Classical ML & Gold Standard (DISC-P2-12 to DISC-P2-21):** 10 discrepancies (seed dataset 4,500 vs 4,499 drift, scikit-learn 1.6.1 unpickling warnings, Colab provenance of committed voting classifier, negative review prediction divergence on filtered model, `train_category.py` std duplication bug, `train_filtered_experiments.py` dead path bug, ablation study table vs prose contradiction, linguistic subcohort 14 emoticons exclusion, language detector 60% vs 70% threshold contradiction, global language 2016-2026 vs 2014-2026 date-range mismatch, missing `nltk` dependency, critical gold-set benchmark leakage from archived g600, de-anonymization in agreement script, broken documentation links, `[BLIND_106]` rulebook violation, LaTeX syntax errors).
- **Scripts & Integrity Audits (DISC-P2-22 to DISC-P2-32):** 11 discrepancies (3 broken scripts with stale paths, `audit_project_integrity.py` missing Modules 2, 3, 7, assertion message drift, `atol=0.05` tolerance masking, missing econometric floors, Leading University patch weakening, `validate-all.ps1` CWD fragility, CRLF line endings in 8 `.sh` scripts, shallow regexes in `validate-skills.ps1`, legacy tool names in `validate-agents.ps1`).

---

## 6. Phase Verification Verdict

**Final Verdict: PASS**

All 9 must-haves for Phase 2 are verified with concrete empirical proof. All claimed discrepancies against `ml/`, `dl/`, `data/gold_set/`, and `scripts/` have been independently reproduced and validated. Zero non-`.gsd/` files were touched, and zero git commits were created. Phase 2 is complete and verified. Cleared to proceed to Phase 3 (`Research Paper & Cross-Venue Deliverables Audit`).
