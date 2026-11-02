# 📡 Voice-of-Customer Intelligence Report (Jul 2016 – Sep 2026 Common Period)
### Exhaustive Macro-Level Sentiment & Operational Category Analysis across Bangladesh Telecoms
**Common Duration Benchmark Scale**: $N = 655,670$ Verified Google Play Customer Reviews (3,716 Shared Days)  
**Master Corpus in Storage**: $N = 661,160$ Unique Reviews (March 2014 – October 2026)  
**Operators Evaluated**: Grameenphone Ltd. (MyGP), Robi Axiata Limited (MyRobi), Banglalink Digital Communications Limited (MyBL)  
**Strict Operator Serial**: Grameenphone, Robi, Banglalink  
**Models Deployed**: 8 Model Architectures (Production Soft-Voting Ensemble, Logistic Regression, LinearSVC, PyTorch BiLSTM + Bahdanau Attention)

---

## 🏆 1. Executive Summary & Common Duration Operator Performance

Across the shared 3,716-day common window (July 28, 2016 – September 30, 2026, $N = 655,670$ reviews where all three operators coexist simultaneously), every review was scored by the **Production Soft-Voting Ensemble** (trained on 4,500 seed reviews and benchmarked against an empirical human gold standard), cross-verified with **PyTorch BiLSTM + Attention**, **Logistic Regression**, and **LinearSVC**.

| Operator | Total Reviews Harvested | Positive (%) | Neutral (%) | Negative (%) | Net Sentiment Score (NSS) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Grameenphone** | **320,143** | **77.0%** (246,501) | **10.8%** (34,747) | **12.2%** (38,895) | **+64.85%** |
| **Robi** | **198,378** | **77.9%** (154,477) | **10.2%** (20,166) | **12.0%** (23,735) | **+65.91%** |
| **Banglalink** | **137,149** | **70.4%** (96,525) | **12.3%** (16,853) | **17.3%** (23,771) | **+53.05%** |
| **Combined Industry Total** | **655,670** | **75.9%** (497,503) | **10.9%** (71,766) | **13.2%** (86,401) | **+62.70%** |

> **Net Sentiment Score Formula**:  

> ```
> NSS (%) = [(Positive Reviews - Negative Reviews) / Total Reviews] × 100
> ```

> [!NOTE]
> **Statistical Significance & Central Limit Theorem (CLT) Standard (N ≥ 30)**: In accordance with the classical Central Limit Theorem standard for asymptotic sample normality, time-series trajectory metrics strictly require **N ≥ 30 verified reviews per observation period**. Low-density early adoption months with N < 30 (such as July 2016 where Grameenphone had 3 reviews and Robi had 0, or sporadic months in 2016–2017) are omitted from monthly trend calculations to eliminate small-sample variance spikes. Annual aggregations consistently surpass this N ≥ 30 floor across all operators in every year of the common duration period (ranging from 126 reviews up to >75,000 reviews).

> *Strict operator analysis serial: **Grameenphone**, **Robi**, **Banglalink**.*

---

## 📈 2. Historical Year-by-Year NSS Trajectory

