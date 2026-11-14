---
phase: 3
verified: 2026-11-11T11:35:00+06:00
status: passed
score: 13/13 must-haves verified
is_re_verification: false
gaps: []
---

# Phase 3 Verification Report: Research Paper & Cross-Venue Deliverables Audit

## 1. Executive Summary

Under **`ADR-001`** (strictly read-only on project, data, model, and paper sources; zero `pdflatex` runs; zero mutating scripts; zero git commits) and **`ADR-002`** (sequential execution in `inherit` workspace), Phase 3 audited all academic manuscript deliverables and paper tooling across `paper/eswa_latex/`, root `paper/*.pdf`, `paper/telecommunications_policy_latex/`, `paper/*.html`, `paper/figures/`, and all 32 paper-related scripts in `scripts/`.

Phase 3 is an **audit milestone**: its objective is to empirically surface, document, and catalog all internal and cross-artifact discrepancies, not to mutate or compile paper files.

Every must-have truth across Plans 3.1, 3.2, and 3.3 was independently re-checked with read-only verification commands. All claims made in `.gsd/phases/3/*-SUMMARY.md` and `.gsd/phases/3/evidence/` were confirmed to be 100% factually accurate, empirically grounded, and complete.

**Verdict:** `status: pass` (13/13 must-haves verified, 0 gaps).

---

## 2. Must-Haves Verification Matrix

### 2.1 Observable Truths

