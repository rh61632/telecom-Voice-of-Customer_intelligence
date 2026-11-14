---
phase: 3
plan: 3
status: complete
completed_at: 2026-11-11
files_created:
  - .gsd/phases/3/evidence/03_cross_venue_and_deliverables_audit.md
  - .gsd/phases/3/evidence/03_paper_scripts_and_tooling_audit.md
  - .gsd/phases/3/3-SUMMARY.md
---

# Plan 3.3 Summary: Cross-Venue Deliverables (Telecommunications Policy, HTML, XLSX) & Paper Tooling Audit

## 1. Executive Summary

Under **`ADR-001`** (strictly read-only on project, data, and paper files outside `.gsd/`; zero `pdflatex` runs, zero mutating scripts, zero git commits) and **`ADR-002`** (sequential execution in `inherit` workspace), Plan 3.3 audited the cross-venue deliverables in `paper/` and all 32 paper-related scripts in `scripts/`.

This completes Phase 3 of the VoC Intelligence Discrepancy Audit Milestone. All planned deliverables were validated empirically and synthesized into two comprehensive evidence catalogs:
- [`.gsd/phases/3/evidence/03_cross_venue_and_deliverables_audit.md`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/.gsd/phases/3/evidence/03_cross_venue_and_deliverables_audit.md)
- [`.gsd/phases/3/evidence/03_paper_scripts_and_tooling_audit.md`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/.gsd/phases/3/evidence/03_paper_scripts_and_tooling_audit.md)

---

## 2. Key Empirical Findings

### 2.1 `paper/telecommunications_policy_latex/` vs Active ESWA Deliverable
1. **Target Journal & Author Affiliation:**
   - Targets Elsevier's *Telecommunications Policy* with title: *"With Great Reviews Comes Great Responsibility: A Decade of Telecom Consumer Voice in Bangladesh"*.
   - Author: `Md. Ratul Hasan`, `Department of Electrical and Electronic Engineering, Jashore University of Science and Technology, Jashore -7408, Bangladesh` (contrasting with `Ratul Hasan`, Leading University, Sylhet in ESWA).
