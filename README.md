# 📡 Telecom Voice-of-Customer (VoC) Intelligence Engine
> **An enterprise end-to-end NLP & Business Intelligence pipeline for multilingual sentiment parsing, customer experience benchmarking, and operational strategy across Bangladesh's premier telecommunications operators.**

<div align="center">

| <img src="assets/logos/gp.png" height="55" alt="Grameenphone"/> | <img src="assets/logos/robi.png" height="55" alt="Robi"/> | <img src="assets/logos/banglalink.png" height="55" alt="Banglalink"/> |
| :---: | :---: | :---: |
| **Grameenphone Ltd.** | **Robi Axiata Limited** | **Banglalink Digital Communications Limited** |
| `com.portonics.mygp` | `net.omobio.robisc` | `com.arena.banglalinkmela.app` |
| **MyGP Platform** | **My Robi Platform** | **MyBL Platform** |

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Last Scraped](https://img.shields.io/badge/Data%20Last%20Scraped-Late%20Oct%202026-informational)](scraped_data_global_2020_2026/raw/)
[![Common Period Benchmark: 655.7k Reviews](https://img.shields.io/badge/Active%20Benchmark-655%2C670%20Reviews-emerald.svg)](scraped_data_global_2020_2026/classified/common_duration_summary.json)
[![Master Corpus: 661.2k](https://img.shields.io/badge/Master%20Corpus-661%2C160%20Reviews-blueviolet.svg)](scraped_data_global_2020_2026/classified/)
[![Common Window: 3,716 Days](https://img.shields.io/badge/Common%20Window-Jul%202016--Sep%202026-teal.svg)](scraped_data_global_2020_2026/classified/common_duration_summary.json)
[![Sentiment SOTA: BUET BanglaBERT](https://img.shields.io/badge/Sentiment%20SOTA-BanglaBERT%20(91.6%25%20Acc)-success.svg)](dl/)
[![Category Hero: Soft--Voting Ensemble](https://img.shields.io/badge/Category%20Hero-Ensemble%20(87.4%25%20Acc)-brightgreen.svg)](ml/)
[![Inter-Annotator Reliability: Cohen's Kappa](https://img.shields.io/badge/Cohen's%20Kappa-%CE%BA%20%3D%200.77%20(Substantial)-blueviolet.svg)](data/gold_set/gold_standard_evaluation_report.md)
[![Roadmap: TODO.txt](https://img.shields.io/badge/Roadmap-TODO.txt-orange.svg)](TODO.txt)
</div>

---

## 🎯 1. Executive Summary & Market Intelligence

This flagship project provides an empirical, end-to-end Voice-of-Customer (VoC) intelligence engine analyzing customer sentiment and operational complaints across Bangladesh's top three mobile network operators:
* **Grameenphone Ltd.** (operating the MyGP platform)
* **Robi Axiata Limited** (operating the MyRobi platform)
* **Banglalink Digital Communications Limited** (operating the MyBL platform)

*(Throughout this document, operators are subsequently referred to as **Grameenphone**, **Robi**, and **Banglalink**).*

> **Methodological Note on Common Duration Window & Statistical Significance (CLT Rule)**:  
> 1. **Common Duration Window**: To guarantee strict statistical equity and eliminate temporal selection bias (ensuring no operator has missing historical windows in comparative analytics), all published benchmarks, comparative scorecards, trendlines, and category distributions strictly analyze the continuous **3,716-Day Common Duration Period** (**July 28, 2016 – September 30, 2026**, $N = 655,670$) where all three operators coexist simultaneously. The full multi-year corpus ($N = 661,160$, October 2014 – October 2026) is preserved in storage for extended longitudinal modeling.
> 2. **Central Limit Theorem (CLT) Sampling Rule ($N \ge 30$)**: In monthly time-series analytics, we strictly follow the classical Central Limit Theorem guideline ($N \ge 30$) for sample normality. Any operator-month with fewer than 30 reviews (e.g., July 2016 where Grameenphone had 3 reviews and Robi had 0, or sporadic low-volume early adoption months in 2016–2017) is pruned from the monthly trajectory lines. This prevents small-sample distortion—where a single random negative or positive review would artificially swing net sentiment by $\pm 30\%$ to $100\%$—guaranteeing that every plotted monthly point reflects genuine, statistically meaningful consumer sentiment. Yearly trajectory points enforce an even tighter publication-grade threshold of $N \ge 500$ reviews/year ($\text{Margin of Error} \le \pm 3.5\%$).

### 📊 Common Duration Performance Scorecard ($N = 655,670$, July 28, 2016 – September 30, 2026 | 3,716 Days)

Every review was scored by our production **Hero Soft-Voting Ensemble** (trained on 4,500 Groq LLM-annotated seed reviews and benchmarked against an empirical human gold standard, achieving **87.5% CV Accuracy** on Sentiment and **87.3%** on Operational Categories), cross-verified with **PyTorch BiLSTM + Attention**, **Balanced Logistic Regression**, **Calibrated LinearSVC**, and SOTA **BUET BanglaBERT** (**91.6% CV Accuracy**).

```
+---------------------------------------------------------------------------------------------------------+
|                                COMMON DURATION VoC PERFORMANCE SCORECARD                                |
|                                (July 28, 2016 – September 30, 2026 | 3,716 Days)                        |
+----+----------------------+---------------+------------+-----------+------------+-----------------------+
| #  | Operator             | Total Reviews | Positive % | Neutral % | Negative % | Net Sentiment (NSS)   |
+----+----------------------+---------------+------------+-----------+------------+-----------------------+
| 1  | Grameenphone (MyGP)  | 320,143       | 77.0%      | 10.9%     | 12.1%      | +64.9% (Scale Leader) |
| 2  | Robi (MyRobi)        | 198,378       | 77.9%      | 10.2%     | 12.0%      | +65.9% (NSS Leader)   |
| 3  | Banglalink (MyBL)    | 137,149       | 70.4%      | 12.3%     | 17.3%      | +53.1% (Agile Growth) |
+----+----------------------+---------------+------------+-----------+------------+-----------------------+
| -- | Industry Benchmark   | 655,670       | 75.9%      | 10.9%     | 13.2%      | +62.7%                |
+----+----------------------+---------------+------------+-----------+------------+-----------------------+
```

> **Net Sentiment Score (NSS) Formula**:

$$\text{NSS} = \left(\frac{N_{\text{Positive}} - N_{\text{Negative}}}{N_{\text{Total}}}\right) \times 100$$

> *Consistent operator analysis serial: **Grameenphone**, **Robi**, **Banglalink**.*

---

## 📊 2. Visual Analytics & Publication Intelligence Suite

All visualizations are generated natively in Python at publication-grade **300 DPI** using verified brand hex palettes: **Grameenphone (`#0090ff`)**, **Robi (`#e60000`)**, and **Banglalink (`#ff7a00`)**.

### A. Market Net Sentiment Score & Sentiment Breakdown
| Net Sentiment Score (NSS) Comparison | Sentiment Share by Operator |
| :---: | :---: |
| <img src="assets/plots/net_sentiment_score_comparison_bars.png?v=2" width="450"/> | <img src="assets/plots/operator_sentiment_distribution_bars.png?v=2" width="450"/> |

### B. Longitudinal Trajectory Across Shared Horizon (2016 – 2026)
> **Full Unclipped Horizon**: Y-axis scaled from **-35% to +95%** with an explicit **0% Neutral Baseline**, capturing the full spectrum from 2018's acute 4G rollout backlash (GP $-16.0\%$, Robi $-28.8\%$) to 2026's peak digital adoption (Banglalink $+81.9\%$).

<div align="center">
  <img src="assets/plots/multi_year_sentiment_trend_line.png?v=4" width="900" alt="Complete Multi-Year Net Sentiment Trajectory (2016 - 2026)"/>
</div>

#### Dedicated Standalone Era Trajectories (Yearly)
To prevent early teething volatility from compressing the modern high-volume era, dedicated standalone trajectories are rendered with era-optimized scales:

| Phase 1: Early Era (2016 – 2019 · $N = 20,678$) | Phase 2: Modern Era (2020 – 2026 · $N = 634,992$) |
| :---: | :---: |
| <img src="assets/plots/yearly_sentiment_trend_pre2020.png?v=4" width="450" alt="Early Era NSS Trajectory (2016-2019)"/> | <img src="assets/plots/yearly_sentiment_trend_2020_2026.png?v=4" width="450" alt="Modern Era NSS Trajectory (2020-2026)"/> |
| **Early Infancy & 4G Friction**: Scaled `[-35%, +55%]` with 0% Neutral Baseline highlighting SIM registration and the 2018 4G launch dip. | **Ecosystem Scale & Rivalry**: Scaled `[+30%, +92%]` highlighting 2023–24 VAS friction and 2026 Banglalink surge. |

### C. Operational Complaint Breakdown & Departmental Sentiment
| Actionable Complaint Rates by Operator | Sentiment Composition per Comment Type |
| :---: | :---: |
| <img src="assets/plots/operator_category_complaint_distribution_bars.png?v=4" width="450"/> | <img src="assets/plots/category_sentiment_stacked_bars.png?v=4" width="450"/> |

### D. Monthly-Granularity Sentiment Dynamics & Seasonality (Jul 2016 – Sep 2026)
> **Complete Continuous Monthly Time Series (123 Months, $N = 655,670$)**: Full vertical dynamic range from **-80% to +95%** with a 0% neutral baseline across all 3,716 shared days.
> 
> > [!NOTE]
> > **Statistical Significance & Central Limit Theorem (CLT) Standard ($N \ge 30$)**: In accordance with the classical Central Limit Theorem guideline for asymptotic normality, monthly NSS values are strictly plotted only for operator months with **$N \ge 30$ verified customer reviews**. Low-density early adoption months ($N < 30$, such as July 2016 where GP had 3 reviews and Robi had 0, or occasional early 2017 months) are excluded from the trajectory lines. This eliminates small-sample variance spikes and prevents individual reviews from distorting longitudinal trend integrity.

<div align="center">
  <img src="assets/plots/monthly_nss_trend_line.png?v=5" width="900" alt="Complete Monthly Net Sentiment Trajectory (Jul 2016 - Sep 2026)"/>
</div>

#### Dedicated Standalone Era Trajectories (Monthly)
| Phase 1: Early Era (Jul 2016 – Dec 2019 · 42 Months · $N \ge 30$ CLT Floor) | Phase 2: Modern Era (Jan 2020 – Sep 2026 · 81 Months · $N \ge 30$ CLT Floor) |
| :---: | :---: |
| <img src="assets/plots/monthly_nss_trend_pre2020.png?v=5" width="450" alt="Early Era Monthly NSS (2016-2019)"/> | <img src="assets/plots/monthly_nss_trend_2020_2026.png?v=5" width="450" alt="Modern Era Monthly NSS (2020-2026)"/> |
| **Acute Teething Volatility**: Detailed monthly progression through 2018's network crisis. | **Super-App Stability**: Quarterly ticks tracking seasonal recharges and modern market shifts. |

---

## 📈 3. Longitudinal Trajectory & Inflection Points (2016 – 2026)

Tracking customer sentiment across the shared 3,716-day window (2016 – 2026) reveals the multi-year evolution of Bangladesh's mobile telecom apps:

| Year | Grameenphone (MyGP) | Robi (MyRobi) | Banglalink (MyBL) | Historical Strategic Event |
| :---: | :---: | :---: | :---: | :--- |
| **2016** *(Jul–Dec)* | **+2.5%** (441) | **-57.9%** ⚠️ (126) | **+46.3%** (762) | **Early Smartphone Onboarding**: Early Android app ecosystem; Robi struggled with initial app stability, while Banglalink enjoyed early novelty goodwill. |
| **2017** | **+13.5%** (587) | **-50.7%** (367) | **+45.5%** (2,518) | **Pre-4G Era**: Banglalink expanded MyBL adoption rapidly; Robi self-care app experienced major legacy UI friction and login bugs. |
| **2018** | **-16.0%** 📉 (605) | **-28.8%** (1,418) | **+22.3%** (3,041) | **4G Rollout Disruption**: Nationwide 4G spectrum launch led to customer dissatisfaction with early SIM upgrades and data pricing across all operators. |
| **2019** | **+19.6%** (2,392) | **+16.4%** (4,186) | **+17.8%** (4,235) | **Digital Normalization**: Operators stabilized 4G self-care applications; Robi turned sentiment positive (+16.4%) for the first time. |
| **2020** | **+45.7%** (27,600) | **+63.6%** (32,333) | **+38.3%** (17,538) | **COVID-19 Digital Surge**: Nationwide lockdowns triggered massive digital recharge and self-care adoption across all platforms. |
| **2021** | **+61.0%** (40,535) | **+63.8%** (30,296) | **+46.6%** (25,471) | **App Maturation**: In-app digital payment gateway integrations (bKash/Nagad) drastically improved digital self-care NPS. |
| **2022** | **+64.2%** (45,702) | **+68.4%** (34,418) | **+55.5%** (21,442) | **Organic Retention**: Self-care platforms became primary service touchpoints; Robi and GP maintained strong satisfaction above +64% NSS. |
| **2023** | **+69.8%** (60,609) | **+48.7%** ⚠️ (16,784) | **+40.1%** (14,761) | **The 2023 Friction Point**: Robi and Banglalink faced acute VAS balance deduction & OTP complaints, while GP expanded volume scale. |
| **2024** | **+70.6%** (75,059) | **+66.0%** (16,804) | **+57.2%** (15,333) | **Modernization Wave**: Grameenphone anchored massive volume (>75k reviews) at 70%+ NSS; Robi and Banglalink stabilized core architecture. |
| **2025** | **+70.3%** (54,262) | **+78.6%** 🚀 (42,743) | **+66.4%** (10,238) | **The 2025 Robi Turnaround**: Robi resolved core backend latency, catapulting NSS to +78.6% (cutting negative reviews to just 6.4%). |
| **2026** *(Jan–Sep)* | **+56.8%** 📉 (12,351) | **+76.2%** (18,903) | **+81.9%** 🏆 (21,810) | **The 2026 Market Reversal**: Banglalink surged to industry-leading **+81.9% NSS** on high self-care goodwill; GP dipped to **+56.8% NSS** due to data pack pricing friction. |


---

## 🏷️ 4. Operational Category & Departmental Intelligence

Every review was classified into **5 operational domains** by our Soft-Voting Category Ensemble:

| Operational Category | Grameenphone (320.1k) | Robi (198.4k) | Banglalink (137.1k) | Operational Diagnosis |
| :--- | :---: | :---: | :---: | :--- |
| **General Appreciation / Other** | **87.85%** (281,254) | **86.86%** (172,312) | **83.06%** (113,920) | App praise, short reviews, emojis, and general service feedback. |
| **Offers & Data Packs** | **5.27%** (16,878) | **5.18%** (10,283) | **4.31%** (5,917) | Price sensitivity, validity expiration, and complaints regarding MB pack costs across all operators. |
| **App Login & Technical Bugs** | **3.88%** (12,434) | **4.60%** (9,129) | **8.12%** (11,140) | **Banglalink's Vulnerability**: Authentication/session stability, OTP delays, and biometric login token timeouts. |
| **Network Speed & 4G Latency** | **1.88%** (6,017) | **2.57%** (5,100) | **3.64%** (4,991) | Grameenphone maintains the lowest network complaint rate, while Banglalink users report indoor 4G friction. |
| **Billing & Airtime Deductions** | **1.11%** (3,560) | **0.78%** (1,554) | **0.86%** (1,181) | **Grameenphone's Primary Vulnerability**: Highest accidental deduction and billing complaints among all operators. |

---

## 🏆 5. Empirical Multi-Paradigm Benchmark Suite

Models were trained and evaluated on the curated multi-operator seed dataset ($N=4,500$ across Grameenphone, Robi, and Banglalink, annotated via the Groq LLM API and validated against human benchmarks) using **5-Fold Stratified Cross-Validation**.

To eliminate task ambiguity between 3-class sentiment polarity and 5-class departmental taxonomy, the benchmark results are presented in two dedicated leaderboards and publication-grade visualizations below:

### A. Sentiment Analysis Model Leaderboard (3-Class Polarity)
> Evaluated on 3-class sentiment polarity: **Positive**, **Neutral**, and **Negative**.

<div align="center">
  <img src="assets/plots/sentiment_model_benchmark_bars.png?v=1" width="850" alt="Sentiment Analysis Model Benchmark (3-Class Polarity)"/>
</div>

| Rank | Model Architecture | CV Accuracy | Macro-F1 | Inference Throughput | Key Strengths / Characteristics |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 🥇 | **BUET BanglaBERT (Fine-Tuned)** | **91.60%** | **0.8598** | GPU Batched | **Overall Sentiment SOTA**: End-to-end 12-layer transformer fine-tuning (+4.1% Acc, +9.1% F1 over Ensemble). |
| 🥈 | **Hero Soft-Voting ML Ensemble** | **87.47%** | **0.7684** | **~17,500 rev/s** | **Production Hero Engine**: High-throughput CPU classifier (LR + Calibrated LinearSVC + ComplementNB). |
| 🥉 | **Multilingual MiniLM Head** | **82.33%** | **0.7475** | ~2,100 rev/s | 384-dim multilingual dense embeddings; cross-lingual semantic transfer. |
| 4 | **Hybrid BiLSTM + Attention (GPU)** | **81.50%** | **0.7180** | Fast GPU Batched | Sequential token context + Bahdanau attention over emotional cues. |

---

### B. Operational Category Model Leaderboard (5-Class Taxonomy)
> Evaluated on 5 operational complaint domains: **Offers & Data Packs**, **App Login & Technical Bugs**, **Network Speed & 4G Latency**, **Billing & Airtime Deductions**, and **General Appreciation / Other**.

<div align="center">
  <img src="assets/plots/category_model_benchmark_bars.png?v=1" width="850" alt="Operational Category Model Benchmark (5-Class Taxonomy)"/>
</div>

| Rank | Model Architecture | CV Accuracy | Macro-F1 | Inference Throughput | Key Strengths / Characteristics |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 🥇 | **Hero Soft-Voting ML Ensemble** | **87.44%** | **0.7845** | **~18,200 rev/s** | **Category Champion**: Sub-word character n-grams excel on Romanized Banglish (*"mb"*, *"kete niyeche"*, *"otp"*). |
| 🥈 | **BUET BanglaBERT (Fine-Tuned)** | **85.27%** | **0.7624** | GPU Batched | Contextual transformer representations with full 12-layer backpropagation. |
| 🥉 | **Multilingual MiniLM Head** | **81.15%** | **0.7247** | ~2,100 rev/s | Multilingual sentence semantic representations with regularized head. |
| 4 | **Hybrid BiLSTM + Attention (GPU)** | **80.84%** | **0.7106** | Fast GPU Batched | Sequential token context + inverse frequency class weighting. |

> [!NOTE]
> **Ablation Note on Frozen vs. Fine-Tuned Transformer**: In early baseline experiments, BUET BanglaBERT was evaluated as a static frozen feature extractor (768-dim embeddings + linear head), achieving 74.88% Accuracy / 0.6253 Macro-F1. Full end-to-end fine-tuning delivered a **+10.39% accuracy leap** (85.27% / 0.7624 Macro-F1), proving that updating transformer self-attention layers is essential for adapting to Romanized Banglish and telecom-specific vocabulary. Early frozen baseline notebooks are preserved in [`archive/early_dl_experiments/`](archive/early_dl_experiments/).

### C. Human Ground-Truth Validation & Model Agreement (Zero-Leakage Study)

To rigorously validate whether automated machine learning classifications genuinely reflect human cognitive perception (and eliminate self-reinforcing training feedback loops), a two-step validation framework was conducted under strict zero-leakage conditions (training seed reviews excluded, star ratings stripped, and model predictions hidden):

#### 1. Inter-Annotator Reliability (Human vs. Human Consensus)
Before measuring model accuracy, we established the validity and consistency of our operational taxonomy and sentiment boundaries across an overlapping stratified cohort ($N = 200$ reviews across Grameenphone, Robi, and Banglalink) evaluated by two independent human reviewers:

| Evaluation Dimension | Evaluated Pairs | Raw Human Agreement | Cohen's Kappa ($\kappa$) | Standard Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **Sentiment Analysis (3-Class)** | **200** | **91.00%** | **0.5762** | Moderate Agreement (High raw consistency) |
| **Operational Category (5-Class)** | **196** | **95.41%** | **0.7694** | **Substantial Agreement** |

#### 2. Trained Model Performance on Blind Human Ground Truth (Model vs. Human Agreement)
The trained classifiers were then benchmarked directly against the blind human ground-truth cohort ($N = 300$ primary human reviews; $N = 182$ sentiment / $N = 187$ category dual-human consensus reviews):

| Model Architecture | Evaluated Task | Human Raw Agreement (N=300) | Consensus Agreement (Dual-Human Agreed) | Cohen's Kappa ($\kappa$) | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Hero Soft-Voting ML Ensemble** | **Operational Category (5-Class)** | **91.33%** | **94.12%** | **0.5046** | 🏆 Production Category Hero |
| Challenger LinearSVC | Operational Category (5-Class) | 91.00% | 93.58% | 0.4679 | High Linear Baseline |
| Primary Logistic Regression | Operational Category (5-Class) | 89.33% | 91.98% | 0.4385 | Balanced Regularized Baseline |
| **Hero Soft-Voting ML Ensemble** | **Sentiment Analysis (3-Class)** | **83.67%** | **87.91%** | **0.4670** | 🏆 Production Sentiment Hero |
| Challenger LinearSVC | Sentiment Analysis (3-Class) | 89.00% | 92.31% | 0.5366 | Strong Linear Generalization |
| Primary Logistic Regression | Sentiment Analysis (3-Class) | 82.67% | 86.81% | 0.4624 | High Neutral Class Recall |
| Naive Star-Rating Baseline | Sentiment Analysis (3-Class) | 80.17% | 84.62% | 0.4102 | Heuristic (Fails on Sarcasm/Typos) |

> **Key Takeaway**: On clear human consensus reviews (where both independent human annotators agreed 100%), the Production Hero Ensemble reaches **94.12% agreement** on Operational Categories and **87.91% agreement** on Sentiment Polarity. Across the complete blind human benchmark ($N = 300$, loaded with sarcastic Bengali expressions, informal Banglish slang, and rating-text misclicks), the Ensemble maintains **91.33% agreement** on Operational Categories and **83.67% agreement** on Sentiment Polarity (with Challenger LinearSVC achieving **89.00%**), confirming robust generalization to real-world customer feedback.

* Detailed confusion matrices, operator breakdowns, and linguistic disagreement analyses are documented in **[`gold_standard_evaluation_report.md`](data/gold_set/gold_standard_evaluation_report.md)** and **[`comprehensive_benchmark_table.md`](data/gold_set/comprehensive_benchmark_table.md)**.

---

## 💼 6. Operator Strategic Roadmaps

### 1. Grameenphone (MyGP) — *Scale Anchor*
* **Common Period NSS:** `+64.9%` (320,143 reviews) | **2026 NSS:** `+56.8%` 📉
* **Core Vulnerabilities:** Billing deduction transparency (1.11%) and data pack pricing complaints (5.27%).
* **Strategic Lever:** Deploy dynamic micro-packs with rollover validity and a zero-click "Where Did My Balance Go?" transaction timeline.

### 2. Robi (MyRobi) — *Digital Lifestyle Leader*
* **Common Period NSS:** `+65.9%` (198,378 reviews) | **2026 NSS:** `+76.2%` 🚀
* **Core Vulnerabilities:** Offers and data pack friction (5.18%) and app login bugs (4.60%).
* **Strategic Lever:** Overhaul biometric login token caching and simplify automated VAS cancellation toggles.

### 3. Banglalink (MyBL) — *Agile Value Champion*
* **Common Period NSS:** `+53.1%` (137,149 reviews) | **2026 NSS:** `+81.9%` 🏆
* **Core Vulnerabilities:** Indoor/suburban 4G latency (3.64%) and technical login glitches (8.12%).
* **Strategic Lever:** Leverage high brand sentiment to transition promotional micro-rechargers into recurring monthly commitments while optimizing 4G edge caching.

---

## 📂 7. Repository Organization & File Structure

```text
telecom-Voice-of-Customer_intelligence/
├── assets/
│   ├── logos/                                # Official corporate logos (GP, Robi, BL)
│   └── plots/                                # Publication-grade 300 DPI visualizations
│       ├── multi_year_sentiment_trend_line.png # 📈 Complete All-Years NSS Trajectory (2016–2026, Full Range)
│       ├── yearly_sentiment_trend_pre2020.png  # 📉 Standalone Early Era Trajectory (2016–2019)
│       ├── yearly_sentiment_trend_2020_2026.png # 🚀 Standalone Modern Scale Trajectory (2020–2026)
│       ├── monthly_nss_trend_line.png          # 📅 Complete All-Months Continuous NSS (123 Months)
│       ├── monthly_nss_trend_pre2020.png       # 🔍 Standalone Early Era Monthly NSS (42 Months)
│       ├── monthly_nss_trend_2020_2026.png     # 📊 Standalone Modern Era Monthly NSS (81 Months)
│       ├── net_sentiment_score_comparison_bars.png
│       ├── operator_sentiment_distribution_bars.png
│       ├── operator_category_complaint_distribution_bars.png
│       ├── category_sentiment_stacked_bars.png
│       ├── sentiment_model_benchmark_bars.png  # 🏆 3-Class Sentiment model benchmark
│       └── category_model_benchmark_bars.png   # 🏷️ 5-Class Operational Category benchmark
│
├── data/                                     # Ground Truth & Human Validation Datasets
│   ├── processed/                            # 4,500 Multi-Operator Seed Reviews (GP, Robi, BL)
│   │   ├── mygp_classified_reviews.csv
│   │   ├── myrobi_classified_reviews.csv
│   │   └── mybl_classified_reviews.csv
│   └── gold_set/                             # 🏆 Verified Human Ground Truth & Cohen's Kappa
│       ├── blind_annotation_300_ratul.csv    # Primary human ground-truth labels (N=300)
│       ├── blind_annotation_200_friend.csv   # Overlapping independent secondary review (N=200)
│       ├── calculate_agreement.py            # Cohen's Kappa & inter-rater agreement evaluator
│       ├── ANNOTATION_RULEBOOK.md            # Standardized annotation protocol & edge cases
│       ├── gold_standard_evaluation_report.md # Comprehensive validation & agreement report
│       └── comprehensive_benchmark_table.md  # Multi-model vs human benchmark matrix
│
├── scraped_data_global_2020_2026/            # 🌟 MASTER DATASET SUITE (N=661,160)
│   ├── raw/                                  # 1. Scraped raw reviews (2014 - Oct 2026 with app_version)
│   │   ├── mygp_global_2020_to_sep2026.csv   # 321,374 unique reviews (Jul 2016 - Sep 2026)
│   │   ├── myrobi_global_2020_to_sep2026.csv # 200,652 unique reviews (Mar 2016 - Sep 2026)
│   │   ├── mybl_global_2020_to_sep2026.csv   # 139,134 unique reviews (Oct 2014 - Oct 2026)
│   │   └── robi_backfilled_gap_2024_2025.csv # Historical gap backfilled reviews
│   │
│   ├── classified/                           # 2. Classified Datasets & Common Benchmark
│   │   ├── all_operators_common_duration_classified.csv # 🏆 Active Benchmark (N=655,670 | 3,716 Days)*
│   │   ├── all_operators_classified_global_2020_2026.csv# Master Multi-Year Corpus (N=661,160 | 347 MB)*
│   │   ├── common_duration_summary.json      # Statistical metadata for shared 3,716-day window (2016–2026)
│   │   ├── mygp_classified_global_2020_2026.csv   # 321,374 classified reviews (GP)
│   │   ├── myrobi_classified_global_2020_2026.csv # 200,652 classified reviews (Robi)
│   │   ├── mybl_classified_global_2020_2026.csv   # 139,134 classified reviews (BL)
│   │   ├── global_multi_year_intelligence_report.md
│   │   ├── global_voc_intelligence_report.json
│   │   └── yearly_intelligence_trends.json
│   │
│   └── pipeline/                             # 3. High-Throughput Production Scripts
│       ├── run_parallel_scrapers.py          # Parallel scrapers (supports --incremental)
│       ├── scraper_worker.py                 # Multi-operator worker script
│       ├── backfill_robi_gap.py              # 🛠️ Fair multi-rating backfill scraper for historical gaps
│       ├── merge_and_sync_all_datasets.py    # Strict deduplication & common window extraction
│       ├── classify_global_dataset.py        # Batch classifies reviews across 8 ML/DL architectures
│       └── generate_global_visualizations.py # Dynamic 300 DPI publication plots (Complete & Standalone)
│
├── ml/                                       # Classical Machine Learning Engine
│   ├── models/
│   │   ├── sentiment_voting_classifier.joblib # 🏆 Production Hero Model (Sentiment, 87.5% CV)
│   │   ├── category_voting_classifier.joblib  # 🏷️ Production Category Hero Model (87.4% CV)
│   │   ├── primary_logistic_regression.joblib
│   │   └── challenger_linearsvc.joblib
│   └── predict.py                            # CLI dual prediction utility
│
├── dl/                                       # Deep Learning & Neural Models (Colab GPU Suites)
│   ├── telecom_voc_banglabert_finetuning_colab.ipynb # 🇧🇩 BUET BanglaBERT Fine-Tuning Suite (91.6% Acc)
│   ├── telecom_voc_master_unified_colab.ipynb # 🏆 Master Unified Colab: ALL ML + DL Models
│   ├── finetune_banglabert.py                # Standalone end-to-end BanglaBERT fine-tuning CLI
│   ├── models/
│   │   ├── banglabert_finetuned_sentiment/   # 🥇 SOTA Sentiment Model (91.60% CV Acc)
│   │   ├── banglabert_finetuned_category/    # 🥈 Category Model (85.27% CV Acc)
│   │   ├── bilstm_sentiment_model.pt         # Hybrid BiLSTM + Attention (Sentiment)
│   │   ├── bilstm_category_model.pt          # Hybrid BiLSTM + Attention (Category)
│   │   ├── bilstm_vocab.joblib               # Model vocabulary dictionary
│   │   └── minilm_sent_head.joblib           # Multilingual MiniLM Head
│   ├── reports/
│   │   └── banglabert_finetuning_report.txt  # Detailed classification metrics
│   └── README.md                             # Deep learning documentation
│
├── archive/                                  # 🗄️ ARCHIVED DATASETS & PROBES
│   ├── early_dl_experiments/                 # Early frozen head baseline experiments
│   ├── powerbi_dashboard/                    # Initial prototype Power BI interface recordings
│   ├── seed_pipeline_groq/                   # Phase 1 Groq LLM seed pipeline & datasets
│   └── scraped_data_2020/                    # Historical 402-day common window (N=83,417)
│       └── ios_probe/                        # Apple App Store empirical probe (N=1,199)
│
├── TODO.txt                                  # 📋 Future Roadmap & Deferred Tasks (HF Hub, Demo, Calibration)
├── requirements.txt                          # Top-level unified dependencies
└── README.md                                 # Master Repository Documentation
```

> *\* Note: Due to GitHub file-size limits, the consolidated datasets (`all_operators_classified_global_2020_2026.csv` [347 MB] and `all_operators_common_duration_classified.csv` [344 MB]) are omitted from Git. They are automatically reconstructed in seconds from the 3 tracked operator CSVs by running `sync_post_classification.py`.*

---

## ⚡ 8. Quickstart & Execution Guide

### 1. Initialize Python Environment
```bash
git clone https://github.com/rh61632/telecom-Voice-of-Customer_intelligence.git
cd telecom-Voice-of-Customer_intelligence

source ml/.venv/bin/activate
pip install -r requirements.txt
```

### 2. Refresh Data (Incremental — only fetches reviews newer than last scrape)
```bash
# Full re-scrape from scratch (first-time or reset):
python scraped_data_global_2020_2026/pipeline/run_parallel_scrapers.py

# Incremental update (appends only new reviews since last run — fast):
python scraped_data_global_2020_2026/pipeline/run_parallel_scrapers.py --incremental
```

### 3. Merge, Deduplicate & Re-Classify New Reviews
```bash
python scraped_data_global_2020_2026/pipeline/merge_and_sync_all_datasets.py
```

### 4. Render 300 DPI Visualizations
```bash
python scraped_data_global_2020_2026/pipeline/generate_global_visualizations.py
```

### 5. Real-Time CLI Inference
```bash
# High-throughput production dual inference (CPU, ~18,000 rev/s):
python ml/predict.py --text "নেটওয়ার্ক খুব বাজে কিন্তু অফার ভালো"
```

### 6. Interactive Google Colab Notebooks (GPU Training & SOTA Replication)
For GPU training without local hardware:
* **[BUET BanglaBERT SOTA Suite](dl/telecom_voc_banglabert_finetuning_colab.ipynb)**: End-to-end transformer fine-tuning achieving **91.60% Sentiment Accuracy**.
* **[Master Unified Suite](dl/telecom_voc_master_unified_colab.ipynb)**: Benchmarks all 8 ML/DL architectures in a single unified workflow.

### 7. Evaluate Inter-Annotator Reliability (Cohen's Kappa)
```bash
# Computes raw agreement, Cohen's Kappa, and confusion matrices across annotators:
python data/gold_set/calculate_agreement.py
```

---

## 🗺️ 9. Future Roadmap & Development Milestones

For active tracking of deferred milestones, model checkpoint hosting on Hugging Face Model Hub, and interactive Streamlit web demos, see **[TODO.txt](TODO.txt)**. Multi-annotator reliability verification (Cohen's Kappa $\kappa = 0.5762$ on Sentiment, $\kappa = 0.7694$ on Categories) is completed and documented in [`gold_standard_evaluation_report.md`](data/gold_set/gold_standard_evaluation_report.md).

---

## 📜 Citation & License

This project is licensed under the MIT License. If you use this methodology, multi-year dataset, or dual-gram code-switched Banglish feature extraction in your research:

```bibtex
@misc{telecom_voc_intelligence_2026,
  author = {Ratul Hasan},
  title = {Cross-Operator Voice of Customer (VoC) Intelligence Engine for Bangladesh Telecom Platforms},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/rh61632/telecom-Voice-of-Customer_intelligence}}
}
```

---

## 🙏 Acknowledgments

* **AI-Assisted Engineering:** Data pipeline automation, terminal interactive annotation tooling, and visualization suites were developed in collaborative pair-programming with **Google Antigravity** (Google DeepMind), adhering to COPE and ACM AI transparency guidelines.
* **LLM Weak Supervision:** Gratitude to **Groq** for high-throughput cloud inference (`qwen/qwen3.8-27b`) enabling initial zero-shot seed dataset translation and taxonomy labeling.
* **Open-Source Community:** Built upon foundational open-source packages including `scikit-learn`, `PyTorch`, `sentence-transformers`, `pandas`, `numpy`, `matplotlib`, and `google-play-scraper`.
