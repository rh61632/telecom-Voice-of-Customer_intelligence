# Telecom Voice-of-Customer (VoC) Intelligence: 2020–2026 Extension & Gold Standard Pipeline

This directory contains the complete multi-brand Voice-of-Customer (VoC) intelligence system across Bangladesh's top 3 mobile network operators: **Grameenphone (MyGP)**, **Banglalink (MyBL)**, and **Robi (MyRobi)**.

It encompasses:
1. **Raw Scraped Reviews (2020 – Sep 2026)**
2. **Standardized 402-Day Common Duration Dataset (N=83,417 Reviews)**
3. **Production Multi-Model Classification (Soft-Voting Ensemble Hero Model vs Challengers)**
4. **Verified Human Gold Standard Dataset (N=600 Ground-Truth Reviews)**
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
├── gold_set/                                 # 3. Verified Human Gold Standard Dataset (N=600)
│   ├── gold_set_candidates.csv                     # Stratified 600-sample candidate cohort
│   ├── gold_set_verified.csv                       # 100% human-verified ground-truth dataset
│   ├── gold_standard_evaluation_report.md          # Scientific empirical validation report
│   ├── comprehensive_benchmark_table.md            # Definitive multi-model comparison table
│   └── plots/                                      # 300 DPI Empirical Validation Visualizations
│       ├── confusion_matrix_hero_ensemble.png      # Hero Model vs Human Gold Truth heatmap
│       ├── confusion_matrices_comparison_grid.png  # 2x2 multi-architecture comparison grid
│       ├── model_benchmark_f1_accuracy_bars.png    # Accuracy, Macro-F1 & Weighted-F1 comparison
│       └── operator_accuracy_gold_set_bars.png     # Gold Set accuracy broken down by operator
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

## 🏆 Key Benchmark Findings

| Model Architecture | Role | Gold Matches (N=600) | Gold Accuracy | Macro F1 | Weighted F1 | 83k Consensus | CPU Speed |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 🏆 **Soft-Voting Ensemble** | **Hero Model** | **492 / 600** | **82.00%** | **0.6781** | **0.8237** | **100.0%** | **17,495 rev/s** |
| Challenger LinearSVC | Linear Benchmark | 476 / 600 | 79.33% | 0.6305 | 0.7987 | 98.93% | 37,297 rev/s |
| Logistic Regression | Baseline | 452 / 600 | 75.33% | 0.6347 | 0.7783 | 96.44% | 37,891 rev/s |
| BiLSTM + Attention | Deep Learning | 429 / 600 | 71.50% | 0.6231 | 0.7541 | 91.84% | 490 rev/s |
| Star-Rating Baseline | Heuristic | 481 / 600 | 80.17% | 0.5510 | 0.7685 | 86.12% | Instant |

---

## 📊 Business Intelligence Scorecard (N=83,417 Reviews)

* **Banglalink (MyBL):** Net Sentiment Score = **+81.5%** (88.3% Pos, 6.8% Neg). *Agile value champion; high promotional dynamism.*
* **Robi (MyRobi):** Net Sentiment Score = **+79.4%** (86.5% Pos, 7.1% Neg). *Digital lifestyle & high self-care UI engagement.*
* **Grameenphone (MyGP):** Net Sentiment Score = **+56.6%** (75.0% Pos, 18.4% Neg). *Premium anchor; highest feature utility but higher price sensitivity.*
