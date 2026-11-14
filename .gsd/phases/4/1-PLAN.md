---
phase: 4
plan: 1
wave: 1
depends_on: []
files_modified:
  - .gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md
  - .gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md
  - .gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md
  - .gsd/phases/4/1-SUMMARY.md
autonomous: true
user_setup: []

must_haves:
  truths:
    - "Corpus row counts (N=655,649 vs 661,160), Table 1 deployed percentages, longitudinal NSS eras (Table 5 vs Section 5.1 prose), yearly_intelligence_trends.json 2016 counts, and Rogan-Gladen adjusted NSS are empirically evaluated against live classified datasets"
    - "All 35 modern shocks, Table 6 prominent shocks (all 10 rows and 5 category deltas), 2x2 contingency statistics (Yates chi2, RR, Fisher/Woolf CIs), Priority Matrix functional reviews (88,181 vs 88,184, chi2(3), Cramer's V, ORs, within-domain vs total-corpus prevalence), Case Studies 1 & 2 (app_version), and Table 7/8 decision thresholds are directly calculated from live classified data"
    - "ML/DL model performance on seed N=4,500 (5-fold CV for train_category.py and Colab configs, ComplementNB 0.7418, CPU latency/rps, paired t-tests, full-seed Table 3 confusion matrix, Table 4 linguistic sub-cohorts), model complexity parameters (V and d), active gold N=300 McNemar test, consensus agreement (94.12% / 87.91%), Rogan-Gladen Se/Sp origin, PABAK calculation (0.8650), and uncited 28% ARPU claims are quantitatively verified"
  artifacts:
    - ".gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md"
    - ".gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md"
    - ".gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md"
    - ".gsd/phases/4/1-SUMMARY.md"
  key_links:
    - "Empirical reconciliation links scraped_data_global/classified/all_operators_common_duration_classified.csv directly to paper/eswa_latex/manuscript.tex Tables 1, 5, 6 and Sections 4, 5"
    - "Model cross-validation and gold evaluation link data/processed/all_operators_classified_with_language.csv and data/gold_set/*.csv to paper/eswa_latex/manuscript.tex Tables 2, 3, 4 and Section 4"
---

# Plan 4.1: Comprehensive Quantitative Cross-Reconciliation Against Ground-Truth Datasets

<objective>
Execute comprehensive, read-only Python quantitative calculations directly against live ground-truth CSVs (`all_operators_common_duration_classified.csv`, `all_operators_classified_global.csv`, `all_operators_classified_with_language.csv`, `data/gold_set/*.csv`), JSONs (`yearly_intelligence_trends.json`, `shock_grievance_statistical_evidence.json`), and serialized `.joblib` models. Verify every single numeric claim, table cell, test statistic, and formula in `paper/eswa_latex/manuscript.tex` (Tables 1–8, Sections 4–5 prose, Case Studies 1 & 2, McNemar, `Se/Sp`, PABAK, `88,181` vs `88,184`, and `yearly_intelligence_trends.json` mismatch) and store structured evidence in `.gsd/phases/4/evidence/`.
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- .gsd/REQUIREMENTS.md
- .gsd/DECISIONS.md
- .gsd/phases/4/RESEARCH.md
- paper/eswa_latex/manuscript.tex
- scraped_data_global/classified/all_operators_common_duration_classified.csv
- scraped_data_global/classified/all_operators_classified_global.csv
- scraped_data_global/classified/nss_significant_shocks.csv
- scraped_data_global/classified/yearly_intelligence_trends.json
- scraped_data_global/classified/shock_grievance_statistical_evidence.json
- data/processed/all_operators_classified_with_language.csv
- data/processed/mygp_classified_reviews.csv
- data/processed/mybl_classified_reviews.csv
- data/processed/myrobi_classified_reviews.csv
- data/gold_set/blind_annotation_300_annotator1.csv
- data/gold_set/blind_annotation_200_annotator2.csv
- archive/scraped_data_2020/gold_set/archived_600_plan/gold_set_verified.csv
- scripts/verify_section42_stats.py
</context>

<tasks>

