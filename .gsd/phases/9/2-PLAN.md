---
phase: 9
plan: 2
wave: 2
depends_on: ["1"]
files_modified:
  - paper/telecommunications_policy_latex/manuscript.tex
  - paper/telecommunications_policy_latex/manuscript_twocolumn.tex
  - paper/telecommunications_policy_latex/title_page.tex
  - paper/telecommunications_policy_latex/references.bib
  - paper/telecommunications_policy_latex/compile_tp.py
  - paper/telecommunications_policy_latex/title_page.pdf
  - paper/telecommunications_policy_latex/manuscript.pdf
  - paper/telecommunications_policy_latex/manuscript_twocolumn.pdf
  - scripts/build_paper_html.py
  - paper/index.html
  - paper/paper.html
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "paper/telecommunications_policy_latex/manuscript.tex and manuscript_twocolumn.tex fix Equation 9 Rogan-Gladen identity (P_true = (P_observed - FPR) / (TPR - FPR) = (P_observed + Sp - 1) / (Se + Sp - 1)), eliminating the inverted FPR sign"
    - "Review language breakdown adds 51 null/empty-text ratings (578,780 + 55,689 + 6,585 + 14,544 + 51 = 655,649) and single-column line 272 is synchronized to positive=497,486 / neutral=71,763 / negative=86,400"
    - "Table 2 (+29.9, +61.2, +74.1), Table 3 (GP RMSSD 5.14), Table 4 (Robi 20 months, GP Unrecovered), Fisher CI [1.79, 9.98] / Woolf [1.83, 9.75], and Section 3/Table A.1 model metrics (Star Heuristic 86.67% / 0.5438, 122.4-145.2 rev/s throughput) match canonical empirical ground truth"
    - "Retired g600 ±2.4 pp envelope is replaced by active Rogan-Gladen negative prevalence adjustment (+8.23 to +14.81 pp) and unverified LinearSVC concordance claim is replaced with verified model comparisons per ADR-003"
    - "All 16 unreferenced labels in telecommunications_policy_latex are cited in prose, 3 orphan BibTeX entries (devlin2019bert, hasan2020sentiment, itu2024measuring) are pruned, and blinded manuscripts maintain 100% double-blind anonymity (0 prohibited identifiers)"
    - "paper/telecommunications_policy_latex/compile_tp.py compiles title_page.pdf, manuscript.pdf, and manuscript_twocolumn.pdf strictly inside paper/telecommunications_policy_latex/ with 0 undefined references, 0 undefined citations, and ZERO modification of paper/*.pdf"
    - "scripts/build_paper_html.py replaces all 9 tab-escaped KaTeX math sequences (0 ASCII 0x09 control tabs in generated HTML), removes invalid KaTeX CDN integrity attributes, and aligns JS updateWordCount() and HUD #prose-word-count / .hud-bar-fill with scripts/verify_html.py prose counting"
    - "build_paper_html.py generates byte-identical paper/index.html and paper/paper.html with verified July 2016 exclusion (24 in Jul 28-31 / 149 in Jul / 5,511 total), +51 null-text ratings, no false CNB calibration claim, aligned empirical tables/metrics, and passing verify_html.py & check_equations.py"
  artifacts:
    - "Remediated sources in paper/telecommunications_policy_latex/ (manuscript.tex, manuscript_twocolumn.tex, title_page.tex, references.bib)"
    - "paper/telecommunications_policy_latex/compile_tp.py compilation script"
    - "Compiled TP PDFs in paper/telecommunications_policy_latex/ (title_page.pdf, manuscript.pdf, manuscript_twocolumn.pdf)"
    - "Remediated scripts/build_paper_html.py and regenerated paper/index.html and paper/paper.html"
---

# Plan 9.2: Cross-Venue LaTeX & HTML Remediation (REM-08, DISC-MAJ-15, DISC-MIN-18)

