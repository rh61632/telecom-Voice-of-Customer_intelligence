# Evidence 03B: Project Integrity Script & GSD Harness Validators Gap Audit

**Audited At:** 2026-11-11  
**Environment:** Python 3.15.1, PowerShell 5.1 (Windows 11 AMD64)  
**Constraint Reference:** `ADR-001` (Read-Only Audit, Zero Project Mutations, Zero Git Commits) & `ADR-002` (Sequential Inherit Workspace)  

---

## 1. Executive Summary

This empirical audit investigates the automated validation infrastructure of the project across two tiers:
1. **The Project Domain Integrity Auditor** (`scripts/audit_project_integrity.py`): Advertised as verifying 8 academic and empirical modules, it currently displays a superficial `ALL CHECKS PASSED` status while **completely omitting 3 entire modules (Modules 2, 3, and 7)**, applying loose numerical tolerances (`atol=0.05`), overlooking basic data hygiene checks (nulls, duplicates, unclassified reviews), and dropping paper page budget verifications.
2. **The GSD Harness Validators** (`scripts/validate-all.ps1` and child scripts): While reporting `5/5 passed` when run from the repository root, the harness suffers from **Current Working Directory (CWD) fragility** (yielding silent false-positive passes when invoked from subdirectories), ignores all **8 `.sh` bash scripts** which possess invalid **CRLF (`\r\n`)** line endings breaking POSIX environments, uses **unanchored substring regexes**, and possesses **zero test coverage over codebase source files or `.gsd/` project artifacts**.

---

## 2. Empirical Execution of `scripts/audit_project_integrity.py`

### 2.1 Live Execution Log
```powershell
PS C:\Users\user\Ratul\project\telecom-Voice-of-Customer_intelligence> python scripts/audit_project_integrity.py
================================================================================
TELECOM VOC INTELLIGENCE: NEUTRAL PROJECT INTEGRITY AUDIT
================================================================================

[MODULE 1] Verifying Data Provenance, Counts & Deduplication...
  [PASS] Total rows: 655,649
  [PASS] Operator breakdown: GP=320,140, Robi=198,378, BL=137,131
  [PASS] Synchronized Date Window: 2016-08-01 to 2026-09-30

[MODULE 4] Verifying Mathematical Invariants of NSS & Additive Decomposition...
  [PASS] Banglalink      N=137,131 Pos=70.4% Neg=17.3% NSS=+53.04%
  [PASS] Grameenphone    N=320,140 Pos=77.0% Neg=12.1% NSS=+64.85%
  [PASS] Robi            N=198,378 Pos=77.9% Neg=12.0% NSS=+65.91%
  [PASS] All Operators:   N=655,649 Pos=75.9% Neg=13.2% NSS=+62.70%

[MODULE 5 & 6] Verifying Transitions, Shocks, and Non-Shock Login Counts...
  [PASS] Modern transitions evaluated: 240 (80 per operator)
  [PASS] Shocks identified (|ΔNSS| >= 10.0): 35 (GP=6, Robi=7, BL=22)
  [PASS] Non-shock login leading counts: GP=30/74, Robi=32/73, BL=29/58 => SUM = 91/205 (44.4%)
  [PASS] Corrected Pooled Chi-Square: chi2=12.83 (p=0.0003), Fisher OR=4.23 (p=0.0004)

[MODULE 8] Verifying Double-Blind Anonymity, Section Completeness & Deliverables...
  [PASS] Anonymity check: 0 occurrences of author name, email, institution, or GitHub repo URL.
  [PASS] Manuscript completeness: All 8 core academic sections verified present.
  [PASS] Structural artifacts: All 8 key tables, algorithms, and matrices verified present.
  [PASS] Final deliverables generated: manuscript.pdf and manuscript_twocolumn.pdf both verified.

================================================================================
AUDIT RESULT: 100% OF EMPIRICAL AND MATHEMATICAL CHECKS PASSED PERFECTLY!
================================================================================
```

---

## 3. Exhaustive Line-by-Line Gap Analysis of `scripts/audit_project_integrity.py`