<task type="auto">
  <name>Reconcile corpus counts, Table 1 deployed percentages, longitudinal NSS eras (Table 5 & prose), yearly_intelligence_trends.json mismatch, and Rogan-Gladen adjustments</name>
  <files>
    scraped_data_global/classified/all_operators_common_duration_classified.csv
    scraped_data_global/classified/all_operators_classified_global.csv
    scraped_data_global/classified/common_duration_summary.json
    scraped_data_global/classified/yearly_intelligence_trends.json
    scraped_data_global/classified/global_voc_intelligence_report.json
    ml/reports/global_language_distribution.json
    paper/eswa_latex/manuscript.tex
    .gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md
  </files>
  <action>
    Execute read-only Python quantitative verification against `all_operators_common_duration_classified.csv` (N=655,649) and `all_operators_classified_global.csv` (N=661,160):
    1. Corpus Verification: Verify total row counts, operator split (GP: 320,140 / 48.8%, Robi: 198,378 / 30.3%, BL: 137,131 / 20.9%), null review_id or review_text counts, duplicate review_id rows, exact date boundary `2016-08-01` to `2026-09-30` (3,713 calendar days), and verify that all 122 consecutive calendar months exist with zero gaps.
    2. Table 1 Deployed % Recomputation: Compute empirical 5-class counts and percentages (`App Login & Technical Bugs`, `Network Speed & Connectivity`, `Billing, Recharge & Pricing`, `Offers & Packages`, `General Appreciation & Experience`) on `all_operators_common_duration_classified.csv` overall and per operator. Compare against Table 1 claimed deployed percentages: App 5.0%, Net 2.5%, Bill 1.0%, Off 5.0%, Gen 86.6% (which sum to 100.1%), and check whether `all_operators_classified_global.csv` yields different percentages.
    3. Table 5 Longitudinal Eras vs Section 5.1 Prose: Compute exact monthly, annual (2016–2026), and era NSS scores:
       - Era 1: `2016-08`..`2017-12` (17 calendar months)
       - Era 2: `2018-01`..`2019-12` (24 calendar months) or Table 5 claimed `2018-2020` (36M)
       - Era 3: `2020-01`..`2022-12` (36 calendar months)
       - Era 4: `2023-01`..`2026-09` (45 calendar months) or Table 5 claimed `2023-2026` (38M)
       Empirically demonstrate the month-count arithmetic failure in Table 5 (`24M + 36M + 36M + 38M = 134M` vs actual 122M, double-counting 2020 in both Era 2 and Era 3). Compare computed NSS scores against Table 5 values (`-18.42±4.12`, etc.) AND against Section 5.1 prose (`GP -53.2`, `BL -55.8`, `Robi -57.9`; `GP +40.4`, `BL +38.2`, `Robi +33.9`; `GP +62.3`, `BL +51.8`, `Robi +48.6`; `GP +70.6->+56.8`, `BL +40.1->+81.9`, `Robi -57.9->+78.6`).
    4. `yearly_intelligence_trends.json` & July 2016 Mismatch: Check `yearly_intelligence_trends.json:4,28` where 2016 review counts are recorded as 441 GP and 762 BL (summing to 655,670 including excluded July 2016 rows) instead of common-duration counts, while Section 1 of `global_multi_year_intelligence_report.md` reports 655,649.
    5. Rogan-Gladen Adjusted NSS Simulation: Test whether applying the Rogan-Gladen formula (Eq 5: `p* = (p_hat + Sp - 1) / (Se + Sp - 1)`) with `Se=0.711` and `Sp=0.942` to live data reproduces any of the Table 5 values or if Table 5 values remain irreconcilable.
    6. Global Language Distribution: Compare `ml/reports/global_language_distribution.json` (which covers 2014–2026, N=661,160) against `all_operators_common_duration_classified.csv` (N=655,649), verifying whether line 367 distribution (Eng 77.12%, Banglish 11.27%, Bangla 9.42%, Symbolic 2.19%) holds on the common-duration dataset.
    7. Write all structured findings, comparison tables, and exact Python computation snippets to `.gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md`.

    AVOID: Modifying any CSV, JSON, or Python files outside `.gsd/`. Do NOT re-run active scrapers or classification.
    USE: Read-only Python scripts reading datasets in chunks or with pandas/polars, outputting empirical proof tables into `.gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md`.
  </action>
  <verify>
    python -c "import os; assert os.path.exists('.gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md'), 'Evidence file missing'; print('Task 1 evidence verified')"
  </verify>
  <done>
    `.gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md` exists and contains exact empirical verification of corpus counts, Table 1 deployed percentages, longitudinal NSS eras (Table 5 vs Section 5.1 prose), yearly_intelligence_trends.json mismatch, and Rogan-Gladen adjusted NSS simulation.
  </done>
</task>

