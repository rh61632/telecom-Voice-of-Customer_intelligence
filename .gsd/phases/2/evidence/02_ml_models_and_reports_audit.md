# Empirical Audit: Classical ML Models, Provenance, Training Scripts, and Evaluation Reports

**Phase:** 2 — ML/DL Models, Gold Standard & Empirical Audit Scripts  
**Plan:** 2.2 — Task 1 Evidence  
**Audit Timestamp:** 2026-11-11  
**Python Runtime:** 3.15.1 (`scikit-learn 1.9.1`, `joblib 1.6.0`, `torch 2.15.0+cpu`, `pandas 2.3.2`, `numpy 2.4.2`)  
**Operating Mode:** Read-Only (`ADR-001`, `ADR-002`)  

---

## 1. Seed Dataset Inventory & Sample Drift Audit (`N = 4,500` vs `N = 4,499`)

### 1.1 Ground Truth File Inspection
Direct empirical inspection of the 3 processed seed CSV files in `data/processed/` reveals the true sample counts:

| Seed CSV Path | Rows | Columns | Operator | Nulls Detected | Sentiment Breakdown | Operational Category Breakdown |
|---|---|---|---|---|---|---|
| `data/processed/mygp_classified_reviews.csv` | 1,500 | 8 (`operator` missing) | Grameenphone (implied) | `operator: 1500` (column absent) | Pos: 919, Neg: 417, Neu: 164 | Gen: 888, Off: 288, App: 139, Net: 118, Bill: 67 |
| `data/processed/mybl_classified_reviews.csv` | 1,500 | 9 | Banglalink | 0 | Pos: 934, Neg: 402, Neu: 164 | Gen: 923, Off: 247, App: 140, Net: 122, Bill: 68 |
| `data/processed/myrobi_classified_reviews.csv` | 1,500 | 9 | Robi | 0 | Pos: 921, Neg: 419, Neu: 160 | Gen: 920, Off: 253, App: 121, Net: 124, Bill: 82 |
| **Combined Ground Truth (`total_df`)** | **4,500** | — | **3 Operators** | **0 Nulls in text/sent/cat** | **Pos: 2,774 / Neg: 1,238 / Neu: 488** | **Gen: 2,731 / Off: 788 / App: 400 / Net: 364 / Bill: 217** |

### 1.2 Stale References to `N = 4,499` and Pre-Commit Counts
Across several reports and scripts, outdated counts from prior revisions (specifically commit `60cf0f4` before commit `3e453d0` fixed an off-by-one duplicate in `mygp_classified_reviews.csv`) persist:

1. **`ml/README.md:23,34`**:
   - Line 23: *"boosting recall for minority Neutral reviews (~10.9%)"* (reflects $489 / 4499 = 10.87\%$, whereas live count is $488 / 4500 = 10.84\%$).
   - Line 34: Header says `## Benchmark Results (4,500 Reviews)`, but the text below was generated against the older 4,499 split.
2. **`ml/reports/category_classification_report.md:5,33,37`**:
   - Line 5: *"Trained on $N = 4,499$ multi-operator customer reviews across Grameenphone, Robi, and Banglalink."*
   - Line 33: `General Appreciation / Other` support is reported as **`2730`** (live dataset has **`2,731`**).
   - Line 37: `accuracy` row reports support as **`4499`** instead of **`4500`**.
3. **`ml/reports/short_text_filtering_ablation_study.md:12`**:
   - Table row 1 reports: `| **Full Dataset (No Filter)** | 4,499 | 100.0% | ...`
4. **`scripts/evaluate_linguistic_subcohorts.py:156` & `ml/reports/linguistic_subcohort_report.md:5`**:
   - Line 5: Prose explicitly states: *"the customer review corpus ($N = 4,499$) was partitioned into three distinct linguistic sub-cohorts"*, while the benchmark table row 5 immediately below it reports `N = 4,500`.

---

## 2. Serialized Classical ML Models Inspection (`ml/models/*.joblib`)

All 9 `.joblib` models in `ml/models/` were deserialized and inspected via Python reflection under Python 3.15.1 (`scikit-learn 1.9.1`).

### 2.1 Model Registry & Version Warning Audit

