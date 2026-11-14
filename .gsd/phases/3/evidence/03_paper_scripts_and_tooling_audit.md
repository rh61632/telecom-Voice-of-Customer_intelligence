# Evidence 03: Paper Scripts and Tooling Integrity Audit

**Audit Date:** 2026-11-11  
**Milestone:** Project & Paper Discrepancy Audit (v1.0.0)  
**Phase:** 3 — Research Paper & Cross-Venue Deliverables Audit  
**Plan:** 3.3 — Task 2  
**Governance:** `ADR-001` (Strictly read-only outside `.gsd/`; zero git commits; zero mutating scripts) & `ADR-002` (Sequential execution in `inherit` workspace)

---

## 1. Executive Summary

This empirical audit analyzes all 32 paper-related scripts located in `scripts/`, evaluating their operational viability, target deliverables, error modes, and alignment with current paper artifacts (`paper/eswa_latex/`, `paper/telecommunications_policy_latex/`, `paper/figures/`, and `paper/*.html`).

### Script Classification Overview
All 32 analyzed scripts fall into three distinct operational failure or obsolescence categories:
- **Group 1: Broken Scripts Targeting Deleted Directories or Missing Dependencies (18 scripts):**
  - 3 read-only audit scripts that crash immediately upon execution (`FileNotFoundError`, `PackageNotFoundError`).
  - 12 mutating patcher/builder scripts targeting the deleted directory `paper/journal_manuscript/`.
  - 1 metadata script (`update_audit_integrity.py`) referencing deleted blinded manuscript paths.
  - 2 obsolete `.docx` manuscript builders targeting untracked Word deliverables.
- **Group 2: Broken Visual Crop & Offset Helpers (4 scripts):**
  - Targeting non-existent intermediate check crops in `paper/figures/` (`crop_*_check.png`).
- **Group 3: Stale, Desynchronized, or Self-Contradictory Tooling (10 scripts):**
  - Pipeline scripts that actively inject corrupted numbers ($N = 4,499$, Table 3 arithmetic typos, overlapping 134M eras, phantom shocks).
  - Verification scripts hardcoding obsolete assertions (`3,716 days`, `88,184` reviews, `Expected 655670 rows`).
  - Figure builders with missing target directories (`eswa_latex/figures/` omission) and visual title collisions.

---

## 2. Group 1: Broken Scripts Targeting Deleted Artifacts (18 Scripts)

### 2.1 Read-Only Auditors That Crash Immediately (3 Scripts)
Executing these read-only inspection scripts fails with zero exit code compliance due to deleted repository dependencies:

```powershell
# Stack traces captured during empirical audit:
python scripts/audit_check.py
# FileNotFoundError: [Errno 2] No such file or directory: 'paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex'

python scripts/audit_docx.py
# docx.opc.exceptions.PackageNotFoundError: Package not found at 'paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx'

python scripts/find_tables.py
# docx.opc.exceptions.PackageNotFoundError: Package not found at 'paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx'
```

### 2.2 Complete Group 1 Inventory Table
| Script Path | Operational Status | Target Dependency / Path | Exact Failure Mode / Issue |
|---|---|---|---|
| `scripts/audit_check.py` | Broken (Crashes) | `paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex` | `FileNotFoundError`: attempts to read legacy JBA LaTeX manuscript deleted in earlier cleanup. |
| `scripts/audit_docx.py` | Broken (Crashes) | `paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx` | `PackageNotFoundError`: attempts to open non-existent `.docx` file using `python-docx`. |
| `scripts/find_tables.py` | Broken (Crashes) | `paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx` | `PackageNotFoundError`: attempts to parse tables inside deleted `.docx` deliverable. |
| `scripts/apply_fixes.py` | Broken (Target Missing) | `paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex` | Mutating script regex-replacing text in deleted JBA manuscript file. |
| `scripts/apply_jba_revisions.py` | Broken (Target Missing) | `paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex` | Mutating script injecting reviewer revisions into deleted JBA manuscript. |
| `scripts/apply_peer_review_fixes.py` | Broken (Target Missing) | `paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex` | Mutating script applying peer review revisions to deleted JBA manuscript. |
| `scripts/apply_reviewer_fixes_latex.py` | Broken (Target Missing) | `paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex` | Mutating script applying table and prose fixes to deleted JBA manuscript. |
| `scripts/build_jba_full_manuscript.py` | Broken (Target Missing) | `paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx` | Mutating builder compiling multi-section `.docx` manuscript targeting deleted JBA format. |
| `scripts/build_jba_submission_docx.py` | Broken (Target Missing) | `paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx` | Mutating builder compiling submission-ready `.docx` targeting deleted JBA format. |
| `scripts/convert_latex_to_docx.py` | Broken (Target Missing) | `paper/journal_manuscript/` | Mutating script converting LaTeX files in deleted `paper/journal_manuscript/` into Word documents. |
| `scripts/generate_jba_latex.py` | Broken (Target Missing) | `paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex` | Mutating builder writing LaTeX manuscript directly into deleted directory `paper/journal_manuscript/`. |
| `scripts/sync_latex_jba.py` | Broken (Target Missing) | `paper/journal_manuscript/` | Mutating synchronization script comparing tables between `.docx` and deleted `paper/journal_manuscript/`. |
| `scripts/test_float.py` | Broken (Target Missing) | `paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex` | Mutating test script adjusting float positions in deleted JBA manuscript. |
| `scripts/test_width.py` | Broken (Target Missing) | `paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex` | Mutating test script adjusting column widths in deleted JBA manuscript. |
| `scripts/update_fig_caption.py` | Broken (Target Missing) | `paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex` | Mutating script updating caption strings in deleted JBA manuscript. |
| `scripts/update_audit_integrity.py` | Stale / Misaligned | `paper/journal_manuscript/..._Blinded.tex` | Script hardcodes search strings targeting `paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript_Blinded.tex` to patch `scripts/audit_project_integrity.py`. |
| `scripts/build_paper_docx.py` | Obsolete / Conflicted | `paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx` | Generates obsolete Word manuscript; line 208 hardcodes stale `"3,716-day window"` alongside updated `"655,649"`. |
| `scripts/build_concise_paper_docx.py`| Obsolete / Target Missing | `paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx` | Generates 20-page concise Word manuscript for JBA; deliverable is untracked and unused. |

