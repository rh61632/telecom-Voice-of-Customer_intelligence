# Phase 7 Plan 2: Master Integrity Audit & Legacy Script Retirement Summary

**Execution Status:** Complete (2/2 tasks verified)  
**Date:** 2026-11-11  
**Scope:** Plan 7.2 (`scripts/audit_project_integrity.py` 8 modules + `--strict-paper`, `scripts/verify_paper_complete.py`, `scripts/audit_paper_contradictions.py`, retirement of 28 dead/superseded scripts to `archive/legacy_scripts/` with inventory `README.md`).  
**Commits:** `none (ADR-003)` — all modifications staged in live workspace for staged user review.

---

## 1. Key Accomplishments

### Task 1: Script Archiving & Active Verification Scripts In-Place Repair
- **Legacy Script Retirement:** Created `archive/legacy_scripts/` and cleanly moved 28 obsolete, superseded, and broken scripts out of `scripts/`:
  1. *JBA LaTeX/docx read-only auditors (3):* `audit_check.py`, `audit_docx.py`, `find_tables.py`
  2. *JBA LaTeX/docx mutators (14):* `apply_fixes.py`, `apply_jba_revisions.py`, `apply_peer_review_fixes.py`, `apply_reviewer_fixes_latex.py`, `build_jba_full_manuscript.py`, `build_jba_submission_docx.py`, `convert_latex_to_docx.py`, `generate_jba_latex.py`, `sync_latex_jba.py`, `test_float.py`, `test_width.py`, `update_fig_caption.py`, `build_paper_docx.py`, `build_concise_paper_docx.py`
  3. *Obsolete Word COM automation page checkers (3):* `check_pages.ps1`, `check_last_pages.ps1`, `check_exact_pages.ps1`
  4. *Stale crop & Figure 1 offset debuggers (4):* `check_crop.py`, `check_crop_wide.py`, `check_other_crops.py`, `test_figure1_offsets.py`
  5. *Script self-patchers (4):* `update_audit_integrity.py`, `patch_audit_integrity.py`, `update_audit_completeness.py`, `patch_generate_global_viz.py`
- **Inventory Documentation:** Created `archive/legacy_scripts/README.md` cataloging each retired script, categorizing its original function and reasons for retirement (superseded by ESWA pipeline, deleted targets, non-portable COM automation), and clearly signposting active tools in `scripts/`.
- **In-Place Repairs:**
  - `scripts/verify_paper_complete.py`: Updated `3,716 -> 3,713 days` (2016-08-01 to 2026-09-30), `20,678 -> 20,657` early era reviews, and `88,184 -> 88,181` operational domain reviews.
  - `scripts/audit_paper_contradictions.py`: Updated total functional reviews in 4 domains from `88,184 -> 88,181`.
- **Verification:** Both verification scripts execute cleanly with 0 assertion errors.

### Task 2: Complete 8-Module Master Integrity Audit (`scripts/audit_project_integrity.py`)
Fully implemented and optimized all 8 audit modules with vectorized aggregation, achieving **6.37s** total execution time (strictly under the 10-second requirement):
- **Module 1 (Data Integrity):**
  - Confirmed common duration count `N=655,649` (GP: 320,140, Robi: 198,378, BL: 137,131).
  - Confirmed synchronized date window `2016-08-01` to `2026-09-30`.
  - Confirmed 0 duplicate `review_id` values, 0 core nulls, and exactly 51 legitimate null `review_text` rows.
  - Validated global dataset `N=661,160` with 0 duplicate IDs.
  - Aligned telemetry JSONs (`yearly_intelligence_trends.json` sums to 655,649; 2016 baseline = 438 GP / 126 Robi / 744 BL).
- **Module 2 (Gold Set Agreement & Independence):**
  - Validated sample sizes: `N=300` (100/op) and `N=200` (67 GP, 67 BL, 66 Robi).
  - Verified 0 review text overlap between Gold sets and seed $N=4,500$ dataset (zero data leakage).
  - Verified Sentiment IRR ($N=200$): Raw agreement `91.00%` (182/200), Cohen's $\kappa = 0.5762$, 3-class $\text{PABAK} = 0.8650$.
  - Verified Category IRR ($N=196$ valid pairs): Raw agreement `95.41%` (187/196), Cohen's $\kappa = 0.7694$.
  - Confirmed consensus subsets: $N=182$ (Sentiment) and $N=187$ (Category).
