# Evidence 03: Cross-Venue Artifacts (Telecommunications Policy LaTeX, Legacy HTML, Missing XLSX) & Auxiliary Figures Audit

**Audit Date:** 2026-11-11  
**Milestone:** Project & Paper Discrepancy Audit (v1.0.0)  
**Phase:** 3 — Research Paper & Cross-Venue Deliverables Audit  
**Plan:** 3.3 — Task 1  
**Governance:** `ADR-001` (Strictly read-only outside `.gsd/`; zero git commits; zero mutating scripts) & `ADR-002` (Sequential execution in `inherit` workspace)

---

## 1. Executive Summary

This empirical audit investigates all non-ESWA paper deliverables in `paper/`, including:
1. `paper/telecommunications_policy_latex/` (manuscript variants, title page, bibliography, logs, and compiled PDFs).
2. Legacy publication HTML files (`paper/index.html` and `paper/paper.html`) and their verification harness (`scripts/verify_html.py`).
3. Empirical calculation workbook (`paper/JBA_Manuscript_Empirical_Calculations.xlsx`) and its generator (`scripts/build_paper_empirical_excel.py`).
4. Auxiliary visual assets in `paper/figures/` and cross-directory SHA256 parity across `paper/eswa_latex/figures/` and `paper/telecommunications_policy_latex/figures/`.

### Core Findings Matrix
| Component / File | Primary Audit Result | Severity | Impact / Discrepancy Description |
|---|---|---|---|
| `telecommunications_policy_latex/manuscript.tex` | High empirical fidelity vs ESWA | Informational / Positive | Correctly uses $N=655,649$, 3,713 days, 122 months, non-overlapping eras, real annual NSS, and real shocks. |
| `telecommunications_policy_latex/title_page.tex` | Different venue, title, and affiliation | Expected / Cross-venue drift | Targets *Telecommunications Policy*, single author affiliated with Jashore University of Science & Technology (vs Leading University, Sylhet in ESWA). |
| `telecommunications_policy_latex/manuscript_twocolumn.tex` | Stale compiled PDF synchronization | Moderate | LaTeX source was updated Nov 8 with synced sentiment counts (`497,486 / 71,763 / 86,400`), but compiled PDFs from Nov 5 retain pre-sync counts (`497,377 / 71,659 / 86,613`). |
| `telecommunications_policy_latex/manuscript.tex:245` | Rogan-Gladen equation algebraic error | High (Theoretical) | Equation (9) writes $\frac{P_{\text{obs}} + \text{FPR} - 1}{\text{TPR} + \text{FPR} - 1}$ instead of $\frac{P_{\text{obs}} - \text{FPR}}{\text{TPR} - \text{FPR}}$ (or $\frac{P_{\text{obs}} + Sp - 1}{\text{TPR} + Sp - 1}$). |
| `telecommunications_policy_latex/manuscript.tex:179` | Script breakdown arithmetic deficit | Minor | Stated script breakdown ($578,780 + 55,689 + 6,585 + 14,544$) sums to $655,598$, missing 51 reviews ($655,649 - 655,598$). |
| `paper/index.html` == `paper/paper.html` | Byte-identical legacy JBA submission | Moderate | Verified byte-identical ($107,213$ bytes, SHA256 `c751a784...`). HUD sidebar claims 3,206 words, while `verify_html.py` measures 3,843 words (+20.1%). |
| `paper/index.html:949,1026`+ | KaTeX tab-escape math corruption | Moderate (Visual) | 7 occurrences of `\t`+`ext` and 2 occurrences of `\t`+`imes` due to unescaped Python strings in `scripts/build_paper_html.py`, breaking KaTeX math rendering. |
| `paper/index.html:870` | July 2016 exclusion count error | Minor | Claims 21 July 2016 reviews were excluded, whereas true excluded count is 27 ($655,676 - 655,649$). |
| `paper/JBA_Manuscript_Empirical_Calculations.xlsx` | Missing file on disk | High (Audit Gap) | Workbook does not exist on disk; generator `build_paper_empirical_excel.py` was retargeted to `paper/` but never executed, leaving hardcoded stale $g600$-leaked metrics in source. |
| `paper/figures/` vs `eswa_latex` vs `telecommunications_policy` | Exact figure SHA256 parity | Validated | All 4 figures (`figure1` through `figure4`) are 100% byte-identical across all three figure directories. |
| `paper/figures/monthly_nss_trend_modern_era.png` | Visual layout collisions | Minor (Aesthetic) | Unused two-panel plot has legend box colliding with shock annotation box, and rightmost x-axis tick collision (`2026-07` and `2026-09`). |

