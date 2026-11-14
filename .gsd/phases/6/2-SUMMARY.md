# Phase 6 Plan 2 Summary: Classical ML Scripts, Language Detector & ML Reports Remediation

## Executive Overview
Plan 6.2 successfully aligned classical machine learning training pipelines, language detection heuristics, and performance reports with live workspace datasets and deployed production models. All tasks completed autonomously with empirical proof and zero regressions on deployed model weights.

## Tasks Completed

| Task | Name | Status | Verified Changes |
| :--- | :--- | :---: | :--- |
| **Task 1** | Align `ml/train_category.py` with Colab pipeline & fix `ml/train_filtered_experiments.py` and `ml/README.md` | **PASSED** | Updated `train_category.py` feature union (word 12k + char 25k) and classifier hyperparameters to match deployed Colab `category_voting_classifier.joblib`; fixed `std_macro_f1` print bug on line 247; updated `train_filtered_experiments.py` to target active gold standard `data/gold_set/blind_annotation_300_annotator1.csv` and evaluate against `sentiment_label` with `FileNotFoundError` guard; made ablation insights dynamically computed; reconciled `ml/README.md` with live $N=4,500$ 5-fold CV metrics and documented all production joblib models and scripts. |
| **Task 2** | Clarify `ml/language_detector.py` dual-threshold logic & fix `compute_global_language_distribution.py` and report | **PASSED** | Documented Option B two-tier heuristic (0.70 primary CMI dominance + 0.60 secondary typo-tolerance fallback for zero-Banglish Latin text); removed redundant ratio check; preserved exact partition invariants (`3,005` English / `1,091` Bangla / `390` Banglish / `14` Symbolic); updated corpus date coverage to `2014–2026` in `scripts/compute_global_language_distribution.py` and `ml/reports/global_language_distribution.md`. |
| **Task 3** | Fix `scripts/evaluate_linguistic_subcohorts.py`, execute it, and reconcile all ML reports | **PASSED** | Separated Category and Sentiment CV loops so sentiment folds are independently stratified on `y_sent`; added `Symbolic / Emoticons` ($N=14$) to sub-cohorts summing to $N=4,500$; regenerated `data/processed/all_operators_classified_with_language.csv` ($N=4,500$); updated `linguistic_subcohort_report.md` and `linguistic_subcohort_benchmark.csv`; reconciled `category_classification_report.md` ($N=4,500$, `2,731` General support, full-fit `99.00%` Acc / `0.9883` Macro-F1 with live confusion matrix) and `category_benchmark_summary.csv` (`0.7794, 0.8733`); regenerated `short_text_filtering_ablation_study.md` with dynamic ablation and active gold set metrics. |

## Empirical Verification Proofs

1. **Category Model Pipeline & Metrics Alignment:**
   - Word TF-IDF: `ngram_range=(1, 2)`, `min_df=2`, `max_features=12000`, `sublinear_tf=True`
   - Char TF-IDF: `analyzer='char'`, `ngram_range=(3, 5)`, `min_df=2`, `max_features=25000`, `sublinear_tf=True`
   - LR: `C=2.5, class_weight='balanced', max_iter=1000`
   - Calibrated LinearSVC: `cv=3, LinearSVC(C=1.0, class_weight='balanced', max_iter=2000)`
   - ComplementNB: `alpha=0.5, norm=False`
   - Soft-Voting Ensemble: `weights=[2.0, 2.5, 1.0]`, achieving `0.7794 ± 0.0146` Macro-F1 / `87.33% ± 0.81%` Accuracy across 5-fold CV.
   - Line 247 print bug resolved: `± {m['std_macro_f1']:.4f}`.

2. **Short-Text Filtering & Active Gold Standard Evaluation:**
   - Active gold standard: `data/gold_set/blind_annotation_300_annotator1.csv` ($N=300$).
   - Full dataset ($N=4,500$): Cat F1 `0.7892` / Acc `87.78%`, Sent F1 `0.7914` / Acc `88.22%`, Gold F1 `0.5571` / Acc `82.00%`.
   - Filtered ($\ge 3$ words, $N=3,887$ retained 86.4%): Cat F1 `0.7803` / Acc `85.95%`, Sent F1 `0.7822` / Acc `87.37%`, Gold F1 `0.5632` / Acc `67.65%` ($N=68$).
   - Aggressive ($\ge 5$ words, $N=2,286$ retained 50.8%): Cat F1 `0.7498` / Acc `80.05%`, Sent F1 `0.7825` / Acc `84.78%`, Gold F1 `0.7556` / Acc `82.05%` ($N=39$).
   - Operational Category Precision gains: Billing `64.08% ➔ 66.15%`, App Login `75.24% ➔ 76.77%`.

3. **Linguistic Cohort Partition Invariants Preserved:**
   - English: `3,005` (66.78%)
   - Bangla (Native Script): `1,091` (24.24%)
   - Romanized Banglish: `390` (8.67%)
   - Symbolic / Emoticons: `14` (0.31%)
   - Total Seed Corpus: `4,500` (100.0%)
   - Global Corpus ($N=661,160$): English `509,887` (77.12%), Romanized Banglish `74,515` (11.27%), Bangla Script `62,296` (9.42%), Symbolic `14,462` (2.19%), Code-Mixed `16,615` (2.51%).
   - Global coverage date verified: `2014–2026`.

4. **Production Model Weight Integrity:**
   - Zero changes to deployed production models: `category_voting_classifier.joblib`, `sentiment_voting_classifier.joblib`, `ensemble_voting_classifier.joblib`.
   - Zero uncommitted git commits generated (`ADR-003`).

## Artifacts Produced / Updated

- `ml/train_category.py`
- `ml/train_filtered_experiments.py`
- `ml/README.md`
- `ml/language_detector.py`
- `scripts/compute_global_language_distribution.py`
- `ml/reports/global_language_distribution.md`
- `scripts/evaluate_linguistic_subcohorts.py`
- `ml/reports/linguistic_subcohort_report.md`
- `ml/reports/linguistic_subcohort_benchmark.csv`
- `data/processed/all_operators_classified_with_language.csv`
- `ml/reports/category_classification_report.md`
- `ml/reports/category_benchmark_summary.csv`
- `ml/reports/short_text_filtering_ablation_study.md`
