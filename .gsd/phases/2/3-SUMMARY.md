# Phase 2 Plan 3 Summary: Scripts Classification, Empirical/Audit Execution & Validator Gap Audit

**Phase:** 2 - ML/DL Models, Gold Standard & Empirical Audit Scripts  
**Plan:** 3 of 3 (`3-PLAN.md`)  
**Completed At:** 2026-11-11  
**Execution Mode:** Autonomous Subagent (`gsd-executor`), Workspace `inherit`  
**Constraint Reference:** `ADR-001` (Strictly Read-Only on project/paper/data files outside `.gsd/`; Zero Git Commits)  

---

## 1. Executive Summary

Plan 2.3 conducted an exhaustive classification and runtime audit of all 88 scripts in `scripts/`, executed safe read-only empirical/econometric scripts under Python 3.15.1, performed an in-depth line-by-line omission audit of `scripts/audit_project_integrity.py`, and evaluated the GSD harness validator scripts (`scripts/validate-all.ps1`) for CWD fragility and line-ending defects.

All safe scripts were empirically benchmarked, capturing exact execution times and statistical outputs. All mutating scripts (42 files) were quarantined under `ADR-001`. Multiple structural gaps in the project's self-audit script and harness validators were uncovered and empirically proven.

---

## 2. Key Accomplishments & Empirical Findings

### Task 1: Complete Scripts Inventory & Empirical Execution
- **88 Total Scripts Classified:**
  - **Group 1: 27 Read-Only Python Scripts:**
    - 14 executed and verified passing (`rc=0`) with runtimes ranging from 0.08s to 9.79s.
    - 3 broken scripts documented (`rc=1`): `audit_check.py` (`FileNotFoundError` on `paper/journal_manuscript/...`), `audit_docx.py` (`PackageNotFoundError`), and `find_tables.py` (`PackageNotFoundError`).
    - 10 verified read-only by AST inspection (econometric/paper validation logic).
  - **Group 2: 19 Read-Only Shell/PowerShell Scripts:**
    - 12 GSD validator scripts (`validate-*.ps1` / `validate-*.sh`).
    - 4 search helpers (`search_repo.*`, `setup_search.*`).
    - 3 Word COM page counters (`check_exact_pages.ps1`, `check_pages.ps1`, `check_last_pages.ps1`).
  - **Group 3: 42 File-Mutating Python Scripts Quarantined:**
    - 26 LaTeX/DOCX/HTML builders, 8 figure generators, 4 script patchers, 3 dataset/report writers, and 1 Hugging Face uploader (`upload_to_huggingface.py`).
- **Empirical Runtimes and Metrics Captured:**
  - `audit_thresholds.py` (5.79s): Confirmed 35 shocks specific to `|ΔNSS| >= 10.0` under Ensemble model.
  - `check_version_bias.py` (5.91s): Versioned reviews report +10.96 pp higher NSS than unversioned reviews; unversioned reviews dominate BL Spring 2024 (2,886 vs 1,787).
  - `audit_point1.py` (4.80s): Point 1 non-surge Fisher exact test validated: OR = 3.65 ($p = 0.0150$), $\chi^2 = 6.38$ ($p = 0.0116$).
  - `reconcile_empirical_numbers.py` (5.04s): NSS bootstrap 95% CIs: GP 64.85%, Robi 65.91%, BL 53.04%.
  - `analyze_surges.py` (4.80s): General/Other contributions strongly predicted by volume change ($R^2 = 0.5601$, $p = 2.35 \times 10^{-7}$).
  - `point4_prop2_by_operator.py` (6.24s): Uncovered operator asymmetry: Proposition 2 significance is driven by Banglalink (Non-surge Fisher OR = 11.41, $p = 0.0088$), while GP ($p = 1.0000$) and Robi ($p = 1.0000$) show no significant login concentration during shocks.
  - `print_table6_rows.py` (9.79s) & `run_p4.py` (8.21s): Decomposed all 35 shocks for Table 6; Chi-square goodness-of-fit $\chi^2 = 51.97$ ($p = 3.04 \times 10^{-11}$).
  - `verify_html.py` (0.08s): True prose count is 3,843 words, exceeding 3,200 guideline target by 643 words (+20.1%).

### Task 2: Project Integrity Script & GSD Validator Gap Audit
- **`scripts/audit_project_integrity.py` Structural Gaps:**
  - **Omitted Modules:** Docstring promises 8 modules, but code executes only Modules 1, 4, 5 & 6, and 8. **Modules 2 (Gold Set), 3 (Model Predictions), and 7 (Version Telemetry) are completely absent.**
  - **Data Hygiene Blindspots:** Module 1 never checks `isna()`, duplicate `review_id` values, or the 661k global dataset; line 36 error message still says `"Expected 655670 rows"`.
  - **Loose Tolerance:** Module 4 uses `atol=0.05` on NSS checks, masking the discrepancy between 53.05% and true 53.04%.
  - **Missing Econometric Floors:** Modules 5 & 6 lack $N \ge 30$ CLT volume floor checks, lack consecutive-month continuity checks, never calculate RMSSD/SSI, and omit the entire 2016-2019 window.
  - **Weakened Anonymity & Deliverable Checks:** Module 8 swapped Jashore check to Leading University (ignoring actual author affiliation leaks), dropped page budget assertions, inspects only a single LaTeX file, and performs only a shallow `os.path.exists()` check on PDFs.