| # | Must-Have Truth | Status | Empirical Evidence |
|---|---|---|---|
| 1 | Byte-for-byte SHA256 parity and page geometry between `paper/*.pdf` and `paper/eswa_latex/*.pdf` verified across manuscript, twocolumn, and title page | ✓ VERIFIED | `manuscript.pdf`: 2,521,538 B, SHA256 `d632c9db...`, 37 pages, US Letter ($612 \times 792$ pt); `manuscript_twocolumn.pdf`: 2,207,623 B, SHA256 `b41b8d7e...`, 16 pages, ISO A4 ($595.276 \times 841.89$ pt); `title_page.pdf`: 110,587 B, SHA256 `5aed323f...`, 2 pages, US Letter ($612 \times 792$ pt). Exact byte parity confirmed. |
| 2 | Build logs (`*.log`) verified for 0 undefined references/citations, severe overfull hbox in twocolumn (Eq 10, 32.0pt), title_page URL overflow (15.6pt), and Table underfull badness | ✓ VERIFIED | 0 undefined references / citations across all 3 logs. `manuscript_twocolumn.log:1038`: overfull hbox (32.00706pt) at line 206 (Eq 10). `title_page.log:413`: overfull hbox (15.61658pt) on GitHub URL at lines 37–38. `manuscript.log`: 36 badness 10000 underfull hboxes (Tables 1, 5, 7, 8). |
| 3 | Structural elements mapped (8 sections, 21 subsections, 7 subsubsections, 8 tables, 5 figures, 12 equations) with unreferenced labels identified | ✓ VERIFIED | Table 3 (`tab:perclass`) and Table 8 (`tab:decision_matrix`/`tab:executive_matrix`) have 0 references in prose. Eq 8 (`eq:shock_threshold`) has 0 references. Table 7 captioned `"Algorithm 1:"` inside `table*`. Figures 1–5 mapped. |
| 4 | BibTeX database (49 entries) vs compiled citations (32 cited, 17 uncited orphans) verified, including Cohen (2020) and Cambria (2018) year errors | ✓ VERIFIED | 49 bib entries parsed; 32 cited in `manuscript.aux`; exactly 17 uncited orphans (`bitner2000technology`, `byrt1993bias`, `smith1999model`, etc.). `cohen1960coefficient` line 289 has `year = {2020}` (compiled as `Cohen (2020)`); `cambria2017senticnet` line 26 has `year = {2018}` (compiled as `Cambria et al. (2018)`). |
| 5 | Author anonymity in `manuscript.tex`/`manuscript_twocolumn.tex`, `title_page.tex` author/affiliation/repo URL drift, highlights char counts, and backup files cataloged | ✓ VERIFIED | `manuscript.tex` and `manuscript_twocolumn.tex` are 100% anonymized (`\author{}`, 0 matches for author names/affiliations/repo). `title_page.tex:37` specifies `github.com/ratulhasan` vs git remote `github.com/rh61632`. `highlights.txt` has 5 bullets (82, 78, 85, 81, 79 chars; all $\le 85$, no illegal header). Backup drafts cataloged (`test_reconstruct.tex` == `test_up.tex`, SHA256 `fe3dfaa3...`). |
| 6 | Silent failure of 4 string replacements in `scripts/reconstruct_master_manuscript.py` against `manuscript_base_1506.tex` documented with exact lines and clobbered fixes | ✓ VERIFIED | All 4 `.replace()` calls evaluated to `False`: `old_cons` (lines 59–61), `old_contingency` (lines 135–137), `old_bl` (lines 139–146), and `old_cs1` (lines 148–150) failed to match `manuscript_base_1506.tex` due to formatting divergences, leaving modern tables alongside conflicting legacy text. |
| 7 | Internal sample size, cohort arithmetic, and Table 3/4/5/6 contradictions ($N=4,500$ vs $4,499$ vs $4,486$; Table 3 typos; Table 5 overlapping 134M; Table 6 vs Case Studies 1 and 2) cataloged | ✓ VERIFIED | Table 1 asserts $N=4,499$ alongside "($1,500$ per operator)". Table 4 sub-cohorts sum to $1,091 + 390 + 3,005 = 4,486$ (missing 13 reviews, $99.7\%$). Table 3 $\mathcal{C}_1$ precision printed as $0.9528$ instead of $0.9828$, $\mathcal{C}_5$ precision printed as $0.9993$ instead of $1.0000$. Table 5 defines overlapping eras summing to 134 months, and prints Robi Era 1 NSS as $-14.28$ vs narrative $-57.9$. Table 6 conflicts with Case Studies 1 & 2. |
| 8 | Embedded PNG visual defects (Figure 1–4 hardcoded title offset due to Figure 0 insertion, Figure 4 title right-edge clipping, Figure 3 quadrant prevalence denominator mismatch) documented | ✓ VERIFIED | `figure0` prepended as Figure 1 causes Figures 1–4 to render with double contradictory numbering. `figure4_banglalink_reversal_decomposition.png` extends to column 2849 of 2850 px canvas, truncating `"s)"` from `"(+15.54 Points)"`. `figure3_priority_matrix.png` uses total-corpus prevalence ($0.78\%-8.12\%$), misplacing GP App Login into Q2 and BL Offers into Q3. |
| 9 | Contradictions between ESWA paper claims and live codebase/models/data documented | ✓ VERIFIED | Seed LLM in archive is `qwen/qwen3.8-27b` (not `Qwen-2.5-32B`). 0 ZWNJ or phonetic lemmatizers exist. BiLSTM uses random 128d embeddings (no GloVe) and single-head attention (no multi-head). BanglaBERT training used `max_length=96, batch_size=32, epochs=4` (not $128/16/5$). 0 scripts compute paired $t$-tests or McNemar. Gold set consensus is $N=182$ Sent / $N=187$ Cat ($N=261$ fabricated via $300 \times 87\%$). Exactly 7 of 10 shock rows in Table 6 do not exist in ground-truth data. |
| 10 | `telecommunications_policy_latex/` differences from ESWA and internal defects documented | ✓ VERIFIED | Targets *Telecommunications Policy*, Jashore affiliation, real data ($N=655,649$, 3,713 days, 122 non-overlapping months, real shocks, real agreement, correct Cohen 1960). Stale 2-col PDF: `twocolumn.tex` updated Nov 8 with synced counts, but compiled PDFs carry pre-sync counts. Eq 9 inverts FPR sign. Line 179 script counts sum to 655,598 (deficit 51). 16 unreferenced labels. |
| 11 | Legacy `paper/*.html` word count inflation, July 2016 exclusion, CNB calibration claim, and 9 broken tab-escaped KaTeX math blocks documented | ✓ VERIFIED | `index.html` and `paper.html` byte-identical duplicates (107,213 B, SHA256 `c751a784...`). HUD claims $\sim 3,206$ words; `verify_html.py` measures 3,843 words (+20.1%). Line 870 claims 21 July 2016 reviews excluded (ground truth is 27). Line 1021 claims CNB calibration (code is uncalibrated). Exactly 7 `<TAB>ext` and 2 `<TAB>imes` corrupt KaTeX rendering. |
| 12 | Missing `paper/JBA_Manuscript_Empirical_Calculations.xlsx` on disk confirmed, generator script audited, auxiliary `paper/figures/` overlaps documented | ✓ VERIFIED | 0 `.xlsx` files exist in repository. `build_paper_empirical_excel.py` was retargeted to `paper/` but never executed; contains hardcoded `g600`-leaked $82.0\%/0.6781$ metrics. `figure1` through `figure4` are 100% SHA256 identical across `paper/figures/`, `eswa_latex/figures/`, and `telecommunications_policy_latex/figures/`. `monthly_nss_trend_modern_era.png` == `monthly_nss_trend_2020_2026.png` (520,603 B) with legend overlap. |
| 13 | All 32 paper-related scripts in `scripts/` cataloged into broken, crop-dependent, and stale/contradictory categories | ✓ VERIFIED | All 32 scripts verified on disk: Group 1 (18 broken scripts targeting deleted `paper/journal_manuscript/` or docx; 3 read-only auditors crash on execution with exact `FileNotFoundError`/`PackageNotFoundError`); Group 2 (4 broken figure crop helpers); Group 3 (10 stale/contradictory generation and audit scripts, including `verify_paper_complete.py` with 3,716 days and `audit_project_integrity.py` with misleading 655670 assertion message). |

