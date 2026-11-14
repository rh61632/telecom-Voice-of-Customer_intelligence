---
phase: 6
plan: 2
wave: 1
depends_on: []
files_modified:
  - ml/train_category.py
  - ml/train_filtered_experiments.py
  - ml/README.md
  - ml/language_detector.py
  - scripts/compute_global_language_distribution.py
  - ml/reports/global_language_distribution.md
  - scripts/evaluate_linguistic_subcohorts.py
  - ml/reports/linguistic_subcohort_report.md
  - ml/reports/linguistic_subcohort_benchmark.csv
  - data/processed/all_operators_classified_with_language.csv
  - ml/reports/category_classification_report.md
  - ml/reports/category_benchmark_summary.csv
  - ml/reports/short_text_filtering_ablation_study.md
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "ml/train_category.py reflects the deployed Colab VotingClassifier feature union and hyperparameters, fixing line 247 std_macro_f1 output"
    - "ml/train_filtered_experiments.py evaluates against data/gold_set/blind_annotation_300_annotator1.csv without silent 0.0 returns and computes dynamic ablation metrics"
    - "ml/language_detector.py implements Option B preserving existing 3,005 / 509,887 partitions with explicit docstrings for 0.70 CMI + 0.60 typo-tolerance fallback"
    - "compute_global_language_distribution.py and global_language_distribution.md state the true 2014–2026 corpus span"
    - "evaluate_linguistic_subcohorts.py includes all 4 cohorts summing to N=4,500 with independent StratifiedKFold sentiment CV splitting"
    - "All classical ML reports and ml/README.md reflect verified live N=4,500 and active gold metrics without deleting or clobbering deployed joblib models"
  artifacts:
    - "data/processed/all_operators_classified_with_language.csv updated with all 4,500 reviews categorized into 4 cohorts"
    - "ml/reports/linguistic_subcohort_report.md reporting N=4,500 across native Bangla, Romanized Banglish, English, and Symbolic cohorts"
    - "ml/reports/short_text_filtering_ablation_study.md reporting dynamic N=4,500 ablation and active g300 evaluation"
    - "ml/reports/category_classification_report.md reporting live N=4,500 5-fold CV metrics with proper std_macro_f1"
---

# Plan 6.2: Classical ML Scripts, Language Detector & ML Reports Remediation

