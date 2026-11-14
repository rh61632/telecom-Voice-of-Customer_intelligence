# Phase 9 Plan 1 Summary: Empirical Workbook Remediation & Generation

**Plan:** `9/1-PLAN.md` (`Plan 9.1: Empirical Workbook Remediation & Generation`)  
**Status:** Complete  
**Date:** 2026-11-12  
**Adherence:** ADR-002 (sequential `inherit` workspace), ADR-003 (remediation & uncommitted working tree)

---

## 1. Executive Summary

Remediated `scripts/build_paper_empirical_excel.py` and successfully generated the canonical publication-grade reference workbook `paper/JBA_Manuscript_Empirical_Calculations.xlsx` (83.6 KB, 12 sheets) for the Journal of Business Administration (JBA) manuscript.

All 7 defects and data discrepancies identified in `RESEARCH.md` Section 1.2 (`DISC-MAJ-14`, `REM-08`) have been resolved:
1. **Data Ingestion Parity:** Switched ingestion from individual `my*_classified_global.csv` files to `all_operators_common_duration_classified.csv` filtered to `ym >= "2020-01"`. Exactly $N = 634,992$ modern reviews are loaded across 81 calendar months (Grameenphone: 316,118, Robi: 192,281, Banglalink: 126,593), eliminating the 6 boundary timestamp records from `2026-09-30 23:24..23:51`.
2. **Unrounded MoM Differencing & Directional Leading Domain:** Computed monthly NSS and category contributions on raw unrounded floats prior to display formatting, reducing decomposition residuals to $< 10^{-10}$ ($2.75 \times 10^{-14}$). Applied directional driver weighting $\Delta C_k \cdot \operatorname{sgn}(\Delta \text{NSS})$ per `audit_project_integrity.py:438-440`, resolving the 40-transition divergence and producing exact Proposition 2 ground truth:
   - Shocks ($N=35$): App Login leading = **27/35** ($77.1\%$)
   - Non-Shocks ($N=205$): App Login leading = **91/205** ($44.4\%$)
3. **Dynamic RMSSD Baselines & Volume Filtering:** Replaced hardcoded literals with dynamic evaluation:
   - Raw Baseline RMSSD: Grameenphone $6.28$, Robi $5.61$, Banglalink $13.61$
   - Symmetric Percentage Filter ($|\Delta \text{Vol}\%| < 50\%$): Grameenphone $5.14$, Robi $4.53$, Banglalink $7.56$
   - Ratio Filter ($[0.67, 1.50]$): Grameenphone $4.32$, Robi $4.53$, Banglalink $7.55$
   - Banglalink excluding Spring 2024: $13.21$
4. **Dynamic Bootstrap & Monte Carlo Bounds Guard:** Evaluated 10,000 stationary block bootstrap resamples dynamically (GP $6.28$ [$4.33, 7.93$], Robi $5.61$ [$3.88, 7.16$], BL $13.61$ [$8.53, 18.77$]; BL/Robi $2.43$ [$1.45, 4.02$] $p=0.0008$; BL/GP $2.17$ [$1.33, 3.59$] $p=0.0013$; GP/Robi $1.12$ [$0.72, 1.72$] $p=0.3416$). Added `rem_n > 0` guard to hypergeometric Monte Carlo downsampling.
5. **Zero $g600$ Leakage in Model Evaluation:** Completely purged retired $g600$ figures ($85.42$ NSS, $\text{Se}=0.711, \text{Sp}=0.942$). Dynamically evaluated live active `.joblib` models on verified human ground truth `data/gold_set/blind_annotation_300_annotator1.csv` ($\text{Gold\_NSS} = 78.33$):
   - Human Gold Standard ($N=300$): NSS $78.33$, Bias $0.00$ pp, Acc $100.0\%$, Macro-F1 $1.0000$
   - Production Tri-Model Ensemble (`sentiment_voting_classifier.joblib`): NSS $72.67$, Bias $-5.67$ pp, Acc $83.67\%$, Macro-F1 $0.5625$
   - Challenger LinearSVC (`challenger_linearsvc.joblib`): NSS $81.00$, Bias $+2.67$ pp, Acc $89.00\%$, Macro-F1 $0.6330$
   - Primary Logistic Regression (`primary_logistic_regression.joblib`): NSS $71.00$, Bias $-7.33$ pp, Acc $82.67\%$, Macro-F1 $0.5836$
   - CLI Ensemble Voting (`ensemble_voting_classifier.joblib`): NSS $82.67$, Bias $+4.33$ pp, Acc $89.00\%$, Macro-F1 $0.6089$
   - Star-Rating Heuristic: NSS $78.67$, Bias $+0.33$ pp, Acc $86.67\%$, Macro-F1 $0.5438$
   - BiLSTM + Attention Benchmark: documented from `data/gold_set/comprehensive_benchmark_table.md` (Acc $78.67\%$, Macro-F1 $0.5364$)
