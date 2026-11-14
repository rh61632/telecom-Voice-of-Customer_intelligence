---
phase: 3
plan: 1
wave: 1
depends_on: []
files_modified:
  - .gsd/phases/3/evidence/01_eswa_structure_and_build_logs_audit.md
  - .gsd/phases/3/evidence/01_eswa_citations_metadata_and_backups_audit.md
  - .gsd/phases/3/1-SUMMARY.md
autonomous: true
user_setup: []

must_haves:
  truths:
    - "Byte-for-byte SHA256 parity and page geometry between paper/*.pdf and paper/eswa_latex/*.pdf are empirically verified across manuscript, twocolumn, and title page"
    - "Build logs (*.log) are verified for 0 undefined references/citations, severe overfull hbox in twocolumn (Eq 10, 32.0pt), title_page URL overflow (15.6pt), and Table underfull badness"
    - "All 8 sections, 17 subsections, 6 subsubsections, 8 tables, 5 figures, and 12 equations are structurally mapped with unreferenced labels identified"
    - "BibTeX database (49 entries) vs compiled citations (32 cited, 17 uncited orphans) is verified, including Cohen (2020) and Cambria (2018) year errors"
    - "Author anonymity in manuscript.tex/manuscript_twocolumn.tex, title_page.tex author/affiliation/repo URL drift, highlights char counts, and backup/draft .tex files are cataloged"
  artifacts:
    - ".gsd/phases/3/evidence/01_eswa_structure_and_build_logs_audit.md"
    - ".gsd/phases/3/evidence/01_eswa_citations_metadata_and_backups_audit.md"
    - ".gsd/phases/3/1-SUMMARY.md"
  key_links:
    - "ESWA LaTeX build artifacts link paper/eswa_latex/ to compiled paper/*.pdf deliverables"
    - "Unreferenced labels and citation orphans link paper/eswa_latex/references.bib to downstream reconciliation in 2-PLAN.md and Phase 4"
---

# Plan 3.1: Active ESWA Manuscript LaTeX/PDF Parity, Build Logs, Citations & Metadata Audit

<objective>
Audit the active Expert Systems with Applications (ESWA) deliverables in `paper/` and `paper/eswa_latex/` under ADR-001 (strictly read-only on project/paper/data files outside `.gsd/`; zero `pdflatex` runs, zero mutating scripts, zero git commits). Empirically verify SHA256 parity between root `paper/*.pdf` and `paper/eswa_latex/*.pdf`, extract all compile warnings and box overfulls from `*.log`, inventory all sections, tables, figures, equations, and unreferenced labels, audit BibTeX citations (identifying the 17 orphan entries and 2 wrong-year bugs), check double-blind anonymity and title page author/repo metadata drift, and catalog backup/scratch `.tex` files.
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- .gsd/REQUIREMENTS.md
- .gsd/ROADMAP.md
- .gsd/DECISIONS.md
- .gsd/phases/3/RESEARCH.md
- paper/eswa_latex/manuscript.tex
- paper/eswa_latex/manuscript_twocolumn.tex
- paper/eswa_latex/title_page.tex
- paper/eswa_latex/references.bib
- paper/eswa_latex/manuscript.bbl
- paper/eswa_latex/manuscript.blg
- paper/eswa_latex/manuscript.log
- paper/eswa_latex/manuscript_twocolumn.log
- paper/eswa_latex/title_page.log
- paper/eswa_latex/compile_eswa.py
- paper/eswa_latex/highlights.txt
</context>

<tasks>