## Objective
Remediate the secondary venue deliverables: the Telecommunications Policy LaTeX suite (`paper/telecommunications_policy_latex/`) and the standalone HTML paper deliverable (`scripts/build_paper_html.py` -> `paper/{index,paper}.html`). Correct Equation 9 Rogan–Gladen algebra, restore 51 null-text ratings to language breakdowns, align model metrics, throughput, Table 2/3/4 values, and active prevalence adjustments. Prune uncited BibTeX/HTML references, compile TP PDFs strictly in-place without touching ESWA `paper/*.pdf`, eliminate KaTeX tab-escape corruptions, synchronize the HTML HUD word count with `verify_html.py`, and verify both deliverables pass all equation and HTML validators.

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-08`)
- `.gsd/phases/9/RESEARCH.md` (Sections 2, 3, Decisions 2 & 3)
- `scraped_data_global/classified/paper_empirical_ground_truth.json`
- `paper/eswa_latex/manuscript.tex` (canonical empirical baseline)
- `paper/eswa_latex/compile_eswa.py` (compilation reference)
- `scripts/build_paper_html.py`
- `scripts/verify_html.py`
- `scripts/check_equations.py`

## Tasks

<task type="auto">
  <name>Remediate paper/telecommunications_policy_latex sources and references</name>
  <files>
    paper/telecommunications_policy_latex/manuscript.tex
    paper/telecommunications_policy_latex/manuscript_twocolumn.tex
    paper/telecommunications_policy_latex/title_page.tex
    paper/telecommunications_policy_latex/references.bib
  </files>
  <action>
    Remediate `paper/telecommunications_policy_latex/` sources per RESEARCH.md Section 2.2:

    1. **Equation 9 Rogan–Gladen Identity (`manuscript.tex:245`, `manuscript_twocolumn.tex:246`, `\label{eq:rogan}`):**
       - Fix inverted FPR sign:
         Replace `P_{\text{true}} = \frac{P_{\text{observed}} + \text{FPR} - 1}{\text{TPR} + \text{FPR} - 1}`
         with standard Rogan–Gladen identity matching `manuscript_twocolumn.tex`:
         `P_{\text{true}} = \frac{P_{\text{observed}} - \text{FPR}}{\text{TPR} - \text{FPR}} = \frac{P_{\text{observed}} + \mathrm{Sp} - 1}{\mathrm{Se} + \mathrm{Sp} - 1}`.

    2. **Language Breakdown 51-Review Deficit (`manuscript.tex:179`, `manuscript_twocolumn.tex:180`):**
       - Update line 179 to explicitly document the 51 null/empty `review_text` ratings:
         `578,780` Latin ($88.28\%$) + `55,689` Bengali ($8.50\%$) + `6,585` Mixed ($1.00\%$) + `14,544` Emoji-only ($2.22\%$) + `51` null/empty-text ratings ($0.01\%$) = exactly `655,649` reviews ($100.0\%$).

    3. **Single vs Two-Column Class Sentiment Sync (`manuscript.tex:272` vs `manuscript_twocolumn.tex:273`):**
       - Synchronize `manuscript.tex:272` to live classified counts: `Positive = 497,486` ($75.88\%$), `Neutral = 71,763` ($10.95\%$), `Negative = 86,400` ($13.18\%$) (eliminating stale `497,377 / 71,659 / 86,613`).

    4. **Calibration & Classifier Weights (`manuscript.tex:257`, `manuscript_twocolumn.tex:258`):**
       - Replace isotonic regression claim with `CalibratedClassifierCV` sigmoid Platt scaling (`method='sigmoid'`), and state soft ensemble weights `[2.0, 2.5, 1.0]`.

    5. **Model Leaderboard, CV, Throughput & Gold Benchmark Parity (`manuscript.tex:259-261`, `Table A.1 lines 565-587`):**
       - Prod Sentiment CV: `87.44% (0.7688)`, CLI Sentiment: `87.84% (0.7820)`, Category Hero: `87.33% (0.7794)`.
       - Challenger LinearSVC: Sentiment CV `87.64% (0.7798)`, Category CV `86.91% (0.7664)`; Gold $N=300$ Sentiment `89.00%`, Category `91.00%`.
       - Fine-Tuned BUET BanglaBERT: Mark Gold as `---` (unlogged on active Gold $N=300$).
       - BiLSTM CV Sentiment `81.50% (0.7180)`, Category `80.84% (0.7106)`; Gold Sentiment `78.67%`, Category `91.33%`.
       - MiniLM: Sentiment CV `86.00% (0.7809)`, Category CV `81.15% (0.7247)`, Gold `---`.
       - Star-Rating Heuristic: Replace leaked `g600` `80.17% (0.5510)` with active Gold $N=300$ `86.67% (0.5438 Macro-F1)`.
       - Throughput: Single-review CPU inference is `122.4` rev/s (`8.17 ms`) category, `145.2` rev/s prod sentiment (`176.5` rev/s CLI), up to `18,200` rev/s batch (remove `450 reviews/second vs 12 reviews/second on GPU`).

    6. **Empirical Tables & Statistics Alignment:**
       - Table 2 Sector NSS (`lines 319, 325, 328`): `2017: +29.9`, `2023: +61.2`, `2026: +74.1` (exact 74.05).
       - Table 3 GP Filtered RMSSD (`line 376`): `5.14` (not `5.15`).
       - Table 4 Shock Recovery (`lines 404, 409`): `Robi 2022-12 -> 2023-01 (-16.6)` is `20 months` (regained `66.19` in Aug 2024); `GP 2025-08 -> 2025-09 (-18.5)` is `Unrecovered` through Sep 2026. Label positive shocks (`2020-04`, `2023-02`, `2024-05`) as `N/A (Rebound)` or `Sustained`.
       - Line 445 Fisher CI: Replace `[1.78, 10.51]` with exact Fisher `[1.79, 9.98]` / Woolf `[1.83, 9.75]`.
       - Line 481 LinearSVC Invariance: Replace unverified `100% (35/35)` and `98.3% (59/60)` claims with verified model comparisons per ADR-003.
       - Line 484 Leaked `g600` `±2.4 pp` envelope: Replace with verified active `sentiment_voting_classifier` Rogan–Gladen negative prevalence adjustment (`+8.23 to +14.81 pp`: GP 20.60% vs 12.15%, Robi 20.19% vs 11.96%, BL 32.14% vs 17.33%), which raises absolute prevalence while preserving comparative operator rankings.

    7. **Citations, Labels & Double-Blind Verification:**
       - Add explicit prose citations to all 7 unreferenced labels: `tab:leaderboard`, `tab:kappa`, `tab:thresholds`, `eq:nss`, `eq:rmssd`, `eq:ssi`, `eq:shock`.
       - In `references.bib`: prune the 3 uncited orphan entries (`devlin2019bert`, `hasan2020sentiment`, `itu2024measuring`).
       - In `title_page.tex`: add `\usepackage{xurl}` and repo remote `https://github.com/rh61632/telecom-Voice-of-Customer_intelligence` in Data Availability.
       - Verify `manuscript.tex` and `manuscript_twocolumn.tex` contain ZERO prohibited identifiers (`Ratul`, `rh61632`, `Leading University`, `Jashore`, `github.com`).
  </action>
  <verify>
    python -c "b = open('paper/telecommunications_policy_latex/manuscript.tex', encoding='utf-8').read(); assert '+FPR - 1' not in b; assert '655,649' in b; assert '497,486' in b; assert '86.67' in b; print('✓ TP manuscript.tex verified')"
  </verify>
  <done>
    paper/telecommunications_policy_latex sources updated with corrected algebra, aligned empirical statistics, zero g600 leakage, zero orphan bib entries, and strict double-blind anonymity.
  </done>