## Objective
Reconcile classical machine learning training pipelines, language detection heuristics, and performance reports with live workspace datasets and deployed models: align `ml/train_category.py` with the deployed Colab hero voting ensemble pipeline and fix the `std_macro_f1` print bug; repair `ml/train_filtered_experiments.py` by connecting it to the active human gold standard (`blind_annotation_300_annotator1.csv`) and replacing stale static text with dynamic metrics; clarify `ml/language_detector.py`'s dual-threshold logic under Option B (retaining the `0.60` zero-Banglish fallback to preserve existing partition invariants); update global language distribution reporting to `2014–2026`; fix `scripts/evaluate_linguistic_subcohorts.py` ($N=4,500$, separate `cv.split(X, y_sent)`, include `Symbolic / Emoticons` $N=14$); and update all downstream reports in `ml/reports/` and `ml/README.md`.

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-04`)
- `.gsd/DECISIONS.md` (`ADR-002`, `ADR-003`)
- `.gsd/phases/6/RESEARCH.md`
- `ml/train_category.py`
- `ml/train_filtered_experiments.py`
- `ml/language_detector.py`
- `scripts/compute_global_language_distribution.py`
- `scripts/evaluate_linguistic_subcohorts.py`

## Tasks

<task type="auto">
  <name>Align ml/train_category.py with Colab pipeline & fix ml/train_filtered_experiments.py and ml/README.md</name>
  <files>
    ml/train_category.py
    ml/train_filtered_experiments.py
    ml/README.md
  </files>
  <action>
    1. Update `ml/train_category.py`:
       - Align `get_feature_extractor()` and `build_models()` with the deployed Colab `category_voting_classifier.joblib` pipeline:
         - Word TF-IDF: `ngram_range=(1, 2)`, `min_df=2`, `max_features=12000`
         - Char TF-IDF: `analyzer='char'`, `ngram_range=(3, 5)`, `min_df=2`, `max_features=25000`
         - Logistic Regression: `C=2.5`, `class_weight='balanced'`, `max_iter=1000`
         - Calibrated LinearSVC: `CalibratedClassifierCV(LinearSVC(C=1.0, class_weight='balanced', max_iter=2000), cv=3)`
         - ComplementNB: `ComplementNB(alpha=0.5, norm=False)`
         - Voting Classifier: `weights=[2.0, 2.5, 1.0]`
       - Fix line 247: change `{m['mean_macro_f1']:.4f} ± {m['mean_macro_f1']:.4f}` to `{m['mean_macro_f1']:.4f} ± {m['std_macro_f1']:.4f}`.
       - Add docstrings explaining parameter alignment with the Colab hero model.
       - CRITICAL: Do NOT overwrite or delete `ml/models/category_voting_classifier.joblib` or any other `.joblib` model file during testing/verification unless strictly identical.
    2. Update `ml/train_filtered_experiments.py`:
       - Fix `GOLD_CSV` (line 19): point to `PROJECT_ROOT / "data" / "gold_set" / "blind_annotation_300_annotator1.csv"`.
       - In `evaluate_on_gold_standard()`: raise `FileNotFoundError` if `GOLD_CSV` does not exist (eliminate the silent `return 0.0, 0.0` at lines 138-139).
       - Evaluate gold accuracy and macro-F1 against `gold_sub["sentiment_label"]` (was `gold_sentiment`).
       - In `export_ablation_report()`: replace static prose strings (`0.6781 -> 0.7436`, `64.82% -> 67.38%`, etc.) with dynamic values computed from `results` and the fitted model on $N=4,500$ seed data.
       - Fix malformed LaTeX string `(≥ 3$ words)` to `($\ge 3$ words)`.
    3. Update `ml/README.md`:
       - Line 23: Update `(~10.9%)` to `(10.84%, 488/4,500)`.
       - Lines 38-40: Update $N=4,499$ metrics to live $N=4,500$ 5-fold CV metrics:
         - Statistical Floor Dummy: `0.2542 ± 0.0001 / 61.64% ± 0.04%`
         - Primary LR: `0.7779 ± 0.0229 / 85.87% ± 1.80%`
         - Challenger LinearSVC: `0.7798 ± 0.0147 / 87.64% ± 0.93%`
       - Add documentation for `ensemble_voting_classifier.joblib` (CLI/Demo hero, `0.7820 ± 0.0213 / 87.84% ± 1.13%`), `sentiment_voting_classifier.joblib` (Colab global corpus, `0.7688 ± 0.0186 / 87.44% ± 1.31%`), and `category_voting_classifier.joblib` (Colab prod hero, `0.7794 ± 0.0146 / 87.33% ± 0.81%`).
       - Document all scripts: `train_sentiment.py`, `train_category.py`, `train_ensemble.py`, and `train_filtered_experiments.py`.

    AVOID: Deleting or mutating `ml/models/*.joblib`.
    AVOID: Hardcoding static stale numbers in `train_filtered_experiments.py`.
    USE: Dynamic computation and live $N=4,500$ values.
  </action>
  <verify>
    python -c "import ast, re; s=open('ml/train_category.py', encoding='utf-8').read(); assert 'std_macro_f1' in s, 'std_macro_f1 missing in train_category.py'; assert 'max_features=12000' in s, 'word max_features 12000 missing'; assert 'max_features=25000' in s, 'char max_features 25000 missing'; s_filt=open('ml/train_filtered_experiments.py', encoding='utf-8').read(); assert 'blind_annotation_300_annotator1.csv' in s_filt, 'gold path missing in train_filtered_experiments.py'; assert 'sentiment_label' in s_filt, 'sentiment_label column missing'; print('✓ ml/train_category.py and ml/train_filtered_experiments.py verified!')"
  </verify>
  <done>
    ml/train_category.py feature extractor and models match Colab voting classifier parameters; line 247 outputs std_macro_f1; ml/train_filtered_experiments.py points to blind_annotation_300_annotator1.csv and computes dynamic metrics; ml/README.md reflects live N=4,500 metrics.
  </done>
</task>

<task type="auto">
  <name>Clarify ml/language_detector.py dual-threshold logic & fix compute_global_language_distribution.py and report</name>
  <files>
    ml/language_detector.py
    scripts/compute_global_language_distribution.py
    ml/reports/global_language_distribution.md
  </files>
  <action>
    1. Update `ml/language_detector.py` (Option B):
       - Keep the secondary `0.60` English word-ratio fallback when `banglish_matches == 0` to preserve existing dataset partitions (`3,005` in seed $N=4,500$; `509,887` in global $N=661,160$).
       - Remove redundant line 147 (`banglish_ratio >= 0.15` inside `banglish_matches > 0`).
       - Simplify the decision tree in `predict()`:
         ```python
         if banglish_matches > 0:
             lang = "Romanized Banglish"
         elif english_ratio >= self.dominance_threshold:
             lang = "English"
         elif english_ratio >= 0.60:
             # Secondary fallback: allows minor spelling typos in short Latin text
             # with 0 Banglish dictionary hits (e.g. 'Veary High price')
             lang = "English"
         else:
             lang = "Romanized Banglish"
         ```
       - Update class and module docstrings to explicitly describe the two-tier heuristic: `0.70` CMI primary threshold (Gambäck & Das 2016) with a secondary `0.60` zero-Banglish typo-tolerance fallback.
    2. Update `scripts/compute_global_language_distribution.py`:
       - Fix line 116 from `(2016–2026)` to `(2014–2026)` matching the actual corpus date coverage in `all_operators_classified_global.csv` and `global_language_distribution.json`.
    3. Update `ml/reports/global_language_distribution.md`:
       - Fix line 3 title from `(2016–2026)` to `(2014–2026)`.
       - Verify that total count is `661,160` and linguistic breakdown matches `global_language_distribution.json` (`English: 509,887 / 77.12%`, `Romanized Banglish: 74,515 / 11.27%`, `Bangla Script: 62,296 / 9.42%`, `Symbolic: 14,462 / 2.19%`, `Code-Mixed: 16,615 / 2.51%`).

    AVOID: Altering the 0.60 threshold in a way that shifts existing 3,005 / 509,887 partition counts.
    USE: Explicit documentation of the two-tier threshold in docstrings.
  </action>
  <verify>
    python -c "s=open('ml/language_detector.py', encoding='utf-8').read(); assert '0.60' in s and 'dominance_threshold' in s; assert '2014–2026' in open('ml/reports/global_language_distribution.md', encoding='utf-8').read(); assert '2014–2026' in open('scripts/compute_global_language_distribution.py', encoding='utf-8').read(); print('✓ Language detector and global distribution verified!')"
  </verify>
  <done>
    ml/language_detector.py cleanly documents 0.70 primary and 0.60 fallback without redundant logic; scripts/compute_global_language_distribution.py and global_language_distribution.md state 2014–2026.
  </done>
</task>

<task type="auto">
  <name>Fix scripts/evaluate_linguistic_subcohorts.py, execute it, and reconcile all ML reports</name>
  <files>
    scripts/evaluate_linguistic_subcohorts.py
    ml/reports/linguistic_subcohort_report.md
    ml/reports/linguistic_subcohort_benchmark.csv
    data/processed/all_operators_classified_with_language.csv
    ml/reports/category_classification_report.md
    ml/reports/category_benchmark_summary.csv
    ml/reports/short_text_filtering_ablation_study.md
  </files>
  <action>
    1. Update `scripts/evaluate_linguistic_subcohorts.py`:
       - Line 156: Update `$N = 4,499$` to `$N = 4,500$`.
       - Separate category and sentiment cross-validation loops (lines 80-91) so sentiment folds are stratified on `y_sent` (`cv.split(X, y_sent)`) rather than `y_cat`.
       - In `cohorts` list (lines 104-109), include `("Symbolic / Emoticons", df[df["language"] == "Symbolic / Emoticons"])` so the sum of the four cohorts equals exactly $4,500$ (`1,091 + 3,005 + 390 + 14 = 4,500`).
       - Run `python scripts/evaluate_linguistic_subcohorts.py` to regenerate:
         - `data/processed/all_operators_classified_with_language.csv` (4,500 rows)
         - `ml/reports/linguistic_subcohort_benchmark.csv`
         - `ml/reports/linguistic_subcohort_report.md`
    2. Reconcile `ml/reports/category_classification_report.md`:
       - Update total sample size from $4,499$ to $4,500$.
       - Update `General Appreciation / Other` class support from $2,730$ to $2,731$.
       - Update 5-Fold Stratified Cross-Validation table with live $N=4,500$ numbers and corrected `std_macro_f1`.
       - Update full-dataset evaluation section to reflect the deployed `category_voting_classifier.joblib` full fit on $N=4,500$ (`Accuracy: 99.00%`, `Macro-F1: 0.9883`, `Weighted-F1: 0.9900`, `Macro-Precision: 0.9805`, `Macro-Recall: 0.9965`, with live confusion matrix).
    3. Reconcile `ml/reports/category_benchmark_summary.csv`:
       - Update row 2 (VotingClassifier) to live $N=4,500$ metrics (`0.7794, 0.8733` matching the deployed Colab VotingClassifier or `0.7892, 0.8778` for local ensemble, consistent with `category_classification_report.md`).
    4. Reconcile `ml/reports/short_text_filtering_ablation_study.md`:
       - Run `python ml/train_filtered_experiments.py` to regenerate `short_text_filtering_ablation_study.md` with live $N=4,500$ ablation figures and real active `g300` evaluation metrics (`0.5571` on full $N=300$, `0.5632` on $\ge 3$ words $N=68$, `0.7556` on $\ge 5$ words $N=39$).
       - Ensure all LaTeX math expressions are properly delimited (`($\ge 3$ words)`).

    AVOID: Reverting or breaking `category_voting_classifier.joblib`.
    USE: Executable python commands to produce empirically verifiable report markdown.
  </action>
  <verify>
    python -c "import pandas as pd; df=pd.read_csv('data/processed/all_operators_classified_with_language.csv'); assert len(df) == 4500, f'Expected 4500, got {len(df)}'; s=open('ml/reports/linguistic_subcohort_report.md', encoding='utf-8').read(); assert '4,500' in s; assert 'Symbolic / Emoticons' in s; print('✓ Subcohort evaluation and reports verified!')"
  </verify>
  <done>
    evaluate_linguistic_subcohorts.py executed with 4 cohorts summing to 4,500 and independent sentiment CV; category_classification_report.md, category_benchmark_summary.csv, and short_text_filtering_ablation_study.md synchronized with live data.
  </done>
</task>

## Must-Haves
After all tasks complete, verify:
- [ ] `ml/train_category.py` implements the Colab voting classifier parameters and prints `std_macro_f1`
- [ ] `ml/train_filtered_experiments.py` points to `data/gold_set/blind_annotation_300_annotator1.csv` and computes dynamic metrics
- [ ] `ml/language_detector.py` documents 0.70 primary and 0.60 fallback thresholds with redundant logic removed
- [ ] `scripts/compute_global_language_distribution.py` and `ml/reports/global_language_distribution.md` state `2014–2026`
- [ ] `scripts/evaluate_linguistic_subcohorts.py` runs with independent sentiment CV and includes Symbolic cohort ($N=14$)
- [ ] `data/processed/all_operators_classified_with_language.csv` contains 4,500 rows across 4 linguistic cohorts
- [ ] All reports in `ml/reports/` and `ml/README.md` reflect verified live $N=4,500$ metrics

## Success Criteria
- [ ] All tasks verified passing with single-command PowerShell checks
- [ ] No `.joblib` models clobbered or degraded
- [ ] No git commits created (`ADR-003`)
