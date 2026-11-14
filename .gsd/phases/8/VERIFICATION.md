# Phase 8 Verification Report: Publication Figures, Active ESWA Manuscript & Compiled PDFs Remediation

**Phase:** 8 — Publication Figures, Active ESWA Manuscript & Compiled PDFs Remediation  
**Status:** PASS  
**Verified At:** 2026-11-12T01:51:00+06:00  
**Verification Agent:** gsd-verifier (Independent Context)  
**Requirements:** `REM-06`, `REM-07`  
**Decisions:** `ADR-002` (Sequential Inherit Execution), `ADR-003` (100% Empirical Truth & Zero Unsolicited Git Commits)  
**Scorecard:** 24 / 24 Must-Haves Verified Passing  

---

## Executive Summary

Phase 8 independently verified all publication figures (`figure0` through `figure4`), generator scripts, BibTeX references, Title Page, single-column and two-column ESWA LaTeX manuscripts, compilation logs, page budgets, and deliverable PDFs. Every empirical metric, architectural assertion, and artifact checksum was directly queried and validated against live code, logs, datasets, and `scraped_data_global/classified/paper_empirical_ground_truth.json`.

All 24 empirical must-haves passed with zero defects:
- Hardcoded `"Figure 1..4:"` bitmap titles, title clipping, and fictional NLP/ML cards have been permanently eliminated across figures and generators.
- Figures achieve byte-for-byte SHA256 parity across all three venue folders (`paper/figures/`, `paper/eswa_latex/figures/`, `paper/telecommunications_policy_latex/figures/`), and two-panel longitudinal figures achieve 6-way SHA256 parity.
- `references.bib` has 100% citation parity (36 entries, 0 uncited, 0 missing), with `cohen1960coefficient` corrected to 1960 and `cambria2018senticnet` linked to its official AAAI-18 proceedings DOI.
- `title_page.tex` contains remote `rh61632`, `\usepackage{xurl}` (eliminating overfull hbox on long URLs), and the formal title matching `demo/app.py`.
- `manuscript.tex` and `manuscript_twocolumn.tex` share 100% byte-identical body parity (643 lines) via `sync_eswa_twocolumn.py`, 0 raw markdown `**...**` tokens, 0 fictional claims, full double-blind anonymity, and 100% empirical grounding with `paper_empirical_ground_truth.json`.
- All compilation logs report 0 undefined references, 0 undefined citations, and 0 overfull boxes > 2pt.
- Compiled PDFs strictly obey page limits: `manuscript.pdf` = 32 pages ($\le 35$), `manuscript_twocolumn.pdf` = 15 pages ($\le 15$), and `title_page.pdf` = 2 pages ($\le 3$).
- Deliverable PDFs achieve 100% byte-for-byte SHA256 parity between `paper/eswa_latex/*.pdf` and `paper/*.pdf`.
- `python scripts/audit_project_integrity.py` passes 100% of checks with `rc=0`. In `--strict-paper` mode, Checks 1–3 pass cleanly with ONLY Check 4 (`.xlsx` owned by Phase 9) awaiting generation.
- Zero git commits were made (`ADR-003`).

---

## Must-Have Verification Grid

