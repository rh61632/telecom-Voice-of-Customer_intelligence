---
phase: 9
verified: 2026-11-14T12:50:00+06:00
status: passed
score: 26/26 must-haves verified
is_re_verification: true
gaps: []
---

# Phase 9 Verification Report: Cross-Venue Deliverables, Workbook & Final System Verification

**Phase:** 9  
**Goal:** Deliver canonical JBA Excel calculations workbook, compile Telecommunications Policy LaTeX suite in-place, remediate standalone HTML paper deliverable, clean scratch files, execute complete system verification suite, and author `.gsd/AUDIT_v2.md` closing all 55 discrepancies.  
**Result:** **Passed (26/26 must-haves verified)**  
**Re-verification:** True (Following gap closure plan `.gsd/phases/9/4-PLAN.md`)  

---

## 1. Executive Summary

Following execution of gap closure plan 9.4 (`.gsd/phases/9/4-PLAN.md`), Phase 9 has completed all requirements with 100% empirical compliance and zero regressions:

1. **HTML Deliverable Gap Closure (Plan 9.4):** Fully resolved.
   - **Table 4 Shock Recovery:** In `scripts/build_paper_html.py:1382,1427` and `paper/{index,paper}.html`, Robi `2022-12 -> 2023-01` correctly displays `20 months` (regained baseline $+66.19$ in August 2024) and Grameenphone `2025-08 -> 2025-09` correctly displays `Unrecovered` (NSS had not returned to pre-shock baseline through September 2026), matching `paper/telecommunications_policy_latex/manuscript.tex:404,409` and `paper_empirical_ground_truth.json`.
   - **HUD Word Count Synchronization:** Static fallback badge in `build_paper_html.py:696` and `paper/{index,paper}.html` is synchronized to `~3,940 / 3,200 w`, matching the exact 3,940 true prose word count calculated by `scripts/verify_html.py`.
   - **Reference Pruning:** The 7 uncited orphan references (`BTRC (2024)`, `Dellarocas (2003)`, `Devlin et al. (2019)`, `GSMA (2024)`, `Hasan et al. (2020)`, `ITU (2024)`, `Rahman et al. (2021)`) were pruned from `sec8-references`, achieving 1-for-1 parity with in-text citations.
   - **HTML Validators:** `paper/index.html` and `paper/paper.html` are regenerated and byte-identical (105,121 B). `scripts/verify_html.py` (3,940 prose words) and `scripts/check_equations.py` (7/7 equations valid) execute cleanly with return code 0.
2. **JBA Empirical Calculations Workbook (Plan 9.1):** Fully verified. `paper/JBA_Manuscript_Empirical_Calculations.xlsx` loads cleanly with 12 sheets, processes modern reviews ($N=634,992$), computes unrounded float deltas with zero residual ($2.75 \times 10^{-14}$ max), evaluates active models on Gold $N=300$ ($\text{Gold\_NSS} = 78.33$), and passes strict audit.
3. **Telecommunications Policy LaTeX Suite (Plan 9.2):** Fully verified. Compiles in-place via `paper/telecommunications_policy_latex/compile_tp.py` into `title_page.pdf` (2 pp), `manuscript.pdf` (31 pp), and `manuscript_twocolumn.pdf` (16 pp) with 0 undefined refs/cits and 0 overfull boxes >2.0 pt. ESWA deliverables in `paper/*.pdf` remain byte-identical and untouched.
4. **Final System Verification, Cleanup & Audit (Plan 9.3):** Fully verified. `demo/app.py:54` displays benchmark throughput ($8.17\text{ ms} \mid 122.4\text{ rev/s}$), `scratch/` is purged, 15 legacy patchers are archived in `archive/legacy_scripts/eswa_patchers/`, `audit_project_integrity.py --strict-paper` passes 100% in 8.29s (rc=0), `validate-all.ps1` passes with 0 errors/warnings, standalone ML/DL inference scripts execute cleanly, `.gsd/AUDIT_v2.md` comprehensively maps all 55 discrepancies, and repository HEAD remains at `3d9f889` with zero unsolicited git commits per ADR-003.

