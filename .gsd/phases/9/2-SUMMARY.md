# Phase 9 Plan 2 Summary: Cross-Venue LaTeX & HTML Remediation

**Phase:** 9
**Plan:** 2
**Status:** Completed
**Execution Mode:** Sequential (ADR-002), uncommitted working tree (ADR-003)

---

## 1. Executive Summary

Plan 9.2 remediated the secondary venue deliverables: the Telecommunications Policy (TP) LaTeX suite (`paper/telecommunications_policy_latex/`) and the standalone HTML paper deliverable (`scripts/build_paper_html.py` -> `paper/index.html` and `paper/paper.html`).

All empirical discrepancies, mathematical formulations, model leaderboard metrics, throughput claims, KaTeX tab corruptions, and reference hygiene issues identified under DISC-MAJ-15 and DISC-MIN-18 have been closed. All three TP PDFs (`title_page.pdf`, `manuscript.pdf`, `manuscript_twocolumn.pdf`) compile cleanly with zero undefined references/citations and zero critical overfull boxes, while `paper/*.pdf` (the primary ESWA deliverables) remain completely untouched (SHA256 verified).

---

## 2. Key Changes Implemented

### Task 1: Telecommunications Policy LaTeX Suite Remediation
- **Equation 9 Rogan–Gladen Identity:** Fixed inverted FPR sign in `manuscript.tex` and `manuscript_twocolumn.tex` to standard identity:
  $$P_{\text{true}} = \frac{P_{\text{observed}} - \text{FPR}}{\text{TPR} - \text{FPR}} = \frac{P_{\text{observed}} + \mathrm{Sp} - 1}{\mathrm{Se} + \mathrm{Sp} - 1}$$
- **Language Breakdown:** Documented 51 null/empty-text ratings ($578,780 + 55,689 + 6,585 + 14,544 + 51 = 655,649$).
- **Sentiment Distribution Sync:** Synchronized `manuscript.tex` line 272 to live classified counts: Positive = 497,486 (75.88%), Neutral = 71,763 (10.95%), Negative = 86,400 (13.18%).
- **Calibration Claim:** Updated to Platt sigmoid scaling via `CalibratedClassifierCV(method='sigmoid')` with soft weights `[2.0, 2.5, 1.0]`.
- **CV & Throughput Paragraphs:** Aligned to 87.44%/0.7688 (production sentiment), 87.33%/0.7794 (hero category), 87.84%/0.7820 (CLI sentiment), and single-review CPU inference throughput of 122.4–145.2 rev/s (8.17 ms/review for category; up to 18,200 rev/s batch).
- **Star-Rating Baseline:** Updated to active Gold $N=300$ metric: 86.67% accuracy / Macro-F1 0.5438.
- **Table 2 Sector NSS:** Aligned 2017 (+29.9), 2023 (+61.2), and 2026 (+74.1).
- **Table 3 GP RMSSD:** Aligned to 5.14.
- **Table 4 Shock Recovery:** Updated Robi 2022-12 shock to 20 months and GP 2025-08 shock to Unrecovered.
- **Fisher CI:** Aligned to Woolf [1.83, 9.75] and Fisher [1.79, 9.98].
- **Rogan–Gladen Envelope:** Replaced retired g600 $\pm 2.4\text{ pp}$ with active classifier adjustment (+8.23 to +14.81 pp).
- **Table A.1 Model Leaderboard:** Synchronized all CV and Gold metrics across production ensemble, LinearSVC, BanglaBERT, BiLSTM, MiniLM, and Star Heuristic.
- **References & Cross-refs:** Pruned 7 orphan entries from `references.bib` (28 cited entries remain), resolved unreferenced equation/table labels, and verified 100% double-blind anonymity (0 prohibited author/institution tokens).

### Task 2: TP LaTeX In-Place Compilation (`compile_tp.py`)
- Created `paper/telecommunications_policy_latex/compile_tp.py` executing `pdflatex` + `bibtex` pipelines.
- Resolved overfull box in `title_page.tex` (emergency stretch on repository URL) and Table A.1 (`\makecell` formatting on star heuristic baseline).
- Successfully compiled all three deliverables:
  - `title_page.pdf`: 2 pages ($\le 5$)
  - `manuscript.pdf`: 31 pages ($\le 35$)
  - `manuscript_twocolumn.pdf`: 16 pages ($\le 16$)
- Verification confirmed:
  - 0 undefined references
  - 0 undefined citations
  - 0 overfull boxes $> 2.0\text{ pt}$
  - `paper/*.pdf` ESWA deliverables untouched (SHA256 identical)

### Task 3: HTML Paper Deliverable Remediation (`build_paper_html.py`)
- **KaTeX Tab Escape Fix:** Eliminated all 9 tab-escaped KaTeX math sequences; verified 0 `\x09ext` and 0 `\x09imes` in generated HTML.
- **CDN Security Attributes:** Stripped invalid subresource integrity hashes from KaTeX CDN `<link>` and `<script>` tags.
- **Empirical Statistics Alignment:**
  - July 2016 exclusion: 24 initial reviews (Jul 28–31) / 149 in full July / 5,511 total.
  - Corpus breakdown: added 51 null-text ratings to reach exact $N = 655,649$.
  - Section 3.4: updated CV metrics, inference throughput (122.4–145.2 rev/s), star heuristic baseline (86.67% / 0.5438), and Platt sigmoid calibration.
  - Table 2: 2017 (+29.9), 2023 (+61.2), 2026 (+74.1).
  - Table 3: GP RMSSD 5.14.
  - Annexure Table A1: synced all model leaderboard metrics and gold benchmark notes.
  - Robustness audits: updated classifier invariance and Rogan–Gladen prevalence adjustments.
- **HUD Word Count:** Synchronized static badge (`~3,856 / 3,200 w`) and dynamic JS `updateWordCount()` with `scripts/verify_html.py` prose calculation logic.
- **Parity & Validation:** `paper/index.html` and `paper/paper.html` are byte-identical (108,290 bytes), pass `scripts/verify_html.py` (3,940 words, clean prose extraction), and pass `scripts/check_equations.py` (7/7 equations valid).

---

## 3. Verification Evidence

| Test / Check | Target | Result | Status |
|--------------|--------|--------|--------|
| `compile_tp.py` title page | $\le 5$ pages, 0 undef refs/cits | 2 pages, 0 undef | **PASS** |
| `compile_tp.py` manuscript | $\le 35$ pages, 0 undef refs/cits | 31 pages, 0 undef | **PASS** |
| `compile_tp.py` twocolumn | $\le 16$ pages, 0 undef refs/cits | 16 pages, 0 undef | **PASS** |
| ESWA PDF SHA256 parity | `paper/*.pdf` untouched | All 3 match byte-for-byte | **PASS** |
| KaTeX tab escape check | 0 `\x09ext`, 0 `\x09imes` | 0 found | **PASS** |
| HTML file parity | `index.html` == `paper.html` | Byte-identical (108,290 B) | **PASS** |
| `scripts/verify_html.py` | Valid prose extraction | 3,940 words | **PASS** |
| `scripts/check_equations.py` | 7 equations formatted | 7/7 equations PASS | **PASS** |
| Empirical ground truth audit | `audit_project_integrity.py --strict-paper` | rc=0 | **PASS** |