| Model Filename | Architecture | Pickler Sklearn Version | Local Warnings (Sklearn 1.9.1) | Features Pipeline | Prediction on Test Sentence* | Predicted Probabilities |
|---|---|---|---|---|---|---|
| `category_voting_classifier.joblib` | `VotingClassifier` (soft) | **1.6.1** | **34 InconsistentVersionWarnings** | `FeatureUnion` (`word` [1,2] `max_f=12000`, `char` [3,5] `max_f=25000`) | Network Speed & 4G Latency | `[0.0039, 0.0133, 0.0059, 0.9610, 0.0159]` |
| `sentiment_voting_classifier.joblib` | `VotingClassifier` (soft) | **1.6.1** | **28 InconsistentVersionWarnings** | `FeatureUnion` (`word` [1,2] `max_f=12000`, `char` [3,5] `max_f=25000`) | Negative | `[0.5142, 0.1812, 0.3046]` |
| `ensemble_voting_classifier.joblib` | `VotingClassifier` (soft) | 1.9.1 | 0 warnings | `char_wb` [2,5] (`min_df=3`, `max_f=None`) | Negative | `[0.4889, 0.2159, 0.2952]` |
| `primary_logistic_regression.joblib` | `LogisticRegression` | 1.9.1 | 0 warnings | `char_wb` [2,5] (`min_df=3`, `max_f=None`) | Negative | `[0.5304, 0.2930, 0.1765]` |
| `challenger_linearsvc.joblib` | `LinearSVC` | 1.9.1 | 0 warnings | `char_wb` [2,5] (`min_df=3`, `max_f=None`) | Negative | N/A (`AttributeError: predict_proba`) |
| `category_logistic_regression.joblib` | `LogisticRegression` | 1.9.1 | 0 warnings | `FeatureUnion` (`word` [1,2], `char_wb` [3,5] `min_df=3`, `max_f=None`) | Network Speed & 4G Latency | `[0.0071, 0.0105, 0.0161, 0.9546, 0.0117]` |
| `category_linearsvc.joblib` | `CalibratedClassifierCV(LinearSVC)` | 1.9.1 | 0 warnings | `FeatureUnion` (`word` [1,2], `char_wb` [3,5] `min_df=3`, `max_f=None`) | Network Speed & 4G Latency | `[0.0017, 0.0142, 0.0062, 0.9662, 0.0116]` |
| `category_ensemble_filtered_min3words.joblib` | `VotingClassifier` (soft) | 1.9.1 | 0 warnings | `FeatureUnion` (`word` [1,2], `char_wb` [3,5]) | Network Speed & 4G Latency | `[0.0446, 0.0508, 0.0479, 0.8058, 0.0510]` |
| `sentiment_ensemble_filtered_min3words.joblib` | `VotingClassifier` (soft) | 1.9.1 | 0 warnings | `FeatureUnion` (`word` [1,2], `char_wb` [3,5]) | **Positive** *(DIVERGENCE!)* | `[0.4058, 0.1832, 0.4110]` |

*\* Test sentence: `"Network speed khub baje, taka kete niyeche"` ("Network speed is very bad, money has been deducted").*

### 2.2 Critical Provenance Findings

