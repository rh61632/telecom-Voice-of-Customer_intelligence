---
phase: 2
plan: 3
wave: 3
depends_on:
  - "2-PLAN.md"
files_modified:
  - .gsd/phases/2/evidence/03_scripts_classification_and_execution_audit.md
  - .gsd/phases/2/evidence/03_integrity_script_and_validators_gap_audit.md
  - .gsd/phases/2/3-SUMMARY.md
autonomous: true
user_setup: []

must_haves:
  truths:
    - "All 88 scripts in scripts/ are categorized into 27 read-only Python, 19 read-only shell/PowerShell, and 42 mutating Python scripts"
    - "All safe read-only empirical, econometric, and diagnostic scripts in scripts/ are executed under Python 3.15.1 with runtimes and metrics captured, and broken path failures documented"
    - "audit_project_integrity.py structural gaps (omitted modules 2, 3, 7, loose tolerances, missing CLT floors) and GSD validate-all.ps1 gaps (CWD fragility, CRLF in .sh scripts, shallow regexes) are documented"
  artifacts:
    - ".gsd/phases/2/evidence/03_scripts_classification_and_execution_audit.md"
    - ".gsd/phases/2/evidence/03_integrity_script_and_validators_gap_audit.md"
    - ".gsd/phases/2/3-SUMMARY.md"
  key_links:
    - "Scripts classification links all 88 scripts in scripts/ to SPEC read-only audit constraints"
    - "Econometric script executions link statistical outputs (surges, Fisher OR, Table 6) to paper empirical calculations"
---

# Plan 2.3: Scripts Classification, Empirical/Audit Execution & Validator Gap Audit

<objective>
Catalog all 88 scripts in `scripts/` into read-only vs file-mutating categories, execute safe read-only empirical/econometric scripts under Python 3.15.1 to capture live statistical metrics and broken path failures, audit hidden omission gaps in `scripts/audit_project_integrity.py` (which silently omits Modules 2, 3, and 7), and audit GSD harness validator scripts (`scripts/validate-all.ps1`) for CWD fragility and CRLF line-ending defects under `ADR-001`.
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- .gsd/REQUIREMENTS.md
- .gsd/DECISIONS.md
- .gsd/phases/2/RESEARCH.md
- scripts/audit_project_integrity.py
- scripts/audit_thresholds.py
- scripts/check_version_bias.py
- scripts/audit_point1.py
- scripts/reconcile_empirical_numbers.py
- scripts/analyze_surges.py
- scripts/point4_prop2_by_operator.py
- scripts/print_table6_rows.py
- scripts/run_p4.py
- scripts/check_banglabert_gold.py
- scripts/check_equations.py
- scripts/find_all_colors.py
- scripts/test_table_defs.py
- scripts/verify_html.py
- scripts/audit_check.py
- scripts/audit_docx.py
- scripts/find_tables.py
- scripts/validate-all.ps1
- scripts/validate-agents.ps1
- scripts/validate-encoding.ps1
- scripts/validate-skills.ps1
- scripts/validate-templates.ps1
- scripts/validate-workflows.ps1
</context>

<tasks>

<task type="auto">
  <name>Classify all 88 scripts in scripts/ and execute safe read-only empirical/econometric scripts</name>
  <files>
    .gsd/phases/2/evidence/03_scripts_classification_and_execution_audit.md
  </files>
  <action>
    Classify all 88 scripts in `scripts/` and execute the safe read-only empirical/econometric scripts under Python 3.15.1, capturing runtimes, outputs, and path failures.

    Steps:
    1. Build a complete catalog of all 88 files in `scripts/` (`69` `.py` + `19` `.ps1`/`.sh`):
       - Group 1: 27 Read-only Python scripts (14 verified working, 3 broken paths, 10 read-only paper/stat scripts).
       - Group 2: 19 Read-only shell/PowerShell scripts (12 GSD validators, 4 search helpers, 3 Word COM page counters).
       - Group 3: 42 Mutating/network Python scripts strictly prohibited from execution during audit (26 LaTeX/DOCX/HTML builders, 8 figure generators, 4 script patchers, 3 dataset/report writers, 1 Hugging Face uploader).
    2. Execute the safe read-only Python scripts under Python 3.15.1, recording execution command, runtime in seconds, exit code, and key statistical output:
       - `scripts/audit_thresholds.py` (threshold grid scan)
       - `scripts/check_version_bias.py` (version telemetry, N=1,787 vs 2,886)
       - `scripts/audit_point1.py` (Point 1 econometric Fisher OR=3.65)
       - `scripts/reconcile_empirical_numbers.py` (corpus sentiment counts)
       - `scripts/analyze_surges.py` (volume surges and anomalous spikes)
       - `scripts/point4_prop2_by_operator.py` (Point 4 Proposition 2 metrics)
       - `scripts/run_p4.py` and `scripts/print_table6_rows.py` (Table 6 OLS regressions)
       - `scripts/check_banglabert_gold.py` (BanglaBERT evaluations)
       - `scripts/check_equations.py` (LaTeX math equations)
       - `scripts/find_all_colors.py` (color palette consistency)
       - `scripts/test_table_defs.py` (LaTeX table structure)
       - `scripts/verify_html.py` (HTML word count: 3,843 vs 3,200 target)
    3. Document the 3 broken scripts that fail with `rc=1` due to stale paths:
       - `scripts/audit_check.py`: `FileNotFoundError` on `'paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex'`
       - `scripts/audit_docx.py`: `PackageNotFoundError` on `'paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx'`
       - `scripts/find_tables.py`: `PackageNotFoundError` on `'paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx'`
    4. Compile full inventory and execution logs into `.gsd/phases/2/evidence/03_scripts_classification_and_execution_audit.md`.

    AVOID: Executing any of the 42 mutating Python scripts (e.g., `build_*.py`, `apply_*.py`, `patch_*.py`, `upload_to_huggingface.py`).
    USE: Safe single-command execution of verified read-only scripts with output logging.
  </action>
  <verify>
    python scripts/test_table_defs.py
  </verify>
  <done>
    Evidence document 03_scripts_classification_and_execution_audit.md details full 88-script classification, runtime logs of safe scripts, and exact stack traces for the 3 broken scripts.
  </done>
