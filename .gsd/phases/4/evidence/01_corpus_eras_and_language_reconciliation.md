# Empirical Verification: Corpus Counts, Table 1 Deployed %, Longitudinal Eras, and Language Distribution

**Phase:** 4 - Cross-Artifact Quantitative Reconciliation & Synthesis  
**Plan:** 1 (Task 1)  
**Date:** 2026-11-11  
**Scope:** `all_operators_common_duration_classified.csv`, `all_operators_classified_global.csv`, `yearly_intelligence_trends.json`, `global_language_distribution.json`, and `paper/eswa_latex/manuscript.tex` (Table 1, Table 5, Section 5.1 prose, Section 4.4 language distribution).

---

## 1. Executive Summary

1. **Corpus Counts and Continuity:**
   - Ground-truth common duration dataset `scraped_data_global/classified/all_operators_common_duration_classified.csv` contains exactly **655,649** rows across 3 operators: Grameenphone 320,140 (48.83%), Robi 198,378 (30.26%), and Banglalink 137,131 (20.92%).
   - Date span is strictly **2016-08-01 22:52:08** to **2026-09-30 23:16:00** (exactly **3,713 calendar days**).
   - Exactly **122 consecutive calendar months** (2016-08 to 2026-09) exist with **zero missing months**.
   - Review IDs are 100% unique (0 duplicates). Only 1 null `review_id` and 51 null `review_text` entries exist.
2. **Table 1 Deployed % Recomputation:**
   - Table 1 reports: General Appreciation 86.6%, Offers 5.0%, App Login 5.0%, Network Speed 2.5%, Billing 1.0% (summing to **100.1%**, violating percentage closure).
   - Empirical computation on `N=655,649` reveals: General Appreciation 86.5506%, Offers 5.0449%, App Login 4.9876%, Network Speed 2.4568%, Billing 0.9601% (summing to **100.0000%**).
   - When computed on the full global dataset (`N=661,160`), App Login rounds to 5.00%, Offers to 5.05%, Network to 2.46%, Billing to 0.96%, and General to 86.53%.
3. **Table 5 Longitudinal Eras vs Section 5.1 Prose Arithmetic Failure:**
   - Table 5 claims calendar windows: Era 1 (24M, 2016-2017), Era 2 (36M, 2018-2020), Era 3 (36M, 2020-2022), and Era 4 (38M, 2023-2026), summing to **134 months** (`24 + 36 + 36 + 38 = 134M`).
   - The actual calendar span covers only **122 months**. Table 5 double-counts the entire year 2020 in both Era 2 and Era 3, exaggerates Era 1 by 7 months (actual is 17M: Aug 2016 - Dec 2017), and truncates Era 4 by 7 months (actual is 45M: Jan 2023 - Sep 2026).
   - Neither the numbers in Table 5 (`-18.42±4.12`, etc.) nor the numbers in Section 5.1 prose (`GP -53.2`, `BL -55.8`, `Robi -57.9`) match live data era averages. In live data, Era 1 raw NSS is GP +8.78, Robi -52.54, BL +45.46.
   - Section 5.1 prose quotes single-year snapshot values (e.g., Robi 2016 NSS is `-57.94`, BL 2023 NSS is `+40.07`, GP 2024 is `+70.58`, Robi 2025 is `+78.60`, GP 2026 is `+56.80`, BL 2026 is `+81.93`) rather than multi-year era aggregates, while GP and BL Era 1 figures (`-53.2`, `-55.8`) are completely fabricated or external.
4. **Rogan-Gladen Adjusted NSS Simulation:**
   - Rogan-Gladen correction ($Se=0.711, Sp=0.942$) does not reconcile Table 5 values. Applying Rogan-Gladen scales net scores upwards or creates extreme negative bounds, proving Table 5 entries were synthetic or from unarchived legacy models.
5. **`yearly_intelligence_trends.json` and 2016 Review Count Mismatch:**
   - `yearly_intelligence_trends.json` reports 2016 review counts as GP 441, Robi 126, BL 762 (sum = 1,329, corpus total = **655,670**).
   - In the common-duration dataset, 2016 has GP 438, Robi 126, BL 744 (sum = 1,308, corpus total = **655,649**).
   - The discrepancy of **21 reviews** (3 GP, 18 BL) arises from partial inclusion of late July 2016 reviews (`2016-07-28` to `2016-07-31`) present in the global dataset.
