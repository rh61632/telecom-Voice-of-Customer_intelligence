---
phase: 9
plan: 3
wave: 3
depends_on: ["2"]
files_modified:
  - demo/app.py
  - archive/legacy_scripts/eswa_patchers/add_bib_entries.py
  - archive/legacy_scripts/eswa_patchers/add_fontenc.py
  - archive/legacy_scripts/eswa_patchers/apply_eswa_enhancements.py
  - archive/legacy_scripts/eswa_patchers/apply_paper_reconciliations.py
  - archive/legacy_scripts/eswa_patchers/fix_manuscript_latex.py
  - archive/legacy_scripts/eswa_patchers/fix_table_formatting.py
  - archive/legacy_scripts/eswa_patchers/insert_linguistic_section.py
  - archive/legacy_scripts/eswa_patchers/patch_base_tex.py
  - archive/legacy_scripts/eswa_patchers/test_milestone_space.py
  - archive/legacy_scripts/eswa_patchers/test_table_defs.py
  - archive/legacy_scripts/README.md
  - .gsd/AUDIT_v2.md
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "demo/app.py:54 replaces stale 1.42 ms latency | 450 reviews/sec string with empirical measured single-review benchmark (8.17 ms latency | 122.4 reviews/sec)"
    - "scratch/table_renders/ and scratch/ root directories are removed, paper/eswa_latex/__pycache__/ is cleared, and 10 one-off ESWA patcher/debugger scripts in scripts/ are archived to archive/legacy_scripts/eswa_patchers/"
    - "archive/legacy_scripts/README.md is updated documenting the 10 newly archived ESWA patcher scripts"
    - "python scripts/audit_project_integrity.py --strict-paper exits 0 with 100% of empirical checks and Phase 8/9 deliverable checks passing"
    - "powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1 exits 0 across all workflows, skills, subagents, templates, and scripts"
    - "Standalone ML and DL inference scripts (ml/predict.py, dl/predict_dl.py with bilstm and bilstm-colab-category) execute successfully and exit 0, while transformer model check raises clean documented ImportError"
    - "ESWA deliverable PDFs in paper/*.pdf maintain byte-identical SHA256 checksums with paper/eswa_latex/*.pdf and remain <= 35 and <= 15 pages"
    - ".gsd/AUDIT_v2.md provides complete, authoritative audit traceability mapping all 55 cataloged discrepancies from .gsd/DISCREPANCY_REPORT.md to their exact Phase 5-9 resolution, verification evidence, status (Closed / Policy-Deferred for DISC-MAJ-18), and runtime skips"
    - "Working tree remains cleanly reviewable with zero unsolicited git commits per ADR-003"
  artifacts:
    - "demo/app.py updated with measured throughput benchmark"
    - "Cleaned workspace free of scratch/table_renders/ and temporary caches"
    - "archive/legacy_scripts/eswa_patchers/ containing the 10 retired scripts and updated README.md"
    - ".gsd/AUDIT_v2.md comprehensive discrepancy closure audit document"
---

# Plan 9.3: Leftover Fix, Workspace Cleanup, Full Verification & AUDIT_v2.md (REM-08)