6. **Ground-Truth Reference Sheet:** Added `Paper_Ground_Truth_Summary` sheet with 52 canonical reference rows extracted dynamically from `scraped_data_global/classified/paper_empirical_ground_truth.json` (Table 1 review distributions, 122M longitudinal Eras, Table 3 RMSSDs, Table 4 shock inventory, Priority Matrix $\text{Cramer's } V=0.3536$, Rogan-Gladen screening parameters, inter-rater reliability $\kappa = 0.7694 / 0.5762$, Case Studies 1 & 2).
7. **Cell Formatting Guard & Pre-Evaluated Values:** Added explicit `isinstance(cell.value, bool)` guard in `format_sheet()` before integer styling. All values written as pre-evaluated primitives, fully readable under `openpyxl(..., data_only=True)`.

---

## 2. Verification Evidence

### 2.1 AST Syntax Verification
```powershell
python -c "import ast; ast.parse(open('scripts/build_paper_empirical_excel.py', encoding='utf-8').read()); print('build_paper_empirical_excel.py syntax clean')"
# Output: build_paper_empirical_excel.py syntax clean
```

### 2.2 Workbook Generation & 12-Sheet Verification
```powershell
python -c "
import openpyxl, pandas as pd
from pathlib import Path
wb = openpyxl.load_workbook('paper/JBA_Manuscript_Empirical_Calculations.xlsx', data_only=True)
assert len(wb.sheetnames) == 12
"
```
Confirmed sheets and dimensions:
1. `Monthly_NSS_Trajectories`: 244 rows, 20 columns (243 monthly observations, 81 months $\times$ 3 operators)
2. `Volume_Regression_Diagnostics`: 5 rows, 9 columns (GP, Robi, BL, Pooled)
3. `Flagged_Volume_Spikes`: 28 rows, 9 columns
4. `RMSSD_Volume_Sensitivity`: 11 rows, 4 columns (GP $5.14$, Robi $4.53$, BL $7.56$ under $|\Delta\text{Vol}\%| < 50\%$)
5. `Modern_Shocks_35_Transitions`: 36 rows, 26 columns ($35$ shock transitions)
6. `Non_Shocks_205_Transitions`: 206 rows, 26 columns ($205$ non-shock transitions)
7. `Null_Comparison_Prop2`: 5 rows, 5 columns (Shocks App Login: 27/35 = $77.1\%$, Non-Shocks: 91/205 = $44.4\%$)
8. `Bootstrap_Volatility_CIs`: 7 rows, 6 columns (GP $6.28$, Robi $5.61$, BL $13.61$)
9. `Monte_Carlo_Downsampling`: 3 rows, 7 columns
10. `BL_Spring2024_App_Versions`: 16 rows, 11 columns
11. `Model_Bias_and_Ablation`: 8 rows, 7 columns ($\text{Gold\_NSS} = 78.33$, 0 leaked $g600$ values)
12. `Paper_Ground_Truth_Summary`: 53 rows, 6 columns (52 ground-truth metrics)

### 2.3 Strict Project Integrity Audit Gate
```powershell
python scripts/audit_project_integrity.py --strict-paper
```
Output:
```
================================================================================
TELECOM VOC INTELLIGENCE: COMPREHENSIVE PROJECT INTEGRITY AUDIT
Mode: STRICT PAPER GATE (Exit 1 on Phase 8/9 defects)
================================================================================
...
[MODULE 8] Verifying Double-Blind Anonymity, Manuscript Structure & Deliverables...
  [PASS] Anonymity check: 0 prohibited terms across all 4 blinded ESWA files
  [PASS] Manuscript structure: All 8 sections and 8 key labels verified in both tex files
  [PASS] Deliverable PDFs exist: manuscript.pdf (32 pages), manuscript_twocolumn.pdf (15 pages)
  [PASS] 100% of Phase 8/9 paper deliverables also verified present and compliant!

================================================================================
AUDIT RESULT: 100% OF EMPIRICAL & SYSTEM CHECKS PASSED IN 14.41s!
================================================================================
```
Exit code: `0`.

---

## 3. Files Modified

| File | Status | Description |
|---|---|---|
| `scripts/build_paper_empirical_excel.py` | Remediated | Full parity with $N=634,992$ common dataset, unrounded floats, directional driver selection, live Gold $N=300$ evaluation, boolean formatting guard, and `Paper_Ground_Truth_Summary` sheet. |
| `paper/JBA_Manuscript_Empirical_Calculations.xlsx` | Generated | 12 canonical sheets, 83.6 KB, fully pre-evaluated values readable via `openpyxl(..., data_only=True)`. |

Per `ADR-003`, all changes remain uncommitted in the working tree for staged review.
