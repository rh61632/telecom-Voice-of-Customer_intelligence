---
phase: 3
plan: 3
wave: 3
depends_on:
  - "2-PLAN.md"
files_modified:
  - .gsd/phases/3/evidence/03_cross_venue_and_deliverables_audit.md
  - .gsd/phases/3/evidence/03_paper_scripts_and_tooling_audit.md
  - .gsd/phases/3/3-SUMMARY.md
autonomous: true
user_setup: []

must_haves:
  truths:
    - "telecommunications_policy_latex/ differences from ESWA (venue, affiliation, N=655,649, real annual NSS/eras/shocks, correct Cohen 1960) and its internal defects (stale 2-col PDF pre-sync counts, Eq 9 Rogan-Gladen FPR error, script sum 655,598, unreferenced labels) are documented"
    - "Legacy paper/*.html word count inflation (HUD 3,206w vs verified 3,843w), July 2016 exclusion (21 vs 27), CNB calibration claim, and 9 broken tab-escaped KaTeX math blocks are documented"
    - "Missing paper/JBA_Manuscript_Empirical_Calculations.xlsx on disk is confirmed, its generator script audit completed (revealing hardcoded g600-leaked 82.0% metrics), and auxiliary paper/figures/ overlaps documented"
    - "All paper-related scripts in scripts/ are cataloged into 18 broken scripts targeting deleted paper/journal_manuscript/ or docx, 4 broken crop helpers, and 10 stale/contradictory builder/audit scripts"
  artifacts:
    - ".gsd/phases/3/evidence/03_cross_venue_and_deliverables_audit.md"
    - ".gsd/phases/3/evidence/03_paper_scripts_and_tooling_audit.md"
    - ".gsd/phases/3/3-SUMMARY.md"
  key_links:
    - "Cross-venue deliverables link paper/telecommunications_policy_latex/, paper/*.html, and scripts/build_paper_empirical_excel.py to ESWA manuscript"
    - "Paper tooling audit links scripts/*paper* and scripts/audit_project_integrity.py to REQ-06 and downstream Phase 4 synthesis"
---

# Plan 3.3: Cross-Venue Artifacts (Telecom Policy, HTML, XLSX) & Paper-Builder Scripts Audit

<objective>
Audit cross-venue manuscript deliverables and paper tooling scripts under ADR-001 (strictly read-only on project/paper/data files outside `.gsd/`; zero git commits). Compare `paper/telecommunications_policy_latex/` against active ESWA, audit legacy `paper/*.html` (word count drift, KaTeX math tab-escape corruptions, CNB calibration claim), confirm absence of `paper/JBA_Manuscript_Empirical_Calculations.xlsx` on disk while auditing its generator script, verify auxiliary `paper/figures/` overlap, and catalog all 32 paper-related scripts in `scripts/` into broken, crop-dependent, and stale/contradictory categories.
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- .gsd/REQUIREMENTS.md
- .gsd/ROADMAP.md
- .gsd/DECISIONS.md
- .gsd/phases/3/RESEARCH.md
- paper/telecommunications_policy_latex/manuscript.tex
- paper/telecommunications_policy_latex/manuscript_twocolumn.tex
- paper/telecommunications_policy_latex/title_page.tex
- paper/telecommunications_policy_latex/references.bib
- paper/telecommunications_policy_latex/manuscript.pdf
- paper/telecommunications_policy_latex/manuscript_twocolumn.pdf
- paper/telecommunications_policy_latex/manuscript.log
- paper/telecommunications_policy_latex/manuscript_twocolumn.log
- paper/index.html
- paper/paper.html
- scripts/build_paper_html.py
- scripts/verify_html.py
- scripts/build_paper_empirical_excel.py
- scripts/audit_check.py
- scripts/audit_docx.py
- scripts/find_tables.py
- scripts/build_full_eswa_paper.py
- scripts/reconstruct_master_manuscript.py
- scripts/verify_paper_complete.py
- scripts/audit_paper_contradictions.py
- scripts/audit_project_integrity.py
</context>

<tasks>