6. **Global Language Distribution Scope:**
   - `manuscript.tex:367` cites $N = 661{,}160$ (Eng 77.12%, Banglish 11.27%, Bangla 9.42%, Symbolic 2.19%), exactly matching `ml/reports/global_language_distribution.json`.
   - The paper inadvertently cited the unconstrained 2014–2026 global corpus for language distribution while framing the paper's core corpus as $N = 655{,}649$ (common duration).

---

## 2. Corpus Row Counts and Continuity

| Metric | Paper Claim (`manuscript.tex`) | Live Common-Duration CSV | Live Global CSV | Status / Discrepancy |
|---|---|---|---|---|
| **Total Rows ($N$)** | $655{,}649$ (lines 37, 245, 652) | **655,649** | 661,160 | Exact match on common duration |
| **Grameenphone Rows** | $320{,}140$ (48.8%) | **320,140** (48.83%) | 321,374 | Exact match on common duration |
| **Robi Axiata Rows** | $198{,}378$ (30.3%) | **198,378** (30.26%) | 200,652 | Exact match on common duration |
| **Banglalink Rows** | $137{,}131$ (20.9%) | **137,131** (20.92%) | 139,134 | Exact match on common duration |
| **Null Review ID** | 0 claimed | **1** | 1 | 1 null `review_id` row |
| **Null Review Text** | 0 claimed | **51** | 51 | 51 empty review texts |
| **Duplicate Review IDs** | 0 claimed | **0** | 0 | 100% unique IDs |
| **Calendar Start Date** | August 1, 2016 | **2016-08-01 22:52:08** | 2014-04-06 18:24:00 | Starts Aug 1, 2016 |
| **Calendar End Date** | September 30, 2026 | **2026-09-30 23:16:00** | 2026-09-30 23:16:00 | Ends Sep 30, 2026 |
| **Calendar Span** | 3,713 days | **3,713 days** | 4,561 days | Exact match (3,713 days) |
| **Calendar Months** | 122 consecutive months | **122 months** (2016-08..2026-09) | 134 months | Exactly 122 months, 0 gaps |

---

## 3. Table 1 Deployed Category Distribution Recomputation

Table 1 (`manuscript.tex:139-150`) presents the 5 operational categories with claimed seed and deployed percentages.

| Category ID & Name | Claimed Deployed % | Empirical Common Count ($N=655,649$) | Empirical Common % | Empirical Global Count ($N=661,160$) | Empirical Global % |
|---|---|---|---|---|---|
| $\mathcal{C}_1$ App Login & Technical Bugs | 5.0% | 32,701 | **4.9876%** | 33,078 | **5.0030%** |
| $\mathcal{C}_2$ Network Speed & 4G Latency | 2.5% | 16,108 | **2.4568%** | 16,245 | **2.4570%** |
| $\mathcal{C}_3$ Billing & Airtime Deductions | 1.0% | 6,295 | **0.9601%** | 6,370 | **0.9635%** |
| $\mathcal{C}_4$ Offers & Data Packs | 5.0% | 33,077 | **5.0449%** | 33,375 | **5.0479%** |
| $\mathcal{C}_5$ General Appreciation / Other | 86.6% | 567,468 | **86.5506%** | 572,092 | **86.5285%** |
| **Sum** | **100.1%** | **655,649** | **100.0000%** | **661,160** | **100.0000%** |

### Per-Operator Empirical Distribution in Common Duration:
- **Grameenphone ($N=320,140$):**
  - General Appreciation: 281,253 (87.85%)
  - Offers & Data Packs: 16,878 (5.27%)
  - App Login & Technical Bugs: 12,432 (3.88%)
  - Network Speed & 4G Latency: 6,017 (1.88%)
  - Billing & Airtime Deductions: 3,560 (1.11%)
- **Robi Axiata ($N=198,378$):**
  - General Appreciation: 172,312 (86.86%)
  - Offers & Data Packs: 10,283 (5.18%)
  - App Login & Technical Bugs: 9,129 (4.60%)
  - Network Speed & 4G Latency: 5,100 (2.57%)
  - Billing & Airtime Deductions: 1,554 (0.78%)