| # | Must-Have Criterion | Target File / Artifact | Empirical Command / Proof | Result |
|---|---|---|---|:---:|
| 1 | `figure0` 3-way SHA256 parity | `figure0_system_architecture.png` | SHA256: `17092544561c9774...` identical in `paper/figures/`, `paper/eswa_latex/figures/`, `paper/telecommunications_policy_latex/figures/` | **PASS** |
| 2 | `figure1` 3-way SHA256 parity & alias match | `figure1_longitudinal_nss_trajectory.png` | SHA256: `b3c0d02aaedc66be...` identical in 3 venues; identical to alias `figure1_monthly_nss_trajectory.png` | **PASS** |
| 3 | `figure2` 3-way SHA256 parity & alias match | `figure2_annual_leadership_strip.png` | SHA256: `905cb27c4487d93e...` identical in 3 venues; identical to alias `figure2_yearly_leadership_strip.png` | **PASS** |
| 4 | `figure3` 3-way SHA256 parity | `figure3_priority_matrix.png` | SHA256: `81a14d54c0a5c64b...` identical in 3 venues | **PASS** |
| 5 | `figure4` 3-way SHA256 parity | `figure4_banglalink_reversal_decomposition.png` | SHA256: `620339a28ec76fea...` identical in 3 venues | **PASS** |
| 6 | Two-panel 6-way SHA256 parity | `monthly_nss_trend_{modern_era,2020_2026}.png` | SHA256: `b8d496436e1bf269...` identical across `paper/figures/`, `assets/plots/`, and `scraped_data_global/plots/` | **PASS** |
| 7 | Zero hardcoded Figure 1..4 titles in scripts | `generate_eswa_architecture_diagram.py`, `generate_paper_figures.py`, `rebuild_figure3.py`, `generate_two_panel_figure.py` | `re.search(r'(set_title\|title)\([^)]*Figure\s*[1-4]:', ...)` returns 0 matches | **PASS** |
| 8 | Zero fictional model/NLP strings in figure generators | `scripts/*.py` | `Char-CNN`, `GloVe`, `Qwen-2.5-32B`, `Bayesian Margin`, `Star-Rating Inversion` absent across all 4 generator scripts | **PASS** |
| 9 | `figure3` vertical threshold = 3.75% | `generate_paper_figures.py`, `rebuild_figure3.py` | `ax.axvline(3.75)` and quadrant spans `ax.axvspan(3.75, ...)` verified in both scripts | **PASS** |
| 10 | `figure4` canvas configuration & values | `generate_paper_figures.py` | Canvas `figsize=(10.5, 5.4)`, `bbox_inches='tight'`, `+10.33` General, `+5.21` Technical sum (`+2.80` + `+1.07` + `+0.98` + `+0.36`), `+15.54` Net | **PASS** |
| 11 | `references.bib` key & DOI fixes | `paper/eswa_latex/references.bib` | `cohen1960coefficient` year is `{1960}`; `cambria2018senticnet` has official AAAI-18 proceedings DOI `10.1609/aaai.v32i1.11559` | **PASS** |
| 12 | `references.bib` 0 uncited entries | `references.bib` vs `manuscript.tex` | Exactly 36 BibTeX keys in `references.bib`; exactly 36 cited keys in `manuscript.tex`; 0 uncited, 0 missing | **PASS** |
| 13 | `title_page.tex` URL, xurl & title | `paper/eswa_latex/title_page.tex` | Contains `rh61632`, `\usepackage{xurl}`, and unified formal title without colloquial prefix | **PASS** |
| 14 | Exact body parity between manuscripts | `manuscript.tex` vs `manuscript_twocolumn.tex` | 643 lines (single-column lines 25--end $\equiv$ two-column lines 24--end) byte-identical; verified via `sync_eswa_twocolumn.py` | **PASS** |
| 15 | Zero raw markdown `**...**` tokens | `manuscript.tex`, `manuscript_twocolumn.tex` | Regex search `\*\*[^*]+\*\*` yields 0 matches in both manuscripts | **PASS** |
| 16 | Zero fictional claims in manuscripts | Both manuscripts | `28% higher ARPU`, `3.5x-5.0x SAC`, `Char-CNN`, `GloVe`, `Qwen-2.5-32B`, `N=261`, `134M`, `0.711`, `0.942`, `21.64`, `0.7418` absent | **PASS** |
| 17 | Double-blind anonymity | Both manuscripts | 0 occurrences of prohibited terms (`Ratul`, `rh61632`, `Leading University`, `Jashore`, `github.com`) | **PASS** |
| 18 | Empirical ground truth alignment | `manuscript.tex` vs `paper_empirical_ground_truth.json` | 11/11 modules verified: Table 1 ($N=4,500$ seed), Table 2 ($87.33\%$ Cat, $87.44\%$ Sent), Table 3 ($V=29,843$, $8.17$ ms, $109.72$, $99.00\%$), Table 4 (1,091/390/3,005/14 and 661k distribution), Gold ($95.41\%$, $0.7694$, $91.00\%$, $0.5762$, $0.8650$), Shocks ($\chi^2=12.83, 11.55$, $\text{OR}=4.23$ $[1.83, 9.75]$, BL $\text{OR}=10.00$), Case Study 1 ($51.82\%$, $42.82$, $-11.18$, $+32.78$, $-7.59$, $71.71$), Case Study 2 ($+15.54$, $2.13\times$, $+10.33$, $+5.21$), Tables 7--8 ($p_{\text{base}}=4.42\%$, counts 147/58/15/13) | **PASS** |
| 19 | Compilation log cleanliness | `manuscript.log`, `manuscript_twocolumn.log`, `title_page.log` | 0 undefined references, 0 undefined citations, 0 overfull boxes > 2pt across all three compilation logs | **PASS** |
| 20 | PDF page count budgets | `pdfinfo` output | `manuscript.pdf` = 32 pages ($\le 35$), `manuscript_twocolumn.pdf` = 15 pages ($\le 15$), `title_page.pdf` = 2 pages ($\le 3$) | **PASS** |
| 21 | PDF deliverable SHA256 sync | `paper/eswa_latex/*.pdf` vs `paper/*.pdf` | Identical SHA256 hashes: `manuscript.pdf` (`41cda56a...`), `manuscript_twocolumn.pdf` (`54698cef...`), `title_page.pdf` (`ce1ea3f5...`) | **PASS** |
| 22 | System integrity audit (default) | `python scripts/audit_project_integrity.py` | 100% of empirical checks passed across Modules 1--8 (`rc=0`, 19.02s) | **PASS** |
| 23 | System integrity audit (--strict-paper) | `python scripts/audit_project_integrity.py --strict-paper` | Checks 1--3 passed cleanly; ONLY Check 4 (`.xlsx` owned by Phase 9) flagged pending | **PASS** |
| 24 | Git working tree discipline | `git status`, `git log` | Zero unsolicited git commits made; working tree preserves staged review policy (`ADR-003`) | **PASS** |