</task>

<task type="auto">
  <name>Audit audit_project_integrity.py gaps and GSD harness validator scripts</name>
  <files>
    .gsd/phases/2/evidence/03_integrity_script_and_validators_gap_audit.md
    .gsd/phases/2/3-SUMMARY.md
  </files>
  <action>
    Audit `scripts/audit_project_integrity.py` for structural omission and tolerance gaps, and inspect GSD harness validator scripts (`scripts/validate-all.ps1`) for CWD fragility and line-ending defects.

    Steps:
    1. Execute `python scripts/audit_project_integrity.py` under Python 3.15.1 and record output (`ALL CHECKS PASSED`).
    2. Perform an exhaustive line-by-line audit of `scripts/audit_project_integrity.py`:
       - Omitted Modules: Docstring (lines 4-10) promises 8 audit modules, but code jumps from `[MODULE 1]` (line 28) -> `[MODULE 4]` (line 54) -> `[MODULE 5 & 6]` (line 77) -> `[MODULE 8]` (line 172). Modules 2 (Gold Set Agreement & Independence), 3 (ML/DL Predictions & Table 2 Accuracies), and 7 (Spring 2024 App-Version Counterfactual Telemetry) are completely absent.
       - Module 1 data quality gaps: Line 36 error message still says `"Expected 655670 rows"`. The script never checks `isna()`, duplicate `review_id` values, `all_operators_classified_global.csv` (`661,160`), or summary JSON files.
       - Module 4 tolerance: Line 65 uses loose tolerance `atol=0.05` (`assert np.isclose(nss, 53.05, atol=0.05)` passes while Banglalink NSS is 53.04%).
       - Module 5 missing econometric assertions: Never validates `N >= 30` CLT volume floor, consecutive-month continuity (`month_diff == 1`), RMSSD, or early era (`2016-08..2019-12`).
       - Module 8 weakened checks: `update_audit_integrity.py:18-27` swapped `'Jashore'` -> `'Leading University'` (no longer checking Jashore leaks in `manuscript.tex`), dropped `<= 20 pages` check despite docstring, checks only `manuscript.tex` (ignoring `manuscript_twocolumn.tex`, `title_page.tex`, `highlights.txt`, `references.bib`), and only verifies `os.path.exists` on `paper/manuscript*.pdf`.
    3. Execute `powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1` from repository root and record output (`5/5 passed`).
    4. Audit GSD harness validator scripts:
       - CWD fragility: `validate-workflows.ps1:13`, `validate-skills.ps1:13`, `validate-agents.ps1:12`, and `validate-templates.ps1:13` use working-directory-relative paths (`.agent/`, `.agents/`, `.gsd/`) rather than `$PSScriptRoot/..`, causing failure if invoked from another working directory.
       - Untested `.sh` line endings: `validate-encoding.ps1:16` inspects only `*.ps1`. Inspect bytes of all 8 `.sh` scripts (`search_repo.sh`, `setup_search.sh`, `validate-*.sh`) and prove they have CRLF (`\r\n`) line endings that break when run under POSIX `bash`.
       - Shallow schema regexes: `validate-skills.ps1:37,44` uses unanchored substring searches; `validate-agents.ps1:61-67` checks legacy aliases (`view_file`, `write_to_file`).
       - Missing scope: `validate-all.ps1` validates only validator harnesses; it does not check `.gsd/` project files (`SPEC.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `DECISIONS.md`, `STATE.md`) or Python test coverage.
    5. Write findings to `.gsd/phases/2/evidence/03_integrity_script_and_validators_gap_audit.md` and synthesize the overall Phase 2 summary in `.gsd/phases/2/3-SUMMARY.md`.

    AVOID: Running mutating scripts `scripts/update_audit_integrity.py` or `scripts/patch_audit_integrity.py`.
    USE: Read-only Python AST inspection, binary byte inspection for line endings, and PowerShell harness execution.
  </action>
  <verify>
    powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1
  </verify>
  <done>
    audit_project_integrity.py executed and its 5 structural omission gaps documented; validate-all.ps1 executed and its 4 harness fragility gaps documented in 03_integrity_script_and_validators_gap_audit.md and 3-SUMMARY.md.
  </done>
</task>

</tasks>

<verification>
After all tasks, verify:
- [ ] Evidence document `03_scripts_classification_and_execution_audit.md` details classification of all 88 scripts and runtime logs of safe scripts
- [ ] Evidence document `03_integrity_script_and_validators_gap_audit.md` details omission gaps in audit_project_integrity.py and harness fragility in validate-all.ps1
- [ ] Summary file `3-SUMMARY.md` is complete with all observed discrepancies
</verification>

<success_criteria>
- [ ] All 2 tasks verified passing
- [ ] Must-haves confirmed
- [ ] Zero project source or paper files modified outside `.gsd/`
- [ ] Zero git commits created
</success_criteria>
