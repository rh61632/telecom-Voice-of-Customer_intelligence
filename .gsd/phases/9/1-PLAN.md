---
phase: 9
plan: 1
wave: 1
depends_on: []
files_modified:
  - scripts/build_paper_empirical_excel.py
  - paper/JBA_Manuscript_Empirical_Calculations.xlsx
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "scripts/build_paper_empirical_excel.py loads exactly N=634,992 modern reviews from all_operators_common_duration_classified.csv (ym >= 2020-01), eliminating the 6 boundary timestamp records from 2026-09-30 23:24..23:51"
    - "Monthly NSS and category contribution deltas are computed on unrounded floats before display rounding, eliminating the 0.0200 additive residual"
    - "Leading operational domain selection applies directional delta weighting c_deltas[c] * sgn(d_nss), resolving the 40-transition discrepancy and producing exactly 27/35 shocks (77.1%) and 91/205 non-shocks (44.4%) in Null_Comparison_Prop2"
    - "RMSSD_Volume_Sensitivity computes baseline RMSSDs dynamically (GP 6.28, Robi 5.61, BL 13.61) and provides both |ΔVol%| < 50% symmetric percentage filter (GP 5.14, Robi 4.53, BL 7.56) and ratio-symmetric [0.67, 1.50] sensitivity rows"
    - "Bootstrap volatility point estimates and p-values vs 1.0 are computed dynamically from data (BL/Robi 2.43 p=0.0008, BL/GP 2.17 p=0.0013, GP/Robi 1.12 p=0.3416), and Monte Carlo downsampling guards rem_n > 0 before calling hypergeometric sampling"
    - "Model_Bias_and_Ablation completely eliminates leaked g600 values (85.42 NSS, Se=0.711, Sp=0.942), dynamically evaluating live active models on blind_annotation_300_annotator1.csv (Gold_NSS = 78.33)"
    - "Workbook includes Paper_Ground_Truth_Summary sheet derived from paper_empirical_ground_truth.json (Table 1, 122M Eras, Priority Matrix, IRR, Rogan-Gladen, CV, Case Study 2)"
    - "format_sheet() guards boolean types before integer formatting (isinstance(cell.value, bool))"
    - "paper/JBA_Manuscript_Empirical_Calculations.xlsx is generated with pre-evaluated values readable via openpyxl data_only=True and pandas, causing python scripts/audit_project_integrity.py --strict-paper to pass cleanly (rc=0)"
  artifacts:
    - "scripts/build_paper_empirical_excel.py remediated and conforming to active empirical ground truth"
    - "paper/JBA_Manuscript_Empirical_Calculations.xlsx generated with all 12 canonical sheets"
---

# Plan 9.1: Empirical Workbook Remediation & Generation (REM-08, DISC-MAJ-14)