---

## Detailed Evidence & Audit Trail

### 1. Figures & Generator Scripts Parity (REM-06)
- **Publication Figures 3-Way SHA256 Parity:**
  - `figure0_system_architecture.png`: `17092544561c9774...` (717,376 bytes)
  - `figure1_longitudinal_nss_trajectory.png`: `b3c0d02aaedc66be...` (677,943 bytes)
  - `figure2_annual_leadership_strip.png`: `905cb27c4487d93e...` (191,113 bytes)
  - `figure3_priority_matrix.png`: `81a14d54c0a5c64b...` (515,264 bytes)
  - `figure4_banglalink_reversal_decomposition.png`: `620339a28ec76fea...` (250,329 bytes)
- **Two-Panel Longitudinal Figures 6-Way Parity:**
  - SHA256: `b8d496436e1bf269...` across `paper/figures/monthly_nss_trend_{modern_era,2020_2026}.png`, `assets/plots/monthly_nss_trend_{modern_era,2020_2026}.png`, and `scraped_data_global/plots/monthly_nss_trend_{modern_era,2020_2026}.png`.
- **Generator Scripts Verification:**
  - `scripts/generate_paper_figures.py`: `plt.title` calls contain zero hardcoded `"Figure 1..4:"` prefixes.
  - `scripts/rebuild_figure3.py`: `plt.title` contains no hardcoded figure number.
  - Figure 3 vertical boundary in both scripts: `3.75` ($3.75\%$).
  - Figure 4 canvas in `generate_paper_figures.py`: `figsize=(10.5, 5.4)`, `bbox_inches='tight', pad_inches=0.15`, components $+10.33$ General and Technical components $+2.80 + 1.07 + 0.98 + 0.36 = +5.21$ summing to $+15.54$.

### 2. LaTeX Manuscript, BibTeX & Ground Truth Alignment (REM-07)
- **BibTeX Cleansing (`references.bib`):**
  - `cohen1960coefficient`: year `{1960}` verified.
  - `cambria2018senticnet`: AAAI-18 proceedings DOI `10.1609/aaai.v32i1.11559` verified.
  - Pruned 13 uncited orphan entries. All 36 keys in `references.bib` are cited in `manuscript.tex` (0 uncited, 0 missing).
- **Title Page (`title_page.tex`):**
  - Remote repository URL: `https://github.com/rh61632/telecom-Voice-of-Customer_intelligence`.
  - Package: `\usepackage{xurl}` verified.
  - Formal title: `An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling`.
- **Manuscript Parity & Cleanliness:**
  - `sync_eswa_twocolumn.py` validated: Single-column lines 25--end $\equiv$ Two-column lines 24--end (643 lines of byte-identical body).
  - Raw markdown tokens `**...**`: 0 in `manuscript.tex`, 0 in `manuscript_twocolumn.tex`.
  - Fictional claims: 0 occurrences of `28% higher ARPU`, `3.5x-5.0x SAC`, `Char-CNN`, `GloVe`, `Qwen-2.5-32B`, `N=261`, `134M`, `0.711`, `0.942`, `21.64`, `0.7418`.
  - Double-blind anonymity: 0 occurrences of author names, affiliations, or repo URLs across both manuscripts.