| Year | Operator | Volume | Net Sentiment Score (NSS) | Positive (%) | Negative (%) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **2016** | **Grameenphone** | 441 | **+2.5%** | 39.7% | 37.2% |
| **2016** | **Robi** | 126 | **-57.9%** | 14.3% | 72.2% |
| **2016** | **Banglalink** | 762 | **+46.3%** | 63.8% | 17.4% |
| **2017** | **Grameenphone** | 587 | **+13.5%** | 46.0% | 32.5% |
| **2017** | **Robi** | 367 | **-50.7%** | 17.7% | 68.4% |
| **2017** | **Banglalink** | 2,518 | **+45.5%** | 66.5% | 21.0% |
| **2018** | **Grameenphone** | 605 | **-16.0%** | 34.4% | 50.4% |
| **2018** | **Robi** | 1,418 | **-28.8%** | 27.9% | 56.7% |
| **2018** | **Banglalink** | 3,041 | **+22.3%** | 55.9% | 33.6% |
| **2019** | **Grameenphone** | 2,392 | **+19.6%** | 46.5% | 26.9% |
| **2019** | **Robi** | 4,186 | **+16.4%** | 50.9% | 34.5% |
| **2019** | **Banglalink** | 4,235 | **+17.8%** | 53.6% | 35.8% |
| **2020** | **Grameenphone** | 27,600 | **+45.7%** | 66.2% | 20.5% |
| **2020** | **Robi** | 32,333 | **+63.6%** | 76.5% | 12.9% |
| **2020** | **Banglalink** | 17,538 | **+38.3%** | 63.7% | 25.4% |
| **2021** | **Grameenphone** | 40,535 | **+61.0%** | 75.1% | 14.1% |
| **2021** | **Robi** | 30,296 | **+63.8%** | 76.8% | 13.0% |
| **2021** | **Banglalink** | 25,471 | **+46.6%** | 67.2% | 20.7% |
| **2022** | **Grameenphone** | 45,702 | **+64.2%** | 76.8% | 12.6% |
| **2022** | **Robi** | 34,418 | **+68.4%** | 79.4% | 10.9% |
| **2022** | **Banglalink** | 21,442 | **+55.5%** | 70.9% | 15.4% |
| **2023** | **Grameenphone** | 60,609 | **+69.8%** | 79.7% | 9.9% |
| **2023** | **Robi** | 16,784 | **+48.7%** | 68.2% | 19.5% |
| **2023** | **Banglalink** | 14,761 | **+40.1%** | 59.6% | 19.5% |
| **2024** | **Grameenphone** | 75,059 | **+70.6%** | 79.3% | 8.7% |
| **2024** | **Robi** | 16,804 | **+66.0%** | 77.2% | 11.1% |
| **2024** | **Banglalink** | 15,333 | **+57.2%** | 72.2% | 14.9% |
| **2025** | **Grameenphone** | 54,262 | **+70.3%** | 81.0% | 10.7% |
| **2025** | **Robi** | 42,743 | **+78.6%** | 85.0% | 6.4% |
| **2025** | **Banglalink** | 10,238 | **+66.4%** | 78.5% | 12.1% |
| **2026** | **Grameenphone** | 12,351 | **+56.8%** | 74.2% | 17.4% |
| **2026** | **Robi** | 18,903 | **+76.2%** | 83.5% | 7.3% |
| **2026** | **Banglalink** | 21,810 | **+81.9%** | 87.1% | 5.2% |

---

## 🏷️ 3. Operational Category Distribution

Across all 655,670 common period reviews, the operational categories broke down as follows:

- **General Appreciation / Other  **: 86.55% (567,486 reviews)  
  `██████████████████████████████████`
- **Offers & Data Packs           **:  5.04% (33,078 reviews)  
  `██`
- **App Login & Technical Bugs    **:  4.99% (32,703 reviews)  
  `█`
- **Network Speed & 4G Latency    **:  2.46% (16,108 reviews)  
  ``
- **Billing & Airtime Deductions  **:  0.96% (6,295 reviews)  
  ``

---

## 🛠️ 4. True Operational Complaint Rates & Measurement Methodology

When isolating strictly **negative customer reviews** (the direct metric plotted in the *Operational Complaint Rate* chart), verified complaint prevalence is:

| Operational Complaint Domain | Grameenphone (MyGP) | Robi (My Robi) | Banglalink (MyBL) | Measured Operational Vulnerability |
| :--- | :---: | :---: | :---: | :--- |
| **App Login & Technical Bugs** | **3.45%** (11,059) | **4.01%** (7,951) | **7.25%** (9,946) | **Banglalink**: Elevated technical login and session bug complaints. |
| **Offers & Data Packs** | **2.99%** (9,557) | **2.61%** (5,168) | **2.42%** (3,321) | **Grameenphone**: Highest negative pack pricing and validity friction. |
| **Network Speed & 4G Latency** | **1.39%** (4,453) | **1.96%** (3,895) | **2.72%** (3,735) | **Banglalink**: Highest negative signal and 4G speed feedback. |
| **Billing & Airtime Deductions** | **1.03%** (3,307) | **0.70%** (1,395) | **0.79%** (1,085) | **Grameenphone**: Highest balance deduction grievance rate. |

### Measurement Methodology & Formulas

Each review undergoes a **dual-classifier inference pipeline**:
- **Sentiment Model**: Classifies review into `Positive`, `Neutral`, or `Negative`.
- **Category Model**: Classifies review into one of 5 operational domains (*Offers & Data Packs*, *App Login & Technical Bugs*, *Network Speed & 4G Latency*, *Billing & Airtime Deductions*, *General Appreciation / Other*).

A review constitutes an actionable operational complaint *if and only if* it satisfies both criteria:

> **Operational Complaint Rule**:  
> `Predicted Category = [Specific Domain]` **AND** `Predicted Sentiment = Negative`

#### Relative Prevalence across Operator Voice (% of Total Operator Reviews):
```
                                 Count of Negative Reviews in Category
Operational Complaint Rate (%) = ------------------------------------- × 100
                                        Total Operator Reviews
```

