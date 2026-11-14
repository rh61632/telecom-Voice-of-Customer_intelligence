# Telecom VoC Intelligence: Empirical Ground Truth Summary
**Generated:** `2026-11-11T19:04:23.515382+00:00` | **Platform:** `Windows-11-10.0.26300-SP0` | **Python:** `3.15.1`

---

## 1. Table 1: Category Taxonomy & Deployed Distributions (N = 655,649)
| Operational Category | Deployed Count | Deployed % | Seed N=4,500 | GP Count | Robi Count | BL Count |
|---|---:|---:|---:|---:|---:|---:|
| General Appreciation / Other | 567,468 | 86.55% | 2,731 | 281,253 | 172,312 | 113,903 |
| Offers & Data Packs | 33,077 | 5.04% | 788 | 16,878 | 10,283 | 5,916 |
| App Login & Technical Bugs | 32,701 | 4.99% | 400 | 12,432 | 9,129 | 11,140 |
| Network Speed & 4G Latency | 16,108 | 2.46% | 364 | 6,017 | 5,100 | 4,991 |
| Billing & Airtime Deductions | 6,295 | 0.96% | 217 | 3,560 | 1,554 | 1,181 |
| **Total** | **655,649** | **100.00%** | **4,500** | **320,140** | **198,378** | **137,131** |

---

## 2. Decade Scorecard (2016–2026 Common Duration)
- **Grameenphone:** 320,140 reviews (48.83%), NSS = **+64.85%** (95% CI: [64.61%, 65.09%])
- **Robi:** 198,378 reviews (30.26%), NSS = **+65.91%** (95% CI: [65.61%, 66.21%])
- **Banglalink:** 137,131 reviews (20.92%), NSS = **+53.04%** (95% CI: [52.63%, 53.45%])
- **Sector Overall:** 655,649 reviews, NSS = **+62.70%**

---

## 3. Active Gold Standard (N = 300 / 200), Consensus & McNemar
- **Inter-Rater Reliability:**
  - Sentiment ($N=200$): Raw Agreement **91.0%**, Cohen's $\kappa = 0.5762$, 3-Class PABAK = **0.865**
  - Category ($N=196$): Raw Agreement **95.41%**, Cohen's $\kappa = 0.7694**
- **Ensemble Voting Classifier (CLI / Demo):**
  - $N=300$ Accuracy: **89.00%** | Consensus ($N=182$): **91.21%**
  - McNemar vs Star Heuristic ($b=22, c=15$): $\chi^2_c = 0.973, p = 0.3240$
  - Rogan-Gladen Active Parameters: $\mathrm{Se} = 0.5217, \mathrm{Sp} = 0.9747$
- **Sentiment Voting Classifier (Global Production):**
  - $N=300$ Accuracy: **83.67%** | Consensus ($N=182$): **87.91%**
  - McNemar vs Star Heuristic ($b=21, c=30$): $\chi^2_c = 1.2549, p = 0.2624$
  - Rogan-Gladen Active Parameters: $\mathrm{Se} = 0.4783, \mathrm{Sp} = 0.9711$
- **Category Voting Classifier:**
  - $N=300$ Accuracy: **91.33%** | Consensus ($N=187$): **94.12%**

---

## 4. Complexity & Table 3 Fit (N = 4,500)
- **Category Model Fit:** Acc = **99.00%**, Macro-F1 = **0.9883**
- **Feature Space:** $V = 29,843$ features
- **Active Density ($d$):** Mean = **109.72**, Median = **59.0**, Range = [0, 1199]

---

## 5. Modern Intra-Era Shocks (2020–2026, 240 Transitions)
- **Total Shocks ($|\Delta\text{NSS}| \ge 10.0$):** **35** (GP: 6, Robi: 7, BL: 22)
  - Direction: 20 positive expansions, 15 negative drops
  - Leading Operational Domain: **App Login & Technical Bugs: 27**, Network: 4, Offers: 4, Billing: 0
- **Contingency Analysis (Proposition 2):**
  - Pooled 2x2: Shocks 27/35 (77.1%) vs Non-shocks 91/205 (44.4%) $\implies \chi^2(1) = 12.8317, p = 3.4080e-04, \text{OR} = 4.228~[1.79, 9.98]$
  - Non-Surge 2x2: Shocks 14/19 (73.7%) vs Non-shocks 82/189 (43.4%) $\implies \chi^2(1) = 6.377, p = 0.0116, \text{OR} = 3.6537$
  - Banglalink Asymmetry: Shocks 20/22 vs Non-shocks 29/58 $\implies \text{OR} = 10.0, p = 0.0007$
- **Proposition 1 Regression:** $\text{Gen/Other Diff} = 11.52 \cdot d_{\ln(\text{vol})} \implies R^2 = 0.56, p = 2.3561e-07$
- **RMSSD Volatility:**
  - Raw: GP 6.28, Robi 5.61, BL 13.61 (BL/Robi ratio: 2.43x)
  - Non-surge filtered: GP 5.14, Robi 4.53, BL 7.56 (BL/Robi ratio: 1.67x)

---

## 6. Priority Matrix (N = 88,181 in 4 Functional Domains)
- **Omnibus Test:** $\chi^2(3) = 11,027.6, p < 0.0001, V = 0.3536$
- **Domain Breakdown & Odds Ratios vs Offers:**
  - **Billing & Airtime Deductions:** 5,787/6,295 (91.93%) | $\text{OR} = 9.49~[8.64, 10.42]$
  - **App Login & Technical Bugs:** 28,955/32,701 (88.54%) | $\text{OR} = 6.44~[6.18, 6.7]$
  - **Network Speed & 4G Latency:** 12,083/16,108 (75.01%) | $\text{OR} = 2.5~[2.4, 2.61]$
  - **Offers & Data Packs:** 18,046/33,077 (54.56%) | Reference ($	ext{OR} = 1.0$)
  - **Login vs Network:** $\text{OR} = 2.57~[2.45, 2.7]$

---

## 7. Case Studies 1 & 2 Telemetry & Decision Framework
- **Case Study 1 (Banglalink Spring 2024):**
  - Apr 2024 Shock: $\Delta\text{NSS} = -11.18$ pts (Login impact: $-8.74$ pp)
  - May 2024 Rebound: $\Delta\text{NSS} = +32.78$ pts (Login impact: $+13.73$ pp, General: $+17.38$ pp)
  - Telemetry: Build `v11.8.0` Apr 2024 NSS = **$-7.59$** ($N=158$); BL Version missingness = **51.82%**
- **Case Study 2 (Banglalink 2025 $\to$ 2026 Turnaround):**
  - Annual swing: **$+15.54$** NSS pts (2.13x volume growth)
  - Decomposed: General = **$+10.33$** pts (66.5%), Technical 4 Domains = **$+5.21$** pts (33.5%: Login $+2.80$, Network $+1.07$, Offers $+0.98$, Billing $+0.36$)
- **Decision Framework (Tables 7 & 8):**
  - Baseline $p_{\text{base}} = P(\text{App Login & Neg}) = 0.044162$ (4.42%)
  - Alert Level Counts (240 Transitions):
    - Level 1 (Routine: $|\Delta\text{NSS}| < 5.0$): **147** (61.25%)
    - Level 2 (Warning: $5.0 \le |\Delta\text{NSS}| < 10.0$): **58** (24.17%)
    - Level 3 (Incident: $\Delta\text{NSS} \le -10.0$): **15** (6.25%)
    - Level 4 (Surge: $\text{vol\_pct} \ge 50\% \land \Delta\text{Gen} \ge 5.0$): **13** (5.42%)
