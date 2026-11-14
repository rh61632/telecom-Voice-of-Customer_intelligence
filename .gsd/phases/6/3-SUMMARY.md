# Phase 6 Plan 3 Summary: Ground Truth Schema, Gold Standard Benchmarks & README Gold Sync

## Executive Overview
Plan 6.3 harmonized the primary ground truth dataset schema, fully anonymized agreement evaluation tooling, retired all historical prototype $g600$ leakage from benchmark reports in favor of active $N=300$ / $N=200$ empirical data, and synchronized repository documentation while strictly preserving human annotations and keeping paper references out of README.md.

## Tasks Completed

| Task | Name | Status | Verified Changes |
| :--- | :--- | :---: | :--- |
| **Task 1** | Align `mygp_classified_reviews.csv` schema and document `BLIND_106` in `ANNOTATION_RULEBOOK.md` | **PASSED** | Inserted `operator="Grameenphone"` at column index 5 across all 1,500 rows with 0 nulls, matching the 9-column schema of `mybl_classified_reviews.csv` and `myrobi_classified_reviews.csv`; added explicit Edge-Case Disambiguation Note in `ANNOTATION_RULEBOOK.md` detailing the tariff vs generic cost boundary (`[BLIND_106]` / `[BLIND_111]`) while documenting verbatim human annotation preservation per ADR-003. |
| **Task 2** | Anonymize `data/gold_set/calculate_agreement.py` and sync `data/README.md` | **PASSED** | Replaced all occurrences of specific individual names with "Annotator 1" and "Annotator 2" across code, comments, docstrings, variable names, and console logs; cleaned candidate file paths to look strictly for `blind_annotation_300_annotator1.csv` and `blind_annotation_200_annotator2.csv`; added per-operator sentiment agreement reporting (GP: 89.55% / 0.6921, BL: 94.03% / 0.4846, Robi: 89.39% / 0.3400); updated `data/README.md` file links and corrected LaTeX math formatting ($\kappa$). |
| **Task 3** | Rebuild gold benchmark reports on active g300/consensus data and sync `README.md` | **PASSED** | Completely cleansed `comprehensive_benchmark_table.md` and `gold_standard_evaluation_report.md` of prototype $g600$ leakage (82.00%, 0.6781, 600-row matrices, retired quotes `VOC_0035`); inserted verified active $N=300$ and consensus ($N=182$ Sentiment, $N=187$ Category) tables, $3\times 3$ confusion matrices, active Rogan-Gladen sensitivity/specificity parameters ($Se=0.5217, Sp=0.9747$), active qualitative case studies (`BLIND_085`, `BLIND_238`, `BLIND_325`), and explained the $N=182$ Sentiment 0-Neutral artifact; updated `README.md` lines 375–384 with verified active gold benchmarks (86.67% / 92.86% Naive Star-Rating, 91.21% LinearSVC) with paper references strictly excluded. |

## Empirical Verification Proofs

1. **Schema Harmonization (`data/processed/mygp_classified_reviews.csv`):**
   - Header: `['user_name', 'rating', 'review_date', 'review_text', 'thumbs_up', 'operator', 'category', 'sentiment', 'english_summary']` (9 columns, operator at index 5).
   - Rows: 1,500 rows, 0 nulls, all `operator == "Grameenphone"`.
   - Exact schema match with `mybl_classified_reviews.csv` and `myrobi_classified_reviews.csv`.

2. **Human Ground Truth Preservation (`ADR-003`):**
   - `data/gold_set/blind_annotation_300_annotator1.csv` and `data/gold_set/blind_annotation_200_annotator2.csv` are 100% untouched (`git status` confirms zero modifications).
   - `BLIND_106` preserved verbatim as `Negative` / `Billing & Airtime Deductions` (Annotator 1) vs `Positive` / `General Appreciation / Other` (Annotator 2).