---

## 2. Must-Haves Verification

### 2.1 Observable Truths

| # | Truth | Status | Empirical Evidence |
|---|-------|:------:|-------------------|
| 1 | `build_paper_empirical_excel.py` loads exactly $N=634,992$ modern reviews ($ym \ge 2020\text{-}01$), eliminating 6 boundary records | **✓ VERIFIED** | `python scripts/build_paper_empirical_excel.py` asserts `len(df) == 634992` (GP 316,118, Robi 192,281, BL 126,593). Ingestion loaded directly from `all_operators_common_duration_classified.csv`. |
| 2 | Monthly NSS and category contribution deltas computed on unrounded floats, eliminating additive residual | **✓ VERIFIED** | Asserted `abs(sum(c_deltas.values()) - d_nss_raw) < 1e-10` across all 240 transitions. Max residual observed: $2.75 \times 10^{-14}$. |
| 3 | Directional delta weighting $c\_deltas[c] \cdot \operatorname{sgn}(d\_nss)$ produces 27/35 shocks (77.1%) and 91/205 non-shocks (44.4%) in `Null_Comparison_Prop2` | **✓ VERIFIED** | Querying `Null_Comparison_Prop2` via pandas confirms: Shocks App Login = 27 (77.1%), Non-Shocks App Login = 91 (44.4%). |
| 4 | `RMSSD_Volume_Sensitivity` computes baselines dynamically (GP 6.28, Robi 5.61, BL 13.61) and provides both $|\Delta\text{Vol}\%| < 50\%$ filter (GP 5.14, Robi 4.53, BL 7.56) and ratio [0.67, 1.50] filter | **✓ VERIFIED** | Querying `RMSSD_Volume_Sensitivity` confirms: GP 6.28 / 5.14 / 4.32; Robi 5.61 / 4.53 / 4.53; BL 13.61 / 7.56 / 7.55; BL Excl. Spring 2024 = 13.21. |
| 5 | Bootstrap volatility point estimates and p-values vs 1.0 computed dynamically (BL/Robi 2.43 $p=0.0008$, BL/GP 2.17 $p=0.0013$, GP/Robi 1.12 $p=0.3416$), and Monte Carlo guards `rem_n > 0` | **✓ VERIFIED** | Querying `Bootstrap_Volatility_CIs` confirms BL/Robi 2.43 [1.45, 4.02] $p=0.0008$; BL/GP 2.17 [1.33, 3.59] $p=0.0013$; GP/Robi 1.12 [0.72, 1.72] $p=0.3416$. Line 430 guards `(rem_tot > 0 and rem_n > 0)`. |
| 6 | `Model_Bias_and_Ablation` eliminates leaked $g600$ values, evaluating live active models on `blind_annotation_300_annotator1.csv` ($\text{Gold\_NSS} = 78.33$) | **✓ VERIFIED** | Querying `Model_Bias_and_Ablation` confirms $\text{Gold\_NSS} = 78.33$ across all rows, Prod Ensemble Acc 83.67%, Macro-F1 0.5625, LinearSVC Acc 89.00%, Macro-F1 0.6330. Zero 85.42 values. |
| 7 | Workbook includes `Paper_Ground_Truth_Summary` sheet derived from `paper_empirical_ground_truth.json` | **✓ VERIFIED** | Sheet exists with 52 canonical reference rows across Table 1 distributions, 122M Eras, Table 3 RMSSDs, Table 4 shocks, Priority Matrix, IRR, and Rogan-Gladen parameters. |
| 8 | `format_sheet()` guards boolean types before integer formatting | **✓ VERIFIED** | Confirmed guard `if isinstance(cell.value, bool): continue`. |
| 9 | `paper/JBA_Manuscript_Empirical_Calculations.xlsx` readable via openpyxl `data_only=True` and passes `audit_project_integrity.py --strict-paper` | **✓ VERIFIED** | All 12 sheets load with pre-evaluated values. Check 4 passed, script exited with code 0. |
| 10 | TP LaTeX `manuscript.tex` and `manuscript_twocolumn.tex` fix Equation 9 Rogan-Gladen identity ($P_{\text{true}} = \frac{P_{\text{observed}} - \text{FPR}}{\text{TPR} - \text{FPR}} = \frac{P_{\text{observed}} + \mathrm{Sp} - 1}{\mathrm{Se} + \mathrm{Sp} - 1}$) | **✓ VERIFIED** | Verified in `paper/telecommunications_policy_latex/manuscript.tex:245` and `manuscript_twocolumn.tex:246`. Inverted FPR sign completely eliminated. |
| 11 | Review language breakdown adds 51 null/empty-text ratings ($N=655,649$) and line 272 synchronized to pos=497,486 / neu=71,763 / neg=86,400 | **✓ VERIFIED** | Verified in line 179 ($578,780 + 55,689 + 6,585 + 14,544 + 51 = 655,649$) and line 272 across both single-column and two-column TP tex files. |
| 12 | Table 2 (+29.9, +61.2, +74.1), Table 3 (GP RMSSD 5.14), Table 4 (Robi 20 months, GP Unrecovered), Fisher CI [1.79, 9.98] / Woolf [1.83, 9.75], and model metrics match ground truth in TP LaTeX | **✓ VERIFIED** | Verified in `paper/telecommunications_policy_latex/manuscript.tex`: Table 2 lines 319, 325, 328; Table 3 line 376; Table 4 lines 404, 409; line 445; Section 3/Table A.1. |
| 13 | Retired $g600$ $\pm 2.4\text{ pp}$ envelope replaced by active Rogan-Gladen prevalence adjustment (+8.23 to +14.81 pp) and LinearSVC claim replaced | **✓ VERIFIED** | Verified in `paper/telecommunications_policy_latex/manuscript.tex:484` and `manuscript_twocolumn.tex:485`. |
| 14 | All 16 unreferenced labels in TP LaTeX cited in prose, 3 orphan BibTeX entries pruned, and 100% double-blind anonymity | **✓ VERIFIED** | `references.bib` pruned (28 entries remain); 0 prohibited tokens across blinded files. |
| 15 | `paper/telecommunications_policy_latex/compile_tp.py` compiles all 3 PDFs in-place with 0 undefined refs/cits and ZERO modification of `paper/*.pdf` | **✓ VERIFIED** | Executed `compile_tp.py`: `title_page.pdf` (2 pp), `manuscript.pdf` (31 pp), `manuscript_twocolumn.pdf` (16 pp). 0 undefined refs, 0 undefined cits. `paper/*.pdf` SHA256 hashes identical to `paper/eswa_latex/*.pdf`. |
| 16 | `scripts/build_paper_html.py` replaces 9 tab-escaped KaTeX math sequences (0 ASCII 0x09 control tabs in HTML), removes invalid CDN integrity, and aligns HUD count with `verify_html.py` (~3,940 / 3,200 w) | **✓ VERIFIED** | Verified line 696 displays `~3,940 / 3,200 w`. `verify_html.py` calculates exactly 3,940 prose words. 0 control tabs in KaTeX math sequences. Invalid CDN integrity attributes removed. |
| 17 | `build_paper_html.py` generates byte-identical `paper/index.html` and `paper/paper.html` with July 2016 exclusion, +51 null-text ratings, no false CNB calibration claim, aligned empirical tables/metrics (Table 4: Robi 20 months, GP Unrecovered; 0 orphan references), and passing `verify_html.py` & `check_equations.py` | **✓ VERIFIED** | `index.html` and `paper.html` are byte-identical (105,121 B). Table 4 Robi is '20 months' (Aug 2024 baseline note), GP is 'Unrecovered' (through Sep 2026 note). All 7 orphan references pruned. `scripts/verify_html.py` (3,940 w) and `scripts/check_equations.py` (7/7 eqns) pass cleanly. |
| 18 | `demo/app.py:54` replaces stale 1.42 ms / 450 rev/s string with measured benchmark (8.17 ms latency \| 122.4 reviews/sec) | **✓ VERIFIED** | Line 54 contains: `**Inference Hardware:** CPU (8.17 ms latency \| 122.4 reviews/sec)`. Verified with `python -m py_compile demo/app.py`. |
| 19 | `scratch/table_renders/` and `scratch/` root removed, `paper/eswa_latex/__pycache__/` cleared, and 10 one-off ESWA patcher scripts archived | **✓ VERIFIED** | `scratch/` directory does not exist. `paper/eswa_latex/__pycache__/` does not exist. All 10 patcher scripts removed from `scripts/` (15 total archived in `archive/legacy_scripts/eswa_patchers/`). |
| 20 | `archive/legacy_scripts/README.md` updated documenting newly archived ESWA patcher scripts | **✓ VERIFIED** | README Section 6 catalogs the archived patcher scripts in `archive/legacy_scripts/eswa_patchers/` (15 total). |
| 21 | `python scripts/audit_project_integrity.py --strict-paper` exits 0 with 100% of empirical and Phase 8/9 checks passing | **✓ VERIFIED** | Executed in 8.29s: All 8 modules passed. Check 4 passed. Exit code: 0. |
| 22 | `powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1` exits 0 across all workflows, skills, subagents, templates, and scripts | **✓ VERIFIED** | Executed cleanly: 27 workflows, 12 skills, 5 subagents, 24 templates, 16 scripts passed with 0 errors and 0 warnings. Exit code: 0. |
| 23 | Standalone ML and DL inference scripts execute successfully and exit 0; transformer check raises clean documented `ImportError` | **✓ VERIFIED** | `ml/predict.py`: rc=0 (Neutral 41.27%, General Appreciation 78.81%); `dl/predict_dl.py --model bilstm`: rc=0 (Neutral 70.50%); `dl/predict_dl.py --model bilstm-colab-category`: rc=0 (App Login 98.54%); `dl/predict_dl.py --model transformer`: rc=1 raising documented `ImportError: The 'transformers' library is required to run the MiniLM model`. |
| 24 | ESWA deliverable PDFs in `paper/*.pdf` maintain byte-identical SHA256 checksums with `paper/eswa_latex/*.pdf` and remain $\le 35$ and $\le 15$ pages | **✓ VERIFIED** | Checksums match byte-for-byte: `title_page.pdf` (`ce1ea3f5a58c...`, 2 pp), `manuscript.pdf` (`41cda56a2ef9...`, 32 pp $\le 35$), `manuscript_twocolumn.pdf` (`54698cef8948...`, 15 pp $\le 15$). |
| 25 | `.gsd/AUDIT_v2.md` provides complete audit traceability mapping all 55 cataloged discrepancies from `.gsd/DISCREPANCY_REPORT.md` | **✓ VERIFIED** | Verified programmatic coverage of all 55 discrepancies (`DISC-CRIT-01..08`, `DISC-MAJ-01..19`, `DISC-MIN-01..18`, `DISC-HYG-01..10`), detailing technical fixes, verification sections, and runtime skips. |
| 26 | Working tree remains cleanly reviewable with zero unsolicited git commits per ADR-003 | **✓ VERIFIED** | `git log -n 5` confirms repository HEAD remains unchanged at `3d9f889` (from Phase 6). Zero unsolicited commits created. |

