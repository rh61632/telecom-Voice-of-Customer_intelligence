# 📡 Voice-of-Customer Intelligence Report (Jul 2016 – Sep 2026 Common Period)
### Exhaustive Macro-Level Sentiment & Operational Category Analysis across Bangladesh Telecoms
**Common Duration Benchmark Scale**: $N = 655,670$ Verified Google Play Customer Reviews (3,716 Shared Days)  
**Master Corpus in Storage**: $N = 661,160$ Unique Reviews (March 2014 – October 2026)  
**Operators Evaluated**: Grameenphone Ltd. (MyGP), Robi Axiata Limited (MyRobi), Banglalink Digital Communications Limited (MyBL)  
**Strict Operator Serial**: Grameenphone, Robi, Banglalink  
**Models Deployed**: 8 Model Architectures (Hero Soft-Voting Ensemble, Logistic Regression, LinearSVC, PyTorch BiLSTM + Bahdanau Attention)

---

## 🏆 1. Executive Summary & Common Duration Operator Performance

Across the shared 3,716-day common window (July 28, 2016 – September 30, 2026, $N = 655,670$ reviews where all three operators coexist simultaneously), every review was scored by the **Hero Soft-Voting Ensemble** (trained on 4,500 seed reviews and benchmarked against an empirical human gold standard), cross-verified with **PyTorch BiLSTM + Attention**, **Logistic Regression**, and **LinearSVC**.

| Operator | Total Reviews Harvested | Positive (%) | Neutral (%) | Negative (%) | Net Sentiment Score (NSS) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Grameenphone** | **320,143** | **77.0%** (246,501) | **10.8%** (34,747) | **12.2%** (38,895) | **+64.85%** |
| **Robi** | **198,378** | **77.9%** (154,477) | **10.2%** (20,166) | **12.0%** (23,735) | **+65.91%** |
| **Banglalink** | **137,149** | **70.4%** (96,525) | **12.3%** (16,853) | **17.3%** (23,771) | **+53.05%** |
| **Combined Industry Total** | **655,670** | **75.9%** (497,503) | **10.9%** (71,766) | **13.2%** (86,401) | **+62.70%** |

> **Net Sentiment Score Formula**:  

\text{NSS} = \left(\frac{N_{\text{Positive}} - N_{\text{Negative}}}{N_{\text{Total}}}\right) \times 100

> [!NOTE]
> **Statistical Significance & Central Limit Theorem (CLT) Standard ( \ge 30$)**: In accordance with the Central Limit Theorem for asymptotic sample normality, monthly NSS trajectory metrics strictly require ** \ge 30$ verified reviews per operator-month**. Early adoption months with  < 30$ (e.g., July 2016 where Grameenphone had 3 reviews and Robi had 0, or sporadic months in 2016–2017) are omitted from monthly trend calculations to eliminate small-sample variance spikes. Annual benchmarks enforce  \ge 500$ reviews/year ($\\text{Margin of Error} \le \pm 3.5\\%$).

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