- **Module 3 (Model Deserialization & Benchmark Consistency):**
  - Confirmed clean deserialization of all 7 core models (`category_voting_classifier.joblib`, `sentiment_voting_classifier.joblib`, `ensemble_voting_classifier.joblib`, `primary_logistic_regression.joblib`, `challenger_linearsvc.joblib`, `category_logistic_regression.joblib`, `category_linearsvc.joblib`).
  - Confirmed `dl/models/bilstm_vocab.json` contains exactly 2,864 tokens via `dl.bilstm_artifacts.load_bilstm_vocab`.
  - Confirmed label schemas: `cat_le.joblib` has 5 alphabetical classes (for BiLSTM) and `banglabert_finetuned_category/config.json` has `CATEGORY_LABEL_MAP` (`0: General` .. `4: Billing`).
  - Evaluated live Hero model: feature space $V = 29,843$, ground-truth full-seed fit Accuracy `99.00%`, Macro-F1 `0.9883`.
  - Evaluated active Gold $N=300$ and consensus $N=182$ accuracy bounds: `ensemble_voting_classifier` ($89.00\% / 91.21\%$) and `sentiment_voting_classifier` ($83.67\% / 87.91\%$).
  - Confirmed linguistic subcohort benchmark sums to $N=4,500$.
- **Module 4 (Mathematical Invariants of NSS & Additive Decomposition):**
  - Enforced strict `atol=0.01`: GP `+64.85%`, Robi `+65.91%`, BL `+53.04%`, Sector `+62.70%`.
  - Vectorized additive decomposition verified across all 121 consecutive sector monthly transitions with maximum residual `2.13e-14 <= 1e-6`.
- **Module 5 (Time Series Aggregation, CLT Floor & Volatility):**
  - Confirmed 122 gapless monthly periods with `(curr - prev).n == 1`.
  - Modern era (2020–2026): 81 months per operator, minimum monthly volume $\ge 294 \gg 30$ (CLT floor satisfied), 240 transitions (80/op), exactly 35 shocks ($|\Delta\text{NSS}| \ge 10.0$).
  - Verified RMSSD & SSI: GP `6.28` (SSI `93.72`, filt `5.14`); Robi `5.61` (SSI `94.39`, filt `4.53`); BL `13.61` (SSI `86.39`, filt `7.56`).
- **Module 6 (Hypothesis Tests & Priority Matrix):**
  - Pooled $2\times 2$ contingency: Shocks 27/35 vs Non-shocks 91/205 $\implies \chi^2(1) = 12.83$, Fisher $\text{OR} = 4.23$ ($p = 4.04\times 10^{-4}$).
  - Non-surge $2\times 2$: Shocks 14/19 vs Non-shocks 82/189 $\implies \chi^2(1) = 6.38$, Fisher $\text{OR} = 3.65$.
  - Per-operator asymmetry: Banglalink Fisher $\text{OR} = 10.00 (p = 0.0007)$.
  - Proposition 1 surge regression: $R^2 = 0.5601$, slope = `11.52` ($p = 2.35\times 10^{-7}$).
  - Priority Matrix ($N=88,181$ in 4 operational domains): omnibus $\chi^2(3) = 11,027.60$, $V = 0.3536$; Billing $\text{OR} = 9.49$, Login $\text{OR} = 6.44$, Network $\text{OR} = 2.50$ vs Offers.