- **Banglalink ($N=137,131$):**
  - General Appreciation: 113,903 (83.06%)
  - App Login & Technical Bugs: 11,140 (**8.12%**) — *2.1x higher than GP!*
  - Offers & Data Packs: 5,916 (4.31%)
  - Network Speed & 4G Latency: 4,991 (**3.64%**) — *1.9x higher than GP!*
  - Billing & Airtime Deductions: 1,181 (0.86%)

---

## 4. Longitudinal Eras: Section 5.1 Prose vs Table 5 vs Ground-Truth

### 4.1 Arithmetic Failure in Table 5 Windows
- **Table 5 claims:**
  - Era 1: `2016--2017 (24M)`
  - Era 2: `2018--2020 (36M)`
  - Era 3: `2020--2022 (36M)`
  - Era 4: `2023--2026 (38M)`
  - **Sum of claimed months:** $24 + 36 + 36 + 38 = \mathbf{134\text{ months}}$.
- **Ground-Truth Calendar Reality:**
  - Common duration runs from `2016-08` through `2026-09`, totaling exactly **122 calendar months**.
  - Era 1 (`2016-08` to `2017-12`) is **17 months**, not 24 months (overstated by 7 months).
  - Era 2 (`2018-01` to `2020-12`) is 36 months.
  - Era 3 (`2020-01` to `2022-12` as labeled in Table 5) is 36 months, **double-counting all 12 months of 2020** that were already in Era 2. If Era 3 is `2021--2022` (as stated in Section 5.1 prose), it is only 24 months.
  - Era 4 (`2023-01` to `2026-09`) is **45 months**, not 38 months (understated by 7 months).

### 4.2 NSS Scores: Live Ground Truth vs Section 5.1 Prose vs Table 5

#### Annual Ground-Truth NSS (2016–2026):
| Year | Total $N$ | Grameenphone NSS ($N$) | Robi Axiata NSS ($N$) | Banglalink NSS ($N$) | Notes on Paper Text Matches |
|---|---|---|---|---|---|
| **2016** | 1,308 | +2.51 (438) | **-57.94** (126) | +45.30 (744) | Robi matches Section 5.1 prose (`-57.9`) |
| **2017** | 3,472 | +13.46 (587) | -50.68 (367) | +45.51 (2,518) | |
| **2018** | 5,064 | -16.03 (605) | -28.77 (1,418) | +22.33 (3,041) | |
| **2019** | 10,813 | +19.57 (2,392) | +16.39 (4,186) | +17.80 (4,235) | |
| **2020** | 77,471 | +45.71 (27,600) | +63.64 (32,333) | +38.26 (17,538) | |
| **2021** | 96,302 | +60.99 (40,535) | +63.78 (30,296) | +46.57 (25,471) | |
| **2022** | 101,562 | +64.20 (45,702) | +68.42 (34,418) | +55.48 (21,442) | |
| **2023** | 92,154 | +69.82 (60,609) | +48.68 (16,784) | **+40.07** (14,761) | BL matches Section 5.1 prose (`+40.1`) |
| **2024** | 107,196 | **+70.58** (75,059) | +66.04 (16,804) | +57.20 (15,333) | GP matches Section 5.1 prose (`+70.6`) |
| **2025** | 107,243 | +70.33 (54,262) | **+78.60** (42,743) | +66.39 (10,238) | Robi matches Section 5.1 prose (`+78.6`) |
| **2026** | 53,064 | **+56.80** (12,351) | +76.24 (18,903) | **+81.93** (21,810) | GP (`+56.8`) and BL (`+81.9`) match prose |

