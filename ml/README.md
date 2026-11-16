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

Both sentiment models exist in the repository to balance historical reproducibility with state-of-the-art interactive inference:

| Model Artifact | Model Designation | Features & Architecture | Accuracy (Gold N=300) | Consensus (N=182) | Deployed Use Case & Rationale |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **`ensemble_voting_classifier.joblib`** | **Model B (Hero Inference Model)** | Word TF-IDF (1–2) + Soft Voting (LR + Calibrated LinearSVC + ComplementNB) | **89.00%** | **91.21%** | 🏆 **Default for CLI (`ml/predict.py`) & Web Demo (`demo/app.py`)**.<br>_Why chosen:_ Achieves the highest human ground-truth accuracy (+5.33% over Model A) by focusing on clean word tokens without noise from irregular letter n-grams. |
| **`sentiment_voting_classifier.joblib`** | **Model A (Global Corpus Classifier)** | Dual-Gram FeatureUnion: Word (1–2) + Char (3–5, 25k) + Soft Voting | 83.67% | 87.91% | 📦 **Preserved for Master Dataset Lineage (`classify_global_dataset.py`)**.<br>_Why preserved:_ Scored all 655,649 historical reviews in `all_operators_common_duration_classified.csv`; preserved verbatim to guarantee exact reproducibility of all historical longitudinal trends and metrics. |
| `category_voting_classifier.joblib` | Production Category Model | Dual-Gram FeatureUnion: Word (1–2) + Char (3–5, 25k) + Soft Voting | 91.33% | 94.12% | Production Operational Category Classification (5 Classes) |
| `category_ensemble_filtered_min3words.joblib` | Filtered Category Experiment | Word (1–2) + Char_wb (3–5) | 85.95% | — | Filtered Category Experiment ($\ge 3$ words) |
| `sentiment_ensemble_filtered_min3words.joblib` | Filtered Sentiment Experiment | Word (1–2) + Char_wb (3–5) | 87.37% | — | Filtered Sentiment Experiment ($\ge 3$ words) |

### 🔍 Why Model B Was Chosen Over Model A for Interactive Inference

While both models employ a tri-classifier soft-voting ensemble (Logistic Regression + Calibrated LinearSVC + ComplementNB), **Model B (`ensemble_voting_classifier.joblib`) was selected as the default interactive inference engine** for the following empirical reasons:

1. **Superior Human Agreement (+5.33% Gain on Gold Standard):**
   - On the primary blind-annotated human ground truth ($N = 300$), Model B achieves **89.00% accuracy** (Macro-F1: 0.6089) compared to Model A's **83.67% accuracy** (Macro-F1: 0.5625).
   - On the dual-human consensus subset ($N = 182$, where two independent reviewers reached 100% agreement), Model B reaches **91.21% accuracy** vs. Model A's **87.91%**.
2. **Noise Resistance on Short & Ambiguous Reviews:**
   - Model A includes character 3–5 n-grams, which occasionally overfit to sub-word character fragments in short slang or typos. Model B relies on regularized word unigrams and bigrams, avoiding sub-word false triggers.
3. **Preservation of Model A for Dataset Lineage:**
   - Rather than discarding Model A or silently re-scoring the 655k historical database (which would alter longitudinal monthly NSS timelines), Model A remains fully preserved in `ml/models/` to ensure end-to-end data provenance for all retrospective research.

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
