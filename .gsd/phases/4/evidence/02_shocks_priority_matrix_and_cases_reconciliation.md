# Empirical Verification: Econometric Shocks, Contingency Statistics, Priority Matrix, Case Studies, and Decision Framework

**Phase:** 4 - Cross-Artifact Quantitative Reconciliation & Synthesis  
**Plan:** 1 (Task 2)  
**Date:** 2026-11-11  
**Scope:** `all_operators_common_duration_classified.csv`, `nss_significant_shocks.csv`, `nss_stability_and_shocks_summary.json`, `shock_grievance_statistical_evidence.json`, `scripts/verify_section42_stats.py`, `scripts/point4_prop2_by_operator.py`, and `paper/eswa_latex/manuscript.tex` (Section 5.2, Table 6, Section 5.3, Figure 3, Section 5.4, Tables 7 & 8).

---

## 1. Executive Summary

1. **Modern Shocks Recomputation (35 vs 37 vs 98):**
   - Filtering the common-duration dataset for the modern era (2020-01 to 2026-09) yields exactly **240 intra-era monthly transitions** (80 per operator).
   - Exactly **35 transitions** meet the acute shock criterion ($|\Delta\text{NSS}| \ge 10.0$ points): Grameenphone **6**, Robi Axiata **7**, and Banglalink **22**.
   - `nss_stability_and_shocks_summary.json` reports **37 modern shocks** because it included the inter-era boundary transition `2019-12 \to 2020-01` (GP: $-14.2$ pts, Robi: $+55.2$ pts).
   - `nss_significant_shocks.csv` contains **98 shocks** across the full decade (2016–2026).
2. **Table 6 Prominent Shocks Verification (7 Phantom Shocks):**
   - **Rows 1 & 2** (Banglalink `2024-04` and `2024-05`): Exact empirical match to ground truth ($\Delta\text{NSS} = -11.18$ and $+32.78$, with identical 5-class additive decompositions).
   - **Row 10** (Banglalink `2026-01`): Labeled as monthly shock with $\Delta\text{NSS} = +15.5$ and $\Delta\text{Gen} = +10.3$, but true monthly transition `2025-12 \to 2026-01` was actually $\mathbf{\Delta\text{NSS} = +48.15}$ ($\Delta\text{Gen} = +30.26$, $\Delta\text{Login} = +12.00$). The $+15.54$ figure was an annual/partial decomposition conflated into a monthly table.
   - **Rows 3–9** (GP `2022-09`, GP `2023-03`, Robi `2021-11`, Robi `2022-04`, GP `2024-01`, BL `2023-08`, Robi `2024-07`): **All 7 transitions were non-shocks** ($|\Delta\text{NSS}| < 10.0$ pts). Actual transitions ranged from $-7.46$ to $+9.06$ pts (e.g., GP `2022-09` was $+2.83$ vs claimed $-24.5$; Robi `2021-11` was $+0.07$ vs claimed $-19.8$). Their claimed deltas are completely phantom values.
3. **2x2 Contingency Statistics & Asymmetric Operator Attribution:**
   - Client App Login leads in **27 of 35 shocks (77.14%)** vs **91 of 205 non-shocks (44.39%)**.
   - Pearson $\chi^2(1) = 12.8317$ ($p = 0.00034$), Yates corrected $\chi^2(1) = 11.5547$ ($p = 0.00068$), Fisher's exact test $\text{OR} = 4.2280$ ($p = 0.00040$), and Relative Risk $= 1.7378$ (95% CI $[1.37, 2.20]$).
   - In non-surge transitions ($|\Delta V| < 50\%$), App Login leads in **14 of 19 shocks (73.68%)** vs **82 of 189 non-shocks (43.39%)**, with $\chi^2(1) = 6.38$ ($p = 0.0116$) and $\text{OR} = 3.65$ ($p = 0.0150$).
   - **Crucial Asymmetry Finding:** This relationship is driven almost entirely by Banglalink (20/22 shocks login-led, $\text{OR} = 10.00, p = 0.0007$). For Grameenphone (3/6 shocks, $p = 0.6866$) and Robi (4/7 shocks, $p = 0.6949$), the software dominance hypothesis is statistically insignificant.
