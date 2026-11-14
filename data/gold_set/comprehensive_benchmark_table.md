# Comprehensive Benchmark & Validation Table
**Telecom Voice-of-Customer Intelligence Framework**

---

## 1. Human Inter-Annotator Agreement (Cohen's Kappa Study)

* **Dual-Review Cohort:** $N = 200$ Stratified Reviews (67 GP, 67 BL, 66 Robi)
* **Annotation Mode:** 100% Blind (Model suggestions & metadata hidden)
* **Rulebook:** Compliant with [`ANNOTATION_RULEBOOK.md`](ANNOTATION_RULEBOOK.md)

| Dimension | Classes | Paired Reviews | Raw Agreement (%) | Cohen's Kappa ($\kappa$) | Standard Interpretation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Sentiment Analysis** | 3 (`Positive`, `Neutral`, `Negative`) | 200 | **91.00%** | **0.5762** | Moderate Agreement (High Consistency) |
| **Operational Category** | 5 (`Billing`, `Bugs`, `Network`, `Offers`, `Other`) | 196 | **95.41%** | **0.7694** | **Substantial Agreement** |

### Operator-by-Operator Sentiment Reliability
| Operator | Cohort Size ($N$) | Raw Agreement (%) | Cohen's Kappa ($\kappa$) | Reliability Tier |
| :--- | :---: | :---: | :---: | :--- |
| **Grameenphone** | 67 | 89.55% | **0.6921** | Substantial Agreement |
| **Banglalink** | 67 | **94.03%** | **0.4846** | Moderate Agreement |
| **Robi** | 66 | 89.39% | **0.3400** | Fair-to-Moderate Agreement |

---

## 2. Model Performance on Active Gold Standard Ground Truth

Evaluated on the active human-verified gold cohort ($N = 300$, 100 reviews per operator) and the dual-human consensus subset ($N = 182$ Sentiment, $N = 187$ Category). Historical prototype $g600$ figures have been retired in favor of these verified active benchmarks.

### Sentiment Analysis Models on Active Gold Standard ($N = 300$)
| Architecture | Model Artifact / Name | Accuracy | Macro F1 | Weighted F1 | Cohen's Kappa ($\kappa$) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Soft-Voting Ensemble** | `ensemble_voting_classifier.joblib` | **89.00%** | **0.6089** | **0.8820** | **0.5150** | 🏆 **Hero CLI/Demo Model** |
| **Challenger LinearSVC** | `challenger_linearsvc.joblib` | **89.00%** | **0.6330** | **0.8862** | **0.5366** | Strong Linear Baseline |
| **Soft-Voting Ensemble** | `sentiment_voting_classifier.joblib` | 83.67% | 0.5625 | 0.8638 | 0.4670 | Production Global Corpus Model |
| **Logistic Regression** | `primary_logistic_regression.joblib` | 82.67% | 0.5836 | 0.8577 | 0.4624 | High Neutral Recall |
| **BiLSTM + Attention** | `bilstm_attention_model.pt` (Word+Char-CNN) | 79.67% | 0.5790 | 0.8409 | — | Sequence Baseline |
| **BiLSTM** | `bilstm_sentiment_model.pt` (Colab Word-only) | 78.67% | 0.5364 | 0.8297 | — | Colab Sequence Baseline |
| **Star-Rating Baseline** | 1-2★=Neg, 3★=Neu, 4-5★=Pos | 86.67% | 0.5438 | 0.8539 | 0.4244 | Naive Heuristic (Fails on Sarcasm) |

### Operational Category Models on Active Gold Standard ($N = 300$)
| Architecture | Model Artifact / Name | Accuracy | Macro F1 | Weighted F1 | Cohen's Kappa ($\kappa$) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Soft-Voting Ensemble** | `category_voting_classifier.joblib` | **91.33%** | 0.4919 | **0.9098** | **0.5046** | 🏆 **Production Category Model** |
| **Challenger LinearSVC** | `category_linearsvc.joblib` | 91.00% | 0.4904 | 0.9051 | 0.4679 | High Linear Baseline |
| **Logistic Regression** | `category_logistic_regression.joblib` | 89.33% | 0.4760 | 0.8985 | 0.4385 | Balanced Regularized Baseline |
| **BiLSTM** | `bilstm_category_model.pt` (Colab Word-only) | **91.33%** | **0.5154** | **0.9132** | — | Colab Sequence Model |

### Performance on Dual-Human Consensus Subset ($N = 182$ Sentiment, $N = 187$ Category)
On reviews where both independent human annotators reached complete consensus:

| Task & Architecture | Model / Heuristic | Consensus Accuracy | 3-Class / 5-Class Macro F1 | 2-Class Macro F1 (Neg, Pos) | Cohen's Kappa ($\kappa$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Sent:** Soft-Voting Ensemble | `ensemble_voting_classifier.joblib` | **91.21%** | 0.4589 | **0.6884** | 0.3253 |
| **Sent:** Soft-Voting Ensemble | `sentiment_voting_classifier.joblib` | 87.91% | **0.4769** | **0.7153** | **0.4031** |
| **Sent:** Challenger LinearSVC | `challenger_linearsvc.joblib` | **91.21%** | 0.4519 | — | 0.3233 |
| **Sent:** Logistic Regression | `primary_logistic_regression.joblib` | 85.71% | 0.4560 | — | 0.3569 |
| **Sent:** Star-Rating Baseline | Heuristic (1-2★=Neg, 3★=Neu, 4-5★=Pos) | 92.86% | 0.5282 | — | 0.5593 |
| **Cat:** Soft-Voting Ensemble | `category_voting_classifier.joblib` | **94.12%** | 0.5166 | — | **0.5403** |
| **Cat:** Challenger LinearSVC | `category_linearsvc.joblib` | **94.12%** | 0.5166 | — | **0.5403** |
| **Cat:** Logistic Regression | `category_logistic_regression.joblib` | 92.51% | 0.5181 | — | 0.5077 |
| **Cat:** BiLSTM Category | `bilstm_category_model.pt` | **94.12%** | **0.6153** | — | — |

> **Note on the Sentiment Consensus ($N = 182$) 0-Neutral Statistical Artifact:**  
> The dual-human consensus sentiment cohort consists of 169 Positive, 13 Negative, and **0 Neutral** reviews because Annotator 2 assigned zero Neutral labels across the 200 evaluated reviews. Consequently, any automated model that predicts one or more `Neutral` classifications on this subset incurs a precision penalty and an undefined/zero ground-truth recall for Neutral ($F_1(\text{Neutral}) = 0.0$), depressing 3-class unweighted Macro-F1. For this reason, both 3-class Macro-F1 and 2-class Macro-F1 (Negative vs. Positive) as well as Raw Accuracy are reported.

---

## 3. Production Artifact Manifest

* **Primary Annotator (Annotator 1):** [`blind_annotation_300_annotator1.csv`](blind_annotation_300_annotator1.csv) ($N=300$)
* **Secondary Annotator (Annotator 2):** [`blind_annotation_200_annotator2.csv`](blind_annotation_200_annotator2.csv) ($N=200$)
* **Kappa Evaluation Engine:** [`calculate_agreement.py`](calculate_agreement.py)
* **Comprehensive Report:** [`gold_standard_evaluation_report.md`](gold_standard_evaluation_report.md)