## Objective
Correct the subtle throughput string leftover in `demo/app.py:54`, delete workspace scratch renders and pycache, archive the 10 legacy one-off ESWA patcher scripts from `scripts/` to `archive/legacy_scripts/eswa_patchers/`, execute the comprehensive post-remediation verification battery across the entire repository and research paper suite, and author `.gsd/AUDIT_v2.md` formally closing all 55 cataloged discrepancies (`DISC-CRIT-01..08`, `DISC-MAJ-01..19`, `DISC-MIN-01..18`, `DISC-HYG-01..10`).

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-08`)
- `.gsd/DISCREPANCY_REPORT.md` (authoritative catalog of 55 discrepancies)
- `.gsd/phases/9/RESEARCH.md` (Section 4.1, 4.2, 4.3)
- `demo/app.py`
- `archive/legacy_scripts/README.md`
- `scripts/audit_project_integrity.py`
- `scripts/validate-all.ps1`

## Tasks

<task type="auto">
  <name>Fix demo/app.py throughput string, clean scratch files, and archive legacy patchers</name>
  <files>
    demo/app.py
    archive/legacy_scripts/eswa_patchers/add_bib_entries.py
    archive/legacy_scripts/eswa_patchers/add_fontenc.py
    archive/legacy_scripts/eswa_patchers/apply_eswa_enhancements.py
    archive/legacy_scripts/eswa_patchers/apply_paper_reconciliations.py
    archive/legacy_scripts/eswa_patchers/fix_manuscript_latex.py
    archive/legacy_scripts/eswa_patchers/fix_table_formatting.py
    archive/legacy_scripts/eswa_patchers/insert_linguistic_section.py
    archive/legacy_scripts/eswa_patchers/patch_base_tex.py
    archive/legacy_scripts/eswa_patchers/test_milestone_space.py
    archive/legacy_scripts/eswa_patchers/test_table_defs.py
    archive/legacy_scripts/README.md
  </files>
  <action>
    1. **Remediate `demo/app.py:54`:**
       - Replace `f"**Inference Hardware:** CPU (1.42 ms latency | 450 reviews/sec)\n"`
         with `f"**Inference Hardware:** CPU (8.17 ms latency | 122.4 reviews/sec)\n"` to reflect measured single-review CPU throughput.
       - Verify syntax via `python -m py_compile demo/app.py`.

    2. **Clean Workspace Scratch Artifacts:**
       - Delete directory `scratch/table_renders/` and any other files in `scratch/`, then remove `scratch/` directory.
       - Delete `paper/eswa_latex/__pycache__/` if present.

    3. **Archive 10 One-Off Legacy ESWA Patcher Scripts:**
       - Move the following 10 scripts from `scripts/` to `archive/legacy_scripts/eswa_patchers/`:
         - `add_bib_entries.py`
         - `add_fontenc.py`
         - `apply_eswa_enhancements.py`
         - `apply_paper_reconciliations.py`
         - `fix_manuscript_latex.py`
         - `fix_table_formatting.py`
         - `insert_linguistic_section.py`
         - `patch_base_tex.py`
         - `test_milestone_space.py`
         - `test_table_defs.py`
       - Update `archive/legacy_scripts/README.md` to catalog this second batch of 10 archived ESWA patcher/debugger scripts under Section 6 ("ESWA Manuscript Patchers and Formatting Debuggers").

    4. Verify working tree status:
       - Confirm `git status -s` shows no stray untracked scratch files.
  </action>
  <verify>
    python -c "import ast, pathlib; ast.parse(open('demo/app.py', encoding='utf-8').read()); assert not pathlib.Path('scratch').exists(); assert pathlib.Path('archive/legacy_scripts/eswa_patchers/patch_base_tex.py').exists(); print('✓ App.py, scratch cleanup, and archived patchers verified')"
  </verify>
  <done>
    demo/app.py throughput string updated, scratch files removed, 10 legacy patchers archived to eswa_patchers, and archive README updated.
  </done>
</task>

<task type="auto">
  <name>Execute full system verification suite across code, data, models, demo, and manuscripts</name>
  <files>
    scripts/audit_project_integrity.py
    scripts/validate-all.ps1
  </files>
  <action>
    Execute the entire post-remediation verification battery sequentially (single-command per step, never using `&&` or `||`):

    1. Run `python scripts/audit_project_integrity.py --strict-paper`:
       - Assert all 8 modules pass (`rc=0`).
       - Assert Checks 1–4 all pass with 0 warnings and 0 pending defects.

    2. Run `powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1`:
       - Assert all workflows (27), skills (12), subagents (5), templates (24), and scripts (16) pass validation (`rc=0`).

    3. Run paper and HTML verification tools:
       - Run `python scripts/verify_paper_complete.py` (`rc=0`).
       - Run `python scripts/audit_paper_contradictions.py` (`rc=0`).
       - Run `python scripts/verify_html.py` (`rc=0`).
       - Run `python scripts/check_equations.py` (`rc=0`).

    4. Run ML and DL standalone inference tests:
       - Run `python ml/predict.py --text "App login hoy na otp problem"` (assert exit code 0, Banglish detected, Negative, App Login).
       - Run `python dl/predict_dl.py --model bilstm --text "Network speed khub e baje"` (assert exit code 0, Negative).
       - Run `python dl/predict_dl.py --model bilstm-colab-category --text "App login hoy na otp problem"` (assert exit code 0, App Login).
       - Run `python dl/predict_dl.py --model transformer --text "Good app"` and assert it fails with the expected graceful `ImportError` on missing `transformers` package without crashing the environment.

    5. Confirm ESWA PDF SHA256 parity and page budgets:
       - Check SHA256 hashes of `paper/manuscript.pdf`, `paper/manuscript_twocolumn.pdf`, and `paper/title_page.pdf` match `paper/eswa_latex/*.pdf`.
       - Check page limits: `manuscript.pdf` <= 35, `manuscript_twocolumn.pdf` <= 15.

    6. Confirm git hygiene (`ADR-003`):
       - Run `git status -s` and `git log -n 3` to verify zero unsolicited git commits were created.
  </action>
  <verify>
    powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1
  </verify>
  <done>
    Entire post-remediation verification suite passes with rc=0 across integrity auditor, GSD validator, ML/DL models, paper checks, and PDF hashes.
  </done>
</task>

<task type="auto">
  <name>Author .gsd/AUDIT_v2.md closing all 55 cataloged discrepancies</name>
  <files>
    .gsd/AUDIT_v2.md
  </files>
  <action>
    Author the comprehensive Milestone v2.0.0 remediation audit report in `.gsd/AUDIT_v2.md`:

    1. **Executive Summary:**
       - Detail the full transition from Milestone v1.0.0 (Audit, 55 cataloged discrepancies across 4 tiers) to Milestone v2.0.0 (Remediation across Phases 5 through 9).
       - Summary table: 8 Critical (8 Closed), 19 Major (18 Closed, 1 Policy-Deferred for user commit), 18 Minor (18 Closed), 10 Hygiene (10 Closed) = 54 Closed, 1 Policy-Deferred (`DISC-MAJ-18`).

    2. **Canonical Discrepancy Closure Matrix:**
       - Map every single discrepancy ID from `.gsd/DISCREPANCY_REPORT.md` to:
         - Discrepancy ID & Title
         - Severity & Functional Group
         - Remediation Phase (5, 6, 7, 8, or 9)
         - Summary of Concrete Technical Fix Applied
         - Verification Artifact (referencing specific `.gsd/phases/{N}/VERIFICATION.md` sections)
         - Final Closure Status (`Closed` / `Policy-Deferred`)

    3. **Domain Verification Evidence Logs:**
       - Group A: Data Pipeline, Serialization, Demo UI & Dependencies (Phases 5, 6, 9).
       - Group B: Academic Manuscripts, Figures, BibTeX & Cross-Venue Deliverables (Phases 8, 9).
       - Group C: Cross-Artifact Quantitative Alignment & Ground Truth (Phases 6, 7, 8, 9).

    4. **Documented Environment Bounds & Policy Exceptions:**
       - Explicitly document local test skips: `transformers` (cloud/Colab-only for BanglaBERT fine-tuning) and `gradio` (cloud/demo web UI server). Note that models and demo script syntax are verified via unit tests and `py_compile`.
       - Document `DISC-MAJ-18` staged review status per `ADR-003`: working tree is intentionally left uncommitted for final human sign-off.

    5. **Empirical Sign-Off & System Certification:**
       - Include execution timestamp, GSD pipeline phase summaries, and formal sign-off declaring the repository 100% empirically aligned.
  </action>
  <verify>
    python -c "b = open('.gsd/AUDIT_v2.md', encoding='utf-8').read(); assert 'DISC-CRIT-01' in b; assert 'DISC-CRIT-08' in b; assert 'DISC-MAJ-19' in b; assert 'DISC-MIN-18' in b; assert 'DISC-HYG-10' in b; print('✓ .gsd/AUDIT_v2.md 55-discrepancy closure matrix verified')"
  </verify>
  <done>
    .gsd/AUDIT_v2.md authored with complete traceability for all 55 cataloged discrepancies, verified closure evidence, and formal sign-off.
  </done>
</task>

## Verification
After all tasks complete:
- [ ] `demo/app.py:54` displays `8.17 ms latency | 122.4 reviews/sec`.
- [ ] `scratch/` directory is deleted and 10 legacy patchers reside in `archive/legacy_scripts/eswa_patchers/`.
- [ ] `python scripts/audit_project_integrity.py --strict-paper` passes cleanly (`rc=0`).
- [ ] `powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1` passes cleanly (`rc=0`).
- [ ] Standalone ML/DL inference commands succeed.
- [ ] `.gsd/AUDIT_v2.md` comprehensively covers all 55 discrepancies.

## Success Criteria
- [ ] All tasks completed and verified with single-command PowerShell checks.
- [ ] Goal-backward must-haves confirmed.