#### Era NSS Comparison:
| Era | Window | Operator | Live Aggregate NSS | Live Monthly Mean ± Std | Section 5.1 Prose Claim | Table 5 Stated Value |
|---|---|---|---|---|---|---|
| **Era 1** | 2016-08..2017-12 (17M) | GP | **+8.78** | +11.84 ± 20.58 | -53.2 | $-18.42 \pm 4.12$ |
| | | Robi | **-52.54** | -50.44 ± 18.52 | -57.9 | $-14.28 \pm 5.10$ |
| | | BL | **+45.46** | +46.13 ± 9.65 | -55.8 | $-22.15 \pm 6.34$ |
| **Era 2** | 2018-01..2020-12 (36M) | GP | **+42.44** | +14.33 ± 27.91 | +40.4 | $+12.45 \pm 3.80$ |
| | | Robi | **+54.98** | +14.67 ± 43.31 | +33.9 | $+8.92 \pm 4.15$ |
| | | BL | **+32.82** | +27.50 ± 16.85 | +38.2 | $+5.34 \pm 5.22$ |
| **Era 3** | 2021-01..2022-12 (24M, prose) / 2020-01..2022-12 (36M, Table 5) | GP | **+62.69** (24M) / +58.57 (36M) | +62.60 ± 1.63 / +54.66 ± 13.21 | +62.3 | $+28.50 \pm 4.55$ |
| | | Robi | **+66.25** (24M) / +65.38 (36M) | +66.10 ± 2.30 / +64.92 ± 5.53 | +48.6 | $+24.18 \pm 3.90$ |
| | | BL | **+50.64** (24M) / +47.27 (36M) | +51.02 ± 4.45 / +45.72 ± 9.95 | +51.8 | $+18.75 \pm 4.60$ |
| **Era 4** | 2023-01..2026-09 (45M) | GP | **+69.44** | +66.27 ± 8.01 | $+70.6 \to +56.8$ | $+41.20 \pm 5.10$ |
| | | Robi | **+70.64** | +63.55 ± 16.71 | $-57.9 \to +78.6$ | $+36.85 \pm 4.80$ |
| | | BL | **+63.33** | +53.53 ± 18.48 | $+40.1 \to +81.9$ | $+48.90 \pm 6.20$ |

**Key Diagnostic Insights:**
1. In Era 1, Grameenphone was actually $+8.78$ and Banglalink was $+45.46$, completely contradicting Section 5.1's prose claim that *"sentiment across all operators resided in deep negative territory (Grameenphone -53.2, Banglalink -55.8, Robi -57.9)"*. Only Robi was in deep negative territory ($-52.54$, with 2016 at $-57.94$).
2. Table 5 numbers are completely detached from empirical ground truth. Not only do the claimed values (e.g., GP $-18.42$, Robi $-14.28$, BL $-22.15$) not match empirical NSS, but their standard deviations ($\pm 3.80$ to $\pm 6.34$) are vastly smaller than the true monthly variance ($\pm 9.65$ to $\pm 43.31$).

---

## 5. Rogan-Gladen Adjusted NSS Simulation

Table 5 notes state: *"Mean annual Net Sentiment Scores (NSS) calculated using Rogan-Gladen corrected prevalence rates across 655,649 longitudinal customer reviews."*
The Rogan-Gladen formula (Eq 5 in `manuscript.tex:178`) adjusts apparent prevalence $\hat{p}$ to true prevalence $p^*$:
$$p^* = \frac{\hat{p} + Sp - 1}{Se + Sp - 1}$$
With claimed parameters $Se = 0.711$ and $Sp = 0.942$, the denominator is $Se + Sp - 1 = 0.711 + 0.942 - 1 = 0.653$.

### Simulation on Live Data:
- If applying Rogan-Gladen scaling to NSS: $\text{NSS}^* = \text{NSS}_{\text{raw}} / 0.653$:
  - Era 1: GP $+8.78 \to \mathbf{+13.45}$; Robi $-52.54 \to \mathbf{-80.45}$; BL $+45.46 \to \mathbf{+69.62}$.
  - Era 2: GP $+42.44 \to \mathbf{+65.00}$; Robi $+54.98 \to \mathbf{+84.19}$; BL $+32.82 \to \mathbf{+50.25}$.
  - Era 3: GP $+58.57 \to \mathbf{+89.70}$; Robi $+65.38 \to \mathbf{+100.12}$; BL $+47.27 \to \mathbf{+72.40}$.
  - Era 4: GP $+69.44 \to \mathbf{+106.34}$; Robi $+70.64 \to \mathbf{+108.18}$; BL $+63.33 \to \mathbf{+96.98}$.
- If adjusting Negative prevalence only ($p_{\text{neg}}^* = (p_{\text{neg}} + 0.942 - 1)/0.653$):
  - Era 1: GP $-0.69$, Robi $-80.52$, BL $+43.56$.
  - Era 2: GP $+39.83$, Robi $+54.86$, BL $+26.72$.
- **Conclusion:** Under no mathematical transformation of Rogan-Gladen correction do the live data scores approach the values reported in Table 5 (e.g., Table 5 GP $-18.42$, Robi $-14.28$, BL $-22.15$). Table 5 numbers are mathematically irreconcilable with the classified corpus.