<task type="auto">
  <name>Audit ESWA LaTeX vs PDF parity, structural inventory (sections, tables, figures, equations), and compilation build logs</name>
  <files>
    paper/manuscript.pdf
    paper/manuscript_twocolumn.pdf
    paper/title_page.pdf
    paper/eswa_latex/manuscript.pdf
    paper/eswa_latex/manuscript_twocolumn.pdf
    paper/eswa_latex/title_page.pdf
    paper/eswa_latex/manuscript.tex
    paper/eswa_latex/manuscript_twocolumn.tex
    paper/eswa_latex/manuscript.log
    paper/eswa_latex/manuscript_twocolumn.log
    paper/eswa_latex/title_page.log
    paper/eswa_latex/compile_eswa.py
    .gsd/phases/3/evidence/01_eswa_structure_and_build_logs_audit.md
  </files>
  <action>
    Perform an exhaustive read-only audit of ESWA deliverables structure, PDF synchronization, and compilation logs:
    1. Verify SHA256 checksums and file sizes between `paper/*.pdf` and `paper/eswa_latex/*.pdf`:
       - `manuscript.pdf` (Letter, 37 pages, 2,521,538 B)
       - `manuscript_twocolumn.pdf` (A4, 16 pages, 2,207,623 B)
       - `title_page.pdf` (Letter, 2 pages, 110,587 B)
       Confirm that root `paper/*.pdf` files are exact binary duplicates copied by `paper/eswa_latex/compile_eswa.py:29-31`.
    2. Audit preamble differences and body parity between `manuscript.tex` (668 lines) and `manuscript_twocolumn.tex` (663 lines):
       - Compare lines 1-24: note `elsarticle` documentclass options (`review,12pt,authoryear` vs `final,5p,times,twocolumn,authoryear`) and review-only packages (`lmodern`, `lineno`, `geometry` 1in, `\doublespacing`, `\linenumbers`).
       - Empirically verify that lines 25-668 of `manuscript.tex` are 100% byte-identical to lines 20-663 of `manuscript_twocolumn.tex` with a constant -5 line offset.
    3. Audit LaTeX compilation build logs (`manuscript.log`, `manuscript_twocolumn.log`, `title_page.log`):
       - Verify zero undefined references or missing citation keys (`MISSING_REFS: []`, `MISSING_BIB_KEYS: []`).
       - Extract and catalog all overfull hboxes with exact log line numbers and excess widths:
         - `manuscript_twocolumn.log:1038`: severe overfull hbox (32.00706pt too wide) at `manuscript_twocolumn.tex` line 206 (Equation 10 $\Delta\ln(V_{o,t})$ overflowing the single column).
         - `title_page.log:413`: overfull hbox (15.61658pt too wide) on GitHub URL at `title_page.tex:37-38`.
         - `manuscript.log:728,834`: minor overfull hboxes (1.09677pt at lines 239-241; 2.21463pt at Table 8 line 606).
       - Extract underfull hboxes and badness warnings: badness up to 10000 in Table 1 (`log:722`), Table 5 (`log:741-761`), Table 7 (`log:789-794`), and Table 8 (`log:799-1004`).
       - Extract hyperref Unicode/PDF-string warnings in `title_page.log:419-432` (`\cnotenum`, `\@corref`) producing trailing `; ` in PDF `Author: Ratul Hasan; `.
    4. Construct the complete structural element inventory:
       - 8 top-level sections, 17 subsections, and 6 subsubsections with section titles, LaTeX label keys, and line numbers.
       - 8 tables (`tab:taxonomy`, `tab:leaderboard`/`tab:model_leaderboard`, `tab:perclass`, `tab:linguistic_benchmark`, `tab:eras`, `tab:shocks`, `alg:canary`/`tab:canary_algorithm`, `tab:decision_matrix`/`tab:executive_matrix`). Record float types (`table*`), page placements in review vs 2-col PDFs, and document unreferenced tables (`Table 3` `tab:perclass`, `Table 8` `tab:decision_matrix`) and float/caption naming anomalies (`Table 7` captioned `Algorithm 1:` inside a `table*` environment).
       - 5 figures (`fig:system_architecture`, `fig:monthly_nss`, `fig:leadership_strip`, `fig:priority_matrix`, `fig:banglalink_reversal`), embedded PNG paths, and note caption/numbering defects.
       - 12 numbered equations (Eq 1 to Eq 12) and document unreferenced equation `eq:shock_threshold` (line 197).
    5. Save comprehensive empirical audit evidence with tables, code snippets, and line references to `.gsd/phases/3/evidence/01_eswa_structure_and_build_logs_audit.md`.

    AVOID: Running `pdflatex`, running `compile_eswa.py`, or modifying any `.tex`, `.pdf`, or `.log` file.
    USE: Read-only Python scripts or PowerShell commands to hash files, parse logs, parse LaTeX trees, and record exact line numbers and byte counts.
  </action>
  <verify>
    python -c "import pathlib; p = pathlib.Path('.gsd/phases/3/evidence/01_eswa_structure_and_build_logs_audit.md'); assert p.exists() and p.stat().st_size > 1000, f'File missing or too small: {p}'; print('ESWA structure and build logs audit evidence verified successfully')"
  </verify>
  <done>
    `.gsd/phases/3/evidence/01_eswa_structure_and_build_logs_audit.md` exists and contains verified SHA256 checksums, page counts, complete section/table/figure/equation inventory, unreferenced label lists, and exact line/pt evidence for all overfull/underfull log warnings.
  </done>
</task>