<task type="auto">
  <name>Reconcile econometric shocks (35 shocks & Table 6), contingency statistics, Priority Matrix (88,181 vs 88,184), Case Studies 1 & 2, and decision framework</name>
  <files>
    scraped_data_global/classified/all_operators_common_duration_classified.csv
    scraped_data_global/classified/nss_significant_shocks.csv
    scraped_data_global/classified/nss_stability_and_shocks_summary.json
    scraped_data_global/classified/shock_grievance_statistical_evidence.json
    scripts/verify_section42_stats.py
    paper/eswa_latex/manuscript.tex
    .gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md
  </files>
  <action>
    Execute read-only Python verification across shock telemetry, 2x2 contingency statistics, Section 5.3 priority matrix, case studies, and decision thresholds:
    1. 35 Shocks Recomputation & Table 6 Prominent Shocks:
       - Run intra-era modern transition filter (`2020-01` to `2026-09`, 240 transitions) with CLT floor N >= 30 and shock threshold |Delta NSS| >= 10.0 pp on `all_operators_common_duration_classified.csv`. Re-verify exact count: 35 shocks (GP: 6, Robi: 7, BL: 22).
       - Directly compute exact ground-truth monthly Delta NSS and all 5 category deltas (Delta Login, Delta Net, Delta Bill, Delta Offer, Delta Gen) for ALL 10 Table 6 rows (`2020-05` GP, `2020-07` BL, `2021-04` Robi, `2021-09` GP, `2022-03` BL, `2023-06` GP, `2023-11` Robi, `2024-04` BL, `2024-05` BL, `2026-01` BL). Empirically document which rows were non-shocks (< 10 pp) and verify Rows 1, 2, 10 deltas.
       - Reconcile `nss_stability_and_shocks_summary.json` (37 modern shocks including `2019-12 -> 2020-01` transition, and label `"Jul 2016 - Sep 2026"`) vs `nss_significant_shocks.csv` (98 multi-year shocks) vs 35 intra-era modern shocks.
    2. 2x2 Contingency & Statistical Tests:
       - Recompute the 2x2 table comparing App Login leading operational driver during shocks (27/35 = 77.1%) vs non-shocks (91/205 = 44.4%).
       - Calculate Pearson chi2(1) (claimed 12.83, p=0.0003), Yates continuity-corrected chi2(1) (claimed 11.55, p=0.0007), Fisher's Exact test odds ratio and 95% CI (claimed OR=4.23 [1.78, 10.51], p=0.0004), Relative Risk (claimed 1.74), and Woolf 95% logit CI.
       - Recompute non-surge contingency: 14/19 (73.7%) vs 82/189 (43.4%), Pearson chi2(1)=6.38, p=0.0116, OR=3.65.
    3. Section 5.3 Priority Matrix (88,181 vs 88,184):
       - Filter `all_operators_common_duration_classified.csv` for functional grievance categories (App Login, Network Speed, Billing, Offers).
       - Check exact row count: verify if total is 88,181 (`manuscript.tex:488`) or 88,184 (`scripts/verify_section42_stats.py:19`). Break down by operator and category to pinpoint the 3-row difference.
       - Execute the statistical logic of `scripts/verify_section42_stats.py`: compute chi2(3) = 11,027.6, p < 0.0001, Cramer's V = 0.3536, Billing negativity OR 9.49 [8.64, 10.42], Login OR 6.44 vs Offers and 2.57 vs Network.
       - Compute BOTH within-domain prevalence (out of N=88,181) AND total-corpus prevalence (out of N=655,649, as plotted in Figure 3) and operator negativity ranges (Billing 89.8%-92.9%, Login 87.1%-89.3%, Network 71.0%-76.4%, Offers 50.3%-56.6%).
    4. Case Studies 1 & 2 & app_version Telemetry:
       - Case Study 1: Recompute BL monthly NSS, Delta NSS, and category shares for `2024-02` through `2024-06`. Inspect `app_version` column to check whether `v11.8.0` and `v11.9.1` reviews exist and evaluate the claimed -32.8 plunge (+65.2 -> +32.4) vs Table 6 Row 8 (`2024-04`, -11.2).
       - Case Study 2: Recompute BL 2025 vs 2026 annual volume (21,810 vs 10,238), NSS (+53.0 vs +81.9), and monthly transition 2025-12 to 2026-01 (+15.54 vs +6.95 claimed in CS2 prose, additive decomposition into General Appreciation and technical categories).
    5. Decision Framework Verification (Tables 7 & 8):
       - Table 7: Compute empirical `p_base` = fraction of reviews with `predicted_category == 'App Login & Technical Bugs'` AND `predicted_sentiment == 'Negative'` across all 655,649 reviews and per operator. Compare against claimed `p_base = 0.046`. Test exact binomial gate on `MyBL v11.8.0` reviews.
       - Table 8: Count how many of the 240 modern transitions meet Level 1, Level 2, Level 3 (Delta NSS <= -10.0), and Level 4 (Delta V >= 50%, Delta Gen >= 5.0 pp) criteria.
    6. Save complete empirical results to `.gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md`.

    AVOID: Modifying any CSV, JSON, or Python files outside `.gsd/`.
    USE: Read-only Python scripts executing exact mathematical formulas (scipy.stats, statsmodels, or pure Python).
  </action>
  <verify>
    python -c "import os; assert os.path.exists('.gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md'), 'Evidence file missing'; print('Task 2 evidence verified')"
  </verify>
  <done>
    `.gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md` exists and contains empirical verification of 35 shocks, all 10 Table 6 rows, 2x2 contingency statistics, 88,181 vs 88,184 Priority Matrix stats, Case Studies 1 & 2 app_version breakdown, and Table 7/8 decision thresholds.
  </done>