</task>

<task type="auto">
  <name>Create compile_tp.py and compile TP PDFs strictly in-place</name>
  <files>
    paper/telecommunications_policy_latex/compile_tp.py
    paper/telecommunications_policy_latex/title_page.pdf
    paper/telecommunications_policy_latex/manuscript.pdf
    paper/telecommunications_policy_latex/manuscript_twocolumn.pdf
  </files>
  <action>
    1. Create `paper/telecommunications_policy_latex/compile_tp.py` modeled on `paper/eswa_latex/compile_eswa.py`:
       - Compile `title_page.tex`, `manuscript.tex`, and `manuscript_twocolumn.tex` using `pdflatex` (Pass 1), `bibtex` (Pass 1 for manuscripts), `pdflatex` (Pass 2), and `pdflatex` (Pass 3).
       - Fail fast on any non-zero exit code.
       - Parse `.log` files to assert 0 undefined references (`Reference .* undefined`) and 0 undefined citations (`Citation .* undefined`).
       - Scan for overfull `\hbox` warnings > 2pt.
       - Query page counts via `pdfinfo` (`manuscript.pdf` target <= 35, `manuscript_twocolumn.pdf` target <= 16).
       - **CRITICAL RESTRICTION (Decision 2):** Never copy compiled PDFs to `paper/*.pdf`! `paper/*.pdf` are the ESWA submission deliverables whose SHA256 hashes must remain byte-identical to `paper/eswa_latex/*.pdf`.
    2. Execute `python paper/telecommunications_policy_latex/compile_tp.py`.
    3. Assert all 3 PDFs compile cleanly inside `paper/telecommunications_policy_latex/`.
    4. Confirm ESWA PDFs in `paper/*.pdf` remain completely untouched by verifying SHA256 hashes against `paper/eswa_latex/*.pdf`.
  </action>
  <verify>
    python -c "import hashlib, pathlib; r=pathlib.Path('paper'); e=r/'eswa_latex'; t=r/'telecommunications_policy_latex'; assert (t/'manuscript.pdf').exists(); assert hashlib.sha256((r/'manuscript.pdf').read_bytes()).hexdigest() == hashlib.sha256((e/'manuscript.pdf').read_bytes()).hexdigest(); print('✓ TP compiled in-place; ESWA PDFs untouched')"
  </verify>
  <done>
    compile_tp.py created and executed; TP PDFs compiled in-place with 0 undefined refs/cits; ESWA deliverable PDFs untouched and verified.
  </done>