---

## 3. Group 2: Broken Visual Crop & Offset Helpers (4 Scripts)

During iterative figure optimization for Figure 1, four helper scripts were authored to inspect crop coordinates for milestone callout boxes. All four scripts target temporary PNG files that were discarded:

| Script Path | Operational Status | Target Dependencies | Exact Issue / Failure Mechanism |
|---|---|---|---|
| `scripts/check_crop.py` | Broken (Target Missing) | `paper/figures/crop_4g_check.png` | Attempts to crop and display `crop_4g_check.png`; file does not exist on disk. |
| `scripts/check_crop_wide.py` | Broken (Target Missing) | `paper/figures/crop_4g_check_wide.png` | Attempts to crop and display `crop_4g_check_wide.png`; file does not exist on disk. |
| `scripts/check_other_crops.py` | Broken (Target Missing) | `paper/figures/crop_5g_check.png`, `crop_bl_check.png`, `crop_covid_check.png` | Attempts to crop and inspect 5G, BL crash, and COVID callouts from intermediate check files; all 3 target PNGs are missing. |
| `scripts/test_figure1_offsets.py` | Broken (Target Missing) | `paper/figures/crop_*_check.png` | Test suite evaluating bounding box offsets across the four intermediate crop check PNGs; targets missing. |

---

## 4. Group 3: Stale, Desynchronized, or Self-Contradictory Tooling (10 Scripts)

### 4.1 Detailed Inventory Table
| Script Path | Primary Role | Status / Category | Exact Issue / Contradiction |
|---|---|---|---|
| `scripts/build_full_eswa_paper.py` | Table & Section Generator | Active Bug Vector | Actively introduces corrupted tables: defines $N = 4,499$ in Table 1–4, Table 3 arithmetic typo ($\mathcal{C}_1$ Precision $0.9528$), Table 5 overlapping 134M eras and fabricated NSS, Table 6 fabricated shock rows. |
| `scripts/reconstruct_master_manuscript.py` | Master Pipeline Rebuilder | Active Drift Vector | Spliced corrupted tables from `build_full_eswa_paper.py` into older base files (`manuscript_base_1506.tex`) while silently failing 100% of its four `.replace()` prose updates, creating deep internal manuscript contradictions. |
| `scripts/rebuild_figure3.py` | Figure 3 Visual Generator | Directory Omission | Lines 179–180 save to `paper/figures/` and `paper/telecommunications_policy_latex/figures/`, completely omitting `paper/eswa_latex/figures/`. |
| `scripts/generate_paper_figures.py` | Master Figure Suite Builder | Visual & Directory Defect | Writes only to `paper/figures/` (not `eswa_latex/figures/`); bakes hardcoded titles `"Figure 1:"` through `"Figure 4:"` directly into raster PNGs (causing off-by-one with LaTeX Figure 1); line 346 tight layout clips title. |
| `scripts/verify_paper_complete.py` | Paper Verification Auditor | Stale Assertions | Line 19 hardcodes assertion for `"3,716 days"` (vs true 3,713 days); line 43 hardcodes assertion for `"88,184"` (vs `manuscript.tex:488` stating $88,181$). |
| `scripts/audit_paper_contradictions.py` | Contradiction Checker | Stale Assertions | Line 23 hardcodes assertion that paper says `"88,184"`, masking the active $88,181$ text count. |
| `scripts/audit_project_integrity.py` | Master Repository Integrity Gate | Incomplete & Misleading | Line 36 error message prints `"Expected 655670 rows"`; inspects only `manuscript.tex` (ignoring `manuscript_twocolumn.tex` and `title_page.tex`); checks only `Leading University` (ignoring `Jashore`); omits page budget assertions. |
| `scripts/check_equations.py` | Equation Auditor | Format Mismatch | Scrapes equation blocks only from `paper/index.html` (`<div class="equation-row">`), completely ignoring active LaTeX equations in `paper/eswa_latex/`. |
| `scripts/fix_table_formatting.py` | Table Formatter | Stale Hardcoding | Hardcodes Table 1 column widths and taxonomy text from legacy drafts, bypassing current `elsarticle` formatting. |
| `scripts/patch_base_tex.py` | Base LaTeX Patcher | Stale Base Targets | Patches computational complexity text directly into `manuscript_base_1506.tex` and `manuscript_twocolumn_base_1508.tex`, leaving active `manuscript.tex` unpatched unless reconstruction is re-run. |

