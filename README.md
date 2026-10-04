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
[![Main Dataset: 353.7k Reviews](https://img.shields.io/badge/Main%20Dataset-353%2C714%20Reviews-emerald.svg)](scraped_data_global_2020_2026/classified/)
[![Time Horizon: 2020--2026](https://img.shields.io/badge/Time%20Horizon-Jan%202020--Sep%202026-blueviolet.svg)](scraped_data_global_2020_2026/)
[![Archived Dataset: 83.4k](https://img.shields.io/badge/Archived%20Cohort-83%2C417%20Reviews-gray.svg)](archive/scraped_data_2020/)
[![Hero Model: Soft--Voting Ensemble](https://img.shields.io/badge/Hero%20Model-Ensemble%20(87.5%25%20Acc)-brightgreen.svg)](ml/)

</div>

---

## 🎯 1. Executive Summary & Market Intelligence

This flagship project provides an empirical, end-to-end Voice-of-Customer (VoC) intelligence engine analyzing customer sentiment and operational complaints across Bangladesh's top three mobile network operators:
* **Grameenphone Ltd.** (operating the MyGP platform)
* **Robi Axiata Limited** (operating the MyRobi platform)
* **Banglalink Digital Communications Limited** (operating the MyBL platform)

*(Throughout this document, operators are subsequently referred to as **Grameenphone**, **Robi**, and **Banglalink**).*

### 📊 Master Lifetime Performance Scorecard ($N = 353,714$, January 2020 – September 2026)

Every review across all 81 continuous months was scored by our production **Hero Soft-Voting Ensemble** (calibrated on 4,500 human-annotated multi-operator reviews, achieving **87.5% CV Accuracy** on Sentiment and **87.3%** on Operational Categories), cross-verified with **PyTorch BiLSTM + Attention**, **Balanced Logistic Regression**, and **Calibrated LinearSVC**.

```
+---------------------------------------------------------------------------------------------------------+
|                                    LIFETIME VoC PERFORMANCE SCORECARD                                   |
|                                    (January 1, 2020 – September 30, 2026)                               |
+----+----------------------+---------------+------------+-----------+------------+-----------------------+
|Rank| Operator             | Total Reviews | Positive % | Neutral % | Negative % | Net Sentiment (NSS)   |
+----+----------------------+---------------+------------+-----------+------------+-----------------------+
| 2  | Grameenphone (MyGP)  | 161,461       | 79.7%      | 10.4%     | 9.9%       | +69.8% (Scale Anchor) |
| 3  | Robi (MyRobi)        | 155,655       | 77.6%      | 10.4%     | 12.0%      | +65.6% (Engaged/Polar)|
| 1  | Banglalink (MyBL)    | 36,598        | 82.4%      | 9.0%      | 8.5%       | +73.9% (High Goodwill)|
+----+----------------------+---------------+------------+-----------+------------+-----------------------+
| -- | Industry Benchmark   | 353,714       | 79.1%      | 10.2%     | 10.7%      | +68.4%                |
+----+----------------------+---------------+------------+-----------+------------+-----------------------+
```

> **Net Sentiment Score (NSS) Formula**:  
> $$\text{NSS} = \left(\frac{N_{\text{Positive}} - N_{\text{Negative}}}{N_{\text{Total}}}\right) \times 100$$  
> *Consistent operator analysis serial: **Grameenphone**, **Robi**, **Banglalink**.*

---

## 📊 2. Visual Analytics & Publication Intelligence Suite

All visualizations are generated natively in Python at publication-grade **300 DPI** using verified brand hex palettes: **Grameenphone (`#0090ff`)**, **Robi (`#e60000`)**, and **Banglalink (`#ff7a00`)**.

### A. Market Net Sentiment Score & Sentiment Breakdown
| Net Sentiment Score (NSS) Comparison | Sentiment Share by Operator |
| :---: | :---: |
| <img src="assets/plots/net_sentiment_score_comparison_bars.png" width="450"/> | <img src="assets/plots/operator_sentiment_distribution_bars.png" width="450"/> |

### B. 6-Year Longitudinal Trajectory (2020 – 2026)
<div align="center">
  <img src="assets/plots/multi_year_sentiment_trend_line.png" width="900" alt="Multi-Year Net Sentiment Trajectory"/>
</div>

### C. Operational Complaint Breakdown & Departmental Sentiment
| Actionable Complaint Rates by Operator | Sentiment Composition per Comment Type |
| :---: | :---: |
| <img src="assets/plots/operator_category_complaint_distribution_bars.png" width="450"/> | <img src="assets/plots/category_sentiment_stacked_bars.png" width="450"/> |

---

## 📈 3. Longitudinal Trajectory & Inflection Points (2020 – 2026)

Tracking customer sentiment across 81 continuous months revealed three macro-level market events:

| Year | Grameenphone (MyGP) | Robi (MyRobi) | Banglalink (MyBL) | Historical Strategic Event |
| :---: | :---: | :---: | :---: | :--- |
| **2020** | — | **+63.6%** (32,333) | — | Pandemic surge in digital self-care adoption. |
| **2021** | — | **+63.8%** (30,296) | — | Nationwide 4G expansion; baseline stability. |
| **2022** | — | **+68.4%** (34,416) | — | Pre-inflationary consumer satisfaction peak. |
| **2023** | **+73.2%** (19,829) | **+48.7%** ⚠️ (16,784) | — | **The 2023 Robi Crisis**: Robi negative complaints surged to **19.5%** driven by aggressive airtime deductions and session crashes. GP maintained high trust (+73.2%). |
| **2024** | **+70.6%** (75,046) | **+52.1%** (6,816) | **+52.8%** (4,612) | GP dominated review volume with steady 70%+ NSS; Banglalink scaled into public view. |
| **2025** | **+70.3%** (54,244) | **+78.0%** 🚀 (16,112) | **+66.4%** (10,235) | **The 2025 Robi Turnaround**: Robi resolved backend latency, cutting negative reviews to just **6.0%**. |
| **2026** | **+56.8%** 📉 (12,342) | **+76.2%** (18,898) | **+81.9%** 🏆 (21,751) | **The 2026 Market Reversal**: Banglalink surged to industry-leading **+81.9% NSS** (only 5.2% negative); Grameenphone dipped sharply to **+56.8% NSS** (17.4% negative) due to data pack price increases and OTP delivery failures. |

---

## 🏷️ 4. Operational Category & Departmental Intelligence

Every review was classified into **5 operational domains** by our Soft-Voting Category Ensemble:

| Operational Category | Grameenphone (161.5k) | Robi (155.7k) | Banglalink (36.6k) | Operational Diagnosis |
| :--- | :---: | :---: | :---: | :--- |
| **Offers & Data Packs** | **5.30%** (8,559) | **5.09%** (7,922) | **3.36%** (1,228) | GP and Robi face **~50% more pricing friction** than Banglalink. |
| **App Login & Technical Bugs** | **2.31%** (3,725) | **4.45%** (6,926) | **2.97%** (1,088) | **Robi's Primary Vulnerability**: Nearly **2x the login/crash rate** of Grameenphone. |
| **Network Speed & 4G Latency** | **1.55%** (2,500) | **2.72%** (4,239) | **2.82%** (1,032) | Grameenphone maintains the strongest reputation for indoor 4G reliability. |
| **Billing & Airtime Loss** | **1.23%** (1,978) | **0.78%** (1,215) | **0.63%** (232) | **Grameenphone's Primary Vulnerability**: Double the accidental deduction complaints of Banglalink. |
| **General Appreciation / Other** | **89.62%** (144,699) | **86.96%** (135,353) | **90.22%** (33,018) | App praise, short reviews, emojis. |

---

## 🏆 5. Empirical Multi-Paradigm Benchmark Matrix

Models were trained and evaluated on the curated ground truth ($N=4,500$ across Grameenphone, Robi, and Banglalink) using **5-Fold Stratified Cross-Validation**:

| Model Architecture | Task | CV Accuracy | Macro-F1 | Inference Throughput | Key Strengths / Characteristics |
| :--- | :---: | :---: | :---: | :---: | :--- |
| 🥇 **Hero Soft-Voting ML Ensemble** | **Operational Category** | **87.44%** | **0.7845** | **~18,200 rev/s** | **Overall Champion**: Sub-word character n-grams excel on Romanized Banglish (*"mb"*, *"kete niyeche"*, *"otp"*). |
| 🥇 **Hero Soft-Voting ML Ensemble** | **Sentiment Analysis** | **87.47%** | **0.7684** | **~17,500 rev/s** | Balanced voting between Logistic Regression, Calibrated LinearSVC, and ComplementNB. |
| 🚀 **Multilingual MiniLM Head** | **Operational Category** | **81.15%** | **0.7247** | ~2,100 rev/s | 384-dim multilingual dense embeddings; resilient to English/Bengali code-mixing. |
| 🚀 **Multilingual MiniLM Head** | **Sentiment Analysis** | **82.33%** | **0.7475** | ~2,100 rev/s | Cross-lingual sentence semantic capture. |
| 🧠 **Hybrid BiLSTM + Attention (GPU)**| **Operational Category** | **80.84%** | **0.7106** | Fast GPU Batched | Bidirectional context + Bahdanau attention on salient complaint tokens. |
| 🧠 **Hybrid BiLSTM + Attention (GPU)**| **Sentiment Analysis** | **81.50%** | **0.7180** | Fast GPU Batched | PyTorch neural architecture with inverse frequency class weighting. |
| 🇧🇩 **BUET BanglaBERT Head** | **Operational Category** | **74.88%** | **0.6253** | GPU Required | Native Bengali representations; sensitive to Romanized Banglish transliterations. |
| 📉 **Statistical Floor (Dummy)** | **Operational Category** | **60.68%** | **0.1511** | Instant | Naive majority-class guess without language understanding. |

---

## 💼 6. Operator Strategic Roadmaps

### 1. Grameenphone (MyGP) — *Scale Anchor*
* **Lifetime NSS:** `+69.8%` | **2026 NSS:** `+56.8%` 📉
* **Core Vulnerabilities:** Billing deduction transparency (1.23%) and data pack pricing complaints (5.30%).
* **Strategic Lever:** Deploy dynamic micro-packs with rollover validity and a zero-click "Where Did My Balance Go?" transaction timeline.

### 2. Robi (MyRobi) — *Digital Lifestyle Leader*
* **Lifetime NSS:** `+65.6%` | **2026 NSS:** `+76.2%` 🚀
* **Core Vulnerabilities:** App login bugs (4.45%—highest in industry) and OTP delivery delays.
* **Strategic Lever:** Overhaul biometric login token caching and simplify automated VAS cancellation toggles.

### 3. Banglalink (MyBL) — *Agile Value Champion*
* **Lifetime NSS:** `+73.9%` | **2026 NSS:** `+81.9%` 🏆
* **Core Vulnerabilities:** Suburban and indoor 4G coverage gaps (2.82%).
* **Strategic Lever:** Leverage high brand sentiment to transition promotional micro-rechargers into recurring monthly commitments.

---

## 📂 7. Repository Organization & File Structure

```text
telecom-Voice-of-Customer_intelligence/
├── assets/
│   ├── logos/                                # Official corporate logos (GP, Robi, BL)
│   └── plots/                                # Publication-grade 300 DPI visualizations
│       ├── net_sentiment_score_comparison_bars.png
│       ├── operator_sentiment_distribution_bars.png
│       ├── multi_year_sentiment_trend_line.png
│       ├── operator_category_complaint_distribution_bars.png
│       └── category_sentiment_stacked_bars.png
│
├── scraped_data_global_2020_2026/            # 🌟 MAIN DATASET SUITE (N=353,714)
│   ├── raw/                                  # 1. Scraped raw reviews (2020 - Sep 2026)
│   │   ├── mygp_global_2020_to_sep2026.csv   # 161,461 reviews (17 MB)
│   │   ├── myrobi_global_2020_to_sep2026.csv # 155,655 reviews (20 MB)
│   │   └── mybl_global_2020_to_sep2026.csv   # 36,598 reviews (4 MB)
│   │
│   ├── classified/                           # 2. Fully Classified Multi-Model Datasets
│   │   ├── all_operators_classified_global_2020_2026.csv # Master dataset (353.7k rows, 96 MB)
│   │   ├── mygp_classified_global_2020_2026.csv
│   │   ├── myrobi_classified_global_2020_2026.csv
│   │   ├── mybl_classified_global_2020_2026.csv
│   │   ├── global_multi_year_intelligence_report.md
│   │   ├── global_voc_intelligence_report.json
│   │   └── yearly_intelligence_trends.json
│   │
│   └── pipeline/                             # 3. High-Throughput Production Scripts
│       ├── run_parallel_scrapers.py
│       ├── classify_global_dataset.py        # Batch classifies 353k reviews (~1,000 rev/s)
│       └── generate_global_visualizations.py # Renders 300 DPI publication plots
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
│   ├── telecom_voc_master_unified_colab.ipynb # 🏆 Master Unified Colab: ALL ML + DL Models
│   ├── models/
│   │   ├── bilstm_sentiment_model.pt         # Hybrid BiLSTM + Attention (Sentiment)
│   │   ├── bilstm_category_model.pt          # Hybrid BiLSTM + Attention (Category)
│   │   ├── bilstm_vocab.joblib               # Model vocabulary dictionary
│   │   └── minilm_sent_head.joblib           # Multilingual MiniLM Head
│   └── README.md                             # Deep learning documentation
│
├── archive/                                  # 🗄️ ARCHIVED DATASETS & PROBES
│   └── scraped_data_2020/                    # Historical 402-day common window (N=83,417)
│       ├── common_duration/                  # Archived 83.4k common duration cohort
│       ├── gold_set/                         # Human Gold Standard benchmark (N=600)
│       └── ios_probe/                        # Apple App Store empirical probe (N=1,199)
│
├── requirements.txt                          # Top-level dependencies
└── README.md                                 # Master Repository Documentation
```

---

## ⚡ 8. Quickstart & Execution Guide

### 1. Initialize Python Environment
```bash
git clone https://github.com/rh61632/telecom-Voice-of-Customer_intelligence.git
cd telecom-Voice-of-Customer_intelligence

source ml/.venv/bin/activate
pip install -r requirements.txt
```

### 2. Execute Batch Classification over All 353,714 Reviews
```bash
python scraped_data_global_2020_2026/pipeline/classify_global_dataset.py
```

### 3. Render 300 DPI Visualizations
```bash
python scraped_data_global_2020_2026/pipeline/generate_global_visualizations.py
```

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