- **Empirical Ground Truth Check (`scratch/verify_ground_truth_alignment.py`):**
  - Table 1 Taxonomy: Seed $N=4,500$ (General 2,731, Offers 788, Network 364, Billing 217, Login 400).
  - Table 2 Leaderboard: Ensemble $87.33\%$ Category CV Acc, $87.44\%$ Sentiment CV Acc.
  - Table 3 Complexity: $V=29,843$, latency $8.17$ ms, density $109.72$, full-seed Acc $99.00\%$, Macro-F1 $0.9883$.
  - Table 4 Linguistics: Bangla 1,091 ($24.2\%$), Banglish 390 ($8.7\%$), English 3,005 ($66.8\%$), Symbolic 14 ($0.3\%$). 661k distribution: English $77.12\%$, Banglish $11.27\%$, Bangla $9.42\%$, Symbolic $2.19\%$.
  - Gold Set & IRR: Category agreement $95.41\%$ ($\kappa=0.7694$), Sentiment agreement $91.00\%$ ($\kappa=0.5762$, $\text{PABAK}=0.8650$).
  - Shocks & Contingency: Pearson $\chi^2(1)=12.83$, Yates $\chi^2(1)=11.55$, $\text{OR}=4.23$ ($95\%$ CI $[1.83, 9.75]$), Banglalink $\text{OR}=10.00$ ($p=0.0007$).
  - Case Study 1: Missingness $51.82\%$, March $42.82$, April $-11.18$, May $+32.78$, $v11.8.0$ April $-7.59$, $v11.9.1$ $71.71$.
  - Case Study 2: Turnaround $+15.54$, volume multiplier $2.13\times$, General $+10.33$, Technical $+5.21$.
  - Tables 7 & 8: $p_{\text{base}}=4.42\%$ (GP $3.45\%$, Robi $4.01\%$, BL $7.25\%$), 240 transition alert levels (Level 1: 147, Level 2: 58, Level 3: 15, Level 4: 13).

### 3. Compilation Logs, Page Budgets & Deliverables (REM-07)
- **Log Parsing:**
  - `paper/eswa_latex/manuscript.log`: 0 undefined refs, 0 undefined cits, 0 overfull boxes > 2pt (max overfull: 1.09677 pt).
  - `paper/eswa_latex/manuscript_twocolumn.log`: 0 undefined refs, 0 undefined cits, 0 overfull boxes > 2pt.
  - `paper/eswa_latex/title_page.log`: 0 undefined refs, 0 undefined cits, 0 overfull boxes > 2pt.
- **Page Count Bounds (via `pdfinfo`):**
  - `manuscript.pdf`: 32 pages (target $\le 35$ pages)
  - `manuscript_twocolumn.pdf`: 15 pages (target $\le 15$ pages)
  - `title_page.pdf`: 2 pages (target $\le 3$ pages)
- **SHA256 Parity between `paper/eswa_latex/*.pdf` and `paper/*.pdf`:**
  - `manuscript.pdf`: `41cda56a2ef9180ce87fafe3ff97204f69fc3057e930514a3832d6fe047ce562` (both match)
  - `manuscript_twocolumn.pdf`: `54698cef89484caa42a5d491eb004ea7e66d2a71be7f9fe6dfcf5781a54ee5aa` (both match)
  - `title_page.pdf`: `ce1ea3f5a58c722510f274cb7eb45d2e7a1fccefe2ec2637ce07525287f3ee18` (both match)
- **Integrity Tooling (`scripts/audit_project_integrity.py`):**
  - Default mode: 100% PASS in 19.02s (`rc=0`).
  - `--strict-paper` mode: Checks 1, 2, and 3 pass cleanly. Output confirms ONLY Check 4 (`paper/JBA_Manuscript_Empirical_Calculations.xlsx does not exist yet (owned by Phase 9)`) remains pending.

### 4. Git Policy Compliance (`ADR-003`)
- `git status --short` confirms modified and untracked files remain uncommitted in the working tree.
- `git log -n 5` confirms HEAD commit remains `3d9f889` from prior milestone. Zero unsolicited commits were executed.

---

## Verdict & Phase Gate Status

**Verdict:** **PASS**  
**Phase 8 Score:** 24 / 24 must-haves verified passing.  
**Failures:** 0  
**Gaps / Blockers:** None. Phase 8 has fulfilled all requirements under `REM-06` and `REM-07`. The repository is ready to proceed to Phase 9 (`Cross-Venue Deliverables, Workbook & Final System Verification`).