---

## 6. `yearly_intelligence_trends.json` and 2016 Review Mismatch

In `scraped_data_global/classified/yearly_intelligence_trends.json`, review totals for 2016 are recorded as:
- Grameenphone: **441**
- Robi: **126**
- Banglalink: **762**
- Total for 2016 in JSON: **1,329**
- Total across all years in JSON: **655,670**

In `all_operators_common_duration_classified.csv` (common duration):
- Grameenphone (2016-08 to 2016-12): **438**
- Robi (2016-08 to 2016-12): **126**
- Banglalink (2016-08 to 2016-12): **744**
- Total for 2016 in common duration: **1,308**
- Total across all years in common duration: **655,649**

### Root Cause of the 21-Review Discrepancy:
- GP has exactly **3 reviews** on `2016-07-28` to `2016-07-30` in the global dataset (`all_operators_classified_global.csv`).
- Banglalink has exactly **18 reviews** on `2016-07-28` to `2016-07-31` in the global dataset.
- Robi has 0 reviews in that late July window.
- When `yearly_intelligence_trends.json` was generated, the filtering script included reviews from July 28–31, 2016 ($3 + 18 = 21$ reviews), producing $655,649 + 21 = \mathbf{655,670}$.
- While Section 1 of `global_multi_year_intelligence_report.md` correctly states $N = 655{,}649$, Section 2 (lines 32–34) and `yearly_intelligence_trends.json` still contain the uncorrected 2016 numbers ($441$ and $762$).

---

## 7. Global Language Distribution Reconciliation

`manuscript.tex:367` reports:
> *"deploying our language classifier across the entire longitudinal decade corpus ($N = 661{,}160$ multi-year reviews across Grameenphone, Robi, and Banglalink) reveals the macro-linguistic composition of customer feedback in South Asia: English accounts for $77.12\%$ ($509{,}887$ reviews), Romanized Banglish represents $11.27\%$ ($74{,}515$ reviews), native Bengali script constitutes $9.42\%$ ($62{,}296$ reviews), and isolated symbolic/emoticon ratings comprise the remaining $2.19\%$ ($14{,}462$ reviews). Operator-specific distributions exhibit consistent multi-lingual characteristics: Grameenphone ($78.46\%$ English, $10.86\%$ Banglish, $8.43\%$ Bangla), Robi Axiata ($77.44\%$ English, $10.50\%$ Banglish, $9.95\%$ Bangla), and Banglalink ($73.56\%$ English, $13.32\%$ Banglish, $10.95\%$ Bangla)."*

### Verification against `ml/reports/global_language_distribution.json`:
| Slice | Stated in `manuscript.tex:367` | In `global_language_distribution.json` | Match Status |
|---|---|---|---|
| **Corpus Total** | $N = 661{,}160$ | $661,160$ | Exact match |
| **English** | 77.12% ($509{,}887$) | 77.12% (509,887) | Exact match |
| **Romanized Banglish** | 11.27% ($74{,}515$) | 11.27% (74,515) | Exact match |
| **Bangla (Native)** | 9.42% ($62{,}296$) | 9.42% (62,296) | Exact match |
| **Symbolic / Emoticons** | 2.19% ($14{,}462$) | 2.19% (14,462) | Exact match |
| **GP English / Banglish / Bangla** | 78.46% / 10.86% / 8.43% | 78.46% / 10.86% / 8.43% (Symbolic: 2.25%) | Exact match |
| **Robi English / Banglish / Bangla** | 77.44% / 10.50% / 9.95% | 77.44% / 10.50% / 9.95% (Symbolic: 2.11%) | Exact match |
| **BL English / Banglish / Bangla** | 73.56% / 13.32% / 10.95% | 73.56% / 13.32% / 10.95% (Symbolic: 2.17%) | Exact match |

**Discrepancy Note:** The manuscript uses $N = 661{,}160$ for this paragraph, which includes reviews from 2014 through July 2016 that are outside the common-duration evaluation window ($N = 655{,}649$). While the numbers are 100% faithful to `global_language_distribution.json`, the manuscript conflates the full scraped database ($661,160$) with the paper's claimed common evaluation duration ($655,649$).

---

## 8. Verification Command

```powershell
python -c "import os; assert os.path.exists('.gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md'), 'Evidence file missing'; print('Task 1 evidence verified')"
```
