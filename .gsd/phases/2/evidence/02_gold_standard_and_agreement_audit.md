# Empirical Audit: Gold Standard Dataset Provenance, Inter-Annotator Agreement, and Benchmark Provenance Leakage

**Phase:** 2 — ML/DL Models, Gold Standard & Empirical Audit Scripts  
**Plan:** 2.2 — Task 2 Evidence  
**Audit Timestamp:** 2026-11-11  
**Python Runtime:** 3.15.1 (`scikit-learn 1.9.1`, `pandas 2.3.2`, `numpy 2.4.2`)  
**Operating Mode:** Read-Only (`ADR-001`, `ADR-002`)  

---

## 1. Inter-Annotator Reliability & Cohen's Kappa Empirical Verification

### 1.1 Script Execution & Overall Agreement
Executing `python data/gold_set/calculate_agreement.py` under Python 3.15.1 against the dual blind annotation CSV files:
- Primary Annotator ($N = 300$): `data/gold_set/blind_annotation_300_annotator1.csv`
- Secondary Annotator ($N = 200$): `data/gold_set/blind_annotation_200_annotator2.csv`
- Overlapping Evaluation Cohort: $N = 200$ pairs (Grameenphone: 67, Banglalink: 67, Robi: 66)

**Empirical Results:**

| Evaluation Dimension | Evaluated Pairs ($N$) | Raw Agreement (%) | Cohen's Kappa ($\kappa$) | Standard Interpretation (Landis & Koch 1977) |
|---|---|---|---|---|
| **Sentiment Classification** | 200 | **91.00%** (182 / 200) | **$\kappa = 0.5762$** | Moderate Agreement |
| **Operational Category Classification** | 196* | **95.41%** (187 / 196) | **$\kappa = 0.7694$** | Substantial Agreement |

*\* 4 reviews had null or `Unclassified` category labels in Annotator 2's submission, leaving 196 complete pairs.*