- **`scripts/validate-all.ps1` Harness Fragility:**
  - **CWD Fragility:** Child validators use working-directory-relative paths. When run from `scripts/`, `validate-skills.ps1` fails to find `.agents/skills`, checks 0 skills, and prints `✅ All skills valid!` with exit code 0.
  - **CRLF in `.sh` Scripts:** `validate-encoding.ps1` checks only `*.ps1`. All 8 `.sh` bash scripts contain pure Windows CRLF (`\r\n`) line endings, which cause syntax errors in POSIX bash environments.
  - **Shallow Regexes:** `validate-skills.ps1` uses unanchored substring searches matching anywhere in markdown text.
  - **Legacy Tool Aliases:** `validate-agents.ps1` checks obsolete tool names (`view_file`, `write_to_file`) rather than active native Antigravity tools.

---

## 3. Discrepancy Catalog Updates (Phase 2 Plan 3)

| Discrepancy ID | File / Component | Category | Severity | Summary |
|---|---|---|---|---|
| **DISC-P2-22** | `scripts/audit_check.py` | Stale Path | Medium | Fails with `FileNotFoundError` looking for deleted `paper/journal_manuscript/...tex`. |
| **DISC-P2-23** | `scripts/audit_docx.py`, `find_tables.py` | Stale Path | Medium | Fail with `PackageNotFoundError` looking for missing `paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx`. |
| **DISC-P2-24** | `scripts/audit_project_integrity.py` | Structural Omission | High | Docstring advertises 8 modules, but Modules 2, 3, and 7 are completely absent from code. |
| **DISC-P2-25** | `scripts/audit_project_integrity.py:36` | Assertion Drift | Low | Error message states `"Expected 655670 rows"`, inconsistent with `assert total_rows == 655649`. |
| **DISC-P2-26** | `scripts/audit_project_integrity.py:65` | Tolerance Masking | Low | Uses `atol=0.05` to assert Banglalink NSS is 53.05% when empirical value is 53.04%. |
| **DISC-P2-27** | `scripts/audit_project_integrity.py` | Econometric Omission | Medium | Omits $N \ge 30$ CLT volume floor, consecutive-month validation, RMSSD/SSI, and 2016-2019 era. |
| **DISC-P2-28** | `scripts/audit_project_integrity.py:177` | Verification Weakening | Medium | Patched to check Leading University instead of Jashore; dropped page budget checks; inspects only single LaTeX file. |
| **DISC-P2-29** | `scripts/validate-*.ps1` | Harness Fragility | Medium | CWD-relative paths cause silent false-positive pass (`Skills checked: 0, Errors: 0, ✅ All valid`) when run in subdirectories. |
| **DISC-P2-30** | `scripts/*.sh` (8 files) | Line Ending Defect | Medium | All 8 shell scripts have CRLF (`\r\n`) endings that fail under POSIX bash; completely ignored by `validate-encoding.ps1`. |
| **DISC-P2-31** | `scripts/validate-skills.ps1` | Shallow Regex | Low | Uses unanchored substring searches (`name:`, `description:`) rather than parsing YAML frontmatter. |
| **DISC-P2-32** | `scripts/validate-agents.ps1` | Stale Schema | Low | Checks legacy tool names (`view_file`, `write_to_file`) rather than native Antigravity tools. |

---

## 4. Verification Evidence

### Verification Block 1 (Task 1)
```powershell
PS C:\Users\user\Ratul\project\telecom-Voice-of-Customer_intelligence> python scripts/test_table_defs.py
TABLE1_NEW: 2531 chars, labels: ['tab:taxonomy']
TABLE2_NEW: 2281 chars, labels: ['tab:leaderboard']
TABLE3_NEW: 1868 chars, labels: ['tab:perclass']
TABLE4_NEW: 1699 chars, labels: ['tab:linguistic_benchmark']
TABLE5_NEW: 2520 chars, labels: ['tab:eras']
TABLE6_NEW: 2426 chars, labels: ['tab:shocks']
TABLE7_NEW: 2957 chars, labels: ['alg:canary']
TABLE8_NEW: 1980 chars, labels: ['tab:decision_matrix']
# Exit Code: 0
```

### Verification Block 2 (Task 2)
```powershell
PS C:\Users\user\Ratul\project\telecom-Voice-of-Customer_intelligence> powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1
# Output:
# Workflows checked: 27, Errors: 0
# Skills checked: 12, Errors: 0
# Subagents checked: 5, Errors: 0
# Templates checked: 24, Errors: 0
# Scripts checked: 11, Errors: 0
# ✅ All validators passed!
# Exit Code: 0
```

---

## 5. Artifacts Created & Updated

1. `.gsd/phases/2/evidence/03_scripts_classification_and_execution_audit.md` (Detailed inventory of all 88 scripts, runtimes, outputs, stack traces).
2. `.gsd/phases/2/evidence/03_integrity_script_and_validators_gap_audit.md` (Exhaustive line-by-line audit of `audit_project_integrity.py` and `validate-all.ps1`).
3. `.gsd/phases/2/3-SUMMARY.md` (This document).

---

## 6. Constraints Adherence (`ADR-001` & `ADR-002`)
- **Zero Project Code Mutations Outside `.gsd/`:** Confirmed. All code, notebook, paper, model, and data files remain untouched.
- **Zero Git Commits:** Confirmed (`commits: none (ADR-001)`).
- **Single-Command Shell Discipline:** Confirmed. No chained `&&` or `||` operators used.