</task>

<task type="auto">
  <name>Remediate build_paper_html.py and regenerate byte-identical index.html and paper.html</name>
  <files>
    scripts/build_paper_html.py
    paper/index.html
    paper/paper.html
  </files>
  <action>
    Remediate `scripts/build_paper_html.py` to fix all KaTeX, HUD, empirical, and reference defects (RESEARCH.md Section 3.2):

    1. **Eliminate 9 Tab-Escaped KaTeX Sequences (0 ASCII 0x09 tabs in HTML math):**
       - Fix escaped `\text` and `\times` sequences in `scripts/build_paper_html.py`:
         - Line 967: `\\text{NSS}_m`
         - Line 1044: `\\text{Vol}` and `\\times`
         - Line 1345: `\\text{Vol}`
         - Line 1433: `\\text{NSS}` (both occurrences!)
         - Line 1502: `\\times`
         - Line 1590: `\\text{NSS}`
         - Line 1591: `\\text{Vol}`
       - Check `lines 1840-1857` in `<script>`: ensure JavaScript regexes and delimiters (`\\(`, `\\)`, `\\[`, `\\]`, `/\\s+/`) emit valid runtime JS without double-escaping issues.
       - Remove placeholder `integrity="sha512-...5p0v0q5bW2N+Z6w5d5e5p0v0w=="` hashes from CDN `<link>` and `<script>` tags on lines 28–29 so browsers do not reject KaTeX.

    2. **HUD Word Count Synchronization:**
       - Align JS `updateWordCount()` (`lines 1850-1861`) with `scripts/verify_html.py` prose logic:
         Sum prose text across `page2-abstract` and `sec1..sec7`, excluding `.callout-box`, `.table-note`, `.figure-note`, `.metadata-box`, `button`, and `h1..h3`.
       - Update the static fallback text on `line 696` (`#prose-word-count`) and `.hud-bar-fill` style width (`line 122`) to match the exact prose word count calculated by `verify_html.py`.

    3. **Empirical & Architecture Alignments:**
       - July 2016 exclusion (line 888): State `24` reviews from `2016-07-28..31` (21 BL, 3 GP), `149` in full July 2016, and `5,511` total boundary/partial reviews excluded.
       - Review language breakdown (line 888): Add `+ 51 empty/null-text ratings = 655,649`.
       - Remove false CNB calibration claim (line 1039: `"84.76% to 74.47%"`), clarifying that ComplementNB is uncalibrated and Platt sigmoid scaling is applied to LinearSVC.
       - Model metrics (lines 1036, 1705-1744): Active Gold $N=300$ Star Heuristic = `86.67% / 0.5438`, CPU single-review throughput = `122.4–145.2 rev/s`, unlogged DL cells marked `---`.
       - Table 2 Sector NSS (lines 1171, 1213, 1234): `2017: +29.9`, `2023: +61.2`, `2026: +74.1`.
       - Table 3 GP Filtered RMSSD (line 1307): `5.14`.
       - Table 4 Shock Recovery (lines 1382, 1427): `Robi 2022-12->2023-01: 20 months`, `GP 2025-08->2025-09: Unrecovered`.
       - Line 1553 & 1562: Replace LinearSVC concordance and retired `g600` `±2.4 pp` envelope with verified active `+8.23 to +14.81 pp`.
       - HTML References (lines 1649-1676): Prune or cite uncited entries (`BTRC (2024)`, `Dellarocas (2003)`, `Devlin et al. (2019)`, `GSMA (2024)`, `Hasan et al. (2020)`, `ITU (2024)`, `Rahman et al. (2021)`).

    4. **Generate and Verify HTML Files:**
       - Execute `python scripts/build_paper_html.py`.
       - Assert `paper/index.html` and `paper/paper.html` are created and byte-identical.
       - Assert 0 ASCII `0x09` tab control characters exist inside KaTeX blocks in both HTML files.
       - Run `python scripts/verify_html.py` and `python scripts/check_equations.py`.
  </action>
  <verify>
    python -c "import pathlib; h1=pathlib.Path('paper/index.html').read_bytes(); h2=pathlib.Path('paper/paper.html').read_bytes(); assert h1 == h2, 'HTML files differ'; assert b'\text' not in h1, 'Unescaped tab in HTML'; print('✓ HTML byte parity and clean math confirmed')"
  </verify>
  <done>
    scripts/build_paper_html.py remediated; paper/index.html and paper/paper.html regenerated with byte identity, 0 tab math corruptions, synchronized HUD word count, and passing validation scripts.
  </done>
</task>

## Verification
After all tasks complete:
- [ ] `paper/telecommunications_policy_latex/manuscript.tex` Equation 9 uses standard Rogan–Gladen identity without inverted signs.
- [ ] Review counts across TP and HTML equal exactly 655,649 (including 51 null-text ratings).
- [ ] `paper/telecommunications_policy_latex/compile_tp.py` compiles all 3 PDFs in-place with 0 undefined refs/cits.
- [ ] `paper/*.pdf` ESWA SHA256 hashes are untouched and byte-identical to `paper/eswa_latex/*.pdf`.
- [ ] `paper/index.html` and `paper/paper.html` have 0 tab-escaped math sequences and are byte-identical.
- [ ] `python scripts/verify_html.py` and `python scripts/check_equations.py` pass cleanly.

## Success Criteria
- [ ] All tasks completed and verified with single-command PowerShell checks.
- [ ] Goal-backward must-haves confirmed.