### 1.2 Per-Operator Reliability Metrics
Direct calculation across the overlapping 200 reviews validates the per-operator table in [`data/gold_set/comprehensive_benchmark_table.md:18-22`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/data/gold_set/comprehensive_benchmark_table.md#L18-L22) to four decimal places:

| Operator Cohort | Overlap Count ($N$) | Sentiment Raw Agreement (%) | Sentiment Cohen's Kappa ($\kappa$) | Category Overlap ($N$) | Category Agreement (%) | Category Cohen's Kappa ($\kappa$) |
|---|---|---|---|---|---|---|
| **Grameenphone** | 67 | 89.55% | **0.6921** (Substantial) | 65 | 92.31% | **0.7979** (Substantial) |
| **Banglalink** | 67 | 94.03% | **0.4846** (Moderate) | 65 | 98.46% | **0.7937** (Substantial) |
| **Robi** | 66 | 89.39% | **0.3400** (Fair) | 66 | 95.45% | **0.6087** (Moderate) |

### 1.3 De-Anonymization Defect in `calculate_agreement.py`
Lines 77–78, 154, and 188 of [`data/gold_set/calculate_agreement.py`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/data/gold_set/calculate_agreement.py) output personal names rather than anonymized roles:
```text
Ratul CSV : .../blind_annotation_300_annotator1.csv
Friend CSV: .../blind_annotation_200_annotator2.csv
Confusion Matrix (Rows: Ratul, Columns: Friend):
```
Furthermore, the script does not output the per-operator breakdown table despite those numbers being published in `comprehensive_benchmark_table.md`.

---

## 2. Critical Benchmark Provenance Contradiction (`g600` vs `g300`)

### 2.1 The Published Claims vs Archive Notice
1. **The Archival Notice:**
   [`archive/scraped_data_2020/gold_set/archived_600_plan/README.md:3,11,16`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/archive/scraped_data_2020/gold_set/archived_600_plan/README.md#L3) explicitly asserts:
   - *"The files in this directory are preserved strictly for historical record and experimental provenance. They represent an early, exploratory 600-sample evaluation plan that was **discarded and never executed** as a human annotation study."*
   - *"However, comprehensive manual human annotation for 600 reviews was **never performed**."*
   - *"All active project reports, paper manuscripts, and repository documentation reference the authentic $N = 300$ / $N = 200$ human ground truth."*
2. **The Active Published Reports:**
   Contradicting this statement, [`data/gold_set/comprehensive_benchmark_table.md:28-36`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/data/gold_set/comprehensive_benchmark_table.md#L28-L36) and [`data/gold_set/gold_standard_evaluation_report.md:18-58`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/data/gold_set/gold_standard_evaluation_report.md#L18-L58) present a full benchmark leaderboard, an operator-by-operator table ($200 + 200 + 200 = 600$), and a confusion matrix ($54+5+17 + 22+35+15 + 27+22+403 = 600$).

### 2.2 Empirical Demonstration of the Provenance Leakage
All deployed models were evaluated in a controlled read-only Python harness on both the archived 600-sample dataset (`archive/.../gold_set_verified.csv`) and the active 300-sample ground-truth dataset (`data/gold_set/blind_annotation_300_annotator1.csv`):

| Model Evaluated | Archived Dataset (`g600`, $N = 600$) | Published in `comprehensive_benchmark_table.md` & `report.md` | Active Human Ground Truth (`g300`, $N = 300$) | Discrepancy Note |
|---|---|---|---|---|
| **`ensemble_voting_classifier.joblib`** | **Acc: 82.00% / Macro-F1: 0.6781** | **Acc: 82.00% / Macro-F1: 0.6781** | **Acc: 89.00% / Macro-F1: 0.6089** | **Exact match to archived `g600`**; on `g300`, Accuracy is $+7.00\%$ higher while Macro-F1 is $-0.0692$ lower |
| **`challenger_linearsvc.joblib`** | **Acc: 79.33% / Macro-F1: 0.6305** | **Acc: 79.33% / Macro-F1: 0.6305** | **Acc: 89.00% / Macro-F1: 0.6330** | **Exact match to archived `g600`** |
| **`primary_logistic_regression.joblib`** | **Acc: 75.33% / Macro-F1: 0.6347** | **Acc: 75.33% / Macro-F1: 0.6347** | **Acc: 82.67% / Macro-F1: 0.5836** | **Exact match to archived `g600`** |
| `sentiment_voting_classifier.joblib` | Acc: 82.00% / Macro-F1: 0.6908 | *(Not listed in gold report)* | Acc: 83.67% / Macro-F1: 0.5625 | Model used for 655k global corpus |
| `category_voting_classifier.joblib` | *(g600 lacks category labels)* | *(Not evaluated in gold report)* | Acc: 91.33% / Macro-F1: 0.4919 | Category evaluation on $N=300$ active gold |

### 2.3 Proof of Confusion Matrix and Operator Breakdown Provenance
In [`data/gold_set/gold_standard_evaluation_report.md:34-58`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/data/gold_set/gold_standard_evaluation_report.md#L34-L58):
- Section 2 states: *"each operator was independently evaluated on an identical cohort of 200 reviews"* (Grameenphone 200, Robi 200, Banglalink 200 = 600 total).
- Section 3 confusion matrix:
  - True Negative: $54 + 5 + 17 = 76$
  - True Neutral: $22 + 35 + 15 = 72$
  - True Positive: $27 + 22 + 403 = 452$
  - Total: $76 + 72 + 452 = \mathbf{600}$.
- Direct query of `gold_sentiment` in `archive/.../gold_set_verified.csv` yields exactly:
  `Positive: 452, Negative: 76, Neutral: 72`. Total = **`600`**.
- In contrast, the active primary ground-truth set `blind_annotation_300_annotator1.csv` contains only **300 reviews** (`Positive: 258, Negative: 23, Neutral: 19`).

**Critical Finding:**  
The reported benchmark accuracy (82.00%) and macro-F1 (0.6781) advertised across project summaries, the gold evaluation report, and the comprehensive benchmark table were **empirically generated from the archived 600-sample exploratory dataset**, directly refuting the claim in `archive/.../archived_600_plan/README.md` that the 600-sample dataset was "never executed". Furthermore, evaluating the models against the active 300-sample human ground truth yields an entirely different performance profile (Macro-F1 drops to 0.6089).

---

## 3. Documentation Linkages, Rulebook Violations, and Formatting Defects

### 3.1 Missing and Non-Anonymized File References
Multiple documents link to personal names (`ratul` / `friend`) that do not exist on disk:
1. **`data/README.md:23-24`**:
   - `data/gold_set/blind_annotation_300_ratul.csv` (File does not exist; on disk as `blind_annotation_300_annotator1.csv`)
   - `data/gold_set/blind_annotation_200_friend.csv` (File does not exist; on disk as `blind_annotation_200_annotator2.csv`)
2. **`data/gold_set/comprehensive_benchmark_table.md:42-43`**:
   - Links to `blind_annotation_300_ratul.csv` and `blind_annotation_200_friend.csv`.
3. **`data/gold_set/gold_standard_evaluation_report.md:14,91`**:
   - Links to `blind_annotation_300_ratul.csv` and `blind_annotation_200_friend.csv`.
4. **`archive/scraped_data_2020/gold_set/archived_600_plan/README.md:13-14,24`**:
   - Links to `../blind_annotation_300_ratul.csv` and `../blind_annotation_200_friend.csv`.

### 3.2 Broken Relative Directory Link
In [`data/gold_set/gold_standard_evaluation_report.md:14`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/data/gold_set/gold_standard_evaluation_report.md#L14):
- Links to `[archived_600_plan/](archived_600_plan/README.md)`.
- However, `archived_600_plan/` does not exist inside `data/gold_set/`; it was moved to `archive/scraped_data_2020/gold_set/archived_600_plan/`. The relative link is dead (`404`).

### 3.3 Annotation Rulebook Compliance Defect (`[BLIND_106]`)
In [`data/gold_set/ANNOTATION_RULEBOOK.md:122`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/data/gold_set/ANNOTATION_RULEBOOK.md#L122):
- The rulebook explicitly instructs that complaints regarding data pricing or high package costs must be assigned to **`Offers & Data Packs`**:
  ```text
  "Net speed onek bhalo kintu dam ektu beshi" | 3★ | Negative | Offers & Data Packs
  ```
- **Observed Inspection:**
  - Sample `[BLIND_106]`: `"Good but price is some high"` (Rating: 3★).
  - Annotator 1 assigned: `sentiment_label = Negative`, `category_label = Billing & Airtime Deductions`.
  - Annotator 2 assigned: `sentiment_label = Positive`, `category_label = General Appreciation / Other`.
  - Both annotators failed to follow Rulebook line 122: Annotator 1 erroneously classified price under `Billing & Airtime Deductions`, and Annotator 2 ignored the price complaint entirely.

### 3.4 LaTeX Formatting Errors in Reports
In [`data/README.md:25`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/data/README.md#L25) and [`data/gold_set/gold_standard_evaluation_report.md:139`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/data/gold_set/gold_standard_evaluation_report.md#L139):
- Missing opening `$` in math mode:
  - `data/README.md:25`: `(Cohen's Kappa evaluator: κ = 0.7694$ Substantial Agreement)`
  - `gold_standard_evaluation_report.md:139`: `**κ = 0.5762$** on sentiment, and **95.41% raw agreement** with **κ = 0.7694$**`

---

## 4. Empirical Summary of Discrepancies

| # | Discrepancy Description | Affected Artifacts | Severity | Root Cause |
|---|---|---|---|---|
| 1 | **Archived 600-sample metrics published as active benchmark** | `comprehensive_benchmark_table.md`, `gold_standard_evaluation_report.md`, `archived_600_plan/README.md` | **Critical** | Early evaluation on `archive/.../gold_set_verified.csv` was copied into published reports without re-running on active `g300`. |
| 2 | **Active `g300` performance divergence** | `ml/models/ensemble_voting_classifier.joblib`, `data/gold_set/` | **High** | True active Macro-F1 on `g300` is 0.6089 (vs reported 0.6781), while accuracy is 89.00% (vs reported 82.00%). |
| 3 | **Stale de-anonymized file paths** | `data/README.md`, `comprehensive_benchmark_table.md`, `gold_standard_evaluation_report.md` | **Medium** | CSV files were renamed to `_annotator1` / `_annotator2` on disk, but markdown links retain `_ratul` / `_friend`. |
| 4 | **De-anonymized printouts in agreement evaluator** | `data/gold_set/calculate_agreement.py` | **Low** | Console print statements still hardcode `"Ratul"` and `"Friend"`. |
| 5 | **Broken relative link to archived plan** | `data/gold_set/gold_standard_evaluation_report.md:14` | **Low** | Directory was archived under `archive/scraped_data_2020/` without updating relative markdown link. |
| 6 | **Annotation rulebook violation (`[BLIND_106]`)** | `blind_annotation_300_annotator1.csv`, `blind_annotation_200_annotator2.csv` | **Medium** | Both annotators diverged from `ANNOTATION_RULEBOOK.md:122` on price complaint. |
| 7 | **Malformed LaTeX math syntax** | `data/README.md:25`, `gold_standard_evaluation_report.md:139` | **Low** | Missing opening `$` delimiter before `\kappa`. |
