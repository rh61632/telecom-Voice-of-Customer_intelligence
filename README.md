# 📡 Telecom Voice-of-Customer (VoC) Intelligence Engine
> **An enterprise end-to-end NLP & Business Intelligence pipeline for multilingual sentiment parsing, customer experience benchmarking, and operational strategy across Bangladesh's premier telecommunications operators.**

<div align="center">

| <img src="assets/logos/gp.png" height="55" alt="Grameenphone"/> | <img src="assets/logos/banglalink.png" height="55" alt="Banglalink"/> | <img src="assets/logos/robi.png" height="55" alt="Robi"/> |
| :---: | :---: | :---: |
| **Grameenphone** | **Banglalink** | **Robi Axiata** |
| `com.portonics.mygp` | `com.arena.banglalinkmela.app` | `net.omobio.robisc` |
| **MyGP Platform** | **MyBL Platform** | **My Robi Platform** |

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dataset: 83.4k Reviews](https://img.shields.io/badge/Dataset-83%2C417%20Reviews-emerald.svg)](scraped_data_2020/common_duration/)
[![Gold Standard: N=600](https://img.shields.io/badge/Gold%20Standard-600%20Verified%20Samples-purple.svg)](scraped_data_2020/gold_set/)
[![Hero Model: Soft--Voting Ensemble](https://img.shields.io/badge/Hero%20Model-Ensemble%20(82.0%25%20Acc)-brightgreen.svg)](ml/)

</div>

---

## 🎯 Executive Summary & Key Highlights

This flagship project provides an empirical, end-to-end Voice-of-Customer (VoC) intelligence system analyzing customer feedback for Bangladesh's top 3 mobile network operators. 

By eliminating seasonal distortion through an identical **402-day common temporal duration (August 24, 2025 – September 30, 2026)** across **83,417 customer reviews**, this pipeline benchmarks multi-paradigm NLP architectures (Classical ML vs. Neural Sequence Models vs. Pretrained Transformers) and validates them against a **100% human-verified Gold Standard ground truth (N=600)**.

```
+---------------------------------------------------------------------------------------------------+
|                                  EXECUTIVE VoC PERFORMANCE SCORECARD                              |
+-------------------+---------------+------------+-----------+------------+-------------------------+
| Operator          | Total Reviews | Positive % | Neutral % | Negative % | Net Sentiment (NSS)     |
+-------------------+---------------+------------+-----------+------------+-------------------------+
| Banglalink (MyBL) | 28,068        | 88.3%      | 4.9%      | 6.8%       | +81.5% (High Goodwill)  |
| Robi (MyRobi)     | 33,825        | 86.5%      | 6.4%      | 7.1%       | +79.4% (Broad Engagement|
| Grameenphone(MyGP)| 21,524        | 75.0%      | 6.6%      | 18.4%      | +56.6% (Premium Anchor) |
+-------------------+---------------+------------+-----------+------------+-------------------------+
| Industry Baseline | 83,417        | 84.1%      | 5.9%      | 9.9%       | +74.2%                  |
+-------------------+---------------+------------+-----------+------------+-------------------------+
```
*Note: Net Sentiment Score (NSS) = % Positive Reviews − % Negative Reviews. Model inter-agreement exceeds 96% across ML architectures.*

---

## 📊 Visual Analytics & Intelligence Suite

All visualizations are generated natively in Python at publication-grade **300 DPI**:

### 1. Market Net Sentiment Score (NSS) & Sentiment Breakdown
| Net Sentiment Score (NSS) Scorecard | Sentiment Share by Operator |
| :---: | :---: |
| <img src="scraped_data_2020/common_duration/plots/net_sentiment_score_comparison_bars.png" width="450"/> | <img src="scraped_data_2020/common_duration/plots/operator_sentiment_distribution_bars.png" width="450"/> |

### 2. 14-Month Temporal Trajectory (Aug 2025 – Sep 2026)
<div align="center">
  <img src="scraped_data_2020/common_duration/plots/monthly_sentiment_trend_line.png" width="850" alt="Monthly NSS Trend"/>
</div>

---

## 🏗️ Technical Architecture & Data Lineage

```text
[Google Play Store Ingestion Pipeline]
           │  (Historical Scraping: 2020 to Sep 2026)
           ▼
[scraped_data_2020/raw/*.csv] (35 MB, Multi-Year Review Archives)
           │
           ▼  (Strict Temporal Alignment Filter)
[scraped_data_2020/common_duration/*.csv] (402 Shared Days: Aug 24, 2025 to Sep 30, 2026 | N=83,417)
           │
           ▼  (Multi-Model High-Throughput Inference Engine)
  ├── 1. Soft-Voting Ensemble ML (TF-IDF sub-word n-grams) ──► 17,495 reviews/sec [HERO MODEL]
  ├── 2. Calibrated LinearSVC (Linear Maximum Margin)     ──► 37,297 reviews/sec
  ├── 3. Balanced Logistic Regression (Linear Probabilistic)──► 37,891 reviews/sec
  └── 4. Hybrid BiLSTM + Bahdanau Attention (Neural Seq)   ──►    490 reviews/sec
           │
           ▼  (Active Human-in-the-Loop Stratification)
[scraped_data_2020/gold_set/gold_set_candidates.csv]
  ├── 50% Consensus Anchors
  ├── 30% Multi-Model Disagreements (Stress-Test Cases)
  └── 20% Low-Confidence Ambiguous Code-Switched Cases
           │
           ▼  (Interactive CLI Annotation with Undo & Jump Navigation)
[scraped_data_2020/gold_set/gold_set_verified.csv] (N=600 Human Verified Ground Truth)
           │
           ▼  (Empirical Scientific Evaluation & BI Synthesis)
  ├── gold_standard_evaluation_report.md
  └── telecom_voc_business_intelligence_report.md
```

---

## 🏆 Empirical Model Benchmark (Validated on Human Gold Standard)

To rigorously determine the production **Hero Model**, all architectures were benchmarked against the verified **Gold Standard Dataset (N=600)**:

| Model Architecture | Model Role | Gold Matches (N=600) | Gold Accuracy | Macro F1 | Weighted F1 | 83k Consensus | CPU Speed | Final Verdict |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 🏆 **Soft-Voting Ensemble** | **Hero Model** | **492 / 600** | **82.00%** | **0.6781** | **0.8237** | **100.0%** *(Ref)* | **~17,495 rev/s** | **Undisputed Champion: Best accuracy, highest F1 & Banglish resilience** |
| **Calibrated LinearSVC** | Challenger | 476 / 600 | 79.33% | 0.6305 | 0.7987 | 98.93% | ~37,297 rev/s | High-speed linear baseline; 98.9% alignment with Hero |
| **Balanced Logistic Regression** | Linear Baseline | 452 / 600 | 75.33% | 0.6347 | 0.7783 | 96.44% | ~37,891 rev/s | Strong neutral recall; lightweight inference |
| **Deep Learning BiLSTM + Attention**| Neural Sequence | 429 / 600 | 71.50% | 0.6231 | 0.7541 | 91.84% | ~490 rev/s | Solid sequential syntax; sensitive to OOV slang/emojis |
| **Star-Rating Baseline** | Naive Heuristic | 481 / 600 | 80.17% | 0.5510 | 0.7685 | 86.12% | Instant | Naive rule; collapses on Neutral (`F1 = 0.106`) & Sarcasm |

### Confusion Matrix Validations (N=600 Human Ground Truth)
| Hero Model (Soft-Voting Ensemble) | Multi-Architecture Comparison (2×2 Grid) |
| :---: | :---: |
| <img src="scraped_data_2020/gold_set/plots/confusion_matrix_hero_ensemble.png" width="420"/> | <img src="scraped_data_2020/gold_set/plots/confusion_matrices_comparison_grid.png" width="480"/> |

---

## 🔍 Key Qualitative & Linguistic Discoveries

Human-in-the-loop annotation exposed critical failure modes that automated heuristics and deep sequence models miss:

1. **Bengali Sarcasm & Mockery (Where Humans Win):**
   * *Customer Text:* `"লোট পাটের জন্য সেরা রে"` *(Rating: 5★)*
   * **Human Ground Truth:** `Negative`
   * **All Automated Models:** `Positive`
   * **Insight:** The reviewer awarded 5 stars sarcastically while writing *"Best for looting [the customer] haha"*. Automated models were fooled by the 5-star rating and the positive keyword *"সেরা"* (best). Human annotation captured the socio-linguistic irony.

2. **Star-Rating Misalignment (1-Star User Mistakes):**
   * *Customer Text:* `"ভালো"` *(Rating: 1★)*
   * **Human Ground Truth:** `Positive`
   * **Star Heuristic:** `Negative`
   * **Ensemble ML:** `Positive`
   * **Insight:** Mobile users frequently misclick 1 star by accident while writing glowing reviews. The Ensemble model correctly trusted textual semantics over the star rating.

3. **Code-Switched Slang & Contractions:**
   * *Customer Text:* `"nc app 🫠"` *(Rating: 5★)*
   * **Human Ground Truth:** `Positive`
   * **Ensemble ML:** `Positive`
   * **BiLSTM:** `Neutral`
   * **Insight:** The sub-word character n-grams of the TF-IDF Ensemble recognized *"nc"* as *"nice"*, whereas word-level neural tokenizers failed on out-of-vocabulary contractions.

---

## 💼 Cross-Operator Strategic Intelligence

### 1. Grameenphone (MyGP) — *Premium Anchor*
* **Net Sentiment Score:** `+56.6%` (75.0% Positive, 18.4% Negative)
* **Strengths:** Market-leading digital self-care ecosystem, high app stability, deep lifestyle integration (Flexiplan, emergency balance, health services).
* **Friction Points:** Data bundle unit pricing, rapid validity expiration, and balance deduction transparency.
* **Strategic Lever:** Deploy dynamic micro-packs with rollover validity and a zero-click "Where Did My Balance Go?" transaction timeline.

### 2. Banglalink (MyBL) — *Agile Value Champion*
* **Net Sentiment Score:** `+81.5%` (88.3% Positive, 6.8% Negative)
* **Strengths:** Strongest consumer goodwill, aggressive promotional bundles, highly popular gamified daily loyalty rewards.
* **Friction Points:** Suburban and indoor data throughput drops, peak-hour OTP delivery delays.
* **Strategic Lever:** Transition promotional micro-rechargers into recurring monthly packs via personalized bundle recommendations.

### 3. Robi Axiata (MyRobi) — *Digital Lifestyle Leader*
* **Net Sentiment Score:** `+79.4%` (86.5% Positive, 7.1% Negative)
* **Strengths:** Highly engaging personalized UI (*Amar Offer*), seamless multi-account management, responsive recharge flows.
* **Friction Points:** Inadvertent Value-Added Service (VAS) auto-renewals, occasional balance sync lag post-recharge.
* **Strategic Lever:** Implement a 1-tap "Active Subscriptions" dashboard with instant cancellation toggles to protect high user goodwill.

---

## 📂 Repository File Structure

```text
telecom-Voice-of-Customer_intelligence/
├── assets/
│   ├── logos/                                # Brand logo assets (GP, Banglalink, Robi)
│   ├── page1_demo.gif                        # Interactive dashboard recording
│   └── page2_demo.gif                        # VoC inspector recording
│
├── ml/                                       # Classical Machine Learning Engine
│   ├── models/
│   │   ├── ensemble_voting_classifier.joblib # 🏆 Production Hero Model (17.5k rev/s)
│   │   ├── challenger_linearsvc.joblib       # Calibrated LinearSVC Model
│   │   └── primary_logistic_regression.joblib# Balanced Logistic Regression Model
│   ├── train_ensemble.py                     # Ensemble training script
│   ├── train_sentiment.py                    # Classical ML trainer
│   └── predict.py                            # CLI prediction utility
│
├── dl/                                       # Deep Learning & Neural Models
│   ├── models/
│   │   ├── bilstm_attention_model.pt         # Hybrid BiLSTM + Bahdanau Attention
│   │   └── minilm_transformer_head.pt        # Multilingual MiniLM Transformer Head
│   ├── train_bilstm.py                       # PyTorch BiLSTM trainer
│   ├── train_transformer.py                  # Transformer fine-tuner
│   └── predict_dl.py                         # Deep Learning inference engine
│
├── scraped_data_2020/                        # Multi-Year Extension & Production Pipeline
│   ├── README.md                             # Pipeline execution documentation
│   │
│   ├── raw/                                  # 1. Raw multi-year datasets (2020 to Sep 2026, 35 MB)
│   │   ├── all_operators_scraped_2020_to_sep2026.csv
│   │   ├── mygp_scraped_2020_to_sep2026.csv
│   │   ├── mybl_scraped_2020_to_sep2026.csv
│   │   └── myrobi_scraped_2020_to_sep2026.csv
│   │
│   ├── common_duration/                      # 2. Standardized 402-day shared duration (N=83,417)
│   │   ├── all_operators_common_duration.csv
│   │   ├── classified_all_operators_pretrained.csv
│   │   ├── mygp_classified_pretrained.csv
│   │   ├── mybl_classified_pretrained.csv
│   │   ├── myrobi_classified_pretrained.csv
│   │   ├── telecom_voc_business_intelligence_report.md
│   │   └── plots/                            # 300 DPI VoC Visualizations
│   │
│   ├── gold_set/                             # 3. Verified Human Gold Standard (N=600)
│   │   ├── gold_set_candidates.csv
│   │   ├── gold_set_verified.csv
│   │   ├── gold_standard_evaluation_report.md
│   │   ├── comprehensive_benchmark_table.md
│   │   └── plots/                            # 300 DPI Validation Visualizations
│   │
│   └── pipeline/                             # 4. Sequentially Numbered Pipeline Scripts
│       ├── 01_scrape_2020_to_sep2026.py
│       ├── 02_create_common_duration.py
│       ├── 03_classify_with_pretrained_models.py
│       ├── 04_interactive_gold_annotator.py
│       ├── 05_evaluate_gold_set.py
│       └── 06_generate_visualizations.py
│
├── requirements.txt                          # Top-level dependencies
└── README.md                                 # Master Repository Documentation
```

---

## ⚡ Quickstart & Reproducibility Guide

### 1. Initialize Python Environment
```bash
git clone https://github.com/rh61632/telecom-Voice-of-Customer_intelligence.git
cd telecom-Voice-of-Customer_intelligence

source ml/.venv/bin/activate
pip install -r requirements.txt
```

### 2. Execute End-to-End Pipeline
```bash
# Step 1: Extract standardized 402-day shared duration cohort (N=83,417)
python scraped_data_2020/pipeline/02_create_common_duration.py

# Step 2: Classify all 83,417 reviews using pre-trained models (~17.5k reviews/sec)
python scraped_data_2020/pipeline/03_classify_with_pretrained_models.py

# Step 3: Launch interactive CLI annotator to verify or inspect Gold Standard reviews
python scraped_data_2020/pipeline/04_interactive_gold_annotator.py

# Step 4: Compute empirical metrics and generate benchmark reports
python scraped_data_2020/pipeline/05_evaluate_gold_set.py

# Step 5: Render all publication-grade 300 DPI heatmaps and bar charts
python scraped_data_2020/pipeline/06_generate_visualizations.py
```

---

## 📜 Citation & License

This project is licensed under the MIT License. If you use this methodology, code-switched Banglish preprocessing, or empirical Gold Standard benchmarking in your research or commercial applications, please cite:

```bibtex
@misc{telecom_voc_intelligence_2026,
  author = {Ratul Hasan and Antigravity AI},
  title = {Cross-Operator Voice of Customer (VoC) Intelligence Engine for Bangladesh Telecom Platforms},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/rh61632/telecom-Voice-of-Customer_intelligence}}
}
```
