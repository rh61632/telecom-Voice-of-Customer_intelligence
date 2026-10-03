# 🤖 Telecom VoC Multilingual Sentiment Model

This directory contains the self-contained Machine Learning pipeline for sentiment classification across multilingual telecom reviews (Bangla script, Banglish / Romanized Bengali, and English).

---

## 🏗️ Architecture & Specifications

### 1. Feature Extractor: Character N-Gram TF-IDF
* **Configuration:**
  * `analyzer="char_wb"`
  * `ngram_range=(2, 5)`
  * `min_df=3`
  * `sublinear_tf=True`
* **Linguistic Role:** Sub-word character slicing within word boundaries captures phonetic roots across non-standardized Banglish spellings (e.g., `faltu`, `faaltu`, `faltoo`) while seamlessly processing native Bengali script and English in a single unified sparse representation.
* **Noise Mitigation:** Prunes rare typos and noisy singletons (`min_df=3`) while compressing repetitive frequency spikes (`sublinear_tf=True`).

### 2. Primary Classifier: Balanced Multinomial Logistic Regression
* **Configuration:**
  * `class_weight="balanced"`
  * `max_iter=1000`
  * `random_state=42`
* **Imbalance Handling:** Inverse frequency class weighting offsets the 61.6% Positive skew, boosting recall for minority Neutral reviews (~10.9%).
* **Inference Output:** Well-calibrated continuous posterior probabilities across all 3 sentiment classes (`Positive`, `Neutral`, `Negative`).

### 3. Benchmarks & Validation
* **Statistical Floor:** `DummyClassifier(strategy="most_frequent")`
* **Challenger:** `LinearSVC(class_weight="balanced", random_state=42)`
* **Validation Strategy:** 5-Fold Stratified Cross-Validation (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`)
* **Primary Metric:** Macro-Averaged F1 (`f1_macro`)

---

## 📊 Benchmark Results (4,500 Reviews)

| Model | Macro-F1 (Mean ± Std) | Accuracy (Mean ± Std) | Role |
| :--- | :---: | :---: | :--- |
| **DummyClassifier** (Most Frequent) | 0.2542 ± 0.0001 | 61.62% ± 0.05% | Baseline Floor |
| **Logistic Regression** (Balanced) | **0.7796 ± 0.0182** | **85.96% ± 1.36%** | **Primary Model (Selected)** |
| **LinearSVC** (Balanced) | **0.7852 ± 0.0142** | **87.89% ± 0.93%** | Challenger Model |

*Target range: 0.75–0.83 Macro-F1 achieved.*

---

## 🚀 Usage

### 1. Run Benchmark & Model Training
```bash
python ml/train_sentiment.py
```
This fits all models, outputs cross-validation scores, and saves model artifacts to `ml/models/`.

### 2. Inference via CLI
Single review inference:
```bash
python ml/predict.py --text "Network speed khub e baje, 4G thakleo kono kaje ase na"
```

Interactive shell:
```bash
python ml/predict.py
```