### 3.1 Structural Module Omissions (Modules 2, 3, and 7 Missing)
The script docstring explicitly outlines eight core audit modules:
```python
# scripts/audit_project_integrity.py:3-12
"""
Comprehensive neutral audit script executing automated sanity checks across all 8 modules:
1. Data integrity (counts, dates, nulls, duplicates)
2. Gold set agreement and independence
3. Classification model predictions and Table 2 accuracy
4. Exact mathematical identities of NSS and Additive Decomposition
5. Time series aggregation and RMSSD volume filtering
6. Proposition 1 and Proposition 2 statistical tests
7. Spring 2024 counterfactual telemetry
8. Anonymity verification and Word/PDF page limits
"""
```
However, code inspection reveals that the implementation jumps directly:
- `Line 28`: `[MODULE 1] Verifying Data Provenance, Counts & Deduplication...`
- `Line 54`: `[MODULE 4] Verifying Mathematical Invariants of NSS & Additive Decomposition...`
- `Line 77`: `[MODULE 5 & 6] Verifying Transitions, Shocks, and Non-Shock Login Counts...`
- `Line 172`: `[MODULE 8] Verifying Double-Blind Anonymity, Section Completeness & Deliverables...`

**The following modules are completely absent from code:**
1. **Module 2 (Gold Set Agreement & Independence):** Zero assertions for inter-annotator agreement (Cohen's Kappa $\kappa = 0.5762$ sentiment, $\kappa = 0.7694$ category), zero checks for train/gold overlap leakage, and zero validation of `data/gold_set/` files.
2. **Module 3 (ML/DL Predictions & Table 2 Accuracies):** Zero validation of model predictions, zero verification of model accuracy or macro-F1 against reported Table 2 benchmarks, and zero checks that model joblib checkpoints exist or deserialize properly.
3. **Module 7 (Spring 2024 App-Version Counterfactual Telemetry):** Zero checks on app version distributions (e.g., Banglalink v11.11.0 vs legacy builds), unversioned review proportion (24.9%), or counterfactual NSS calculations.

### 3.2 Data Hygiene & Assertion Gaps in Module 1
1. **Stale Error Message:**
   ```python
   # Line 36:
   assert total_rows == 655649, f"Expected 655670 rows, got {total_rows}"
   ```
   The error string still references the older pre-deduplication count `655670`, revealing historical assertion drift.
2. **Missing Quality Checks:**
   - Despite claiming to check `"counts, dates, nulls, duplicates"` (`line 4`), the script loads only 6 columns (`usecols=['operator', 'review_date', 'review_id', 'predicted_sentiment', 'predicted_category', 'ym']`) and **never calls `df.isna().sum()` or `df['review_id'].duplicated().any()`**.
   - It verifies only the common duration subset (`scraped_data_global/classified/all_operators_common_duration_classified.csv`, `655,649`), completely ignoring the full corpus (`all_operators_classified_global.csv`, `661,160` rows) and the summary JSON files (`common_duration_summary.json`).

### 3.3 Loose Numerical Tolerances in Module 4
In Module 4 (`lines 60-66`):
```python
if op == 'Grameenphone':
    assert np.isclose(nss, 64.85, atol=0.05)
elif op == 'Robi':
    assert np.isclose(nss, 65.91, atol=0.05)
elif op == 'Banglalink':
    assert np.isclose(nss, 53.05, atol=0.05)
```
- Line 65 tests `Banglalink` against target `53.05` with `atol=0.05`. Because actual Banglalink NSS is `53.040523%` (`53.04%`), this loose tolerance hides the `0.01 pp` discrepancy between script target `53.05%` and true value `53.04%`.

### 3.4 Missing Econometric and Time Series Assertions in Modules 5 & 6
1. **No CLT Volume Floor Check:** The script aggregates monthly groups without asserting that each month satisfies the Central Limit Theorem sample size floor ($N \ge 30$).
2. **No Consecutive-Month Continuity Check:** Transition differences (`d_nss = curr['nss'] - prev['nss']`) are computed strictly by row index (`iloc[i] - iloc[i-1]`) without verifying that `year_month` differences equal exactly 1 month (`month_diff == 1`). If a month were missing from the sequence, it would silently calculate a jump across non-consecutive periods.
3. **Missing Volatility Metrics:** The script never computes or verifies RMSSD (Root Mean Square of Successive Differences) or SSI (Sentiment Stability Index), despite docstring claim `"5. Time series aggregation and RMSSD volume filtering"`.
4. **Omission of Early Historical Window:** Line 78 filters `df[(df['ym'] >= '2020-01') & (df['ym'] <= '2026-09')]`, omitting the historical era from August 2016 through December 2019 (`41 months`), meaning only 240 of 345 valid monthly transitions are audited.

### 3.5 Weakened Verification and Patch Artifacts in Module 8
1. **Weakened Anonymity Inspection:**
   `scripts/update_audit_integrity.py` (`lines 18-21`) patched Module 8 to swap `'Jashore'` for `'Leading University'`. Consequently, any textual leakage referencing Jashore University of Science and Technology (the author's actual prior affiliation) in `paper/eswa_latex/manuscript.tex` is no longer flagged!
2. **Missing Page Budget Verification:**
   Docstring line 11 explicitly promises `"Word/PDF page limits"` verification (such as the ESWA 20-page or JBA page budget). In the code, zero page counting commands exist.
3. **Single File LaTeX Scope:**
   Module 8 inspects only `paper/eswa_latex/manuscript.tex`. It does not inspect:
   - `paper/eswa_latex/manuscript_twocolumn.tex`
   - `paper/eswa_latex/title_page.tex`
   - `paper/eswa_latex/highlights.txt`
   - `paper/eswa_latex/references.bib`
   - `paper/html/index.html`
4. **Shallow Deliverable Assertion:**
   Lines 212-216 perform only an `os.path.exists()` check on `paper/manuscript.pdf` and `paper/manuscript_twocolumn.pdf`. They do not check file sizes, page counts, build timestamps, or whether the PDFs are non-empty valid documents.

---

## 4. Empirical Audit of GSD Harness Validators (`scripts/validate-all.ps1`)

### 4.1 Master Harness Execution Log
Execution from repo root:
```powershell
PS C:\Users\user\Ratul\project\telecom-Voice-of-Customer_intelligence> powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1
╔═══════════════════════════════════════════════════════╗
║         GSD ► RUNNING ALL VALIDATORS                  ║
╚═══════════════════════════════════════════════════════╝
▶ Running workflow validation... (27 workflows checked, 0 errors)
▶ Running skill validation... (12 skills checked, 0 errors)
▶ Running subagent validation... (5 subagents checked, 0 errors)
▶ Running template validation... (24 templates checked, 0 errors)
▶ Running script encoding validation... (11 scripts checked, 0 errors)
╔═══════════════════════════════════════════════════════╗
║                    SUMMARY                            ║
╚═══════════════════════════════════════════════════════╝
✅ All validators passed!
```

### 4.2 Structural Flaws Identified in Validator Scripts

#### Flaw 1: Current Working Directory (CWD) Fragility & False-Positive Passes
`validate-workflows.ps1:13`, `validate-skills.ps1:13`, `validate-agents.ps1:12`, and `validate-templates.ps1:13` use paths relative to the current working directory (`.agent/...`, `.agents/...`, `.gsd/...`) instead of resolving against `$PSScriptRoot/..`.

**Empirical Proof of Silent Failure:**
When invoked from within the `scripts/` directory:
```powershell
PS C:\Users\user\Ratul\project\telecom-Voice-of-Customer_intelligence> Set-Location scripts; .\validate-skills.ps1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GSD ► VALIDATING SKILLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Get-ChildItem : Cannot find path 'C:\...\scripts\.agents\skills' because it does not exist.
───────────────────────────────────────────────────────
Skills checked: 0
Errors: 0

✅ All skills valid!
```
The script throws a PowerShell non-terminating path error, loops over 0 items, and outputs:
`✅ All skills valid!` with exit code `0`. This creates a hazardous false sense of security.

#### Flaw 2: Untested `.sh` Line Endings (CRLF Defect)
`scripts/validate-encoding.ps1:16` inspects only PowerShell scripts:
```powershell
$scripts = Get-ChildItem $PSScriptRoot -Filter "*.ps1" -File | Sort-Object Name
```
It completely ignores all shell scripts. Binary inspection of all 8 `.sh` scripts in `scripts/` reveals:

| Script Name | CRLF Count (`\r\n`) | LF Count (`\n`) | Line Ending Status |
|---|---|---|---|
| `scripts/search_repo.sh` | 58 | 0 | ❌ 100% CRLF (Breaks POSIX) |
| `scripts/setup_search.sh` | 103 | 0 | ❌ 100% CRLF (Breaks POSIX) |
| `scripts/validate-agents.sh` | 115 | 0 | ❌ 100% CRLF (Breaks POSIX) |
| `scripts/validate-all.sh` | 56 | 0 | ❌ 100% CRLF (Breaks POSIX) |
| `scripts/validate-encoding.sh` | 56 | 0 | ❌ 100% CRLF (Breaks POSIX) |
| `scripts/validate-skills.sh` | 65 | 0 | ❌ 100% CRLF (Breaks POSIX) |
| `scripts/validate-templates.sh` | 58 | 0 | ❌ 100% CRLF (Breaks POSIX) |
| `scripts/validate-workflows.sh` | 58 | 0 | ❌ 100% CRLF (Breaks POSIX) |

Every `.sh` script has pure Windows `\r\n` line endings. If executed in a Linux, macOS, or CI/CD bash shell, the carriage return will cause syntax errors (`\r: command not found`).

#### Flaw 3: Shallow Unanchored Regexes and Legacy Tool Aliases
1. **Unanchored Substring Matching in `validate-skills.ps1`:**
   ```powershell
   # lines 37, 44:
   if ($content -notmatch "name:") { ... }
   if ($content -notmatch "description:") { ... }
   ```
   These regexes match the substring anywhere in the markdown file (including comments, prose, or code blocks) rather than parsing structured YAML frontmatter between `---` boundaries.
2. **Outdated Tool List in `validate-agents.ps1`:**
   ```powershell
   # lines 61-67:
   $knownTools = @(
       "view_file", "write_to_file", "replace_file_content", "multi_replace_file_content",
       "list_dir", "find_by_name", "grep_search", "search_web", "read_url_content", ...
   )
   ```
   `validate-agents.ps1` validates subagent YAML tool references against legacy tool names rather than the active native Antigravity tool standard (`read_file`, `write_file`, `edit_file`, `run_command`, `send_message`, `manage_task`).

#### Flaw 4: Missing Scope Over Project Codebase and `.gsd/` State
`validate-all.ps1` is strictly an agent-framework harness validator. It does **not** validate:
- Project state documents (`.gsd/SPEC.md`, `.gsd/REQUIREMENTS.md`, `.gsd/ROADMAP.md`, `.gsd/STATE.md`).
- Project Python code syntax, imports, or linters.
- Python unit test coverage (there are **0 unit tests** in the entire repository; no `tests/` directory exists).

---

## 5. Summary of Discrepancies Cataloged

| ID | Component | Type | Severity | Description |
|---|---|---|---|---|
| **GAP-01** | `audit_project_integrity.py` | Structural Omission | High | Modules 2 (Gold Set), 3 (Model Predictions), and 7 (Version Telemetry) are completely missing from execution. |
| **GAP-02** | `audit_project_integrity.py` | Data Validation | Medium | Never checks for nulls, duplicated `review_id` values, or the full 661,160-row global dataset. |
| **GAP-03** | `audit_project_integrity.py` | Assertion Drift | Low | Line 36 error string still claims `"Expected 655670 rows"`. Line 65 uses loose `atol=0.05` for Banglalink NSS. |
| **GAP-04** | `audit_project_integrity.py` | Econometric Logic | Medium | Lacks $N \ge 30$ CLT volume floor check and consecutive-month continuity checks; ignores 2016-2019 era. |
| **GAP-05** | `audit_project_integrity.py` | Verification Weakening | Medium | Swapped Jashore check to Leading University; dropped page budget assertions; checks only single LaTeX file. |
| **GAP-06** | `validate-*.ps1` | Harness Fragility | Medium | All child validators use CWD-relative paths, causing silent false-positive passes when run outside root. |
| **GAP-07** | `validate-*.sh` | Portability Defect | Medium | All 8 `.sh` scripts have pure Windows CRLF (`\r\n`) endings that fail under POSIX bash. |
| **GAP-08** | `validate-skills.ps1` | Shallow Parsing | Low | Uses unanchored substring regexes rather than parsing YAML frontmatter. |
| **GAP-09** | `validate-all.ps1` | Scope Blindspot | Low | Harness validates only agent definitions; repository has zero unit test runner or Python source linting. |

---

## 6. Verification Checklist

- [x] Executed `python scripts/audit_project_integrity.py` and captured execution log.
- [x] Documented all 5 major structural and assertion gaps in `scripts/audit_project_integrity.py`.
- [x] Executed `powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1` from root.
- [x] Empirically demonstrated CWD failure and false-positive pass of `validate-skills.ps1` in subfolder.
- [x] Inspected raw byte encodings of all 8 `.sh` scripts and proved CRLF defect.
- [x] Documented shallow regexes, legacy tool aliases, and test coverage omissions.