## Objective
Remediate `scripts/build_paper_empirical_excel.py` and generate the canonical reference workbook `paper/JBA_Manuscript_Empirical_Calculations.xlsx`. Align data ingestion with `all_operators_common_duration_classified.csv` ($N = 634,992$ modern reviews), replace unsigned leading-domain selection with directional driver weighting to match `Null_Comparison_Prop2` ground truth ($27/35$ shocks, $91/205$ non-shocks), make bootstrap and Monte Carlo downsampling fully dynamic with bounds guards, eliminate leaked `g600` metrics by evaluating live models against active Gold $N=300$ (`Gold_NSS = 78.33`), add the `Paper_Ground_Truth_Summary` sheet, and ensure `python scripts/audit_project_integrity.py --strict-paper` passes cleanly (`rc=0`).

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-08`)
- `.gsd/phases/9/RESEARCH.md` (Section 1.1, 1.2, Decision 1)
- `scraped_data_global/classified/paper_empirical_ground_truth.json`
- `scripts/build_paper_empirical_excel.py`
- `scripts/audit_project_integrity.py` (lines 438-535, 726-737)
- `data/gold_set/blind_annotation_300_annotator1.csv`

## Tasks

<task type="auto">
  <name>Remediate build_paper_empirical_excel.py with active ground truth and dynamic calculations</name>
  <files>
    scripts/build_paper_empirical_excel.py
  </files>
  <action>
    Remediate `scripts/build_paper_empirical_excel.py` to fix all defects identified in RESEARCH.md Section 1.2:

    1. **Data Ingestion Parity (lines 69-83):**
       - Replace loading the 3 separate `my*_classified_global.csv` files with direct loading from `CLS_DIR / "all_operators_common_duration_classified.csv"`.
       - Filter to modern era: `df = df[df["ym"] >= "2020-01"].copy()`.
       - Assert `len(df) == 634992` (exact row counts: Grameenphone 316,118, Robi 192,281, Banglalink 126,593). This eliminates the 6 boundary timestamp records from `2026-09-30 23:24..23:51`.

    2. **Unrounded MoM Deltas & Directional Leading Operational Domain (lines 114-120, 145-159):**
       - Compute `d_nss` and `c_deltas` from raw unrounded floats *before* rounding display columns, ensuring `abs(sum(c_deltas.values()) - d_nss) < 1e-12`.
       - In leading operational domain selection (line 157), replace `max(ACTIONABLE_CATS, key=lambda c: abs(c_deltas[c]))` with directional driver weighting matching `audit_project_integrity.py:438-440`:
         ```python
         sgn = 1.0 if d_nss >= 0 else -1.0
         leading_op = max(ACTIONABLE_CATS, key=lambda c: c_deltas[c] * sgn)
         leading_all = max(ALL_CATS, key=lambda c: c_deltas[c] * sgn)
         ```
       - This resolves the 40-transition divergence and produces exact ground-truth `Null_Comparison_Prop2` counts:
         - Shocks ($N=35$): App Login leading = **27/35** (77.1%).
         - Non-Shocks ($N=205$): App Login leading = **91/205** (44.4%).

    3. **RMSSD Volume Sensitivity (lines 237-246):**
       - Compute raw RMSSDs dynamically from `mdf` (GP: 6.28, Robi: 5.61, BL: 13.61).
       - Provide both:
         a) `|ΔVol%| < 50%` symmetric percentage filter (`GP 5.14, Robi 4.53, BL 7.56`) matching paper Table 3 and `audit_project_integrity.py:443`.
         b) Ratio-symmetric `[0.67, 1.50]` sensitivity row (`GP 4.32, Robi 4.53, BL 7.55`).
         c) Banglalink excluding Spring 2024 (`13.21`).
       - Remove hardcoded `80`, `6.28`, `5.61` literals.

    4. **Dynamic Bootstrap Volatility CIs & Monte Carlo Bounds Guard (lines 283-368):**
       - Compute `Point_Estimate` and `p_value_vs_1` dynamically from `tdf` and the 10,000 bootstrap resamples. Ensure output matches: GP 6.28 [4.33, 7.93], Robi 5.61 [3.88, 7.16], BL 13.61 [8.53, 18.77]; BL/Robi 2.43 [1.45, 4.02] $p=0.0008$; BL/GP 2.17 [1.33, 3.59] $p=0.0013$; GP/Robi 1.12 [0.72, 1.72] $p=0.3416$.
       - In Monte Carlo downsampling (line 354-356), guard `rem_n > 0` before calling `np.random.hypergeometric`:
         ```python
         rem_n = t_n - s_pos
         rem_tot = tot_arr[i] - p
         s_neg = np.random.hypergeometric(ng, max(0, neu), rem_n) if (rem_tot > 0 and rem_n > 0) else 0
         ```
       - Compute original and downsampled RMSSD statistics dynamically.

    5. **Eliminate Leaked `g600` from `Model_Bias_and_Ablation` (lines 468-477):**
       - Replace the hardcoded `g600` rows (`Gold_NSS: 85.42`, Soft-Voting `82.50 / -2.92 / 82.0% / 0.6781`, etc.) with live evaluation on verified human ground truth `data/gold_set/blind_annotation_300_annotator1.csv` ($N = 300$, verified `Gold_NSS = 78.33`):
         - `Human Gold Standard (N=300)`: NSS 78.33, Model NSS 78.33, Bias 0.00 pp, Acc 100.0%, Macro-F1 1.0000.
         - `Production Tri-Model Soft-Voting Ensemble (sentiment_voting_classifier.joblib)`: NSS 72.67, Bias -5.67 pp, Acc 83.67%, Macro-F1 0.5625.
         - `Challenger LinearSVC (challenger_linearsvc.joblib)`: NSS 81.00, Bias +2.67 pp, Acc 89.00%, Macro-F1 0.6330.
         - `Primary Logistic Regression (primary_logistic_regression.joblib)`: NSS 71.00, Bias -7.33 pp, Acc 82.67%, Macro-F1 0.5836.
         - `CLI Ensemble Voting (ensemble_voting_classifier.joblib)`: NSS 82.67, Bias +4.33 pp, Acc 89.00%, Macro-F1 0.6089.
         - `Star-Rating Heuristic`: NSS 87.33, Bias +9.00 pp, Acc 86.67%, Macro-F1 0.5438.
         - `BiLSTM + Attention Benchmark`: Documented from `data/gold_set/comprehensive_benchmark_table.md` (Sentiment Acc 78.67%, Category Acc 91.33%).

    6. **Add `Paper_Ground_Truth_Summary` Sheet:**
       - Read `scraped_data_global/classified/paper_empirical_ground_truth.json`.
       - Create a summary sheet documenting canonical ground-truth reference values: Table 1 review distributions, 122-month non-overlapping Era NSS values, Table 3 RMSSDs, Table 4 shock inventory, Priority Matrix odds ratios ($V=0.3536$), Rogan-Gladen screening parameters, inter-rater reliability ($\kappa = 0.7712$ Cat, $0.5762$ Sent), and Case Study 2 turnaround ($+15.54$ pp).

    7. **Cell Formatting Guard in `format_sheet()` (lines 53-56):**
       - Add boolean type check before integer formatting:
         ```python
         if isinstance(cell.value, bool):
             continue
         elif isinstance(cell.value, (int, np.integer)):
             cell.number_format = "#,##0"
         elif isinstance(cell.value, (float, np.floating)):
             cell.number_format = "0.00"
         ```
       - Write pre-evaluated values (no unevaluated formula strings that break `data_only=True` readers).

    AVOID: Loading separate `my*_classified_global.csv` files with `>= "2020-01-01"` date filtering, which leaks 6 boundary records.
    AVOID: Differencing rounded numbers, which inflates additive residuals.
    AVOID: Using `abs()` for leading operational domain, which causes 40 transitions to misidentify the driver.
  </action>
  <verify>
    python -c "import ast; ast.parse(open('scripts/build_paper_empirical_excel.py', encoding='utf-8').read()); print('build_paper_empirical_excel.py syntax clean')"
  </verify>
  <done>
    scripts/build_paper_empirical_excel.py remediated with all 7 specification updates, syntax validated, and free of g600 leakage.
  </done>
</task>

<task type="auto">
  <name>Generate JBA_Manuscript_Empirical_Calculations.xlsx and verify all sheets & integrity gate</name>
  <files>
    paper/JBA_Manuscript_Empirical_Calculations.xlsx
  </files>
  <action>
    1. Execute `python scripts/build_paper_empirical_excel.py`.
    2. Confirm `paper/JBA_Manuscript_Empirical_Calculations.xlsx` is created on disk.
    3. Run verification script via Python checking all 12 sheets:
       - `Monthly_NSS_Trajectories` (243 rows = 81 months * 3 operators)
       - `Volume_Regression_Diagnostics`
       - `Flagged_Volume_Spikes`
       - `RMSSD_Volume_Sensitivity` (GP 5.14, Robi 4.53, BL 7.56 under |ΔVol%| < 50%)
       - `Modern_Shocks_35_Transitions` (35 rows)
       - `Non_Shocks_205_Transitions` (205 rows)
       - `Null_Comparison_Prop2` (Shocks App Login: 27/35 = 77.1%, Non-Shocks: 91/205 = 44.4%)
       - `Bootstrap_Volatility_CIs` (GP 6.28, Robi 5.61, BL 13.61)
       - `Monte_Carlo_Downsampling`
       - `BL_Spring2024_App_Versions`
       - `Model_Bias_and_Ablation` (Gold_NSS = 78.33, no 85.42 g600 values)
       - `Paper_Ground_Truth_Summary`
    4. Assert `data_only=True` reader in openpyxl can read all values without returning `None` for data cells.
    5. Run `python scripts/audit_project_integrity.py --strict-paper` and confirm Check 4 passes and the script exits with code 0!
  </action>
  <verify>
    python scripts/audit_project_integrity.py --strict-paper
  </verify>
  <done>
    paper/JBA_Manuscript_Empirical_Calculations.xlsx generated with 12 verified sheets, 0 formula-caching gaps, 0 g600 leakage, and scripts/audit_project_integrity.py --strict-paper exits 0.
  </done>
</task>

## Verification
After all tasks complete:
- [ ] `scripts/build_paper_empirical_excel.py` processes exactly 634,992 modern reviews.
- [ ] `Null_Comparison_Prop2` sheet contains 27/35 shocks (77.1%) and 91/205 non-shocks (44.4%).
- [ ] `Model_Bias_and_Ablation` reflects live Gold $N=300$ ground truth (`Gold_NSS = 78.33`).
- [ ] `paper/JBA_Manuscript_Empirical_Calculations.xlsx` exists and is readable via `openpyxl(..., data_only=True)`.
- [ ] `python scripts/audit_project_integrity.py --strict-paper` exits with code 0.

## Success Criteria
- [ ] All tasks completed and verified with single-command PowerShell checks.
- [ ] Goal-backward must-haves confirmed.