3. **Inter-Annotator Reliability (`data/gold_set/calculate_agreement.py`):**
   - Zero occurrences of individual personal names in code, docstrings, or outputs.
   - Sentiment ($N=200$): Raw agreement **91.00%**, Cohen's Kappa $\kappa = \mathbf{0.5762}$ (Moderate Agreement).
   - Category ($N=196$): Raw agreement **95.41%**, Cohen's Kappa $\kappa = \mathbf{0.7694}$ (Substantial Agreement).
   - Per-operator breakdown:
     - Grameenphone ($N=67$): agreement **89.55%**, $\kappa = \mathbf{0.6921}$
     - Banglalink ($N=67$): agreement **94.03%**, $\kappa = \mathbf{0.4846}$
     - Robi ($N=66$): agreement **89.39%**, $\kappa = \mathbf{0.3400}$

4. **Gold Standard Benchmark Rebuild ($N=300$ & Consensus):**
   - Sentiment on active $N=300$:
     - `ensemble_voting_classifier.joblib`: **89.00%** Acc / **0.6089** Macro-F1 / **0.8820** Wtd-F1 / **0.5150** $\kappa$
     - `challenger_linearsvc.joblib`: **89.00%** Acc / **0.6330** Macro-F1 / **0.8862** Wtd-F1 / **0.5366** $\kappa$
     - `sentiment_voting_classifier.joblib`: **83.67%** Acc / **0.5625** Macro-F1 / **0.8638** Wtd-F1 / **0.4670** $\kappa$
     - `primary_logistic_regression.joblib`: **82.67%** Acc / **0.5836** Macro-F1 / **0.8577** Wtd-F1 / **0.4624** $\kappa$
     - `bilstm_attention_model.pt`: **79.67%** Acc / **0.5790** Macro-F1 / **0.8409** Wtd-F1
     - `bilstm_sentiment_model.pt`: **78.67%** Acc / **0.5364** Macro-F1 / **0.8297** Wtd-F1
     - Star-Rating Heuristic: **86.67%** Acc / **0.5438** Macro-F1 / **0.8539** Wtd-F1 / **0.4244** $\kappa$
   - Category on active $N=300$:
     - `category_voting_classifier.joblib`: **91.33%** Acc / **0.4919** Macro-F1 / **0.9098** Wtd-F1 / **0.5046** $\kappa$
     - `category_linearsvc.joblib`: **91.00%** Acc / **0.4904** Macro-F1 / **0.9051** Wtd-F1 / **0.4679** $\kappa$
     - `category_logistic_regression.joblib`: **89.33%** Acc / **0.4760** Macro-F1 / **0.8985** Wtd-F1 / **0.4385** $\kappa$
     - `bilstm_category_model.pt`: **91.33%** Acc / **0.5154** Macro-F1 / **0.9132** Wtd-F1
   - Consensus ($N=182$ Sentiment, $N=187$ Category):
     - `ensemble_voting_classifier`: **91.21%** Acc / **0.4589** (3-cls) / **0.6884** (2-cls)
     - `sentiment_voting_classifier`: **87.91%** Acc / **0.4769** (3-cls) / **0.7153** (2-cls)
     - `category_voting_classifier`: **94.12%** Acc / **0.5166**
     - Star-Rating Heuristic: **92.86%** Acc / **0.5282**
   - Active Rogan-Gladen parameters:
     - `ensemble_voting_classifier`: $Se = 0.5217, Sp = 0.9747$
     - `sentiment_voting_classifier`: $Se = 0.4783, Sp = 0.9711$

5. **README.md Synchronization:**
   - Lines 375–384 updated with live active $N=300$ and consensus metrics (Challenger LinearSVC Cat 94.12%, LogReg Cat 92.51%, LinearSVC Sent 91.21%, LogReg Sent 85.71%, Star-Rating 86.67% / 92.86%).
   - Zero paper references in `README.md` (preserved commit `4d5aaad`).
   - Zero unsolicited git commits generated (`ADR-003`).

## Artifacts Produced / Updated

- `data/processed/mygp_classified_reviews.csv`
- `data/gold_set/ANNOTATION_RULEBOOK.md`
- `data/gold_set/calculate_agreement.py`
- `data/README.md`
- `data/gold_set/comprehensive_benchmark_table.md`
- `data/gold_set/gold_standard_evaluation_report.md`
- `README.md`
