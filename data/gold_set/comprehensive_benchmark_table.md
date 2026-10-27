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

## 2. Model Performance on Gold Standard Ground Truth

Evaluated on the curated human-verified gold cohort:

| Architecture | Model Family | Accuracy | Macro F1 | Weighted F1 | Macro Precision | Macro Recall | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Soft-Voting Ensemble** | LogisticRegression + LinearSVC (TF-IDF) | **82.00%** | **0.6781** | **0.8237** | **0.6717** | **0.6961** | 🏆 **Hero Model** |
| **LinearSVC** | Support Vector Machine (C=1.0) | 79.33% | 0.6305 | 0.7987 | 0.6192 | 0.6536 | Challenger |
| **Logistic Regression** | Balanced Elastic-penalized | 75.33% | 0.6347 | 0.7783 | 0.6138 | 0.7038 | High Neutral Recall |
| **BiLSTM + Attention** | Neural Word+Char BiLSTM (128d) | 71.50% | 0.6231 | 0.7541 | 0.6230 | 0.6934 | Sequence Baseline |
| **Star-Rating Baseline** | 1-2★=Neg, 3★=Neu, 4-5★=Pos | 80.17% | 0.5510 | 0.7685 | 0.5789 | 0.5530 | Naive Heuristic |

---

## 3. Production Artifact Manifest

* **Primary Annotator (Ratul):** [`blind_annotation_300_ratul.csv`](blind_annotation_300_ratul.csv) ($N=300$)
* **Secondary Annotator (Friend):** [`blind_annotation_200_friend.csv`](blind_annotation_200_friend.csv) ($N=200$)
* **Kappa Evaluation Engine:** [`calculate_agreement.py`](calculate_agreement.py)
* **Comprehensive Report:** [`gold_standard_evaluation_report.md`](gold_standard_evaluation_report.md)

