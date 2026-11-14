# 🤖 Telecom VoC Multilingual Sentiment & Category Models

This directory contains the self-contained Classical Machine Learning pipeline for sentiment and operational category classification across multilingual telecom reviews (Bangla script, Banglish / Romanized Bengali, and English).

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

### 2. Primary Classifiers & Ensembles
* **Configuration:**
  * `class_weight="balanced"`
  * `max_iter=1000`
  * `random_state=42`
* **Imbalance Handling:** Inverse frequency class weighting offsets the 61.6% Positive skew, boosting recall for minority Neutral reviews (10.84%, 488/4,500).
* **Inference Output:** Well-calibrated continuous posterior probabilities across all 3 sentiment classes (`Positive`, `Neutral`, `Negative`) and 5 operational categories.

### 3. Benchmarks & Validation
* **Statistical Floor:** `DummyClassifier(strategy="most_frequent")`
* **Primary Baseline:** `LogisticRegression(class_weight="balanced", random_state=42)`
* **Challenger:** `CalibratedClassifierCV(LinearSVC(class_weight="balanced", random_state=42))`
* **Hero Ensemble:** Soft-voting ensemble combining Logistic Regression, Calibrated LinearSVC, and ComplementNB.
* **Validation Strategy:** 5-Fold Stratified Cross-Validation (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`)
* **Primary Metric:** Macro-Averaged F1 (`f1_macro`)

---

## 📊 Benchmark Results (4,500 Seed Reviews)

### Sentiment 5-Fold Stratified Cross-Validation

| Model | Macro-F1 (Mean ± Std) | Accuracy (Mean ± Std) | Role |
| :--- | :---: | :---: | :--- |
| **DummyClassifier** (Most Frequent) | 0.2542 ± 0.0001 | 61.64% ± 0.04% | Baseline Floor |
| **Logistic Regression** (Balanced) | **0.7779 ± 0.0229** | **85.87% ± 1.80%** | Primary Baseline |
| **LinearSVC** (Balanced) | **0.7798 ± 0.0147** | **87.64% ± 0.93%** | Challenger Model |
| **VotingClassifier (Local CLI/Demo)** | **0.7820 ± 0.0213** | **87.84% ± 1.13%** | **CLI & Demo Hero Model** |

---

## 🚀 Deployed Production & Ensemble Models

| Model Artifact | Origin / Task | Features | Macro-F1 | Accuracy | Deployed Use Case |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `ensemble_voting_classifier.joblib` | Local (`train_ensemble.py`) / Sentiment | Char TF-IDF (2–5) min_df=3 | 0.7820 ± 0.0213 | 87.84% ± 1.13% | Interactive CLI (`ml/predict.py`) & Web Demo (`demo/app.py`) |
| `sentiment_voting_classifier.joblib` | Google Colab / Sentiment | Word (1–2, 12k) + Char (3–5, 25k) | 0.7688 ± 0.0186 | 87.44% ± 1.31% | Global 661k Corpus Classification (`classify_global_dataset.py`) |
| `category_voting_classifier.joblib` | Google Colab / 5 Categories | Word (1–2, 12k) + Char (3–5, 25k) | 0.7794 ± 0.0146 | 87.33% ± 0.81% | Production Operational Category Classification |
| `category_ensemble_filtered_min3words.joblib` | Local (`train_filtered_experiments.py`) | Word (1–2) + Char_wb (3–5) | 0.7803 | 85.95% | Filtered Category Experiment ($\ge 3$ words) |
| `sentiment_ensemble_filtered_min3words.joblib` | Local (`train_filtered_experiments.py`) | Word (1–2) + Char_wb (3–5) | 0.7822 | 87.37% | Filtered Sentiment Experiment ($\ge 3$ words) |

---

## 🛠️ Pipeline & Training Scripts

- **`ml/train_sentiment.py`**: Benchmarks sentiment baseline models (Dummy, Logistic Regression, LinearSVC) with 5-fold Stratified CV on $N=4,500$ customer reviews.
- **`ml/train_category.py`**: Benchmarks 5 operational telecom categories using sub-word char and word TF-IDF feature union aligned with the Colab hero pipeline (`category_voting_classifier.joblib`).
- **`ml/train_ensemble.py`**: Trains the soft-voting ensemble (`ensemble_voting_classifier.joblib`) combining Logistic Regression, Calibrated LinearSVC, and ComplementNB for CLI and Demo inference.
- **`ml/train_filtered_experiments.py`**: Conducts short-text filtering ablation studies ($N=4,500$, $N=3,887$, $N=2,286$), evaluates performance against the active human gold standard (`blind_annotation_300_annotator1.csv`), and dynamically exports `short_text_filtering_ablation_study.md`.

---

## 💻 Usage

### 1. Run Benchmark & Model Training
```bash
python ml/train_sentiment.py
python ml/train_category.py
python ml/train_ensemble.py
python ml/train_filtered_experiments.py
```

### 2. Inference via CLI
Single review inference:
```bash
python ml/predict.py --text "Network speed khub e baje, 4G thakleo kono kaje ase na"
```

Interactive shell:
```bash
python ml/predict.py
```