---

## 5. Diagnostic Deep-Dive: The "Green Audit" Mirage

A critical systemic vulnerability revealed by this audit is the existence of self-referential or loose integrity test scripts that produce false assurances of project completeness:

### 5.1 `scripts/audit_project_integrity.py` Line 36 Assertion Error String
```python
# scripts/audit_project_integrity.py:35-37
total_rows = len(df)
assert total_rows == 655649, f"Expected 655670 rows, got {total_rows}"
print(f"  [PASS] Total rows: {total_rows:,}")
```
- While the assertion tests `total_rows == 655649`, the failure message retains the stale pre-sync count of `655670`.
- If an assertion failure occurred, the user would be directed towards an outdated target ($655,670$).

### 5.2 `scripts/audit_project_integrity.py` Lines 173–216 Omissions
```python
# scripts/audit_project_integrity.py:177-180
for term in ['Ratul', 'rh61632', 'Leading University', 'github.com']:
    matches = len(re.findall(re.escape(term), tex_content, re.IGNORECASE))
    assert matches == 0, f"Found {matches} occurrences of prohibited identifier '{term}' in blinded manuscript!"
```
- **Blinded File Omission:** Only `paper/eswa_latex/manuscript.tex` is checked. `manuscript_twocolumn.tex` and `title_page.tex` are uninspected.
- **Affiliation Omission:** Only `Leading University` is checked. `Jashore University` (present in TP and root artifacts) is unmonitored.
- **Page Budget Omission:** Lines 212–216 assert that `paper/manuscript.pdf` and `paper/manuscript_twocolumn.pdf` exist (`os.path.exists`), but **zero page budget assertions exist**.
  - `manuscript.pdf` is **37 pages** (review format ceiling is typically 35 pages).
  - `manuscript_twocolumn.pdf` is **16 pages** (final layout ceiling is 15 pages).
- Despite these uninspected failure modes, line 218 proclaims:
  ```python
  print("AUDIT RESULT: 100% OF EMPIRICAL AND MATHEMATICAL CHECKS PASSED PERFECTLY!")
  ```

### 5.3 `scripts/verify_paper_complete.py` Stale Hardcoded Claims
```python
# scripts/verify_paper_complete.py:19, 43
print(f"Total days: {days} (Paper says: 3,716 days)")
...
print(f"\nTotal in 4 domains: {len(df_4):,} (Paper says: 88,184)")
```
- **3,716 Days:** Both `paper/eswa_latex/manuscript.tex:46` and `paper/telecommunications_policy_latex/manuscript.tex:172` state `3,713 days`. The verification script asserts that the paper says `3,716 days`.
- **88,184 Reviews:** `manuscript.tex:488` explicitly states:
  ```latex
  N = 88{,}181 \text{ functional reviews across the four operational domains}
  ```
  The verification script asserts that the paper says `88,184`, masking a 3-review divergence between text and data.

---

## 6. Recommendations for Downstream Remediation (Phase 4 / Post-Audit)

1. **Retire or Archive Broken Scripts:**
   - Move the 18 broken scripts in Group 1 to an `archive/legacy_scripts/` directory or delete them to eliminate repository clutter and confusing crash traces.
2. **Harmonize Verification Assertions:**
   - Update `verify_paper_complete.py` and `audit_paper_contradictions.py` to assert verified ground truth (`3,713 days` and verified domain review counts).
   - Fix `audit_project_integrity.py` line 36 error message to match asserted value ($655,649$).
3. **Synchronize Figure Target Paths:**
   - Update `scripts/rebuild_figure3.py` and `scripts/generate_paper_figures.py` to write atomically to all active manuscript directories (`paper/figures/`, `paper/eswa_latex/figures/`, and `paper/telecommunications_policy_latex/figures/`).
4. **Implement Page-Budget Verification:**
   - Add explicit `pdfinfo` page count assertions in `audit_project_integrity.py` to ensure submitted manuscripts respect journal length constraints.