<task type="auto">
  <name>Audit BibTeX references, citations, author/repo metadata, anonymity, and auxiliary/backup files in paper/eswa_latex/</name>
  <files>
    paper/eswa_latex/references.bib
    paper/eswa_latex/manuscript.bbl
    paper/eswa_latex/manuscript.blg
    paper/eswa_latex/title_page.tex
    paper/eswa_latex/highlights.txt
    paper/eswa_latex/manuscript_base_1506.tex
    paper/eswa_latex/manuscript_twocolumn_base_1508.tex
    paper/eswa_latex/test_reconstruct.tex
    paper/eswa_latex/test_up.tex
    paper/eswa_latex/update_paper.py
    paper/eswa_latex/update_banglabert.py
    paper/eswa_latex/apply_full_review_fixes.py
    .gsd/phases/3/evidence/01_eswa_citations_metadata_and_backups_audit.md
    .gsd/phases/3/1-SUMMARY.md
  </files>
  <action>
    Perform an exhaustive read-only audit of citations, author metadata, anonymity, and auxiliary files in `paper/eswa_latex/`:
    1. Audit BibTeX database and citation coverage:
       - Parse all 49 `@article`/`@inproceedings`/`@book`/`@misc` entries in `paper/eswa_latex/references.bib`.
       - Parse all `\citep{...}` and `\citet{...}` keys across `manuscript.tex` (32 cited entries).
       - Document all 17 uncited orphan BibTeX entries (e.g. `hirschman1970exit`, `smith1999model`, `parasuraman1985conceptual`, `oliver1980cognitive`, `landis1977measurement`, `feinstein1990high`, `byrt1993bias`, `kazmaier2022power`, `platt1999probabilistic`, etc.).
       - Identify erroneous year fields in `references.bib`: `cohen1960coefficient` line 289 having `year = {2020}` (compiled as `Cohen (2020)` in `manuscript.bbl:63-64` and review/2-col PDFs), and `cambria2017senticnet` line 26 having `year = {2018}` (compiled as `Cambria et al. (2018)`).
    2. Audit author metadata, repository URLs, and double-blind anonymity:
       - Verify double-blind anonymity in `manuscript.tex:34` and `manuscript_twocolumn.tex:29` (`\author{}` with zero occurrences of author names, emails, affiliations, or repo URLs; PDF metadata `Author: ; `).
       - Audit `title_page.tex:17-22,37`: verify author name (`Ratul Hasan`), email (`rh61632@gmail.com`), affiliation (`Leading University, Sylhet`), and GitHub URL (`https://github.com/ratulhasan/telecom-Voice-of-Customer_intelligence`). Compare GitHub URL against active git remote (`https://github.com/rh61632/telecom-Voice-of-Customer_intelligence.git`), noting account username mismatch (`ratulhasan` vs `rh61632`).
       - Audit `highlights.txt:1-5`: measure character length of each of the 5 bullet lines (82, 78, 85, 81, 79 chars; all within Elsevier ESWA 85-char limit), and verify absence of an illegal header line.
    3. Audit auxiliary, backup, draft, and helper script files in `paper/eswa_latex/`:
       - Analyze `manuscript_base_1506.tex` (489 lines, old title at line 28) and `manuscript_twocolumn_base_1508.tex` (483 lines, old title at line 22).
       - Compare `test_reconstruct.tex` and `test_up.tex`: verify byte-identical SHA256 (`fe3dfaa322de...`, 364 lines, missing Sections 4 and 5 entirely).
       - Audit orphaned local python scripts (`update_paper.py`, `update_banglabert.py`, `apply_full_review_fixes.py`): document their timestamps, intended purpose, and how their edits were overridden by `scripts/reconstruct_master_manuscript.py`.
    4. Write findings to `.gsd/phases/3/evidence/01_eswa_citations_metadata_and_backups_audit.md` and generate `.gsd/phases/3/1-SUMMARY.md`.

    AVOID: Modifying any `.tex`, `.bib`, or `.txt` file. Do NOT execute mutating helper scripts.
    USE: Read-only Python parsing of BibTeX and LaTeX sources.
  </action>
  <verify>
    python -c "import pathlib; p1 = pathlib.Path('.gsd/phases/3/evidence/01_eswa_citations_metadata_and_backups_audit.md'); p2 = pathlib.Path('.gsd/phases/3/1-SUMMARY.md'); assert p1.exists() and p1.stat().st_size > 1000, f'Evidence missing: {p1}'; assert p2.exists() and p2.stat().st_size > 1000, f'Summary missing: {p2}'; print('Citations, metadata, backups, and 1-SUMMARY verified successfully')"
  </verify>
  <done>
    `.gsd/phases/3/evidence/01_eswa_citations_metadata_and_backups_audit.md` and `.gsd/phases/3/1-SUMMARY.md` exist and contain all 17 uncited bib keys, the 2 wrong-year bib bugs, title page repo divergence, highlights length metrics, and backup file characterizations.
  </done>
</task>

</tasks>

<verification>
After all tasks, verify:
- [ ] Evidence document `01_eswa_structure_and_build_logs_audit.md` documents SHA256 PDF parity, build log warnings (Equation 10 overfull hbox), section/table/figure/equation inventory, and unreferenced labels
- [ ] Evidence document `01_eswa_citations_metadata_and_backups_audit.md` documents all 17 uncited BibTeX entries, Cohen (2020) / Cambria (2018) year errors, anonymity/metadata checks, highlights char counts, and backup files
- [ ] Summary file `1-SUMMARY.md` is complete with all observed ESWA structural discrepancies and build log findings
</verification>

<success_criteria>
- [ ] All tasks verified passing with exit code 0
- [ ] Must-haves confirmed
- [ ] Zero project source, data, or paper files modified outside `.gsd/`
- [ ] Zero git commits created
</success_criteria>
