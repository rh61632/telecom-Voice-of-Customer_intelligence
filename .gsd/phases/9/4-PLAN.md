---
phase: 9
plan: 4
wave: 4
gap_closure: true
files_modified:
  - scripts/build_paper_html.py
  - paper/index.html
  - paper/paper.html
autonomous: true

must_haves:
  truths:
    - "scripts/build_paper_html.py Table 4 lines 1382 and 1427 update Robi 2022-12 -> 2023-01 to 20 months (with baseline regained in August 2024 noted) and GP 2025-08 -> 2025-09 to Unrecovered (with unrecovered through Sep 2026 noted), achieving 100% parity with TP LaTeX manuscript.tex:404,409 and empirical ground truth"
    - "scripts/build_paper_html.py line 678 and CSS line 101-105 synchronize static HUD prose badge and fill width to match scripts/verify_html.py (~3,940 / 3,200 w)"
    - "scripts/build_paper_html.py sec8-references prunes the 7 uncited orphan references (BTRC 2024, Dellarocas 2003, Devlin et al. 2019, GSMA 2024, Hasan et al. 2020, ITU 2024, Rahman et al. 2021) or provides contextual inline prose citations, establishing 1-for-1 parity with paper/telecommunications_policy_latex/references.bib"
    - "build_paper_html.py regenerates byte-identical paper/index.html and paper/paper.html passing scripts/verify_html.py and scripts/check_equations.py"
  artifacts:
    - path: "scripts/build_paper_html.py"
      provides: "Remediated HTML builder with correct Table 4 recovery, HUD prose count, and clean references"
    - path: "paper/index.html"
      provides: "Regenerated canonical interactive HTML paper deliverable"
    - path: "paper/paper.html"
      provides: "Byte-identical alias of index.html"
---

# Plan 9.4: HTML Deliverable Gap Closure (Table 4 Shock Recovery, HUD Count & Reference Pruning)