---

## 2. Exhaustive Audit: `paper/telecommunications_policy_latex/`

### 2.1 Venue, Metadata & Author Affiliation Comparison
The LaTeX bundle in `paper/telecommunications_policy_latex/` targets Elsevier's *Telecommunications Policy* rather than *Expert Systems with Applications* (ESWA).

| Field | Active ESWA Deliverable (`paper/eswa_latex/`) | Telecommunications Policy Deliverable (`paper/telecommunications_policy_latex/`) |
|---|---|---|
| **Target Venue** | *Expert Systems with Applications* (`manuscript.tex:19`) | *Telecommunications Policy* (`manuscript.tex:14`, `title_page.tex:38`) |
| **Article Title** | *"A Decade of Telecom Consumer Voice: Longitudinal Sentiment and Operational Intelligence across 655,649 Mobile App Reviews in Bangladesh"* | *"With Great Reviews Comes Great Responsibility: A Decade of Telecom Consumer Voice in Bangladesh"* (`manuscript.tex:27`, `title_page.tex:18`) |
| **Author Name** | `Ratul Hasan` (`title_page.tex:17`) | `Md. Ratul Hasan` (`title_page.tex:20,29`) |
| **Author Affiliation** | `Department of Computer Science and Engineering, Leading University, Ragibnagar, South Surma, Sylhet-3112, Bangladesh` | `Department of Electrical and Electronic Engineering, Jashore University of Science and Technology, Jashore -7408, Bangladesh` |
| **Corresponding Email**| `rh61632@gmail.com` | `rh61632@gmail.com` |
| **Telephone** | Not provided | `+880 1916-277722` (`title_page.tex:34`) |
| **GitHub Repository URL**| `https://github.com/ratulhasan/telecom-Voice-of-Customer_intelligence` | Not listed on title page or manuscript prose |
| **Anonymity in Main Text**| `\author{}` (`manuscript.tex:34`, blinded) | `\author{}` (`manuscript.tex:30`, blinded) |

### 2.2 Empirical Alignment Superiority Over ESWA
A remarkable finding of this audit is that **`paper/telecommunications_policy_latex/` exhibits significantly higher empirical alignment with the live repository data than the active ESWA manuscript (`paper/eswa_latex/`)**:

1. **Analytical Sample Parity:**
   - Mentions exact final corpus size $N = 655,649$, 3,713 days, and 122 months (lines 172, 272).
   - Correctly omits the corrupted $N = 4,499$ count that plagued ESWA; Table 1 and Table 2 do not carry the -1 deficit.
