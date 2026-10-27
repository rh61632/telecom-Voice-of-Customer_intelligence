# Telecom Voice-of-Customer (VoC) Intelligence: 2020–2026 Extension & Gold Standard Pipeline

This directory contains the complete multi-brand Voice-of-Customer (VoC) intelligence system across Bangladesh's top 3 mobile network operators: **Grameenphone (MyGP)**, **Banglalink (MyBL)**, and **Robi (MyRobi)**.

It encompasses:
1. **Raw Scraped Reviews (2020 – Sep 2026)**
2. **Standardized 402-Day Common Duration Dataset (N=83,417 Reviews)**
3. **Production Multi-Model Classification (Soft-Voting Ensemble Hero Model vs Challengers)**
4. **Verified Human Ground-Truth Dataset (N=300 Primary, N=200 Dual-Annotator Consensus)**
5. **Executive Business Intelligence & Scientific Benchmark Reports**
6. **Publication-Quality 300 DPI Visualizations (Heatmaps & Trend Charts)**

---

## 📁 Directory Structure

```text
scraped_data_2020/
├── README.md                                 # Master directory guide & reproduction instructions
│
├── raw/                                      # 1. Raw scraped multi-year reviews (2020 to Sep 2026)
│   ├── all_operators_scraped_2020_to_sep2026.csv   (18 MB, all operators combined)
│   ├── mygp_scraped_2020_to_sep2026.csv            (9.2 MB, Grameenphone)
│   ├── mybl_scraped_2020_to_sep2026.csv            (6.2 MB, Banglalink)
│   └── myrobi_scraped_2020_to_sep2026.csv          (2.2 MB, Robi)
│
├── common_duration/                          # 2. Standardized 402-day shared duration (Aug 2025 - Sep 2026)
│   ├── all_operators_common_duration.csv           (Unclassified shared dataset, N=83,417)
│   ├── classified_all_operators_pretrained.csv     (Master production dataset with all model predictions)
│   ├── mygp_classified_pretrained.csv              (Classified Grameenphone, N=21,524)
│   ├── mybl_classified_pretrained.csv              (Classified Banglalink, N=28,068)
│   ├── myrobi_classified_pretrained.csv            (Classified Robi, N=33,825)
│   ├── telecom_voc_business_intelligence_report.md # Executive BI Report with strategic recommendations
│   ├── classification_summary_pretrained.txt       # Production consensus & Net Sentiment summary
│   └── plots/                                      # 300 DPI VoC Visualizations
│       ├── net_sentiment_score_comparison_bars.png # Net Sentiment Score (NSS) scorecard
│       ├── operator_sentiment_distribution_bars.png# Positive / Neutral / Negative distributions
│       └── monthly_sentiment_trend_line.png        # 14-month temporal NSS trajectory
│
├── gold_set/archived_600_plan/                # 3. Legacy 600-sample draft files (Active human gold set is in data/gold_set/)
│
└── pipeline/                                 # 4. End-to-End Pipeline Scripts (Numbered for sequential execution)
    ├── 01_scrape_2020_to_sep2026.py                # Scrapes Play Store reviews from 2020 to Sep 2026
    ├── 02_create_common_duration.py                # Extracts exact 402-day shared duration overlap
    ├── 03_classify_with_pretrained_models.py       # High-throughput multi-model classification
    ├── 04_interactive_gold_annotator.py            # Terminal interactive labeling tool (with undo & jump)
    ├── 05_evaluate_gold_set.py                     # Evaluates models against human ground truth
    ├── 06_generate_visualizations.py               # Generates all 300 DPI heatmaps and bar charts
    └── benchmark_cv_models.py                      # 5-fold cross-validation benchmarking utility
```

---

## ⚡ Execution Pipeline (Reproducibility Guide)

All scripts dynamically resolve paths relative to the project root and can be executed from anywhere:

```bash
# Activate the python environment
source ml/.venv/bin/activate

# Step 1: Extract shared 402-day duration overlap across all brands
python scraped_data_2020/pipeline/02_create_common_duration.py

# Step 2: Classify all 83,417 reviews using existing pre-trained models
python scraped_data_2020/pipeline/03_classify_with_pretrained_models.py

# Step 3: Run the interactive Gold Standard terminal annotator (Resume or review)
python scraped_data_2020/pipeline/04_interactive_gold_annotator.py

# Step 4: Compute empirical metrics and generate benchmark reports
python scraped_data_2020/pipeline/05_evaluate_gold_set.py

# Step 5: Generate all publication-quality visual plots (Heatmaps, NSS Bars, Trend Lines)
python scraped_data_2020/pipeline/06_generate_visualizations.py
```

*(Note: Legacy shortcut scripts `prepare_gold_set.py`, `generate_all_visualizations.py`, etc., in the `scraped_data_2020/` folder are preserved for convenience).*

---

## 🏆 Key Benchmark Findings (Evaluated on Verified Human Ground Truth, N=300)

| Model Architecture | Evaluated Task | Human Agreement (N=300) | Consensus Agreement | Cohen's Kappa ($\\kappa$) | Operational Role |
| :--- | :---: | :---: | :---: | :---: | :--- |
| 🏆 **Soft-Voting Ensemble** | **Operational Category (5-Class)** | **91.33%** | **94.12%** | **0.5046** | **Production Category Hero** |
| Challenger LinearSVC | Operational Category (5-Class) | 91.00% | 93.58% | 0.4679 | High Linear Baseline |
| Primary Logistic Regression | Operational Category (5-Class) | 89.33% | 91.98% | 0.4385 | Balanced Regularized Baseline |
| 🏆 **Soft-Voting Ensemble** | **Sentiment Analysis (3-Class)** | **83.67%** | **87.91%** | **0.4670** | **Production Sentiment Hero** |
| Challenger LinearSVC | Sentiment Analysis (3-Class) | 89.00% | 92.31% | 0.5366 | Strong Linear Generalization |
| Primary Logistic Regression | Sentiment Analysis (3-Class) | 82.67% | 86.81% | 0.4624 | High Neutral Class Recall |
| Star-Rating Baseline | Sentiment Analysis (3-Class) | 80.17% | 84.62% | 0.4102 | Heuristic Baseline |

---

## 📊 Business Intelligence Scorecard (N=83,417 Reviews)

* **Banglalink (MyBL):** Net Sentiment Score = **+81.5%** (88.3% Pos, 6.8% Neg). *Agile value champion; high promotional dynamism.*
* **Robi (MyRobi):** Net Sentiment Score = **+79.4%** (86.5% Pos, 7.1% Neg). *Digital lifestyle & high self-care UI engagement.*
* **Grameenphone (MyGP):** Net Sentiment Score = **+56.6%** (75.0% Pos, 18.4% Neg). *Premium anchor; highest feature utility but higher price sensitivity.*