4. **Section 5.3 Priority Matrix ($N=88,181$ vs $88,184$):**
   - Total functional reviews in `all_operators_common_duration_classified.csv` is **88,181**, matching `manuscript.tex:488` exactly.
   - Scripts `verify_paper_complete.py:43` and `audit_paper_contradictions.py:23` erroneously claimed the paper said 88,184 due to a hardcoded script string.
   - Statistical metrics match ground truth: $\chi^2(3) = 11{,}027.60, p < 0.0001, \text{Cramér's } V = 0.3536$.
   - Odds Ratios relative to Offers: Billing $\text{OR} = 9.49$ ($[8.64, 10.42]$), App Login $\text{OR} = 6.44$ ($[6.18, 6.70]$), App Login vs Network $\text{OR} = 2.57$ ($[2.45, 2.70]$).
5. **Case Studies 1 & 2 vs Telemetry:**
   - **Case Study 1:** Claims May 2024 release of `v11.8.0` collapsed NSS by $-32.8$ points ($+65.2 \to +32.4$) and `v11.9.1` restored $+32.8$ points. Ground truth shows the $-11.2$ drop occurred in April 2024 ($+42.8 \to +31.6$), and May 2024 was the $+32.8$ rebound ($+31.6 \to +64.4$). In addition, 51.8% of BL reviews have null `app_version`, and `v11.8.0` represents only 198 reviews.
   - **Case Study 2:** Banglalink 2026 volume doubled (21,810 vs 10,238, 2.13x), NSS surged ($+53.0 \to +81.9$), but decomposition numbers diverge between Section 5.4 prose (Gen $+6.95$ pts, 57.4%) and Table 6 Row 10 (Gen $+10.33$ pts, 66.5%).
6. **Decision Framework (Tables 7 & 8):**
   - Empirical baseline defect rate $p_{\text{base}} = 0.04416$ (4.42%), close to claimed $0.046$. However, operator baselines vary widely: GP 3.45%, Robi 4.01%, BL 7.25% (2.1x higher), creating structural false alarm bias if a uniform threshold is deployed.
   - Across the 240 modern transitions: Level 1 covers 147 (61.3%), Level 2 covers 58 (24.2%), Level 3 covers 15 negative shocks (6.2%), and Level 4 covers 13 promotional surges (5.4%). Zero trace simulation code exists in the repository.

---

## 2. 35 Econometric Shocks & Table 6prominent Shocks Ground Truth

### 2.1 Shock Distribution Across Operators (2020–2026)
Across the 240 intra-era transitions ($80 \times 3$ operators), shocks ($|\Delta\text{NSS}| \ge 10.0$ pp) are distributed as:
- **Grameenphone:** 6 shocks (7.5% shock rate)
- **Robi Axiata:** 7 shocks (8.75% shock rate)
- **Banglalink:** 22 shocks (27.50% shock rate)
- **Total:** **35 acute shocks** (14.58% of all transitions)

### 2.2 Complete Evaluation of All 10 Table 6 Rows Against Live Ground Truth

| Row | Operator | Date | Claimed $\Delta\text{NSS}$ | Claimed Primary Driver | Claimed Deltas (Login, Net, Bill, Offer, Gen) | Ground Truth $\Delta\text{NSS}$ | True Is Shock? | Ground Truth Deltas (Login, Net, Bill, Offer, Gen) | Status / Discrepancy |
|---|---|---|---|---|---|---|---|---|---|
| **1** | Banglalink | 2024-04 | $-11.2$ | App Login | **-8.7**, +1.6, +0.8, +1.1, -5.9 | **-11.18** | **True** | **-8.74**, +1.59, +1.07, +0.77, -5.87 | **Exact Match** |
| **2** | Banglalink | 2024-05 | $+32.8$ | App Login | **+13.7**, +1.0, +0.4, +0.3, +17.4 | **+32.78** | **True** | **+13.73**, +0.96, +0.32, +0.39, +17.38 | **Exact Match** |
| **3** | Grameenphone | 2022-09 | $-24.5$ | Offers | +1.2, -3.4, -2.1, **-18.2**, -2.0 | **+2.83** | **False** | +0.29, +0.05, -0.06, +0.04, +2.51 | **Phantom Shock** ($|\Delta| < 10$) |
| **4** | Grameenphone | 2023-03 | $+18.2$ | Offers | +0.8, +1.1, +0.5, **+12.4**, +3.4 | **-0.15** | **False** | -0.14, -0.23, +0.03, +0.47, -0.29 | **Phantom Shock** ($|\Delta| < 10$) |
| **5** | Robi Axiata | 2021-11 | $-19.8$ | Network | -0.5, **-16.4**, -1.2, +0.2, -1.9 | **+0.07** | **False** | +0.34, +0.14, +0.03, -0.67, +0.23 | **Phantom Shock** ($|\Delta| < 10$) |
| **6** | Robi Axiata | 2022-04 | $+15.4$ | Network | +0.2, **+11.8**, +0.8, +0.4, +2.2 | **+0.79** | **False** | -0.48, +0.13, -0.30, +0.60, +0.84 | **Phantom Shock** ($|\Delta| < 10$) |
| **7** | Grameenphone | 2024-01 | $-14.2$ | App Login | **-11.5**, -0.8, -0.4, -0.2, -1.3 | **-7.46** | **False** | -0.34, -0.09, -0.95, -0.84, -5.24 | **Phantom Shock** ($|\Delta| < 10$) |
| **8** | Banglalink | 2023-08 | $-16.4$ | Billing | +0.4, -2.1, **-12.8**, -0.5, -1.4 | **+9.06** | **False** | +1.49, +1.33, +0.35, +0.10, +5.79 | **Phantom Shock** ($|\Delta| < 10$) |
| **9** | Robi Axiata | 2024-07 | $-28.4$ | Network | -1.2, **-22.1**, -1.8, -0.4, -2.9 | **-5.24** | **False** | -1.42, -0.38, -0.93, +0.80, -3.32 | **Phantom Shock** ($|\Delta| < 10$) |
| **10** | Banglalink | 2026-01 | $+15.5$ | Dual-Track | **+2.8**, +1.1, +0.4, +1.0, **+10.3** | **+48.15** | **True** | **+12.00**, +2.59, +0.77, +2.52, **+30.26** | **Conflated Transition** |

---

## 3. 2x2 Contingency Tables & Statistical Proof of Software Dominance

### 3.1 All 240 Modern Transitions
| Transition Category | App Login Leading Driver | Other Operational Driver Leading | Total Transitions |
|---|---|---|---|
| **Acute Shocks ($|\Delta\text{NSS}| \ge 10.0$)** | **27** (77.14%) | **8** (22.86%) | **35** |
| **Non-Shocks ($|\Delta\text{NSS}| < 10.0$)** | **91** (44.39%) | **114** (55.61%) | **205** |
| **Total** | **118** (49.17%) | **122** (50.83%) | **240** |

- **Pearson Chi-Square:** $\chi^2(1) = 12.8317, p = 0.000341$ (Matches paper $\chi^2(1) = 12.83, p = 0.0003$)
- **Yates Continuity Corrected:** $\chi^2(1) = 11.5547, p = 0.000676$ (Matches paper $\chi^2(1) = 11.55, p = 0.0007$)
- **Fisher's Exact Test:** Odds Ratio $= 4.2280, p = 0.000404$ (Matches paper $\text{OR} = 4.23, p = 0.0004$)
- **Confidence Intervals:**
  - Woolf Logit 95% CI: $[1.8331, 9.7516]$
  - Conditional MLE Profile 95% CI: $[1.78, 10.51]$ (Matches paper stated interval $[1.78, 10.51]$)
- **Relative Risk (RR):** $RR = 1.7378$ (95% CI: $[1.3716, 2.2018]$) (Matches paper $RR = 1.74$)

### 3.2 Non-Surge Transitions Only ($|\Delta V| < 50\%$)
| Transition Category | App Login Leading Driver | Other Operational Driver Leading | Total Transitions |
|---|---|---|---|
| **Non-Surge Shocks** | **14** (73.68%) | **5** (26.32%) | **19** |
| **Non-Surge Non-Shocks** | **82** (43.39%) | **107** (56.61%) | **189** |
| **Total Non-Surge** | **96** (46.15%) | **112** (53.85%) | **208** |

- **Pearson Chi-Square:** $\chi^2(1) = 6.38, p = 0.0116$ (Exact match)
- **Fisher's Exact Test:** Odds Ratio $= 3.65, p = 0.0150$ (Exact match)

### 3.3 Operator-by-Operator Disaggregation (Critical Empirical Discovery)
When disaggregating the pooled 2x2 contingency table by operator, the relationship differs dramatically:
- **Grameenphone:** Shocks $3/6$ (50.0%) vs Non-shocks $30/74$ (40.5%), Fisher $\text{OR} = 1.47, p = 0.6866$ (**Not Significant**).
- **Robi Axiata:** Shocks $4/7$ (57.1%) vs Non-shocks $32/73$ (43.8%), Fisher $\text{OR} = 1.71, p = 0.6949$ (**Not Significant**).
- **Banglalink:** Shocks $20/22$ (90.9%) vs Non-shocks $29/58$ (50.0%), Fisher $\text{OR} = 10.00, p = 0.0007$ (**Highly Significant**).
- **Implication:** The "cross-layer software dominance" conclusion in ESWA Section 5.2 is essentially an artifact of Banglalink's severe application instability. The paper claims this as a universal industry phenomenon across all three operators, but the statistical significance vanishes for GP and Robi.

---

## 4. Section 5.3 Priority Matrix Verification ($N=88,181$)

### 4.1 Sample Size and Category Breakdown
- Live row count in `all_operators_common_duration_classified.csv` across the 4 functional categories: exactly **88,181** (Matches `manuscript.tex:488`).
  - App Login & Technical Bugs: **32,701** (37.08% within domain; 4.99% of total corpus)
  - Offers & Data Packs: **33,077** (37.51% within domain; 5.04% of total corpus)
  - Network Speed & 4G Latency: **16,108** (18.27% within domain; 2.46% of total corpus)
  - Billing & Airtime Deductions: **6,295** (7.14% within domain; 0.96% of total corpus)
- Operator Breakdown of $N=88,181$:
  - Grameenphone: **38,887**
  - Robi Axiata: **26,066**
  - Banglalink: **23,228**

### 4.2 Statistical Significance & Odds Ratios
- **Omnibus Test:** $\chi^2(3) = 11{,}027.60, \text{dof} = 3, p < 0.0001, \text{Cramér's } V = 0.3536$ (Matches `manuscript.tex:488` exactly).
- **Odds Ratios vs Offers & Data Packs (Baseline Negativity: 54.56%):**
  - **Billing & Airtime Deductions:** $\text{OR} = 9.49$ (95% CI: $[8.64, 10.42]$) (Negativity: 91.93%) — Exact match.
  - **App Login & Technical Bugs:** $\text{OR} = 6.44$ (95% CI: $[6.18, 6.70]$) (Negativity: 88.54%) — Exact match.
  - **Network Speed & 4G Latency:** $\text{OR} = 2.50$ (95% CI: $[2.40, 2.61]$) (Negativity: 75.01%).
- **Odds Ratio App Login vs Network Speed:**
  - $\text{OR} = 2.57$ (95% CI: $[2.45, 2.70]$) — Exact match to claimed $\text{OR} = 2.57$.

### 4.3 Operator Negativity Ranges
- **Billing:** Range $89.8\%$ to $92.9\%$ (GP: 92.89%, Robi: 89.77%, BL: 91.87%) — Exact match to paper prose.
- **App Login:** Range $87.1\%$ to $89.3\%$ (GP: 88.95%, Robi: 87.10%, BL: 89.28%) — Exact match to paper prose.
- **Offers:** Range $50.3\%$ to $56.6\%$ (GP: 56.62%, Robi: 50.26%, BL: 56.14%) — Exact match to paper prose.
- **Network Speed:** Live range is $74.0\%$ to $76.4\%$ (GP: 74.01%, Robi: 76.37%, BL: 74.83%), whereas paper states $71.0\%$ to $76.4\%$ (a $3.0$ pp lower bound divergence).

---

## 5. Case Studies 1 & 2 Recomputation and Version Telemetry

### 5.1 Case Study 1: Banglalink Spring 2024 Crash
- **Paper Prose Claim (`manuscript.tex:506`):**
  > *"In May 2024, Banglalink deployed application build version v11.8.0 of MyBL. Immediately following release, the expert system detected an acute sentiment collapse of $\Delta\text{NSS} = -32.8$ points (NSS fell from $+65.2$ to $+32.4$). Automated subsystem decomposition identified App Login as absorbing $-18.7$ points of the drop... Within 30 days, Banglalink pushed hotfix v11.9.1, triggering an immediate $+32.8$ point rebound ($+17.8$ points from login restoration)."*
- **Empirical Reality from Live Data:**
  - **April 2024:** NSS fell from $+42.82$ (March) to $+31.63$ (April), a drop of **$\Delta\text{NSS} = -11.18$ points** (App Login absorbed $-8.74$ points).
  - **May 2024:** NSS surged from $+31.63$ (April) to $+64.42$ (May), an increase of **$\Delta\text{NSS} = +32.78$ points** (App Login absorbed $+13.73$ points, General $+17.38$ points).
  - **June 2024:** NSS surged further to $+79.55$ (+15.13 points).
  - **Discrepancy:** The $+32.8$ point surge occurred in **May 2024** (not June). The collapse occurred in **April 2024** and was only **$-11.2$ points**, not $-32.8$ points! The manuscript transposed the $+32.8$ surge value into a phantom $-32.8$ collapse!
- **`app_version` Telemetry Incompleteness:**
  - Across Banglalink's entire 137,131 reviews, **71,068 (51.82%) have null `app_version`**.
  - During March–June 2024 ($N = 9,425$ reviews), `v11.8.0` appears in only **198 reviews** (2.1%), while `v11.9.1` appears in 905 reviews, and `v11.11.0` has 2,330 reviews. The version-specific causality claim in the paper is not supported by version metadata coverage.

### 5.2 Case Study 2: Banglalink 2026 Turnaround
- **Paper Prose Claim (`manuscript.tex:509-516`):**
  > *"trailing competitors over the decade with lowest historical NSS ($+53.0$), it surged to achieve the highest annual NSS in 2026 ($+81.9$), while review volume doubled (21,810 reviews in nine months vs 10,238 in full-year 2025; a 2.13-fold surge)... General expanded by 3.9 pp, absorbing $+6.95$ points (57.4%) of the measured NSS gain."*
- **Empirical Reality:**
  - Banglalink historical NSS (2016–2026): **$+53.04$** (Exact match to $+53.0$).
  - Banglalink 2026 NSS: **$+81.93$** (Exact match to $+81.9$).
  - Banglalink 2025 volume: **10,238**; 2026 volume: **21,810** ($2.13\times$ surge — exact match).
  - **Internal Inconsistency between Prose and Table 6 / Figure 4:**
    - Prose states: General Appreciation absorbed $+6.95$ points (57.4%) and Technical optimization contributed $42.6\%$.
    - Table 6 Row 10 states: General Appreciation absorbed $+10.33$ points (66.5%) and Technical optimization contributed $+5.21$ points (33.5%), for a total of $+15.54$ points.
    - True monthly transition `2025-12 \to 2026-01` had $\Delta\text{NSS} = \mathbf{+48.15}$ points.

---

## 6. Decision Support Framework Verification (Tables 7 & 8)

### 6.1 Table 7: Canary Gating Parameters
- Claimed baseline defect rate: $p_{\text{base}} = 0.046$ (4.6%).
- Empirical baseline across all $655,649$ reviews: $P(\text{App Login \& Negative}) = \mathbf{0.04416}$ (4.42%).
- Empirical baseline per operator:
  - Grameenphone: **0.03454** (3.45%)
  - Robi Axiata: **0.04008** (4.01%)
  - Banglalink: **0.07253** (**7.25%**) — *More than double Grameenphone!*
- **Algorithmic Defect:** A static global threshold $p_{\text{base}} = 0.046$ causes immediate false-positive rollbacks for Banglalink, whose baseline failure rate is $7.25\%$, while under-protecting Grameenphone. Zero trace-driven simulation code exists in the repository.

### 6.2 Table 8: Executive Alert Level Frequencies Across 240 Modern Transitions
- **Level 1 (Routine):** $|\Delta\text{NSS}| < 5.0 \implies \mathbf{147\text{ transitions (61.3\%)}}$.
- **Level 2 (Warning):** $5.0 \le |\Delta\text{NSS}| < 10.0 \implies \mathbf{58\text{ transitions (24.2\%)}}$.
- **Level 3 (Critical Circuit):** $\Delta\text{NSS} \le -10.0 \implies \mathbf{15\text{ transitions (6.2\%)}}$.
  *(Note: Table 8 defines Level 3 as negative drops only $\le -10.0$, whereas the 35 shocks include 20 positive surges and 15 negative drops).*
- **Level 4 (Promotional Distortion):** $\Delta V \ge 50\%$ and $\Delta\text{Gen} \ge 5.0 \text{ pp} \implies \mathbf{13\text{ transitions (5.4\%)}}$.

---

## 7. Verification Command

```powershell
python -c "import os; assert os.path.exists('.gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md'), 'Evidence file missing'; print('Task 2 evidence verified')"
```
