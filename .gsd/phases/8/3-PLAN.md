---
phase: 8
plan: 3
wave: 3
depends_on: ["2"]
files_modified:
  - paper/eswa_latex/compile_eswa.py
  - paper/eswa_latex/title_page.pdf
  - paper/eswa_latex/manuscript.pdf
  - paper/eswa_latex/manuscript_twocolumn.pdf
  - paper/title_page.pdf
  - paper/manuscript.pdf
  - paper/manuscript_twocolumn.pdf
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "paper/eswa_latex/compile_eswa.py checks return codes fail-fast on every pdflatex and bibtex pass, parses .log files for 0 undefined references/citations and overfull boxes > 2pt, and enforces pdfinfo page targets (manuscript.pdf <= 35, manuscript_twocolumn.pdf <= 15)"
    - "title_page.pdf, manuscript.pdf, and manuscript_twocolumn.pdf compile cleanly with 0 fatal errors, 0 undefined citations, and 0 overfull equation boxes"
    - "manuscript.pdf page count is <= 35 pages and manuscript_twocolumn.pdf page count is <= 15 pages"
    - "Every compiled PDF in paper/eswa_latex/ matches paper/*.pdf with byte-identical SHA256 hashes"
    - "python scripts/audit_project_integrity.py passes cleanly (rc=0) in default mode, and --strict-paper clears ALL ESWA Checks 1-3 with only Phase 9's paper/JBA_Manuscript_Empirical_Calculations.xlsx remaining in pending_defects"
  artifacts:
    - "paper/eswa_latex/compile_eswa.py upgraded with log checking and page count assertions"
    - "Clean compiled PDFs in paper/eswa_latex/ (title_page.pdf, manuscript.pdf, manuscript_twocolumn.pdf)"
    - "Synchronized deliverable PDFs in paper/ (title_page.pdf, manuscript.pdf, manuscript_twocolumn.pdf)"
---

# Plan 8.3: Clean ESWA PDF Compilation, Page Budget & Integrity Verification (REM-07)