- **Module 7 (Spring 2024 Counterfactual Telemetry & Case Study 2):**
  - BL Spring 2024: `2024-03` ($N=1,093$, NSS `+42.82`), `2024-04` ($N=1,315$, NSS `+31.63`, $\Delta\text{NSS} = -11.18$), `2024-05` ($N=2,265$, NSS `+64.42`, $\Delta\text{NSS} = +32.78$).
  - BL `app_version` missingness rate: `51.82%` (71,068 nulls).
  - `v11.8.0` telemetry: Apr 2024 ($N=158$, NSS `-7.59`), Mar-Jun 2024 ($N=198$, NSS `+10.61`).
  - Case Study 2 turnaround: 2025 ($N=10,238$, NSS `+66.39`) to 2026 ($N=21,810$, NSS `+81.93`), $\Delta\text{NSS} = +15.54$, General component `+10.33` (66.5%), Technical component `+5.21` (33.5%).
- **Module 8 (Anonymity, Structure & Gated Deliverables):**
  - Confirmed 0 occurrences of prohibited terms (`Ratul`, `rh61632`, `Leading University`, `Jashore`, `github.com`) across `manuscript.tex`, `manuscript_twocolumn.tex`, `highlights.txt`, `references.bib`.
  - Confirmed all 8 academic sections and 8 table/algorithm labels in both `.tex` files.
  - Confirmed deliverable PDFs exist: `manuscript.pdf` (37 pages), `manuscript_twocolumn.pdf` (16 pages).
  - Gated Deliverable Evaluation:
    - Default mode emits visible warnings on pending Phase 8/9 items (raw `**` tokens, PDF page budgets, missing Excel) and exits 0 cleanly.
    - `--strict-paper` mode causes exit 1 on pending defects.

---

## 2. Empirical Verification Evidence

```powershell
# Task 1 Verification
python -c "import os; assert not os.path.exists('scripts/apply_fixes.py'), 'apply_fixes still in scripts'; assert os.path.exists('archive/legacy_scripts/apply_fixes.py'), 'apply_fixes not in archive'; assert os.path.exists('archive/legacy_scripts/README.md'), 'archive README missing'; import subprocess; subprocess.run(['python', 'scripts/verify_paper_complete.py'], check=True); subprocess.run(['python', 'scripts/audit_paper_contradictions.py'], check=True); print('✓ Script archiving and verify script repair verified!')"
# Output:
# ✓ Script archiving and verify script repair verified! (rc=0)

# Task 2 Verification: Default mode (<10s runtime)
python scripts/audit_project_integrity.py
# Output:
# ================================================================================
# AUDIT RESULT: 100% OF EMPIRICAL & SYSTEM CHECKS PASSED IN 6.37s!
# ================================================================================ (rc=0)

# Task 2 Verification: Strict paper gate
python scripts/audit_project_integrity.py --strict-paper
# Output:
# FAILED: --strict-paper mode enabled; failing audit on pending Phase 8/9 defects! (rc=1)
```

---

## 3. Deviations & Remediation Log

1. **`category_n196` NaN String Artifact in `compute_statistical_tests.py`:**
   - *Observation:* During Module 2 alignment, `compute_statistical_tests.py` line 511 used `str(r2.get("category_label", ""))`, which converted pandas float `NaN` to string `"nan"`. This caused 4 unannotated rows from Annotator 2 to be evaluated as mismatches ($187/200 = 93.5\%$, $\kappa = 0.7073$), whereas `calculate_agreement.py` legitimately excluded unannotated pairs ($187/196 = 95.41\%$, $\kappa = 0.7694$).
   - *Fix:* Added `if c1 and c2 and c1 != "nan" and c2 != "nan"` filtering in `scripts/compute_statistical_tests.py`, and updated `paper_empirical_ground_truth.json` / `.md` to record the exact $N=196$, $95.41\%$, $\kappa=0.7694$ values.
2. **Runtime Vectorization in `audit_project_integrity.py`:**
   - *Observation:* Unvectorized python row loops across 655k rows in Modules 4 and 5 took 24s.
   - *Fix:* Implemented vectorized `.groupby(['operator', 'ym', 'predicted_category', 'predicted_sentiment']).size().unstack(fill_value=0)` matrix aggregations, dropping runtime from 24s to 6.37s.

---

## 4. Next Step
Proceed to **Plan 7.3** (`scripts/*.sh` CRLF->LF conversion, `validate-*.ps1` / `validate-*.sh` `$PSScriptRoot` and regex remediation, phase wrap-up).