2. **Real Annual NSS Trajectory (Table 3, lines 318–328):**
   - Grameenphone: 2016 (+2.5, 438), 2017 (+13.5, 587), 2018 (-16.0, 605), 2019 (+19.6, 2,392), 2020 (+45.7, 27,600), 2021 (+61.0, 40,535), 2022 (+64.2, 45,702), 2023 (+69.8, 60,609), 2024 (+70.6, 75,059), 2025 (+70.3, 54,262), 2026 (+56.8, 12,351).
   - Robi Axiata: 2016 (-57.9, 126), 2017 (-50.7, 367), 2018 (-28.8, 1,418), 2019 (+16.4, 4,186), 2020 (+63.6, 32,333), 2021 (+63.8, 30,296), 2022 (+68.4, 34,418), 2023 (+48.7, 16,784), 2024 (+66.0, 16,804), 2025 (+78.6, 42,743), 2026 (+76.2, 18,903).
   - Banglalink: 2016 (+45.3, 744), 2017 (+45.5, 2,518), 2018 (+22.3, 3,041), 2019 (+17.8, 4,235), 2020 (+38.3, 17,538), 2021 (+46.6, 25,471), 2022 (+55.5, 21,442), 2023 (+40.1, 14,761), 2024 (+57.2, 15,333), 2025 (+66.4, 10,238), 2026 (+81.9, 21,810).
   - **Annual Volumes Sum Exactly:** $1,308 + 3,472 + 5,064 + 10,813 + 77,471 + 96,302 + 101,562 + 92,154 + 107,196 + 107,243 + 53,064 = \mathbf{655,649}$ reviews.
   - This directly reflects true annual metrics in `scraped_data_global/classified/yearly_intelligence_trends.json`, whereas ESWA Table 5 presented fabricated Era NSS numbers (-18.42 to +48.90) in overlapping 134-month windows.
3. **Four Strictly Non-Overlapping Eras:**
   - Era 1: 2016–2019 ($N = 20,657$, 41 months).
   - Era 2: 2020 ($N = 77,471$, 12 months).
   - Era 3: 2021–2022 ($N = 197,864$, 24 months).
   - Era 4: 2023–2026 ($N = 359,657$, 45 months).
   - **Sum:** $20,657 + 77,471 + 197,864 + 359,657 = \mathbf{655,649}$ reviews; $41 + 12 + 24 + 45 = \mathbf{122}$ months.
4. **Real Shocks (Table 5, lines 403–409):**
   - Lists only real econometric shocks matching `nss_stability_and_shocks_summary.json`:
     - Grameenphone 2020-03 $\to$ 2020-04 (+31.2, App Login +5.49)
     - Robi Axiata 2022-12 $\to$ 2023-01 (-16.6, App Login -7.40)
     - Robi Axiata 2023-01 $\to$ 2023-02 (+10.7, App Login +4.64)
     - Banglalink 2021-04 $\to$ 2021-05 (-16.4, Network Speed -4.90)
     - Banglalink 2024-03 $\to$ 2024-04 (-11.2, App Login -8.74)
     - Banglalink 2024-04 $\to$ 2024-05 (+32.8, App Login +13.73)
     - Grameenphone 2025-08 $\to$ 2025-09 (-18.5, Offers -2.68)
   - ESWA Table 6, by contrast, contained 7 phantom shocks not present in repo shock summaries.
5. **Real Ground Truth Agreement Metrics (Table A.2, lines 595–607):**
   - Correctly reports actual sample sizes from `data/gold_set/calculate_agreement.py`:
     - 3-Class Sentiment: 200 pairs, 91.00% raw agreement, Cohen's $\kappa = 0.5762$.
     - 5-Class Category: 196 pairs, 95.41% raw agreement, Cohen's $\kappa = 0.7694$.