## Objective
Close the empirical and bibliographic gaps identified during Phase 9 verification in the standalone HTML paper deliverable (`scripts/build_paper_html.py` -> `paper/{index,paper}.html`):
1. Correct Table 4 shock recovery values and operational context (Robi `20 months`, GP `Unrecovered`).
2. Align HUD static word count badge and progress bar to `verify_html.py` (`~3,940 / 3,200 w`).
3. Prune the 7 uncited orphan references from `sec8-references` for 1-for-1 parity with `references.bib`.
4. Regenerate byte-identical `paper/index.html` and `paper/paper.html` and verify all HTML/equation checks pass.

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/phases/9/VERIFICATION.md`
- `paper/telecommunications_policy_latex/manuscript.tex` (lines 404, 409)
- `paper/telecommunications_policy_latex/references.bib`
- `scripts/build_paper_html.py`
- `scripts/verify_html.py`
- `scripts/check_equations.py`

## Tasks

<task type="auto">
  <name>Align Table 4 recovery, HUD word count, and reference list in build_paper_html.py</name>
  <files>
    scripts/build_paper_html.py
  </files>
  <action>
    Remediate `scripts/build_paper_html.py`:

    1. **Table 4 Shock Recovery & Context (lines 1377-1429):**
       - For Robi Axiata `2022-12 -> 2023-01` (-16.6):
         Replace:
         ```html
         <td class="num">1 month</td>
         <td>Winter token expiration bug; OTP authentication failure.</td>
         ```
         with:
         ```html
         <td class="num">20 months</td>
         <td>Winter token expiration bug; OTP authentication failure. NSS regained pre-shock baseline (+66.19) in August 2024.</td>
         ```
       - For Grameenphone `2025-08 -> 2025-09` (-18.5):
         Replace:
         ```html
         <td class="num">4 months</td>
         <td>5G launch bundle pricing backlash; data expiry reduction.</td>
         ```
         with:
         ```html
         <td class="num">Unrecovered</td>
         <td>5G launch bundle pricing backlash; data expiry reduction. NSS had not returned to pre-shock baseline through September 2026.</td>
         ```

    2. **HUD Word Count Synchronization (lines 678, 101-105):**
       - Update static fallback badge on line 678:
         Replace `~3,856 / 3,200 w` with `~3,940 / 3,200 w` to match the exact output of `scripts/verify_html.py`.
       - Update `.hud-bar-fill` style width or inline style to reflect 3,940 / 3,200 w (100% full or proportional).

    3. **Prune Uncited Orphan References from `sec8-references` (lines 1649-1676):**
       - Prune the 7 uncited orphan references that have no citations in HTML prose, matching `paper/telecommunications_policy_latex/references.bib` (which pruned `devlin2019bert`, `hasan2020sentiment`, `itu2024measuring`):
         - `BTRC. (2024)` (Note: `BTRC (2026)` is cited in prose at line 888, so keep `BTRC (2026)`)
         - `Dellarocas, C. (2003)`
         - `Devlin, J., ... (2019)`
         - `GSMA. (2024)`
         - `Hasan, M. R., ... (2020)`
         - `ITU. (2024)`
         - `Rahman, M. A., ... (2021)`
       - Verify that every remaining entry in `sec8-references` corresponds to an explicit in-text reference citation.

    AVOID: Modifying LaTeX files or compiled PDFs.
    AVOID: Introducing ASCII 0x09 tab characters in math blocks.
  </action>
  <verify>
    python -c "
with open('scripts/build_paper_html.py', encoding='utf-8') as f:
    c = f.read()
assert '20 months' in c
assert 'Unrecovered' in c
assert '3,940' in c
assert 'Dellarocas' not in c
assert 'Devlin' not in c
print('✓ scripts/build_paper_html.py syntax and content verified')
"
  </verify>
  <done>
    scripts/build_paper_html.py updated with aligned Table 4 recovery, HUD word count, and pruned references.
  </done>
</task>

<task type="auto">
  <name>Regenerate index.html and paper.html, and verify HTML/equation validators</name>
  <files>
    paper/index.html
    paper/paper.html
  </files>
  <action>
    1. Execute `python scripts/build_paper_html.py`.
    2. Confirm `paper/index.html` and `paper/paper.html` are regenerated and byte-identical:
       `python -c "import pathlib; h1=pathlib.Path('paper/index.html').read_bytes(); h2=pathlib.Path('paper/paper.html').read_bytes(); assert h1 == h2, 'HTML files differ'; assert b'\text' not in h1; assert b'20 months' in h1; assert b'Unrecovered' in h1; print('✓ Byte-identical HTML verified')"`
    3. Run `python scripts/verify_html.py` and confirm clean execution.
    4. Run `python scripts/check_equations.py` and confirm 7/7 equations pass.
    5. Run `python scripts/audit_project_integrity.py --strict-paper` and confirm exit code 0.
  </action>
  <verify>
    python scripts/audit_project_integrity.py --strict-paper
  </verify>
  <done>
    paper/index.html and paper/paper.html regenerated, byte-identical, free of stale recovery numbers and orphan references, and passing all validators.
  </done>
</task>

## Must-Haves
After all tasks complete, verify:
- [ ] Table 4 in `paper/index.html` and `paper/paper.html` contains `20 months` for Robi and `Unrecovered` for GP.
- [ ] HUD badge in HTML displays `~3,940 / 3,200 w`.
- [ ] Uncited orphan references pruned from HTML bibliography.
- [ ] `paper/index.html` and `paper/paper.html` are byte-identical.
- [ ] `python scripts/verify_html.py` and `python scripts/check_equations.py` pass.
- [ ] `python scripts/audit_project_integrity.py --strict-paper` passes cleanly (`rc=0`).

## Success Criteria
- [ ] All tasks verified passing.
- [ ] Must-haves confirmed with empirical single-command PowerShell checks.
- [ ] Zero unsolicited git commits (ADR-003).