<task type="auto">
  <name>Audit paper/telecommunications_policy_latex/, legacy paper/*.html, missing .xlsx, and auxiliary paper/figures/</name>
  <files>
    paper/telecommunications_policy_latex/manuscript.tex
    paper/telecommunications_policy_latex/manuscript_twocolumn.tex
    paper/telecommunications_policy_latex/title_page.tex
    paper/telecommunications_policy_latex/references.bib
    paper/telecommunications_policy_latex/manuscript.pdf
    paper/telecommunications_policy_latex/manuscript_twocolumn.pdf
    paper/telecommunications_policy_latex/manuscript.log
    paper/telecommunications_policy_latex/manuscript_twocolumn.log
    paper/index.html
    paper/paper.html
    scripts/build_paper_html.py
    scripts/verify_html.py
    scripts/build_paper_empirical_excel.py
    paper/figures/
    .gsd/phases/3/evidence/03_cross_venue_and_deliverables_audit.md
  </files>
  <action>
    Perform an exhaustive read-only audit of cross-venue LaTeX, legacy HTML, and auxiliary calculation workbooks:
    1. Audit `paper/telecommunications_policy_latex/`:
       - Target venue, title, and author affiliation: inspect `manuscript.tex:14,27` (*Telecommunications Policy*, *"With Great Reviews Comes Great Responsibility: A Decade of Telecom Consumer Voice in Bangladesh"*); `title_page.tex:20-34` (`Md. Ratul Hasan`, `Department of Electrical and Electronic Engineering, Jashore University of Science and Technology, Jashore -7408, Bangladesh`, Tel `+880 1916-277722`).
       - Contrast empirical alignment against ESWA: demonstrate that TP paper aligns much closer to ground truth (uses $N = 655,649$, 3,713 days, 122 months, real annual NSS in Table 3 lines 318-328, real 4 eras `20,657 + 77,471 + 197,864 + 359,657 = 655,649`, real shocks in Table 5 lines 403-409, real human kappa/raw $91.00\%/0.5762$ and $95.41\%/0.7694$ in Table A.2, and correct `Cohen (1960)` in `references.bib:235`).
       - Document defects in `telecommunications_policy_latex`:
         - Stale compiled 2-column PDF: `manuscript_twocolumn.tex:272` was updated Nov 8 with synced counts (`497,486 Pos / 71,763 Neu / 86,400 Neg`), but `manuscript.tex:272` and both compiled Nov 5 PDFs (`manuscript.pdf`, `manuscript_twocolumn.pdf`) still carry pre-sync counts (`497,377 / 71,659 / 86,613`).
         - Eq (9) line 245 miswrites Rogan-Gladen equation using `FPR` instead of $Sp = 1 - FPR$: writes `\frac{P_{obs} + FPR - 1}{TPR + FPR - 1}`.
         - Line 179 script breakdown counts sum to `655,598` (`!= 655,649`, 51 reviews missing).
         - Line 257 claims isotonic regression calibration, but code uses default Platt sigmoid scaling.
         - Table A.1 lines 577-582 reports different CV and gold-set metrics (`BiLSTM Sent 81.50%/0.7120`, `MiniLM Cat 81.45%/0.7290`, `LinearSVC 85.33%/0.7410`) from ESWA Table 2 and `dl/README.md`.
         - Unreferenced labels: `tab:leaderboard`, `tab:kappa`, `tab:thresholds`, `eq:nss..eq:shock`.
         - Build logs: verify zero undefined references or missing citations, zero overfull boxes, 30/41 underfull hboxes/vboxes.
    2. Audit legacy HTML files (`paper/index.html` and `paper/paper.html`):
       - Confirm byte-identical match (`107,213` B, SHA256 `c751a7846c86...`, 1,892 lines) built by `scripts/build_paper_html.py` for legacy JBA submission.
       - Discrepancy in word count: HUD sidebar line 678 claims `~3,206 / 3,200 w`, whereas `python scripts/verify_html.py` measures `3,843` words (`+20.1%` over target).
       - July 2016 exclusion discrepancy: line 870 claims `21` July 2016 reviews excluded, whereas true exclusion count is `27` (`655,676 - 655,649`).
       - Calibration claim: line 1021 claims CNB calibration reduced mean maximum predicted confidence from 84.76% to 74.47% (vs CalibratedClassifierCV on LinearSVC).
       - KaTeX syntax corruption: identify `7` occurrences of `\text` corrupted to `\t`+`ext` (literal tab followed by `ext`) and `2` occurrences of `\times` corrupted to `\t`+`imes` (literal tab followed by `imes`) across math blocks, causing rendering failures in KaTeX.
    3. Audit missing `.xlsx` workbook and auxiliary `paper/figures/`:
       - Confirm `paper/JBA_Manuscript_Empirical_Calculations.xlsx` is missing on disk (`Path('.').rglob('*.xlsx')` empty).
       - Inspect `scripts/build_paper_empirical_excel.py`: verify that git diff changed `PAPER_DIR` from `paper/journal_manuscript` to `paper`, but script was never executed. Document hardcoded stale metrics in `Model_Bias_and_Ablation` sheet (lines 470-476 still hardcode `g600`-leaked `82.0% / 0.6781` metrics labeled `N=300`, and `2024-04` note `"-7.59 NSS"`).
       - Audit `paper/figures/`: verify SHA256 parity of `figure1`–`figure4` across `paper/figures/`, `paper/eswa_latex/figures/`, and `paper/telecommunications_policy_latex/figures/`. Inspect `monthly_nss_trend_modern_era.png` == `monthly_nss_trend_2020_2026.png` (`520,603` B, `N = 634,992`, 81 months) generated by `scripts/generate_two_panel_figure.py`; document legend box overlapping `"Spring 2024 Shock Episode / v11.8 Crash & Hotfix"` text and x-tick collision at bottom-right (`2026-07` / `2026-09`).
    4. Save comprehensive empirical audit evidence with tables, code snippets, and line references to `.gsd/phases/3/evidence/03_cross_venue_and_deliverables_audit.md`.

    AVOID: Recompiling HTML or LaTeX, running `build_paper_empirical_excel.py`, or modifying files.
    USE: Read-only Python scripts inspecting text, HTML DOM/regex, log files, and image metadata.
  </action>
  <verify>
    python -c "import pathlib; p = pathlib.Path('.gsd/phases/3/evidence/03_cross_venue_and_deliverables_audit.md'); assert p.exists() and p.stat().st_size > 1000, f'File missing or too small: {p}'; print('Cross-venue deliverables evidence verified successfully')"
  </verify>
  <done>
    `.gsd/phases/3/evidence/03_cross_venue_and_deliverables_audit.md` exists and contains full comparative analysis of `telecommunications_policy_latex/`, HTML word count and tab-escape math defects, confirmation of missing `.xlsx`, and figure SHA256 parity.
  </done>
</task>

<task type="auto">
  <name>Audit paper-builder, patcher, and paper-related audit scripts in scripts/</name>
  <files>
    scripts/audit_check.py
    scripts/audit_docx.py
    scripts/find_tables.py
    scripts/build_full_eswa_paper.py
    scripts/reconstruct_master_manuscript.py
    scripts/build_paper_html.py
    scripts/build_paper_empirical_excel.py
    scripts/build_paper_docx.py
    scripts/build_concise_paper_docx.py
    scripts/verify_paper_complete.py
    scripts/audit_paper_contradictions.py
    scripts/audit_project_integrity.py
    scripts/rebuild_figure3.py
    scripts/generate_paper_figures.py
    scripts/check_crop.py
    .gsd/phases/3/evidence/03_paper_scripts_and_tooling_audit.md
    .gsd/phases/3/3-SUMMARY.md
  </files>
  <action>
    Perform an exhaustive read-only audit of all 32 paper-related scripts in `scripts/`:
    1. Categorize all 32 paper-related scripts in `scripts/`:
       - Group 1: Broken scripts targeting deleted `paper/journal_manuscript/` or missing `.docx` dependencies (18 scripts).
         - Read-only auditors that crash immediately on execution: `audit_check.py` (`FileNotFoundError: paper/journal_manuscript/tables/table1_taxonomy.tex`), `audit_docx.py` (`PackageNotFoundError: paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx`), `find_tables.py` (`PackageNotFoundError: paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx`).
         - Mutating scripts targeting deleted directory (12 scripts): `apply_fixes.py`, `apply_jba_revisions.py`, `apply_peer_review_fixes.py`, `apply_reviewer_fixes_latex.py`, `build_jba_full_manuscript.py`, `build_jba_submission_docx.py`, `convert_latex_to_docx.py`, `generate_jba_latex.py`, `sync_latex_jba.py`, `test_float.py`, `test_width.py`, `update_fig_caption.py` (and `update_audit_integrity.py`).
         - Obsolete JBA `.docx` builders targeting deleted/untracked `.docx` (2 scripts: `build_paper_docx.py` containing stale `3,716` alongside `655,649`; `build_concise_paper_docx.py`).
       - Group 2: Broken figure crop/offset helpers (4 scripts):
         - `check_crop.py`, `check_crop_wide.py`, `check_other_crops.py`, `test_figure1_offsets.py` targeting missing `paper/figures/crop_*_check.png` files.
       - Group 3: Stale or self-contradictory paper generation and verification scripts (10 scripts):
         - `build_full_eswa_paper.py` & `reconstruct_master_manuscript.py`: actively generate the corrupted tables ($N=4,499$, Table 3 typos, Table 5 overlapping 134M, Table 6 fabricated rows).
         - `rebuild_figure3.py`: line 179-180 saves only to `paper/figures/` and `paper/telecommunications_policy_latex/figures/`, failing to update `paper/eswa_latex/figures/`.
         - `generate_paper_figures.py`: writes only to `paper/figures/` (not `eswa_latex/figures/`) and generates hardcoded "Figure 1:" titles, with line 346 title clipping.
         - `verify_paper_complete.py:19-43`: hardcodes assertions for `"3,716 days"` and `"88,184"`, contradicting `all_operators_common_duration_classified.csv` (`3,713 days`) and `manuscript.tex:488` (`88,181`).
         - `audit_paper_contradictions.py:23`: hardcodes `"88,184"`.
         - `audit_project_integrity.py:36,173-215`: prints `"Expected 655670 rows"` in assertion error message, inspects only `manuscript.tex` (ignoring `manuscript_twocolumn.tex` and `title_page.tex`), checks only `Leading University` (ignoring `Jashore`), and omits page budget assertions.
    2. Document exact failure modes, missing file paths, stale assertions, and destination mismatches for each script in markdown tables with `script_path`, `category`, `status`, `target_path`, `exact_issue`.
    3. Write detailed evidence to `.gsd/phases/3/evidence/03_paper_scripts_and_tooling_audit.md` and synthesize the overall Phase 3 conclusion in `.gsd/phases/3/3-SUMMARY.md`.

    AVOID: Running mutating scripts or deleting broken scripts.
    USE: Read-only Python AST analysis and regex inspection of script targets and error handlers.
  </action>
  <verify>
    python -c "import pathlib; p1 = pathlib.Path('.gsd/phases/3/evidence/03_paper_scripts_and_tooling_audit.md'); p2 = pathlib.Path('.gsd/phases/3/3-SUMMARY.md'); assert p1.exists() and p1.stat().st_size > 1000, f'Evidence missing: {p1}'; assert p2.exists() and p2.stat().st_size > 1000, f'Summary missing: {p2}'; print('Paper scripts audit and 3-SUMMARY verified successfully')"
  </verify>
  <done>
    `.gsd/phases/3/evidence/03_paper_scripts_and_tooling_audit.md` and `.gsd/phases/3/3-SUMMARY.md` exist and contain complete classification of all 32 paper scripts, crash stack traces of the 3 broken read-only scripts, inventory of stale assertions in verification scripts, and comprehensive Phase 3 summary.
  </done>
</task>

</tasks>

<verification>
After all tasks, verify:
- [ ] Evidence document `03_cross_venue_and_deliverables_audit.md` documents Telecommunications Policy LaTeX comparison, HTML word count and KaTeX tab defects, missing XLSX workbook, and figure SHA256 parity
- [ ] Evidence document `03_paper_scripts_and_tooling_audit.md` documents all 32 paper scripts categorized into broken, crop-dependent, and stale/contradictory
- [ ] Summary file `3-SUMMARY.md` synthesizes all Phase 3 findings, ready for Phase 3 VERIFICATION.md
</verification>

<success_criteria>
- [ ] All tasks verified passing with exit code 0
- [ ] Must-haves confirmed
- [ ] Zero project source, data, or paper files modified outside `.gsd/`
- [ ] Zero git commits created
</success_criteria>