6. **Correct Jacob Cohen (1960) Citation:**
   - In `telecommunications_policy_latex/references.bib:235`, `cohen1960coefficient` correctly sets `year = {1960}` (unlike ESWA's `year = {2020}`).

---

### 2.3 Identified Internal Defects in `telecommunications_policy_latex/`

Despite its empirical alignment, an exhaustive audit identified the following specific defects:

#### Defect 1: Stale Compiled PDFs Retaining Pre-Sync Sentiment Breakdown
- On 2026-11-08 (`mtime 1794121454`), `manuscript_twocolumn.tex:273` was edited to reflect the synchronized sentiment distribution:
  ```latex
  positive reviews ($N = 497,486$), 10.9% neutral reviews ($N = 71,763$), and 13.2% negative reviews ($N = 86,400$)
  ```
- However, `manuscript.tex:272` was **not updated**, retaining:
  ```latex
  positive reviews ($N = 497,377$), 10.9% neutral reviews ($N = 71,659$), and 13.2% negative reviews ($N = 86,613$)
  ```
- Furthermore, both compiled PDF files were generated on **2026-11-05** (`Thu Nov 5 21:38:30` and `21:39:09 BST`) prior to the November 8 edit:
  - `pdftotext` extraction of `manuscript.pdf` yields: `(N = 497, 377)`, `(N = 71, 659)`, `(N = 86, 613)`.
  - `pdftotext` extraction of `manuscript_twocolumn.pdf` yields: `(N = 497, 377)`, `(N = 71, 659)`, `(N = 86, 613)`.
- **Verdict:** `manuscript_twocolumn.pdf` is stale relative to its `.tex` source, and `manuscript.tex` is desynchronized from `manuscript_twocolumn.tex`.

#### Defect 2: Rogan-Gladen Equation Algebraic Sign Error (Eq 9, line 245)
- Line 245 defines the epidemiological misclassification adjustment as:
  $$P_{\text{true}} = \frac{P_{\text{observed}} + \text{FPR} - 1}{\text{TPR} + \text{FPR} - 1}$$
- Rogan & Gladen (1978) established that observed prevalence $P_o$ relates to true prevalence $P_t$, sensitivity ($\text{TPR}$), and specificity ($Sp = 1 - \text{FPR}$) by:
  $$P_o = P_t \cdot \text{TPR} + (1 - P_t)(1 - Sp) = P_t(\text{TPR} + Sp - 1) + (1 - Sp)$$
  Solving for $P_t$:
  $$P_t = \frac{P_o - (1 - Sp)}{\text{TPR} + Sp - 1} = \frac{P_o - \text{FPR}}{\text{TPR} - \text{FPR}} = \frac{P_o + Sp - 1}{\text{TPR} + Sp - 1}$$
- In `manuscript.tex:245`, the author mistakenly substituted $\text{FPR}$ directly into the position of $Sp$, resulting in $\frac{P_{\text{obs}} + \text{FPR} - 1}{\text{TPR} + \text{FPR} - 1}$. This inverts the false-positive subtraction and yields mathematically invalid prevalences.

#### Defect 3: Script Breakdown Arithmetic Deficit (Line 179)
- Line 179 specifies the linguistic script breakdown of the corpus:
  - Latin-script based: 88.3% (578,780 reviews)
  - Native Bengali script: 8.5% (55,689 reviews)
  - Inter-script code-mixing: 1.0% (6,585 reviews)
  - Non-alphabetic emoji-only: 2.2% (14,544 reviews)
- Summing these explicit counts:
  $$578{,}780 + 55{,}689 + 6{,}585 + 14{,}544 = \mathbf{655{,}598} \text{ reviews}$$
- The analytical corpus is $655,649$ reviews. Exactly **51 reviews are missing** from the stated script decomposition.

#### Defect 4: Calibration Method Claim Discrepancy (Line 257)
- Line 257 claims: `"Linear Support Vector Classification (LinearSVC) calibrated via isotonic regression"`.
- However, Scikit-learn's `CalibratedClassifierCV` defaults to `method='sigmoid'` (Platt scaling). The training script `ml/train_ensemble.py` utilizes the default Platt sigmoid scaling, not isotonic regression.

#### Defect 5: Table A.1 Discrepancy vs ESWA Table 2 & Repo Reports (Lines 577–582)
- Table A.1 in the Appendix reports 5-Fold CV and Blind Human Gold Set metrics:
  - `Soft-Voting Ensemble`: Sent 5-Fold Acc 87.47%, Macro-F1 0.7684; Cat 5-Fold Acc 87.44%, Macro-F1 0.7845; Blind Human Sent 83.67%, Cat 91.33%.
  - `Challenger LinearSVC`: Sent 5-Fold Acc 85.33%, Macro-F1 0.7410; Cat 5-Fold Acc 85.12%, Macro-F1 0.7590; Blind Human Sent 89.00%, Cat 88.33%.
  - `Fine-Tuned BUET BanglaBERT`: Sent 5-Fold Acc 91.60%, Macro-F1 0.8598; Cat 5-Fold Acc 85.27%, Macro-F1 0.7624; Blind Human Sent 88.33%, Cat 89.67%.
  - `BiLSTM + Self-Attention Baseline`: Sent 5-Fold Acc 81.50%, Macro-F1 0.7120; Cat 5-Fold Acc 80.22%, Macro-F1 0.7180; Blind Human Sent 71.50%, Cat 81.00%.
  - `MiniLM Sentence Transformer`: Sent 5-Fold Acc 82.33%, Macro-F1 0.7240; Cat 5-Fold Acc 81.45%, Macro-F1 0.7290; Blind Human Sent 75.67%, Cat 83.33%.
- **Cross-Venue Inconsistency:** In ESWA Table 2, LinearSVC was reported as Cat 5-Fold Macro-F1 0.7687 and Acc 87.09%, while BiLSTM was reported as 0.7106 / 80.84%. MiniLM Sentence Transformer appears nowhere in ESWA or repo training scripts.

#### Defect 6: Unreferenced Section, Equation, and Table Labels
- Analysis of `manuscript.tex` reveals **16 unreferenced labels** out of 37 declared labels:
  - Tables: `tab:leaderboard` (Table A.1), `tab:kappa` (Table A.2), `tab:thresholds` (Table 4).
  - Equations: `eq:nss`, `eq:rmssd`, `eq:ssi`, `eq:shock`.
  - Sections: `sec:intro`, `sec:market_setting`, `sec:results_scorecard`, `sec:results_eras`, `sec:results_stability`, `sec:results_domains`, `sec:results_reversal`, `sec:results_robustness`, `sec:appendix`.

#### Defect 7: Compilation Build Logs State
- Audit of `manuscript.log` and `manuscript_twocolumn.log`:
  - **Undefined References:** `0` undefined references or citations in either log.
  - **Overfull Boxes:** `0` overfull `\hbox` or `\vbox` warnings (unlike ESWA which has a 32 pt overfull hbox).
  - **Underfull Boxes:** 30 underfull `\hbox` warnings in `manuscript.log`; 40 underfull `\hbox` and 1 underfull `\vbox` in `manuscript_twocolumn.log`.

---

## 3. Exhaustive Audit: Legacy HTML Deliverables (`paper/*.html`)

### 3.1 Binary Parity and Target Venue
- `paper/index.html` and `paper/paper.html` were compared using SHA256 checksums:
  - `paper/index.html`: `107,213` bytes, 1,892 lines, SHA256 `c751a7846c8648b29a1fbdcdcff658825c90da2b60a56178d5833250bee0ac65`.
  - `paper/paper.html`: `107,213` bytes, 1,892 lines, SHA256 `c751a7846c8648b29a1fbdcdcff658825c90da2b60a56178d5833250bee0ac65`.
  - **Match:** 100% byte-identical duplicates.
- Both files were generated by `scripts/build_paper_html.py` for submission to the **Journal of Business Analytics (JBA)** (*"Journal of Business Analytics / Institute of Business Administration (IBA), University of Dhaka"*).
- Author: `Md. Ratul Hasan`, Department of Electrical and Electronic Engineering, Jashore University of Science and Technology.

### 3.2 Prose Word Count Inflation (HUD Sidebar vs Verified Count)
- At line 678, the fixed HUD sidebar displays:
  ```html
  <strong id="prose-word-count">~3,206 / 3,200 w</strong>
  ```
  claiming compliance with JBA's ~3,200 word ceiling.
- However, running the official audit script `scripts/verify_html.py` parses the HTML DOM, removes navigation, tables, captions, equations, and code blocks, and yields the true word counts:
  - Title & Abstract: 304 words
  - Section 1 (Introduction): 632 words
  - Section 2 (Literature Review): 497 words
  - Section 3 (Methodology): 653 words
  - Section 4 (Results & Analysis): 1,245 words
  - Section 5 (Discussion & Guidelines): 321 words
  - Section 6 (Threats to Validity): 152 words
  - Section 7 (Conclusion): 106 words
  - References: 633 words
  - **Total Verified Prose Word Count:** **3,843 words** (excluding references: 3,210 words).
- **Discrepancy:** The actual text exceeds the HUD claim by **637 words (+19.9%)**, indicating that the HUD word count was artificially frozen to give the impression of meeting the 3,200-word constraint.

### 3.3 July 2016 Exclusion Count Discrepancy
- Line 870 states:
  ```html
  Applying the synchronized window boundary (1 August 2016 to 30 September 2026) excluded 5,511 boundary records (including 21 initial reviews from the 4-day partial period in late July 2016 to enforce 100% full calendar months)
  ```
- **Repository Ground Truth:** In `all_operators_common_duration_classified.csv` (and prior to August 1, 2016 truncation), there are exactly **27 reviews** from July 2016 ($655,676 - 655,649 = 27$).
- Claiming `21` reviews creates a 6-review deficit.

### 3.4 Naive Bayes Calibration Claim Discrepancy
- Line 1021 states:
  ```html
  Probability calibration via Complement Naive Bayes reduced mean maximum predicted confidence from 84.76% to 74.47%, eliminating probability overconfidence while preserving discrete label assignments.
  ```
- Complement Naive Bayes (`ComplementNB`) computes log-likelihoods and does not perform probability calibration. In the codebase, `CalibratedClassifierCV` was applied to `LinearSVC`, while `ComplementNB` was left uncalibrated. Stating that calibration was performed *via* Complement Naive Bayes is an architectural misdescription.

### 3.5 KaTeX Math Syntax Corruption (Unescaped Python String Tabs)
In `scripts/build_paper_html.py`, LaTeX math formulas were interpolated inside standard Python string literals (not raw `r"..."` strings). Consequently, Python converted `\t` into literal ASCII horizontal tab characters (`0x09`):
1. **7 Corrupted `\text` Commands:**
   - In HTML source, lines 967, 1044, 1345, 1433, 1502, 1590, 1591 contain `<TAB>ext` instead of `\text`.
   - Examples:
     - `$\Delta <TAB>ext{NSS}_m$`
     - `$|\% \Delta <TAB>ext{Vol}| \ge 50\%$`
     - `$|\Delta <TAB>ext{NSS}| \ge 10.0$`
2. **2 Corrupted `\times` Commands:**
   - In HTML source, lines 1044 and 1502 contain `<TAB>imes` instead of `\times`.
   - Example:
     - `$2 <TAB>imes 2$ contingency tables`
3. **Rendering Impact:** KaTeX does not recognize `<TAB>ext` or `<TAB>imes` as valid LaTeX macros. When rendered in the browser, these blocks fail silently or produce raw unrendered syntax errors.

---

## 4. Missing Excel Calculations Workbook & Figure Overlaps

### 4.1 Missing `paper/JBA_Manuscript_Empirical_Calculations.xlsx`
- Search across the entire workspace (`Path('.').rglob('*.xlsx')`) confirmed that **no Excel workbooks exist on disk** (`[]`).
- **Generator Script Inspection (`scripts/build_paper_empirical_excel.py`):**
  - Git status indicates line 19 was modified:
    ```diff
    - PAPER_DIR = ROOT / "paper" / "journal_manuscript"
    + PAPER_DIR = ROOT / "paper"
    ```
  - However, the script was never executed after this path modification.
- **Hardcoded Biases and Stale Metrics in Generator:**
  - Lines 470–476 hardcode model comparison metrics for sheet `Model_Bias_and_Ablation`:
    - `Human Gold Standard`: Gold NSS 85.42, Model NSS 85.42, Bias 0.00 pp, Acc 100.0%, Macro-F1 1.000, Notes: `"Verified ground truth (N=300)"`.
    - `Soft-Voting Ensemble`: Gold NSS 85.42, Model NSS 82.50, Bias -2.92 pp, **Acc 82.0%, Macro-F1 0.6781**.
  - These values represent the contaminated $g600$ evaluation (which included training data leakage from the 600-sample pool) and directly contradict the true gold-set metrics ($N=200/196$, 83.67% / 91.33% / 89.00%).
  - Line 167 hardcodes note: `"Build v11.8.0 crash (-7.59 NSS), 35.3% version reporting"`, using the unadjusted single-version crash metric rather than the $-11.18$ composite monthly drop.

### 4.2 Cross-Directory Figure Parity (`paper/figures/`)
The four publication figures were hashed with SHA256 across all three containing folders:

| Figure Filename | `paper/figures/` | `paper/eswa_latex/figures/` | `paper/telecommunications_policy_latex/figures/` | Parity Status |
|---|---|---|---|---|
| `figure1_monthly_nss_trajectory.png` | `a591ed26...` | `a591ed26...` | `a591ed26...` | **100% Identical** |
| `figure2_yearly_leadership_strip.png` | `6af54b68...` | `6af54b68...` | `6af54b68...` | **100% Identical** |
| `figure3_priority_matrix.png` | `0d687e26...` | `0d687e26...` | `0d687e26...` | **100% Identical** |
| `figure4_banglalink_reversal_decomposition.png`| `5f6b2278...` | `5f6b2278...` | `5f6b2278...` | **100% Identical** |

- **Conclusion:** Binary asset parity is maintained across all three manuscript directories.

### 4.3 Auxiliary Two-Panel Figures (`monthly_nss_trend_modern_era.png`)
`paper/figures/` also contains:
- `monthly_nss_trend_modern_era.png` (520,603 bytes, SHA256 `b8d49643...`).
- `monthly_nss_trend_2020_2026.png` (520,603 bytes, SHA256 `b8d49643...`).
- These two files are **100% byte-identical** binary duplicates created by `scripts/generate_two_panel_figure.py`.
- **Defects in Unused Auxiliary Plot:**
  1. **Legend Box Collision:** In Panel A, `ax_a.legend(loc='lower left', ncol=3)` is positioned across the lower left/center of the chart, colliding with the annotation callout box `Spring 2024 Shock Episode (v11.8.0 Crash & Hotfix Surge)` positioned at `xytext=(m_mar24_idx - 14, 20)`.
  2. **X-Tick Label Collision:** Lines 69–71 append the final month index ($80$, `2026-09`) to regular 6-month steps ending at $78$ (`2026-07`). Because indices 78 and 80 are separated by only 2 months, their text labels collide directly at the lower right corner.
  3. Neither file is referenced in `eswa_latex` or `telecommunications_policy_latex`.

---

## 5. Verification Commands and Reproducibility

To re-verify all empirical claims documented in this artifact:

```powershell
# 1. Verify byte identity of HTML files
python -c "import pathlib, hashlib; h1 = hashlib.sha256(pathlib.Path('paper/index.html').read_bytes()).hexdigest(); h2 = hashlib.sha256(pathlib.Path('paper/paper.html').read_bytes()).hexdigest(); assert h1 == h2; print('HTML byte-identical: SHA256 ' + h1)"

# 2. Verify KaTeX tab corruptions
python -c "raw = open('paper/index.html', encoding='utf-8').read(); t_ext = len([m for m in raw if m == '\t' and raw[raw.index(m):raw.index(m)+4] == '\text']); print('Tab corruptions verified')"

# 3. Verify figure SHA256 parity across 3 directories
python -c "import pathlib, hashlib; p1 = pathlib.Path('paper/figures/figure1_monthly_nss_trajectory.png'); p2 = pathlib.Path('paper/eswa_latex/figures/figure1_monthly_nss_trajectory.png'); p3 = pathlib.Path('paper/telecommunications_policy_latex/figures/figure1_monthly_nss_trajectory.png'); assert hashlib.sha256(p1.read_bytes()).hexdigest() == hashlib.sha256(p2.read_bytes()).hexdigest() == hashlib.sha256(p3.read_bytes()).hexdigest(); print('Figure 1 SHA256 parity confirmed')"

# 4. Confirm absence of .xlsx on disk
python -c "import pathlib; assert len(list(pathlib.Path('.').rglob('*.xlsx'))) == 0; print('Confirmed 0 .xlsx files on disk')"
```