---

### 2.2 Artifacts Verification

| Artifact Path | Exists | Substantive | Status |
|---|:---:|:---:|:---:|
| `.gsd/phases/3/evidence/01_eswa_structure_and_build_logs_audit.md` | ✓ (23,191 B, 294 lines) | ✓ Full tables, line numbers, and log proofs | PASS |
| `.gsd/phases/3/evidence/01_eswa_citations_metadata_and_backups_audit.md` | ✓ (15,769 B, 225 lines) | ✓ 17 orphan keys, 2 wrong-year bugs, anonymity proof | PASS |
| `.gsd/phases/3/evidence/02_eswa_internal_contradictions_and_reconstruction_drift.md` | ✓ (21,180 B, 235 lines) | ✓ 4 failed replacements, math recomputations, 134M overlap | PASS |
| `.gsd/phases/3/evidence/02_eswa_figures_and_codebase_claims_audit.md` | ✓ (17,451 B, 172 lines) | ✓ Figure offsets, clipping, 7 fabricated shocks, model fiction | PASS |
| `.gsd/phases/3/evidence/03_cross_venue_and_deliverables_audit.md` | ✓ (23,104 B, 271 lines) | ✓ TP LaTeX comparison, HTML KaTeX defects, missing XLSX | PASS |
| `.gsd/phases/3/evidence/03_paper_scripts_and_tooling_audit.md` | ✓ (14,516 B, 160 lines) | ✓ Full catalog of 32 scripts with crash stack traces | PASS |
| `.gsd/phases/3/1-SUMMARY.md` | ✓ (4,867 B, 92 lines) | ✓ Structured executive summary for Plan 3.1 | PASS |
| `.gsd/phases/3/2-SUMMARY.md` | ✓ (5,979 B, 104 lines) | ✓ Structured executive summary for Plan 3.2 | PASS |
| `.gsd/phases/3/3-SUMMARY.md` | ✓ (5,630 B, 93 lines) | ✓ Structured executive summary for Plan 3.3 | PASS |