</task>

<task type="auto">
  <name>Reconcile ML/DL model metrics, complexity parameters, gold standard inter-rater reliability, McNemar, Rogan-Gladen Se/Sp, PABAK, and commercial claims</name>
  <files>
    data/processed/all_operators_classified_with_language.csv
    data/processed/mygp_classified_reviews.csv
    data/processed/mybl_classified_reviews.csv
    data/processed/myrobi_classified_reviews.csv
    data/gold_set/blind_annotation_300_annotator1.csv
    data/gold_set/blind_annotation_200_annotator2.csv
    archive/scraped_data_2020/gold_set/archived_600_plan/gold_set_verified.csv
    ml/models/category_voting_classifier.joblib
    ml/models/sentiment_voting_classifier.joblib
    ml/models/ensemble_voting_classifier.joblib
    paper/eswa_latex/manuscript.tex
    .gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md
  </files>
  <action>
    Execute read-only Python evaluation of models, gold sets, and prose claims:
    1. Live 5-fold Stratified Cross-Validation on Seed N=4,500:
       - Load `data/processed/my{gp,bl,robi}_classified_reviews.csv` (or `all_operators_classified_with_language.csv`), ensuring N=4,500.
       - Run 5-fold Stratified CV (`random_state=42`) for the two pipeline configurations: (a) `ml/train_category.py` (`char_wb 3-5`, `LR C=1.0`, `weights=[2,2,1]`) and (b) Colab Cell 7 (`char 3-5 max=25k` + `word 1-2 max=12k`, `LR C=2.5`, `weights=[2.0,2.5,1.0]`) across Dummy, ComplementNB, Balanced Logistic Regression, Calibrated LinearSVC, and Soft-Voting Ensemble.
       - Record Macro-F1 (mean ± std), Weighted-F1, and Accuracy for each model.
       - Compare directly against Table 2 claims: verify whether ComplementNB (`CNB 0.7418±0.018 / 0.8412 / 84.21%±0.95%`) matches either config, and verify Soft-Voting (`0.7845±0.019 / 0.8738 / 87.44%±0.88%`).
       - Compute paired t-tests across the 5 CV folds: Soft-Voting vs CNB (claimed `t(4)=4.82, p=0.008`) and Soft-Voting vs BiLSTM / Dummy.
       - Measure empirical CPU latency: evaluate average inference time per review (ms/review) and throughput (reviews/sec, rps) on single CPU core and compare against Table 2 claims (0.45, 0.82, 0.95, 1.42 ms, >450 rps).
    2. Table 3 Seed Evaluation & Model Complexity Parameters:
       - Evaluate `ml/models/category_voting_classifier.joblib` directly on the full seed N=4,500 to generate the true 5x5 confusion matrix and per-class Precision, Recall, and F1. Compare against Table 3 claimed metrics (checking typos C1 Prec 0.9528 vs 0.9828, C5 Prec 0.9993 vs 1.0000, Macro Prec 0.9717 vs 0.9779).
       - Inspect vocabulary size V (number of features in fitted vectorizers) and non-zero feature density d across seed and sample of 655k reviews for `category_voting_classifier.joblib`, `sentiment_voting_classifier.joblib`, and `ensemble_voting_classifier.joblib`. Compare against claimed `V \approx 50,000` and `d \approx 20-45` (`manuscript.tex:173`).
    3. Table 4 Linguistic Sub-Cohorts Recomputation:
       - Load `data/processed/all_operators_classified_with_language.csv` (N=4,500).
       - Recompute sub-cohort sizes: Bangla (1,091), Banglish (390), English (3,005), and the omitted Symbolic / Emoticons (14 rows, explaining 4,486 vs 4,500).
       - Calculate Category and Sentiment Accuracy and Macro-F1 per language slice for both out-of-fold (`cat_oof`, `sent_oof`) and production model predictions (`cat_prod_pred`, `sent_prod_pred`). Compare against Table 4 reported values.
    4. Gold Standard Consensus Agreement & Inter-Rater Reliability:
       - Match `blind_annotation_300_annotator1.csv` and `blind_annotation_200_annotator2.csv` on sample IDs (handling UTF-8 BOM `'\ufeffsample_id'`).
       - Recompute raw inter-rater agreement on the 200 dual-annotated reviews: Category 95.41% (187/196 valid), Sentiment 91.00% (182/200 valid) vs `manuscript.tex:258` claimed 87.0% and 81.0%.
       - Recompute Cohen's kappa: Category kappa = 0.7694, Sentiment kappa = 0.5762.
       - Recompute PABAK: compute 3-class PABAK `(3 * p_o - 1) / 2` with `p_o = 0.9100` yielding 0.8650 (matching `manuscript.tex:629` claim `PABAK = 0.8650` exactly, demonstrating that PABAK in the paper was computed from the true 91.0% agreement while line 258 claimed 81.0%).
       - Evaluate production models (`category_voting_classifier.joblib`, `sentiment_voting_classifier.joblib`, `ensemble_voting_classifier.joblib`) on the consensus agreement subsets (N=187 for Category, N=182 for Sentiment) to verify claimed consensus agreement: 94.12% (176/187) Category agreement and 87.91% (160/182) Sentiment agreement.
       - Compute McNemar chi2 test on active gold N=300 comparing model sentiment predictions against the star-rating heuristic (1-2* = Neg, 3* = Neu, 4-5* = Pos), testing claimed chi2(1) = 21.64, p < 0.0001.
    5. Negative-Class Sensitivity (Se) and Specificity (Sp) Investigation:
       - Compute empirical Negative-class Sensitivity and Specificity across all sentiment models on active `g300`, consensus `g182`, and archived `g600`.
       - Verify whether `Se = 0.711` and `Sp = 0.942` (`manuscript.tex:627`) originated from archived `g600` (e.g., 54/76 = 0.7105 ≈ 0.711) or elsewhere.
    6. Commercial & Market Share Claims Audit:
       - Audit BTRC subscription and market share arithmetic (GP 87.20M / 45.6%, Robi 59.04M / 30.9%, BL 37.95M / 19.9%, Teletalk 6.90M / 3.6%, total 191.09M).
       - Confirm absence of any data, script, or citation substantiating the commercial claims `28% higher ARPU` (`manuscript.tex:581`) and `3.5x-5.0x SAC ratio` (`manuscript.tex:242`).
    7. Save all empirical evaluations and tables to `.gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md`.

    AVOID: Re-saving or modifying any `.joblib` or CSV files.
    USE: Read-only Python scripts utilizing existing libraries (scikit-learn, joblib, pandas, numpy).
  </action>
  <verify>
    python -c "import os; assert os.path.exists('.gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md'), 'Evidence file missing'; print('Task 3 evidence verified')"
  </verify>
  <done>
    `.gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md` exists and contains live 5-fold CV results (Dummy, CNB, LR, LinearSVC, Soft-Voting), CPU latency, paired t-tests, Table 3 confusion matrix evaluation, Table 4 language sub-cohorts, Gold consensus agreement (94.12% / 87.91%), McNemar chi2, PABAK, Se/Sp empirical origins, and ARPU audit.
  </done>
</task>

</tasks>

<verification>
After all tasks complete, verify:
- [ ] `.gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md` exists and contains empirical verification of corpus counts, Table 1 deployed percentages, longitudinal NSS eras, yearly_intelligence_trends.json mismatch, and Rogan-Gladen adjusted NSS.
- [ ] `.gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md` exists and contains empirical verification of 35 shocks, Table 6 prominent shocks, contingency statistics, Priority Matrix, Case Studies 1 & 2, and decision framework.
- [ ] `.gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md` exists and contains empirical verification of 5-fold CV, Table 2 & 3, Table 4, gold consensus agreement, McNemar, PABAK, Se/Sp, and ARPU claims.
- [ ] `.gsd/phases/4/1-SUMMARY.md` is generated summarizing all Task 1, 2, and 3 reconciliation findings.
</verification>

<success_criteria>
- [ ] All 3 tasks verified passing with exit code 0
- [ ] No project source, data, model, plot, or paper files outside `.gsd/` were modified
- [ ] No git commands (`git add`, `git commit`) were executed
</success_criteria>
