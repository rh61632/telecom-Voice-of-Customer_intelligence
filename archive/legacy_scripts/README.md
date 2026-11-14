# Archive: Legacy & Superseded Scripts

This directory preserves 38 legacy, obsolete, or superseded scripts that were retired from `scripts/` as part of Phase 7 hygiene remediation (`REM-05`) and Phase 9 cross-venue cleanup (`REM-08`).

All active production, evaluation, econometric, and verification tools remain in `scripts/`.

---

## Catalog of Retired Scripts

### 1. JBA LaTeX & Docx Read-Only Auditors (3 scripts)
These scripts targeted deleted intermediate draft files (e.g., `paper/journal_manuscript/...tex` and early `.docx` manuscripts) for the initial target journal prior to the ESWA pipeline migration.
- `audit_check.py`: Audited obsolete JBA LaTeX manuscript sections and table formatting.
- `audit_docx.py`: Inspected styles and table structures in deleted early Word `.docx` manuscripts.
- `find_tables.py`: Extracted table titles and definitions from legacy `.docx` drafts.

### 2. JBA LaTeX & Docx Manuscript Mutators (14 scripts)
These scripts performed automated regex patching, conversion, or compilation for deleted JBA LaTeX and Word formats. Superseded by the reproducible ESWA LaTeX manuscript pipeline (`paper/eswa_latex/`).
- `apply_fixes.py`: Applied early regex patches to legacy JBA LaTeX text.
- `apply_jba_revisions.py`: Injected peer review revisions into legacy JBA manuscript files.
- `apply_peer_review_fixes.py`: Staged early revision blocks for JBA draft.
- `apply_reviewer_fixes_latex.py`: Injected reviewer-specific edits into JBA LaTeX sources.
- `build_jba_full_manuscript.py`: Compiled monolithic JBA manuscript files.
- `build_jba_submission_docx.py`: Built formatted `.docx` submissions using `python-docx`.
- `convert_latex_to_docx.py`: Heuristic pandoc/regex converter for LaTeX to Word.
- `generate_jba_latex.py`: Templated LaTeX generator for initial journal layout.
- `sync_latex_jba.py`: Bidirectional synchronization utility between text notes and JBA LaTeX.
- `test_float.py`: Experimental float/table placement test for legacy LaTeX styles.
- `test_width.py`: Column width calculations for legacy JBA two-column tables.
- `update_fig_caption.py`: One-off caption updater for legacy LaTeX figure tags.
- `build_paper_docx.py`: Legacy generator for formatted paper in Word format.
- `build_concise_paper_docx.py`: Condensed variant builder for Word manuscripts.

### 3. Word COM Automation Page Checkers (3 scripts)
These Windows PowerShell scripts utilized Microsoft Word COM objects (`New-Object -ComObject Word.Application`) to count pages in deleted `.docx` drafts. Obsolete and non-portable in headless environments.
- `check_pages.ps1`: Automated page counting of legacy `.docx` drafts via Word COM.
- `check_last_pages.ps1`: Checked ending page numbers of document sections via Word COM.
- `check_exact_pages.ps1`: Page budget validator for deleted `Telecom_VoC_Intelligence_JBA_Manuscript.docx`.

### 4. Stale Crop & Figure 1 Offset Debuggers (4 scripts)
Temporary diagnostic scripts used during Figure 1 development to inspect bounding box crops and offsets. Replaced by production figure scripts (`scripts/generate_paper_figures.py`, `scripts/generate_two_panel_figure.py`).
- `check_crop.py`: Diagnostic bounding-box crop checker for Figure 1 drafts.
- `check_crop_wide.py`: Crop checker for wide aspect ratio figure drafts.
- `check_other_crops.py`: Diagnostic helper for intermediate panel PNG crops.
- `test_figure1_offsets.py`: Experimental coordinate tester for timeline annotation badges.

### 5. Script Self-Patchers & One-Off Mutators (4 scripts)
Ad-hoc helper scripts used in earlier development waves to patch audit scripts and visualization generators in-place.
- `update_audit_integrity.py`: One-off patcher for audit integrity assertions.
- `patch_audit_integrity.py`: Temporary regex patch script for early integrity checks.
- `update_audit_completeness.py`: Incremental updater for completeness scripts.
- `patch_generate_global_viz.py`: One-off patch applied to visualization generator.

### 6. ESWA Manuscript Patchers and Formatting Debuggers (10 scripts)
These scripts performed one-off regex patching, formatting adjustments, or intermediate compilation checks during the ESWA manuscript layout phase (`archive/legacy_scripts/eswa_patchers/`). Superseded by canonical sources in `paper/eswa_latex/` and `paper/telecommunications_policy_latex/`.
- `add_bib_entries.py`: Injected missing BibTeX entries into ESWA references.bib.
- `add_fontenc.py`: Injected T1 fontenc package into early ESWA LaTeX templates.
- `apply_eswa_enhancements.py`: Applied early review improvements to ESWA draft.
- `apply_paper_reconciliations.py`: Reconciled table figures across ESWA drafts.
- `fix_manuscript_latex.py`: Regex fixer for early ESWA LaTeX compilation errors.
- `fix_table_formatting.py`: Fixed table column specifications and widths in ESWA draft.
- `insert_linguistic_section.py`: Injected linguistic decomposition subsection into manuscript.
- `patch_base_tex.py`: Applied structural patches to base elsarticle template.
- `test_milestone_space.py`: Tested vertical spacing around milestone callouts.
- `test_table_defs.py`: Diagnostic tester for LaTeX table macro definitions.

---

## Active Pipeline Notice

Do not modify or execute scripts in this directory. For active production workflows:
- Machine Learning models & pipelines: `ml/`
- Deep Learning & NLP models: `dl/`
- Econometric & statistical tests: `scripts/compute_statistical_tests.py`
- Repository integrity audit: `scripts/audit_project_integrity.py`
- Manuscript LaTeX sources & figures: `paper/eswa_latex/`