1. **`category_voting_classifier.joblib` Provenance Discrepancy:**
   - **Local script (`ml/train_category.py:84-133`)** constructs:
     - `char_tfidf`: `analyzer="char_wb"`, `ngram_range=(3, 5)`, `min_df=3`, `max_features=None`.
     - `word_tfidf`: `ngram_range=(1, 2)`, `min_df=2`, `max_features=None`.
     - `lr`: `LogisticRegression(C=1.0, class_weight="balanced")`.
     - `cnb`: `ComplementNB(alpha=1.0, norm=True)`.
     - `VotingClassifier`: `weights=[2, 2, 1]`.
   - **Serialized disk artifact (`ml/models/category_voting_classifier.joblib`)** contains:
     - `char_tfidf`: `analyzer="char"`, `ngram_range=(3, 5)`, `min_df=2`, `max_features=25000`.
     - `word_tfidf`: `ngram_range=(1, 2)`, `min_df=2`, `max_features=12000`.
     - `lr`: `LogisticRegression(C=2.5, class_weight="balanced")`.
     - `cnb`: `ComplementNB(alpha=0.5, norm=False)`.
     - `VotingClassifier`: `weights=[2.0, 2.5, 1.0]`.
     - `_sklearn_version`: `1.6.1`.
   - **Empirical Provenance Confirmation:**
     This exact pipeline configuration matches lines 387–436 and Cell 7 of [`dl/telecom_voc_master_unified_colab.ipynb`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_master_unified_colab.ipynb#L387-L436) which was packaged in Cell 18 as `telecom_voc_all_models_colab.zip`. Thus, `category_voting_classifier.joblib` was **not** produced by `ml/train_category.py`, but downloaded from Google Colab.
   - Conversely, `category_logistic_regression.joblib` and `category_linearsvc.joblib` were trained locally by `ml/train_category.py` (matching `char_wb`, `min_df=3`, `max_features=None`, `sklearn 1.9.1`).

2. **Prediction Divergence on Negative Benglish Review:**
   - On the complaint `"Network speed khub baje, taka kete niyeche"`, while all baseline and full-corpus sentiment models classified it as **Negative** (Ensemble: 48.89% Neg, Voting: 51.42% Neg, Primary LR: 53.04% Neg), the filtered model `sentiment_ensemble_filtered_min3words.joblib` misclassified it as **Positive** (`Positive 41.10%` vs `Negative 40.58%`).
   - This occurs because the filtered ensemble was trained with word-level FeatureUnion where vocabulary distribution shifted after stripping 1–2 word reviews.

---

## 3. Training Script Bugs, Report Discrepancies, and Logic Gaps

### 3.1 `ml/train_category.py` Standard Deviation Duplication Bug
In [`ml/train_category.py:247`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/ml/train_category.py#L247):
```python
md_content += f"| **{name}** | {m['mean_macro_f1']:.4f} ± {m['mean_macro_f1']:.4f} | {m['mean_weighted_f1']:.4f} | {m['mean_acc']*100:.2f}% ± {m['std_acc']*100:.2f}% | {status} |\n"
```
- **Bug:** The macro-F1 standard deviation formatting parameter repeats `m['mean_macro_f1']` instead of using `m['std_macro_f1']`. If executed, the output would print e.g. `0.7845 ± 0.7845`.
- **Report Divergence:** The committed report [`ml/reports/category_classification_report.md:11-14`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/ml/reports/category_classification_report.md#L11-L14) contains legitimate standard deviations (`0.7845 ± 0.0190`, `0.7687 ± 0.0195`, `0.7781 ± 0.0175`). Furthermore, lines 16–25 of `category_classification_report.md` include a `## Google Colab GPU Benchmark (Multi-Paradigm Comparison)` table copied from `ml/reports/category_benchmark_summary.csv`.
- **Risk:** Re-running `ml/train_category.py` will overwrite `category_classification_report.md`, introducing the corrupted standard deviations and erasing the GPU Benchmark table.

### 3.2 `ml/train_filtered_experiments.py` Dead Gold Path & Internal Contradiction
1. **Dead Gold Path:**
   - [`ml/train_filtered_experiments.py:19`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/ml/train_filtered_experiments.py#L19) defines:
     ```python
     GOLD_CSV = PROJECT_ROOT / "scraped_data_2020" / "gold_set" / "gold_set_verified.csv"
     ```
   - Because `scraped_data_2020/` was relocated to `archive/scraped_data_2020/`, `GOLD_CSV.exists()` evaluates to `False`. Lines 138–139 silently return `0.0, 0.0`, rendering re-training of ablation gold evaluations broken without editing the path.
2. **Table vs Prose Contradiction in Ablation Report:**
   - In [`ml/reports/short_text_filtering_ablation_study.md:12-14`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/ml/reports/short_text_filtering_ablation_study.md#L12-L14):
     - Table indicates: Full Dataset Gold Macro-F1 = **`0.6737`**, Filtered ($\ge 3$ words) = **`0.7318`** ($\Delta = \mathbf{+5.81\%}$).
   - In [`ml/reports/short_text_filtering_ablation_study.md:18-19`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/ml/reports/short_text_filtering_ablation_study.md#L18-L19):
     - Prose header: *"Massive Surge in Gold Standard Macro-F1 (+6.55% to +7.80%)"*
     - Prose body: *"jumped from `0.6781` on the full dataset up to `0.7436` when removing 1-2 word reviews (≥ 3$ words)."*
   - Origin of contradiction: The prose hardcodes metrics from an older character-only pipeline evaluated on the archived 600-sample gold set (`0.6781` -> `0.7436`), while the markdown table records metrics generated by the `FeatureUnion(word + char_wb)` pipeline in `train_filtered_experiments.py` (`0.6737` -> `0.7318`). Lines 19 and 37 also suffer from broken LaTeX `(≥ 3$ words)`.

### 3.3 `scripts/evaluate_linguistic_subcohorts.py` Cohort Omission & Stratification Defect
1. **Omission of Symbolic Reviews:**
   - In [`scripts/evaluate_linguistic_subcohorts.py:104-109`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/scripts/evaluate_linguistic_subcohorts.py#L104-L109), the benchmark cohorts list explicitly defines only:
     - Bangla (Native Script): 1,091 samples (24.24%)
     - Romanized Banglish: 390 samples (8.67%)
     - English: 3,005 samples (66.78%)
     - Overall (Cross-Validation): 4,500 samples (100.0%)
   - The 14 `Symbolic / Emoticons` reviews (0.31% of the corpus) are silently excluded from the subcohort rows while being included in the Overall CV calculation ($1091 + 390 + 3005 = 4486 \ne 4500$).
2. **Cross-Validation Stratification Leak:**
   - Line 81 performs `cv.split(X, y_cat)` for both `cat_fold_clf` and `sent_fold_clf`. Stratifying cross-validation folds along category labels when fitting sentiment models results in unstratified sentiment distributions across folds.

### 3.4 `ml/language_detector.py` Threshold Contradiction
In [`ml/language_detector.py:6,86,147-156`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/ml/language_detector.py#L6):
- The module docstring (line 6) and `__init__` (line 86) specify adherence to **Gambäck & Das (2016)** with a dominance threshold of **$\ge 70\%$** (`dominance_threshold=0.70`).
- However, the decision logic in lines 147–156:
  ```python
  if banglish_matches > 0 and banglish_ratio >= 0.15:
      lang = "Romanized Banglish"
  elif english_ratio >= self.dominance_threshold and banglish_matches == 0:
      lang = "English"
  elif banglish_matches > 0:
      lang = "Romanized Banglish"
  elif english_ratio >= 0.60:
      lang = "English"
  else:
      lang = "Romanized Banglish"
  ```
- **Contradiction:** Because line 153 falls through to `elif english_ratio >= 0.60: lang = "English"` whenever `banglish_matches == 0`, any review with between 60% and 69.9% English tokens and zero Banglish markers is classified as English. This lowers the effective dominance threshold from 70% to 60%, contradicting the paper citations and docstrings. Furthermore, the check `banglish_ratio >= 0.15` in line 147 is rendered redundant by line 151 (`elif banglish_matches > 0:`).

### 3.5 Global Language Distribution Date-Range Discrepancy
- [`ml/reports/global_language_distribution.md:3`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/ml/reports/global_language_distribution.md#L3) claims:
  *"Analyzed 661,160 multi-operator reviews covering a full decade (2016–2026)."*
- In reality, the underlying JSON file [`ml/reports/global_language_distribution.json:90-152`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/ml/reports/global_language_distribution.json#L90-L152) and the dataset `all_operators_classified_global.csv` span from **2014 to 2026** (with 183 reviews in 2014 and 910 reviews in 2015). The prose misrepresents the temporal window as 2016–2026.

### 3.6 Dependency Omission in `ml/requirements.txt`
[`ml/requirements.txt`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/ml/requirements.txt) specifies `scikit-learn`, `scipy`, `joblib`, `pandas`, and `numpy`. It completely omits **`nltk`**, which is imported directly at module load by:
- [`ml/language_detector.py:18`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/ml/language_detector.py#L18) (`from nltk.corpus import words`)
- [`ml/predict.py:13`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/ml/predict.py#L13) (`from language_detector import LanguageClassifier`)

A fresh virtual environment installing only `ml/requirements.txt` fails immediately on `import language_detector`.

---

## 4. Verification Proof

Execution of CLI inference check:
```powershell
python ml/predict.py --text "valo service"
```
**Output (`rc=0`):**
```
=================================================================
Model Architecture    : ENSEMBLE ML
Input Review          : valo service
Detected Language     : Romanized Banglish [Code-Mixed]
Predicted Sentiment   : Positive (Confidence: 68.95%)
Predicted Comment Type: General Appreciation / Other (Confidence: 95.76%)

Sentiment Class Probabilities:
  - Negative:  18.17% ████
  - Neutral :  12.88% ███
  - Positive:  68.95% █████████████████
=================================================================
```