---

### 2.3 Key Links (Cross-Phase & Downstream Wiring)

| Link | From | To | Status | Proof |
|---|---|---|:---:|---|
| ESWA LaTeX Build Link | `paper/eswa_latex/*.tex` | `paper/*.pdf` | ✓ WIRED | Exact binary duplicate copies by `compile_eswa.py:29-31` confirmed |
| Citations & Unreferenced Labels Link | `paper/eswa_latex/references.bib` | Phase 4 Synthesis | ✓ WIRED | 17 orphans, 2 year bugs, Table 3 & Table 8 ghost tables cataloged |
| Reconstruction Drift Link | `scripts/reconstruct_master_manuscript.py` | `paper/eswa_latex/manuscript.tex` | ✓ WIRED | 4 silent string replacement misses empirically reproduced |
| Paper Claims vs Codebase Link | `paper/eswa_latex/manuscript.tex` | Phase 1 & 2 Findings | ✓ WIRED | Model hyperparams, gold set consensus, 7 fabricated shocks mapped |
| Cross-Venue Alignment Link | `paper/telecommunications_policy_latex/` | `paper/eswa_latex/` | ✓ WIRED | Systematic line-by-line comparative table constructed |
| Paper Tooling Audit Link | `scripts/*paper*` | `scripts/audit_project_integrity.py` | ✓ WIRED | All 32 scripts categorized; 3 crashes reproduced; integrity gaps isolated |

---

## 3. Requirements Coverage

| Requirement | Description | Status | Evidence |
|---|---|:---:|---|
| **REQ-05** | Audit active ESWA manuscript (`paper/eswa_latex/*.tex`, `highlights.txt`, `references.bib`, `compile_eswa.py`, `figures/`) and compiled `paper/*.pdf` for internal contradictions, stale metrics, anonymity, and broken references | ✓ SATISFIED | Thoroughly verified across Plans 3.1 & 3.2. Evidence documents `01_eswa_structure_and_build_logs_audit.md`, `01_eswa_citations_metadata_and_backups_audit.md`, `02_eswa_internal_contradictions_and_reconstruction_drift.md`, and `02_eswa_figures_and_codebase_claims_audit.md` provide empirical proofs for all items. |
| **REQ-06** | Compare active ESWA paper against frozen `paper/telecommunications_policy_latex/`, legacy `paper/*.html`, `paper/JBA_Manuscript_Empirical_Calculations.xlsx`, and `scripts/*paper*`/`*jba*` | ✓ SATISFIED | Thoroughly verified across Plan 3.3. Evidence documents `03_cross_venue_and_deliverables_audit.md` and `03_paper_scripts_and_tooling_audit.md` provide full comparative analysis, missing workbook confirmation, and categorization of all 32 paper scripts. |

---

## 4. Architectural Decision Records (ADR) Adherence

- **`ADR-001` (Read-Only Audit & No-Git-Commit Policy):**
  - Checked `git status --short`: No project, model, data, or paper files were modified by Phase 3. Only `.gsd/` artifacts were created.
  - Checked `git log -n 3 --oneline`: No git commits were created. Latest commit remains `3d9f889` from prior to audit inception.
  - No `pdflatex` compilation was run; no mutating python scripts were executed.
- **`ADR-002` (Sequential `inherit` Workspace Execution):**
  - All subagents operated sequentially directly within the live inherited workspace.

---

## 5. Anti-Patterns Scan

- Stubs / Placeholders: 0 detected in Phase 3 evidence files or summaries.
- Unproven claims: 0 detected. Every reported discrepancy corresponds to demonstrable file lines and executed verification checks.
- Shell discipline: All verification commands executed as standalone single-command PowerShell invocations without `&&` or `||`.

---

## 6. Verdict

```
status: pass
phase: 3
report: .gsd/phases/3/VERIFICATION.md
must_haves: 13/13
failures: []
gap_plans: []
```