---

### 2.2 Artifacts Verification

| Path | Level 1: Exists | Level 2: Substantive | Level 3: Wired | Status |
|---|:---:|:---:|:---:|:---:|
| `scripts/build_paper_empirical_excel.py` | ✓ | ✓ | ✓ | **PASS** |
| `paper/JBA_Manuscript_Empirical_Calculations.xlsx` | ✓ | ✓ | ✓ | **PASS** |
| `paper/telecommunications_policy_latex/manuscript.tex` | ✓ | ✓ | ✓ | **PASS** |
| `paper/telecommunications_policy_latex/manuscript_twocolumn.tex` | ✓ | ✓ | ✓ | **PASS** |
| `paper/telecommunications_policy_latex/title_page.tex` | ✓ | ✓ | ✓ | **PASS** |
| `paper/telecommunications_policy_latex/references.bib` | ✓ | ✓ | ✓ | **PASS** |
| `paper/telecommunications_policy_latex/compile_tp.py` | ✓ | ✓ | ✓ | **PASS** |
| `paper/telecommunications_policy_latex/title_page.pdf` | ✓ | ✓ | ✓ | **PASS** |
| `paper/telecommunications_policy_latex/manuscript.pdf` | ✓ | ✓ | ✓ | **PASS** |
| `paper/telecommunications_policy_latex/manuscript_twocolumn.pdf` | ✓ | ✓ | ✓ | **PASS** |
| `scripts/build_paper_html.py` | ✓ | ✓ | ✓ | **PASS** |
| `paper/index.html` | ✓ | ✓ | ✓ | **PASS** |
| `paper/paper.html` | ✓ | ✓ | ✓ | **PASS** |
| `demo/app.py` | ✓ | ✓ | ✓ | **PASS** |
| `archive/legacy_scripts/eswa_patchers/` | ✓ | ✓ | ✓ | **PASS** |
| `archive/legacy_scripts/README.md` | ✓ | ✓ | ✓ | **PASS** |
| `.gsd/AUDIT_v2.md` | ✓ | ✓ | ✓ | **PASS** |