2. **Empirical Alignment Superiority over ESWA:**
   - Accurately reports $N = 655,649$, 3,713 days, and 122 months.
   - **Real Annual NSS Trajectory (Table 3):** Annual volumes sum exactly ($1,308 + \dots + 53,064 = \mathbf{655,649}$) and annual NSS values match `scraped_data_global/classified/yearly_intelligence_trends.json`.
   - **Real Non-Overlapping Eras:** Era 1 (41M, $N=20,657$), Era 2 (12M, $N=77,471$), Era 3 (24M, $N=197,864$), Era 4 (45M, $N=359,657$) sum exactly to $655,649$ reviews and 122 months (eliminating ESWA's overlapping 134-month anomaly).
   - **Real Econometric Shocks (Table 5):** Contains only real detected shocks matching `nss_stability_and_shocks_summary.json` (eliminating the 7 phantom shocks in ESWA Table 6).
   - **Real Human Agreement (Table A.2):** Accurately reports $N=200$ (Sentiment, raw 91.00%, $\kappa = 0.5762$) and $N=196$ (Category, raw 95.41%, $\kappa = 0.7694$).
   - **Correct Citation Year:** Bibliography sets `cohen1960coefficient` `year = {1960}` (corrected from ESWA's `year = {2020}`).
3. **Internal Defects in `telecommunications_policy_latex`:**
   - **Stale Compiled Two-Column PDF:** Nov 8 update to `manuscript_twocolumn.tex:272` synced counts (`497,486 / 71,763 / 86,400`), but `manuscript.tex:272` and compiled Nov 5 PDFs (`manuscript.pdf`, `manuscript_twocolumn.pdf`) still carry pre-sync counts (`497,377 / 71,659 / 86,613`).
   - **Algebraic Error in Rogan-Gladen Adjustment (Eq 9, line 245):** Inverts sign of false-positive rate, writing $\frac{P_{\text{obs}} + \text{FPR} - 1}{\text{TPR} + \text{FPR} - 1}$ instead of $\frac{P_{\text{obs}} - \text{FPR}}{\text{TPR} - \text{FPR}}$.
   - **Script Breakdown Arithmetic Deficit (Line 179):** Explicit sub-cohort counts ($578,780 + 55,689 + 6,585 + 14,544$) sum to $655,598$, leaving a deficit of 51 reviews against $N = 655,649$.
   - **Calibration Claim Mismatch (Line 257):** Claims LinearSVC was calibrated via isotonic regression, whereas codebase uses default Platt sigmoid scaling.
   - **Cross-Venue Model Discrepancy (Table A.1):** Reports different 5-Fold and gold-set metrics (`LinearSVC 85.33%/0.7410`, `BiLSTM 81.50%/0.7120`, `MiniLM 82.33%/0.7240`) compared to ESWA Table 2.
   - **16 Unreferenced Labels:** Including `tab:leaderboard`, `tab:kappa`, `tab:thresholds`, and `eq:nss..eq:shock`.

### 2.2 Legacy Publication HTML Deliverables (`paper/*.html`)
1. **Binary Parity:** `paper/index.html` and `paper/paper.html` are 100% byte-identical duplicates ($107,213$ bytes, SHA256 `c751a784...`, 1,892 lines) targeting the Journal of Business Analytics (JBA).
2. **Word Count Inflation:** HUD sidebar line 678 claims `~3,206 / 3,200 w`, whereas DOM parsing by `scripts/verify_html.py` verifies **3,843 words** (+20.1% over guideline ceiling).
3. **July 2016 Exclusion Error:** Line 870 claims 21 reviews were excluded from July 2016; ground truth count is **27 reviews** ($655,676 - 655,649$).
4. **Calibration Claim Error:** Line 1021 claims Complement Naive Bayes performed probability calibration, whereas CNB was uncalibrated.
5. **KaTeX Syntax Tab-Escape Corruption:** 7 occurrences of `<TAB>ext` and 2 occurrences of `<TAB>imes` in math blocks because `scripts/build_paper_html.py` interpolated unescaped `\text` and `\times` inside standard Python string literals, corrupting client-side KaTeX rendering.

### 2.3 Calculation Workbooks & Auxiliary Visual Figures
1. **Confirmed Missing Workbook:** `paper/JBA_Manuscript_Empirical_Calculations.xlsx` does not exist on disk (`[]`). Generator script `scripts/build_paper_empirical_excel.py` was retargeted to `paper/` but never executed, leaving contaminated $g600$-leaked metrics (`82.0% / 0.6781`) and obsolete $-7.59$ crash notes hardcoded in source.
2. **Cross-Directory Parity:** Figures `figure1` through `figure4` are 100% byte-identical across `paper/figures/`, `paper/eswa_latex/figures/`, and `paper/telecommunications_policy_latex/figures/`.
3. **Auxiliary Figure Layout Defects:** `monthly_nss_trend_modern_era.png` == `monthly_nss_trend_2020_2026.png` ($520,603$ bytes) generated by `generate_two_panel_figure.py` suffers from legend box overlap onto the Spring 2024 shock annotation box, and rightmost x-tick label collision between `2026-07` and `2026-09`.

### 2.4 Categorization of All 32 Paper-Related Scripts in `scripts/`
1. **Group 1: Broken Scripts Targeting Deleted Artifacts (18 Scripts):**
   - 3 read-only auditors crashing immediately: `audit_check.py` (`FileNotFoundError`), `audit_docx.py` (`PackageNotFoundError`), `find_tables.py` (`PackageNotFoundError`).
   - 12 mutating scripts targeting deleted `paper/journal_manuscript/`: `apply_fixes.py`, `apply_jba_revisions.py`, `apply_peer_review_fixes.py`, `apply_reviewer_fixes_latex.py`, `build_jba_full_manuscript.py`, `build_jba_submission_docx.py`, `convert_latex_to_docx.py`, `generate_jba_latex.py`, `sync_latex_jba.py`, `test_float.py`, `test_width.py`, `update_fig_caption.py`.
   - 1 misaligned search script: `update_audit_integrity.py`.
   - 2 obsolete Word builders: `build_paper_docx.py` (line 208 hardcodes stale `3,716-day window`), `build_concise_paper_docx.py`.
2. **Group 2: Broken Visual Crop & Offset Helpers (4 Scripts):**
   - `check_crop.py`, `check_crop_wide.py`, `check_other_crops.py`, `test_figure1_offsets.py` targeting deleted intermediate crop PNG files.
3. **Group 3: Stale, Desynchronized, or Self-Contradictory Scripts (10 Scripts):**
   - Corrupted table generators: `build_full_eswa_paper.py`, `reconstruct_master_manuscript.py`.
   - Figure builders omitting target paths: `rebuild_figure3.py` (omits `eswa_latex/figures/`), `generate_paper_figures.py` (omits `eswa_latex/figures/`, clips title at line 346).
   - Verification scripts with stale hardcoded assertions: `verify_paper_complete.py` (`3,716 days`, `88,184`), `audit_paper_contradictions.py` (`88,184`).
   - Misleading master integrity script: `audit_project_integrity.py` (line 36 error message says `"Expected 655670 rows"`, checks only `manuscript.tex`, checks only `Leading University`, omits page budgets, yet prints `"100% OF EMPIRICAL AND MATHEMATICAL CHECKS PASSED PERFECTLY!"`).
   - Legacy format checkers/patchers: `check_equations.py` (HTML only), `fix_table_formatting.py`, `patch_base_tex.py`.

---

## 3. Phase 3 Synthesis & Milestone Status

Phase 3 has accomplished an exhaustive Level-3 empirical audit across all academic paper deliverables:
- **Plan 3.1:** Active ESWA LaTeX/PDF parity, build logs, citations, metadata, and backup artifacts.
- **Plan 3.2:** Active ESWA internal contradictions, reconstruction pipeline drift, figure defects, and codebase claim mismatches.
- **Plan 3.3:** Cross-venue deliverables (`telecommunications_policy_latex/`, `paper/*.html`, missing `.xlsx`, `paper/figures/`) and audit of all 32 paper scripts.

The repository is now fully prepared for Phase 3 independent verification (`gsd-verifier`) and subsequent Phase 4 cross-artifact quantitative reconciliation.

---

## 4. Verification Proof

```powershell
# 1. Verify Task 1 Evidence Exists and Exceeds 1000 Bytes
python -c "import pathlib; p = pathlib.Path('.gsd/phases/3/evidence/03_cross_venue_and_deliverables_audit.md'); assert p.exists() and p.stat().st_size > 1000; print('Task 1 verified: ' + str(p.stat().st_size) + ' bytes')"

# 2. Verify Task 2 Evidence and Summary Exist and Exceed 1000 Bytes
python -c "import pathlib; p1 = pathlib.Path('.gsd/phases/3/evidence/03_paper_scripts_and_tooling_audit.md'); p2 = pathlib.Path('.gsd/phases/3/3-SUMMARY.md'); assert p1.exists() and p1.stat().st_size > 1000; assert p2.exists() and p2.stat().st_size > 1000; print('Task 2 & 3-SUMMARY verified: p1=' + str(p1.stat().st_size) + ' B, p2=' + str(p2.stat().st_size) + ' B')"
```