#### Within-Category Grievance Concentration (% Negative within Category):
```
                                        Count of Negative Reviews in Category
Within-Category Dissatisfaction (%) = ----------------------------------------- × 100
                                             Total Reviews in That Category
```

---

## ⚡ 5. Longitudinal NSS Stability & Significant Shock Root-Cause Attribution

### A. NSS Stability Scorecard (2020 – 2026 High-Volume Modern Era | 81 Months)

Evaluated across the 81 continuous high-volume months under the CLT normality floor (N ≥ 30):

| Operator | Mean NSS (2020–2026) | MoM Volatility (RMSSD) | Stability Index (SSI / 100) | Interquartile Range (IQR) | Stability Diagnosis |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Robi (My Robi)** | **+64.16%** | **5.61 points** | **94.39 / 100** | **18.08 points** | **Highest Stability**: Most consistent month-to-month consumer experience across all 81 months. |
| **Grameenphone (MyGP)** | **+61.11%** | **6.28 points** | **93.72 / 100** | **14.07 points** | **High Stability**: Tightest core distribution band (Q1 = 54.2%, Q3 = 68.3%). |
| **Banglalink (MyBL)** | **+50.06%** | **13.61 points** | **86.39 / 100** | **18.25 points** | **High Volatility**: Over 2.4× more volatile month-over-month than Robi, driven by periodic app release swings. |

### B. Significant Shock Detection & Attribution Engine

A shift is flagged as an operational shock when:
```
|Delta NSS| >= 10.0 percentage points
```
Because Net Sentiment Score is linearly additive across categories:
```
Delta NSS = sum(Delta Contribution_c)
```
The category with the largest contribution change (`Delta Contribution_c`) represents the **primary operational driver** of the shock.

#### Verified Historical Operational Shocks (2020 – 2026):

| Operator | Transition Period | NSS Before | NSS After | Shift (Delta NSS) | Primary Operational Driver | Driver Impact | Empirical Root-Cause Breakdown |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: | :--- |
| **Grameenphone** | 2020-03 → 2020-04 | +17.7% | +49.0% | **+31.2 pts** | App Login & Technical Bugs | +5.49 pts | Rapid drop in login bug grievances (+5.49 pts) and increased data pack praise (+3.54 pts). |
| **Grameenphone** | 2021-04 → 2021-05 | +62.3% | +48.5% | **-13.8 pts** | App Login & Technical Bugs | -2.29 pts | Joint increase in login bug complaints (-2.29 pts) and network latency friction (-2.19 pts). |
| **Grameenphone** | 2021-08 → 2021-09 | +50.1% | +63.7% | **+13.6 pts** | App Login & Technical Bugs | +5.08 pts | Sharp decrease in authentication and session crash reports (+5.08 pts). |
| **Grameenphone** | 2025-08 → 2025-09 | +70.1% | +51.5% | **-18.5 pts** | Offers & Data Packs | -2.68 pts | Surge in data pricing/validity dissatisfaction (-2.68 pts) alongside login complaints (-1.25 pts). |
| **Robi** | 2022-12 → 2023-01 | +66.2% | +49.6% | **-16.6 pts** | App Login & Technical Bugs | -7.40 pts | Severe login session failure; App Login complaints accounted for nearly half the total decline. |
| **Robi** | 2023-01 → 2023-02 | +49.6% | +60.3% | **+10.7 pts** | App Login & Technical Bugs | +4.64 pts | Recovery following stability patch, restoring +4.64 pts in login sentiment. |
| **Robi** | 2023-11 → 2023-12 | +38.8% | +48.8% | **+10.0 pts** | Offers & Data Packs | +2.67 pts | Year-end data pack promotions generated positive sentiment lift (+2.67 pts). |
| **Banglalink** | 2021-04 → 2021-05 | +58.8% | +42.4% | **-16.4 pts** | Network Speed & 4G Latency | -4.90 pts | High surge in network speed and coverage complaints (-4.90 pts). |
| **Banglalink** | 2024-03 → 2024-04 | +49.9% | +38.7% | **-11.2 pts** | App Login & Technical Bugs | -8.74 pts | Acute login session and OTP delivery failure (-8.74 pts impact). |
| **Banglalink** | 2024-04 → 2024-05 | +38.7% | +71.5% | **+32.8 pts** | App Login & Technical Bugs | +13.73 pts | App release resolved authentication crashes, driving a +13.73 pts recovery in login sentiment alone. |