---

### 2.3 Key Links Verification

| From | To | Via | Status | Details |
|---|---|---|:---:|---|
| `scripts/build_paper_empirical_excel.py` | `paper/JBA_Manuscript_Empirical_Calculations.xlsx` | OpenPyXL output | **✓ WIRED** | Generates 12 sheets with pre-evaluated cell values |
| `paper/JBA_Manuscript_Empirical_Calculations.xlsx` | `scripts/audit_project_integrity.py` | OpenPyXL `data_only=True` | **✓ WIRED** | Audited by Check 4; rc=0 |
| `paper/telecommunications_policy_latex/compile_tp.py` | `paper/telecommunications_policy_latex/*.pdf` | `pdflatex` + `bibtex` | **✓ WIRED** | Produces title page (2 pp), manuscript (31 pp), twocolumn (16 pp) |
| `paper/telecommunications_policy_latex/compile_tp.py` | `paper/*.pdf` | In-place isolation | **✓ WIRED** | Verified ESWA deliverable PDFs are untouched |
| `scripts/build_paper_html.py` | `paper/{index,paper}.html` | HTML write | **✓ WIRED** | Byte-identical generation (105,121 bytes) |
| `demo/app.py` | User UI display | Gradio Markdown | **✓ WIRED** | Displays 8.17 ms latency \| 122.4 reviews/sec |

---

## 3. Anti-Patterns Check

- Zero stale recovery values in HTML (`20 months` and `Unrecovered` confirmed).
- Zero orphan references in HTML (7 uncited entries pruned).
- Zero HUD badge mismatch (`~3,940 / 3,200 w` perfectly mirrors `verify_html.py`).
- Zero unsolicited commits (HEAD at `3d9f889`, ADR-003 observed).
- Zero broken KaTeX tabs or invalid CDN integrity attributes.
- Zero modifications to ESWA deliverable PDFs (`paper/*.pdf`).

---

## 4. Human Verification Needed

No human verification items are required. All empirical statistics, cross-venue PDFs, HTML outputs, and GSD validation checks have been verified programmatically via automated scripts and compilers.

---

## 5. Final Verdict

**Status:** `passed`  
**Score:** `26/26` must-haves verified (100%)  
**Gaps:** `0` remaining  

Phase 9 is complete and fully verified. All cross-venue deliverables, workbooks, HTML deliverables, and full system verification suites adhere to the highest empirical research standards.