## Objective
Upgrade `paper/eswa_latex/compile_eswa.py` with automated return code validation, log parsing for undefined references/citations and overfull boxes, and strict page limit verification. Recompile all ESWA PDFs (`title_page.pdf`, `manuscript.pdf`, `manuscript_twocolumn.pdf`), confirm that `manuscript.pdf` is $\le 35$ pages and `manuscript_twocolumn.pdf` is $\le 15$ pages, synchronize compiled PDFs to `paper/*.pdf`, and verify full system compliance via `scripts/audit_project_integrity.py` (including `--strict-paper` ESWA Checks 1–3).

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-07`)
- `.gsd/phases/8/RESEARCH.md` (Sections 2.4, 3.1, 4)
- `paper/eswa_latex/compile_eswa.py`
- `paper/eswa_latex/title_page.tex`
- `paper/eswa_latex/manuscript.tex`
- `paper/eswa_latex/manuscript_twocolumn.tex`
- `paper/eswa_latex/references.bib`
- `scripts/audit_project_integrity.py`

## Tasks

<task type="auto">
  <name>Upgrade compile_eswa.py with log validation and page count enforcement</name>
  <files>
    paper/eswa_latex/compile_eswa.py
  </files>
  <action>
    Upgrade `paper/eswa_latex/compile_eswa.py` to be a robust, self-checking compilation script:
    1. Check return codes fail-fast on every compilation pass:
       - Run `pdflatex -interaction=nonstopmode` (Pass 1). Assert `returncode == 0`.
       - For `manuscript` and `manuscript_twocolumn`, run `bibtex <target>`. Assert `returncode == 0`.
       - Run `pdflatex` (Pass 2) and `pdflatex` (Pass 3) to resolve all cross-references and citations.
    2. Add log parsing routine:
       - Inspect `title_page.log`, `manuscript.log`, and `manuscript_twocolumn.log`.
       - Count undefined references (`r"LaTeX Warning: Reference \`.*\' on page .* undefined"`). Fail if > 0.
       - Count undefined citations (`r"LaTeX Warning: Citation \`.*\' on page .* undefined"`). Fail if > 0.
       - Scan for overfull `\hbox` warnings > `2.0 pt` on equations, tables, or URLs.
    3. Query page counts via `pdfinfo`:
       - Assert `manuscript.pdf` has `Pages <= 35`.
       - Assert `manuscript_twocolumn.pdf` has `Pages <= 15`.
    4. Synchronize PDFs:
       - Copy `title_page.pdf`, `manuscript.pdf`, and `manuscript_twocolumn.pdf` directly from `paper/eswa_latex/` to `paper/` using `shutil.copy2`.
       - Verify SHA256 checksums between `paper/eswa_latex/*.pdf` and `paper/*.pdf` match 100%.

    AVOID: Ignoring non-zero return codes from pdflatex or bibtex.
    AVOID: Allowing silently deferred floats to exceed the 35-page and 15-page publication limits.
  </action>
  <verify>
    python -c "import ast; ast.parse(open('paper/eswa_latex/compile_eswa.py', encoding='utf-8').read()); print('✓ compile_eswa.py syntax verified')"
  </verify>
  <done>
    compile_eswa.py upgraded with fail-fast execution checks, log parsing for undefined references/citations and overfull boxes, page limit assertions, and SHA256 sync.
  </done>
</task>

<task type="auto">
  <name>Compile all ESWA PDFs and verify zero errors, zero warnings, and SHA256 sync</name>
  <files>
    paper/eswa_latex/title_page.pdf
    paper/eswa_latex/manuscript.pdf
    paper/eswa_latex/manuscript_twocolumn.pdf
    paper/title_page.pdf
    paper/manuscript.pdf
    paper/manuscript_twocolumn.pdf
  </files>
  <action>
    1. Execute `python paper/eswa_latex/compile_eswa.py` from repository root.
    2. Confirm all 3 documents compile successfully:
       - `title_page.pdf`
       - `manuscript.pdf`
       - `manuscript_twocolumn.pdf`
    3. Assert log files have 0 undefined references and 0 undefined citations.
    4. Assert page limits:
       - `manuscript.pdf`: `Pages <= 35`
       - `manuscript_twocolumn.pdf`: `Pages <= 15`
    5. Assert SHA256 parity between `paper/eswa_latex/*.pdf` and `paper/*.pdf`.
  </action>
  <verify>
    python -c "import hashlib, subprocess, re, pathlib; for f in ['title_page.pdf', 'manuscript.pdf', 'manuscript_twocolumn.pdf']: h1 = hashlib.sha256(pathlib.Path('paper/eswa_latex/' + f).read_bytes()).hexdigest(); h2 = hashlib.sha256(pathlib.Path('paper/' + f).read_bytes()).hexdigest(); assert h1 == h2, f'SHA256 mismatch for {f}'; out_sc = subprocess.check_output(['pdfinfo', 'paper/manuscript.pdf'], text=True); p_sc = int(re.search(r'Pages:\s+(\d+)', out_sc).group(1)); assert p_sc <= 35, f'manuscript.pdf {p_sc} > 35 pages'; out_tc = subprocess.check_output(['pdfinfo', 'paper/manuscript_twocolumn.pdf'], text=True); p_tc = int(re.search(r'Pages:\s+(\d+)', out_tc).group(1)); assert p_tc <= 15, f'manuscript_twocolumn.pdf {p_tc} > 15 pages'; print(f'✓ PDFs compiled cleanly and verified: manuscript {p_sc} pp (<=35), twocolumn {p_tc} pp (<=15), identical hashes!')"
  </verify>
  <done>
    title_page.pdf, manuscript.pdf, and manuscript_twocolumn.pdf compiled cleanly with 0 errors/warnings, meeting all page constraints and synchronized to paper/*.pdf.
  </done>
</task>

<task type="auto">
  <name>Run comprehensive system integrity audit and --strict-paper verification</name>
  <files>
    scripts/audit_project_integrity.py
  </files>
  <action>
    1. Run `python scripts/audit_project_integrity.py` (default mode).
       - Confirm that 100% of Modules 1 through 8 pass cleanly with return code 0.
    2. Run `python scripts/audit_project_integrity.py --strict-paper` and inspect pending defects:
       - Confirm Check 1 (raw markdown bold tokens in `.tex` files) PASSES (0 tokens found).
       - Confirm Check 2 (PDF page count targets: single-column `<= 35`, two-column `<= 15`) PASSES.
       - Confirm Check 3 (PDF SHA256 sync between `paper/` and `paper/eswa_latex/`) PASSES.
       - Confirm that the ONLY defect listed in `pending_defects` is `paper/JBA_Manuscript_Empirical_Calculations.xlsx does not exist yet (owned by Phase 9)`.
    3. Assert all Phase 8 requirements (`REM-06`, `REM-07`) are satisfied.
  </action>
  <verify>
    python -c "import subprocess, sys; res = subprocess.run([sys.executable, 'scripts/audit_project_integrity.py'], capture_output=True, text=True); assert res.returncode == 0, f'audit_project_integrity failed in default mode: {res.stdout}\n{res.stderr}'; sp = subprocess.run([sys.executable, 'scripts/audit_project_integrity.py', '--strict-paper'], capture_output=True, text=True); assert 'raw markdown (**...**) bold tokens' not in sp.stdout, 'Markdown defect found'; assert 'exceeds 35-page target' not in sp.stdout, 'Single-col page defect found'; assert 'exceeds 15-page target' not in sp.stdout, 'Two-col page defect found'; assert 'PDF SHA256 mismatch' not in sp.stdout, 'PDF SHA mismatch defect found'; assert 'paper/JBA_Manuscript_Empirical_Calculations.xlsx does not exist yet (owned by Phase 9)' in sp.stdout, 'Phase 9 xlsx defect note missing'; print('✓ All Phase 8 requirements verified passing! Only Phase 9 xlsx gated in --strict-paper.')"
  </verify>
  <done>
    Full system integrity audit passes with rc=0. --strict-paper clears all Phase 8 ESWA checks (Checks 1-3) with only the Phase 9 Excel workbook remaining.
  </done>
</task>

## Must-Haves
After all tasks complete, verify:
- [ ] `compile_eswa.py` checks all return codes, parses log files, and enforces page targets
- [ ] `title_page.pdf`, `manuscript.pdf`, and `manuscript_twocolumn.pdf` compile with 0 errors
- [ ] `manuscript.pdf` is $\le 35$ pages and `manuscript_twocolumn.pdf` is $\le 15$ pages
- [ ] All 3 PDFs have matching SHA256 checksums in `paper/` and `paper/eswa_latex/`
- [ ] `audit_project_integrity.py` default mode passes with return code 0
- [ ] `audit_project_integrity.py --strict-paper` clears Checks 1–3

## Success Criteria
- [ ] All tasks verified passing
- [ ] Must-haves confirmed
- [ ] Zero uncommitted git changes required (`ADR-003`)
