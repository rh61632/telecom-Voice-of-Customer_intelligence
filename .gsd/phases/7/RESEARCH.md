---
phase: 7
researched_at: 2026-11-11
discovery_level: 2
---

# Phase 7 Research

## Objective
Define the exact implementation specifications for `REM-05` (Phase 7: Statistical Ground Truth, Integrity Tooling & Script Hygiene Remediation):
1. Canonical empirical computation & JSON schema for `scripts/compute_statistical_tests.py` -> `scraped_data_global/classified/paper_empirical_ground_truth.json`.
2. Completion and hardening of all 8 audit modules in `scripts/audit_project_integrity.py`.
3. Retirement vs. in-place repair inventory for `scripts/` (plus cross-reference audit across docs/scripts).
4. Line-ending (`CRLF -> LF`) and `$PSScriptRoot` / regex / `.sh`-encoding remediation for all `scripts/*.sh` and `scripts/validate-*.ps1`.

## Discovery Level
**Level 2** — Standard research (inspecting live repo scripts, serialized `.joblib` models, Colab notebook outputs, CSVs, LaTeX targets, and running read-only empirical prototypes).

---

## Key Decisions

### Decision 1: Scope of `scripts/compute_statistical_tests.py` Model Reproducibility
**Question:** How should `scripts/compute_statistical_tests.py` handle classical ML vs. GPU deep learning benchmarks in Table 2 given `transformers` is not installed (`transformers: False`) and `ADR-003` forbids altering weights?
**Options Considered:**
1. *Classical ML live only, omit DL:* Leaves Table 2 incomplete for BanglaBERT/BiLSTM/MiniLM.
2. *Live 5-fold CV & paired $t$-tests for all reproducible classical ML pipelines (`Category` & `Sentiment`, local CLI + Colab-parity production architectures), plus verified extraction/recording of Colab GPU DL fold scores from `dl/telecom_voc_banglabert_finetuning_colab.ipynb` and `dl/reports/results.txt` with explicit provenance tags.*
**Decision:** Option 2. Every classical ML metric, paired $t$-test, McNemar test, active Rogan-Gladen parameter, confusion matrix, $V$/$d$, era NSS, shock decomposition, Priority Matrix stat, Case Study metric, and Table 7/8 threshold is computed live from disk datasets and `.joblib` models; GPU transformer/BiLSTM 5-fold numbers are recorded with exact file provenance (`dl/telecom_voc_banglabert_finetuning_colab.ipynb` cell 6; `dl/reports/results.txt:20-42`; `ml/reports/category_benchmark_summary.csv:1-5`).
**Confidence:** High.

### Decision 2: Non-Overlapping 4-Era `122M` Partition & Prominent Top-10 Shocks Selection
**Question:** Which non-overlapping 122-month era partition (`17M+36M+24M+45M` vs `17M+24M+36M+45M`) and which top-10 shocks list (`|ΔNSS|` rank vs multi-operator curated) should `paper_empirical_ground_truth.json` emit?
**Options Considered:**
1. *Emit only one hardcoded partition/list:* Risks forcing Phase 8 to re-query raw CSVs if ESWA Table 5 adopts the alternate boundary.
2. *Compute and store ALL valid non-overlapping 122-month partitions (`17M+36M+24M+45M`, `17M+24M+36M+45M`, `41M+12M+24M+45M`) and BOTH `all_35_shocks` + `top10_by_abs_delta_nss` + `top10_curated_multi_operator` (`scripts/print_table6_rows.py:4-15`).*
**Decision:** Option 2. Storing all three non-overlapping 122-month partitions (each verified to sum to `122` months and `655,649` reviews) and both top-10 views guarantees Phase 8 has complete verified truth without extra compute. Note that `17M+24M+36M+45M` aligns with `.gsd/DISCREPANCY_REPORT.md:72` and the `2020-01` modern boundary, whereas `17M+36M+24M+45M` aligns with `manuscript.tex:397-400` calendar labels (`2016–2017`, `2018–2020`, `2021–2022`, `2023–2026`).
**Confidence:** High.

### Decision 3: Phase 7 vs. Phase 8/9 Gate Separation in `scripts/audit_project_integrity.py`
**Question:** Should `scripts/audit_project_integrity.py` Module 8 hard-fail in Phase 7 on un-remediated ESWA manuscript defects (e.g., 3 raw `**...**` tokens in `manuscript.tex:468,478`, PDF page counts `37/16`, missing `paper/JBA_Manuscript_Empirical_Calculations.xlsx`), given `.gsd/SPEC.md:30` expects `audit_project_integrity.py` to pass (`rc=0`) in Phase 7?
**Options Considered:**
1. *Hard-fail on Phase 8/9 paper defects immediately:* Causes `audit_project_integrity.py` to exit `1` throughout Phase 7 verification.
2. *Strict enforcement across Modules 1–7 + Module 8 anonymity/structure/PDF-existence in default mode, plus `--strict-paper` flag (and explicit `[WARN - Pending Phase 8/9]` output in default mode) for Phase 8/9 gates.*
**Decision:** Option 2. Modules 1–7 and core Module 8 checks pass strictly (`rc=0`) in Phase 7 without creating a "Green Audit" mirage (warnings are printed visibly), and `--strict-paper` turns Phase 8/9 paper gates into hard assertions for final verification.
**Confidence:** High.

### Decision 4: Retire vs. Repair Boundary in `scripts/` (Respecting Phase 8/9 Ownership)
**Question:** Which scripts in `scripts/` belong in `archive/legacy_scripts/` vs. stay in `scripts/` for repair in Phase 7 or Phases 8–9?
**Decision:** Retire the **28** dead/broken JBA, `.docx`, Word COM page-check, missing-crop, and one-off script-patcher scripts to `archive/legacy_scripts/` (with an `archive/legacy_scripts/README.md` index). Repair `verify_paper_complete.py` and `audit_paper_contradictions.py` in-place in Phase 7. Keep Phase 8/9-owned builders/figure scripts (`reconstruct_master_manuscript.py`, `build_full_eswa_paper.py`, `generate_*.py`, `rebuild_figure3.py`, `build_paper_empirical_excel.py`, `build_paper_html.py`, `verify_html.py`, `check_equations.py`) in `scripts/` (do not prematurely archive `build_full_eswa_paper.py` because `reconstruct_master_manuscript.py:14` imports it; do not prematurely run `build_paper_empirical_excel.py` or edit `README.md` with paper leaks).
**Confidence:** High.

---

## Findings

### Q1. Canonical Design & Calculations for `scripts/compute_statistical_tests.py`

**Output Target:** `scraped_data_global/classified/paper_empirical_ground_truth.json` (deterministic UTF-8 JSON with `metadata`, `table1_taxonomy`, `model_cv_and_ttests`, `gold_and_irr`, `table3_seed_and_complexity`, `table4_linguistic`, `table5_eras_and_annual`, `shocks_and_contingency`, `priority_matrix`, `case_studies`, `decision_framework_tables7_8`).

#### (a) 5-Fold Stratified CV & Paired $t$-Tests (`N = 4,500`, `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`)
Live inspection of `ml/models/*.joblib` confirmed two distinct soft-voting feature pipelines in production:
- **Category & Global Production Sentiment FeatureUnion (`category_voting_classifier.joblib`, `sentiment_voting_classifier.joblib`):** `word_tfidf(ngram_range=(1,2), min_df=2, max_features=12000, sublinear_tf=True)` + `char_tfidf(analyzer='char', ngram_range=(3,5), min_df=2, max_features=25000, sublinear_tf=True)` with `VotingClassifier(voting='soft', weights=[2.0, 2.5, 1.0])` (`lr` `C=2.5` for Category / `C=2.0` for Sentiment; `CalibratedClassifierCV(LinearSVC(C=1.0, class_weight='balanced', max_iter=2000, random_state=42), cv=3)`; `ComplementNB(alpha=0.5, norm=False)`). Also defined in `ml/train_category.py:78-152`.
- **CLI/Demo Sentiment Pipeline (`ensemble_voting_classifier.joblib`, `ml/train_ensemble.py:46-66`):** `TfidfVectorizer(analyzer='char_wb', ngram_range=(2,5), min_df=3, sublinear_tf=True)` with `weights=[2, 2, 1]` (`lr`, `CalibratedClassifierCV(LinearSVC)`, `ComplementNB(norm=True)`), plus `ml/train_sentiment.py:67-100` standalone `LogisticRegression` and `LinearSVC`.

Live 5-fold CV execution across `N = 4,500` (`mygp + mybl + myrobi`) yielded exact reference benchmarks to verify against:
- **Category 5-Fold CV (`ml/train_category.py:155-204` + `ComplementNB`):**
  - `DummyClassifier(most_frequent)`: Macro-F1 `0.1511 ± 0.0001`, Wtd-F1 `0.4584`, Acc `60.69% ± 0.04%`
  - `ComplementNB(alpha=0.5)`: Macro-F1 `0.6934 ± 0.0191`, Wtd-F1 `0.8160`, Acc `81.47% ± 1.37%` (proves `manuscript.tex:278` `0.7418` was overstated)
  - `Balanced LogisticRegression(C=2.5)`: Macro-F1 `0.7845 ± 0.0135`, Wtd-F1 `0.8730`, Acc `87.16% ± 0.86%`
  - `Calibrated LinearSVC(C=1.0, cv=3)`: Macro-F1 `0.7664 ± 0.0160`, Wtd-F1 `0.8654`, Acc `86.91% ± 0.74%`
  - `Soft-Voting Hero Ensemble`: Macro-F1 `0.7794 ± 0.0146`, Wtd-F1 `0.8717`, Acc `87.33% ± 0.81%`, folds `[0.7678, 0.7644, 0.7908, 0.8022, 0.7716]` (matches `ml/reports/category_classification_report.md:11-14`)
  - **Paired two-tailed $t$-tests (`scipy.stats.ttest_rel`, `df=4`):** Hero vs Dummy `t(4) = 85.6743, p < 0.000001`; Hero vs CNB `t(4) = 12.2483, p = 0.000255`; Hero vs LogReg `t(4) = -2.0116, p = 0.114584`; Hero vs LinearSVC `t(4) = 1.8101, p = 0.144539`. Against recorded BanglaBERT Category folds `[0.7417, 0.7410, 0.7851, 0.7742, 0.7700]` (`dl/telecom_voc_banglabert_finetuning_colab.ipynb` cell 6): `t(4) = 3.0707, p = 0.037266` — note caveat that `dl/finetune_banglabert.py:82-86` concatenates `[gp, robi, bl]` whereas `ml/train_category.py:43-47` concatenates `[gp, bl, robi]`, so CV fold indices are not 1:1 row-identical unless sorted identically.
- **Sentiment 5-Fold CV (`ml/train_sentiment.py`, `ml/train_ensemble.py`, Colab `sentiment_voting_classifier`):**
  - `DummyClassifier`: Macro-F1 `0.2542 ± 0.0001`, Wtd-F1 `0.4702`, Acc `61.64% ± 0.04%`
  - `ComplementNB(alpha=0.5, Colab feats)`: Macro-F1 `0.7055 ± 0.0140`, Wtd-F1 `0.8310`, Acc `84.22% ± 1.50%`
  - `Balanced LogReg (char_wb)`: Macro-F1 `0.7779 ± 0.0229`, Wtd-F1 `0.8641`, Acc `85.87% ± 1.80%`
  - `LinearSVC (char_wb)`: Macro-F1 `0.7798 ± 0.0147`, Wtd-F1 `0.8740`, Acc `87.64% ± 0.93%`
  - `CLI Soft-Voting (ensemble_voting_classifier)`: Macro-F1 `0.7820 ± 0.0213`, Wtd-F1 `0.8753`, Acc `87.84% ± 1.13%`, folds `[0.8001, 0.7646, 0.8114, 0.7798, 0.7542]` (`ml/README.md:42-45`)
  - `Global Prod Soft-Voting (sentiment_voting_classifier)`: Macro-F1 `0.7688 ± 0.0186`, Wtd-F1 `0.8690`, Acc `87.44% ± 1.31%`, folds `[0.7674, 0.7547, 0.7990, 0.7774, 0.7457]` (`ml/README.md:54`)
  - **Paired $t$-tests (`df=4`):** CLI Ensemble vs Dummy `t(4) = 49.6859, p = 0.000001`, vs CNB `t(4) = 6.6386, p = 0.002672`; Global Prod Ensemble vs Dummy `t(4) = 55.6810, p = 0.000001`, vs CNB `t(4) = 7.9601, p = 0.001349`.
- **Recorded DL Benchmarks:** Include `dl/reports/results.txt:20-42` (`BiLSTM+Char-CNN`, `Colab Word-only BiLSTM`, `MiniLM`) and `dl/telecom_voc_banglabert_finetuning_colab.ipynb` cell 6 (`BanglaBERT` Sentiment `0.8598 ± 0.0102` / `91.60% ± 0.74%`, Category `0.7624 ± 0.0179` / `85.27% ± 1.14%`), plus benchmark live single-review CPU latency (`ms/review`, `reviews/sec`) on `category_voting_classifier.joblib`, `sentiment_voting_classifier.joblib`, `ensemble_voting_classifier.joblib`.

#### (b) Active Gold `N = 300`, Consensus `N = 182 / 187`, IRR, McNemar & Active Rogan-Gladen
Evaluated strictly against `data/gold_set/blind_annotation_300_annotator1.csv` (`N = 300`) and `data/gold_set/blind_annotation_200_annotator2.csv` (`N = 200`):
- **Inter-Rater Reliability (`data/gold_set/calculate_agreement.py`, `data/gold_set/gold_standard_evaluation_report.md:114-125`):**
  - Sentiment (`N = 200`): `182/200 = 91.00%` raw agreement, $\kappa = 0.5762$, 3-class $\text{PABAK} = (3 \times 0.9100 - 1)/2 = 0.8650$; per-operator GP `89.55%` ($\kappa=0.6921$, $N=67$), BL `94.03%` ($\kappa=0.4846$, $N=67$), Robi `89.39%` ($\kappa=0.3400$, $N=66$).
  - Category (`N = 196` valid pairs): `187/196 = 95.41%` raw agreement, $\kappa = 0.7694$.
- **Active Gold `N = 300`, Consensus & McNemar vs. Star-Rating Heuristic (`1-2★=Negative, 3★=Neutral, 4-5★=Positive`, Star Accuracy `86.67%` on `N=300`, `92.86%` on `N=182`):**
  - `ensemble_voting_classifier.joblib` (CLI/Demo): `N=300` `89.00%` Acc / `0.6089` Macro-F1; Consensus `N=182` `91.21%` (`166/182`); McNemar `b=22, c=15`, uncorrected $\chi^2(1) = 1.3243, p = 0.2498$, continuity-corrected $\chi^2(1) = 0.9730$, exact binomial $p = 0.3240$; Active Rogan-Gladen (Negative vs Non-Negative): `TP=12, FN=11, TN=270, FP=7` $\implies \mathrm{Se} = 0.5217, \mathrm{Sp} = 0.9747$.
  - `sentiment_voting_classifier.joblib` (Global Prod 655k classifier): `N=300` `83.67%` Acc / `0.5625` Macro-F1; Consensus `N=182` `87.91%` (`160/182`); McNemar `b=21, c=30`, uncorrected $\chi^2(1) = 1.5882, p = 0.2076$, continuity-corrected $\chi^2(1) = 1.2549$, exact binomial $p = 0.2624$; Active Rogan-Gladen: `TP=11, FN=12, TN=269, FP=8` $\implies \mathrm{Se} = 0.4783, \mathrm{Sp} = 0.9711$.
  - `challenger_linearsvc.joblib`: `N=300` `89.00%` / `0.6330`, Consensus `91.21%`, McNemar `b=23, c=16, \chi^2=1.2564, p=0.2623`, $\mathrm{Se}=0.5217, \mathrm{Sp}=0.9711$.
  - `primary_logistic_regression.joblib`: `N=300` `82.67%` / `0.5836`, Consensus `85.71%`, McNemar `b=23, c=35, \chi^2=2.4828, p=0.1151`, $\mathrm{Se}=0.4783, \mathrm{Sp}=0.9747$.
  - `category_voting_classifier.joblib`: `N=300` `91.33%` Acc / `0.4919` Macro-F1; Consensus `N=187` `94.12%` (`176/187`).
  - Also flag `g600` retirement explicitly (`Se=0.711, Sp=0.942` proved to be grafted from deprecated `g600` `pred_ensemble` + `pred_bilstm`, `.gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md:164-184`).

#### (c) Table 3 Full-Seed Confusion Matrix, Complexity `V`/`d`, and Table 4 Linguistic Sub-Cohorts
- **Table 3 Full-Seed Fit (`category_voting_classifier.joblib` on `N = 4,500`, `ml/reports/category_classification_report.md:28-57`):**
  - Accuracy `0.9900`, Macro Prec `0.9805`, Macro Rec `0.9965`, Macro-F1 `0.9883`, Weighted Prec/Rec/F1 `0.9903 / 0.9900 / 0.9900`.
  - Exact 5x5 confusion matrix (in `VALID_CATEGORIES` order `General [2731], Offers [788], App Login [400], Network [364], Billing [217]`):
    - `General Appreciation / Other`: `[2687, 15, 8, 19, 2]` (Prec `0.9996`, Rec `0.9839`, F1 `0.9917`, Support `2,731`)
    - `Offers & Data Packs`: `[1, 787, 0, 0, 0]` (Prec `0.9813`, Rec `0.9987`, F1 `0.9899`, Support `788`)
    - `App Login & Technical Bugs`: `[0, 0, 400, 0, 0]` (Prec `0.9804`, Rec `1.0000`, F1 `0.9901`, Support `400`)
    - `Network Speed & 4G Latency`: `[0, 0, 0, 364, 0]` (Prec `0.9504`, Rec `1.0000`, F1 `0.9746`, Support `364`)
    - `Billing & Airtime Deductions`: `[0, 0, 0, 0, 217]` (Prec `0.9909`, Rec `1.0000`, F1 `0.9954`, Support `217`)
- **Complexity Parameters (`V`, `d`) via `pipeline.steps[0][1].transform(X_seed)`:**
  - `category_voting_classifier.joblib` & `sentiment_voting_classifier.joblib`: `V = 29,843` (`word_tfidf = 4,843` + `char_tfidf = 25,000`), `d_mean = 109.72`, `d_median = 59.0`, `d_min = 0`, `d_max = 1,199`.
  - `ensemble_voting_classifier.joblib`: `V = 18,027`, `d_mean = 110.86`, `d_median = 64.0`, `d_min = 0`, `d_max = 971`.
- **Table 4 Linguistic Sub-Cohorts:** Compute from `data/processed/all_operators_classified_with_language.csv` (`N = 4,500`, including `Symbolic / Emoticons` `N = 14`, matching `ml/reports/linguistic_subcohort_benchmark.csv:1-6` `Cat Acc 87.33% / F1 0.7800` vs `cat_oof` `87.78% / 0.7896` — check and output exact `cat_oof` / `sent_oof` metrics from `all_operators_classified_with_language.csv` so Phase 8 aligns cleanly with `linguistic_subcohort_benchmark.csv`), plus record both `N = 661,160` (`ml/reports/global_language_distribution.json:2-87`) and `N = 655,649` common-duration language counts (`ml.language_detector.LanguageClassifier`).

#### (d) Table 1 Deployed %, Non-Overlapping 4-Era `122M` NSS & Annual Trends
- **Table 1 (`scraped_data_global/classified/all_operators_common_duration_classified.csv`, `N = 655,649`):**
  - `General Appreciation / Other`: `567,468` (`86.5506%` -> `86.55%`)
  - `Offers & Data Packs`: `33,077` (`5.0449%` -> `5.04%`)
  - `App Login & Technical Bugs`: `32,701` (`4.9876%` -> `4.99%`)
  - `Network Speed & 4G Latency`: `16,108` (`2.4568%` -> `2.46%`)
  - `Billing & Airtime Deductions`: `6,295` (`0.9601%` -> `0.96%`)
  - Sum of 2-decimal percentages = **`100.00%`** (eliminates `100.1%` defect in `manuscript.tex:141-150`); also include per-operator distributions and `N = 4,500` seed counts (`400, 364, 217, 788, 2731`).
- **Decade Scorecard (`common_duration_summary.json:2-40`):** GP `320,140` (`48.83%`, NSS `+64.85%`, 95% CI `[64.61%, 65.09%]`), Robi `198,378` (`30.26%`, NSS `+65.91%`, 95% CI `[65.61%, 66.21%]`), BL `137,131` (`20.92%`, NSS `+53.04%`, 95% CI `[52.63%, 53.45%]`), Sector `655,649` (`+62.70%`).
- **Non-Overlapping 4-Era `122M` Partitions (0 overlaps, 122 calendar months `2016-08`..`2026-09`, `655,649` reviews):**
  - **Partition A (`17M + 36M + 24M + 45M = 122M`, matches `manuscript.tex:397-400` calendar years):**
    - Era 1 (`2016-08..2017-12`, 17M, `N=4,780`): GP agg `+8.78` (monthly `+11.84±20.58`), Robi agg `-52.54` (`-50.44±18.52`), BL agg `+45.46` (`+46.13±9.65`).
    - Era 2 (`2018-01..2020-12`, 36M, `N=93,348`): GP agg `+42.44` (`+14.33±27.91`), Robi agg `+54.98` (`+14.67±43.31`), BL agg `+32.82` (`+27.50±16.85`).
    - Era 3 (`2021-01..2022-12`, 24M, `N=197,864`): GP agg `+62.69` (`+61.48±5.91`), Robi agg `+66.25` (`+65.49±5.10`), BL agg `+50.64` (`+49.30±9.33`).
    - Era 4 (`2023-01..2026-09`, 45M, `N=359,657`): GP agg `+69.44` (`+66.27±8.01`), Robi agg `+70.64` (`+63.55±16.71`), BL agg `+63.33` (`+53.53±18.48`).
  - **Partition B (`17M + 24M + 36M + 45M = 122M`, matches `.gsd/DISCREPANCY_REPORT.md:72` & `2020-01` modern cutoff):**
    - Era 1 (`2016-08..2017-12`, 17M, `N=4,780`): same as above.
    - Era 2 (`2018-01..2019-12`, 24M, `N=15,877`): GP agg `+12.38` (`+0.98±23.32`), Robi agg `+4.96` (`-9.90±30.75`), BL agg `+19.69` (`+21.99±17.71`).
    - Era 3 (`2020-01..2022-12`, 36M, `N=275,335`): GP agg `+58.57` (`+54.66±13.21`), Robi agg `+65.38` (`+64.92±5.53`), BL agg `+47.27` (`+45.72±9.95`).
    - Era 4 (`2023-01..2026-09`, 45M, `N=359,657`): same as above.
  - **Partition C (`41M + 12M + 24M + 45M = 122M`, matches `paper/telecommunications_policy_latex/manuscript.tex:335-345`):** `2016-08..2019-12` (`N=20,657`), `2020-01..2020-12` (`N=77,471`), `2021-01..2022-12` (`N=197,864`), `2023-01..2026-09` (`N=359,657`).
  - Include annual `2016–2026` NSS & counts (`yearly_intelligence_trends.json`) and Rogan-Gladen negative prevalence $p^*$ under active `sentiment_voting_classifier` (`Se=0.4783, Sp=0.9711`).

#### (e) All 35 Modern Shocks & Verified Top-10 Prominent Shocks
- **All 35 Intra-Era Modern Shocks (`2020-01..2026-09`, 240 transitions = 80/operator):**
  - GP `6` shocks, Robi `7` shocks, BL `22` shocks; `20` positive jumps, `15` negative drops; operational driver tallies: `App Login & Technical Bugs = 27`, `Network Speed & 4G Latency = 4`, `Offers & Data Packs = 4`, `Billing & Airtime Deductions = 0`.
  - Compute for each of the 35 shocks: `operator, prev_month, curr_month, n_prev, n_curr, pct_vol, d_ln_vol, is_surge, nss_prev, nss_curr, delta_nss, d_login, d_network, d_billing, d_offers, d_general, four_domain_diff, leading_op_domain, leading_op_impact, leading_op_share_pct, leading_5class_domain, recovery_months`.
- **Two Verified Top-10 Lists Stored in JSON:**
  1. `top10_by_abs_delta_nss`: Pure magnitude ranking (`#1` BL `2025-09->2025-10` `+52.67`, `#2` BL `2025-12->2026-01` `+48.15`, `#3` BL `2024-06->2024-07` `-44.75`, `#4` BL `2025-11->2025-12` `-42.63`, `#5` BL `2024-04->2024-05` `+32.78`, `#6` GP `2020-03->2020-04` `+31.24`, `#7` BL `2024-10->2024-11` `-22.01`, `#8` Robi `2024-08->2024-09` `+21.33`, `#9` GP `2025-08->2025-09` `-18.54`, `#10` BL `2025-03->2025-04` `+18.50`). Note this is heavily Banglalink-skewed (7 BL, 2 GP, 1 Robi).
  2. `top10_curated_multi_operator` (`scripts/print_table6_rows.py:4-15`): Balanced across all 3 operators (4 GP, 3 Robi, 3 BL) and spanning 3 operational domains (7 App Login including BL `2024-03->2024-04` `-11.18` & `2024-04->2024-05` `+32.78`, 2 Offers, 1 Network Speed `BL 2021-04->2021-05 -16.43`), plus `top_per_operator` (top 4 per operator) so Phase 8 can assemble a balanced Table 6 without phantom rows.

#### (f) Contingency Tests, Priority Matrix `N = 88,181`, Case Studies 1 & 2, and Table 7/8 Thresholds
- **Pooled & Per-Operator 2x2 Contingency (`scripts/point4_prop2_by_operator.py:60-112`, `scripts/audit_point1.py:74-83`):**
  - Pooled (`240` transitions): Shocks `27/35 (77.14%)` vs Non-shocks `91/205 (44.39%)`, Pearson $\chi^2(1) = 12.8317 (p = 0.000341)$, Yates $\chi^2(1) = 11.5547 (p = 0.000676)$, Fisher $\text{OR} = 4.2280 (p = 0.000404)$, Woolf/profile 95% CI, $\text{RR} = 1.7378$.
  - Non-surge (`|pct_vol| < 50%`, `208` transitions): Shocks `14/19 (73.68%)` vs Non-shocks `82/189 (43.39%)`, $\chi^2(1) = 6.38 (p = 0.0116)$, Fisher $\text{OR} = 3.65 (p = 0.0150)$.
  - Per-operator asymmetry: GP `3/6` vs `30/74` (`OR=1.47, p=0.6866`), Robi `4/7` vs `32/73` (`OR=1.71, p=0.6949`), BL `20/22` vs `29/58` (`OR=10.00, p=0.0007`; non-surge `11/12` vs `27/55`, `OR=11.41, p=0.0088`).
  - Prop 1 regression across 35 shocks (`scripts/analyze_surges.py`): `Gen/Other diff` vs `d_ln_vol` ($R^2 = 0.5601$, slope `11.52`, $p = 2.35\times 10^{-7}$), `Delta NSS` vs `d_ln_vol` ($R^2 = 0.5220, r = 0.7231$); RMSSD raw (`GP 6.28, Robi 5.61, BL 13.61`) & non-surge `|pct_vol| < 50%` filtered (`GP 5.14, Robi 4.53, BL 7.56`, BL/Robi ratio `2.43x -> 1.67x`).
- **Priority Matrix (`N = 88,181`, `scripts/verify_section42_stats.py:5-49`):**
  - Omnibus $\chi^2(3) = 11,027.60, p < 0.0001, V = 0.3536$.
  - Domain negativity & OR vs Offers (`54.56%`, `33,077`): Billing `91.93%` (`5,787/6,295`, $\text{OR}=9.49$ `[8.64, 10.42]`), App Login `88.54%` (`28,955/32,701`, $\text{OR}=6.44$ `[6.18, 6.70]`), Network `75.01%` (`12,083/16,108`, $\text{OR}=2.50$ `[2.40, 2.61]`); App Login vs Network $\text{OR}=2.57$ `[2.45, 2.70]`.
  - Per-operator negativity bounds: Billing `[89.77%, 92.89%]`, App Login `[87.10%, 89.28%]`, Network `[74.01%, 76.37%]` (correcting `71.0%` prose claim in `manuscript.tex:492`), Offers `[50.26%, 56.62%]`; plus within-domain vs total-corpus prevalence.
- **Case Studies 1 & 2:**
  - CS1 (`BL Spring 2024`): `2024-03` (`N=1,093, NSS=+42.82`), `2024-04` (`N=1,315, NSS=+31.63, ΔNSS=-11.18, ΔLogin=-8.74`), `2024-05` (`N=2,265, NSS=+64.42, ΔNSS=+32.78, ΔLogin=+13.73, ΔGen=+17.38`), `2024-06` (`N=4,528, NSS=+79.55, ΔNSS=+15.13`); BL `app_version` null rate `51.82%` (`71,068/137,131`); `v11.8.0` `N=158` (`NSS=-7.59`) in Apr 2024 and `N=198` (`NSS=+10.61`) in Mar–Jun 2024 (`N=9,201`); `v11.9.1` `N=905` (`NSS=+71.71`); corpus version bias (`492,224` vs `163,425`, `+10.96 pp`).
  - CS2 (`BL 2025 -> 2026`): Annual `2025` (`N=10,238, NSS=+66.39`) -> `2026` (`N=21,810, NSS=+81.93`, `2.13x`), $\Delta\text{NSS} = +15.54$ = `General +10.33 (66.5%)` + `4-Domain Tech +5.21 (33.5%)` (`Login +2.80, Net +1.07, Offers +0.98, Billing +0.36`); plus monthly transition `2025-12` (`N=689, NSS=+37.01`) -> `2026-01` (`N=4,644, NSS=+85.16`, $\Delta\text{NSS} = +48.15$).
- **Table 7 & 8 Thresholds:**
  - Empirical $p_{\text{base}} = P(\text{App Login \& Negative}) = 28,955 / 655,649 = 0.044162$ (`4.42%` vs claimed `0.046`), per-operator GP `0.03454` (`11,058/320,140`), Robi `0.04008` (`7,951/198,378`), BL `0.07253` (`9,946/137,131`).
  - Table 8 alert counts across 240 modern transitions: Level 1 (`|ΔNSS| < 5.0`) = `147 (61.25%)`; Level 2 (`5.0 <= |ΔNSS| < 10.0`) = `58 (24.17%)`; Level 3 (`ΔNSS <= -10.0`) = `15 (6.25%)` (plus `20` positive shocks `>= +10.0`); Level 4 (`pct_vol >= 50%` & `ΔGen >= 5.0 pp`) = `13 (5.42%)`.

---

### Q2. Exact Audit of `scripts/audit_project_integrity.py` & 8-Module Remediation Plan

**Current State (`scripts/audit_project_integrity.py:1-219`):**
- Docstring (`lines 3-12`) promises 8 modules, but execution skips **Modules 2, 3, and 7** completely (jumping `Module 1` at `line 28` -> `Module 4` at `line 54` -> `Module 5 & 6` at `line 77` -> `Module 8` at `line 172`).
- **Line-by-line defects observed in current code:**
  - `line 34-36`: Loads 6 columns, never checks `isna()` or `duplicated()`, never checks `all_operators_classified_global.csv` (`661,160`) or telemetry JSONs, and `line 36` error string reads `"Expected 655670 rows, got {total_rows}"`.
  - `lines 60-71`: Module 4 uses `atol=0.05` on all NSS checks and tests Banglalink against wrong target `53.05` (`line 65`) instead of `53.04`, masking the `0.01 pp` error; never verifies monthly additive decomposition across all `122` months.
  - `lines 78-167`: Modules 5 & 6 restrict to `ym >= '2020-01'`, compute transitions by row index (`iloc[i] - iloc[i-1]` at `lines 113-114`) without verifying `month_diff == 1`, never enforce $N \ge 30$ CLT volume floor, never compute RMSSD/SSI or surge-filtered RMSSD, never run per-operator Fisher tests or Priority Matrix `N=88,181`.
  - `lines 173-216`: Module 8 inspects only `paper/eswa_latex/manuscript.tex` (`line 173`), omits `Jashore` from prohibited terms (`line 177`: `['Ratul', 'rh61632', 'Leading University', 'github.com']`), checks obsolete label `tab:model_leaderboard` (`line 200`, noting `manuscript.tex:267-268` currently has both `\label{tab:leaderboard}` and `\label{tab:model_leaderboard}`), never checks `manuscript_twocolumn.tex`, `highlights.txt`, `references.bib`, raw `**` markdown tokens, or `pdfinfo` page counts/file sizes (`lines 212-215` only run `os.path.exists`).

**Clean 8-Module Completion Blueprint (keeping `<10s` runtime by checking `paper_empirical_ground_truth.json` + live dataset/gold/model invariants):**
1. **Module 1 (Data Integrity):** Validate `all_operators_common_duration_classified.csv` (`655,649` rows, GP `320,140`, Robi `198,378`, BL `137,131`, `2016-08-01`..`2026-09-30`, `0` duplicate `review_id`, `0` nulls in structural/prediction columns, `review_text` null count `== 51`), `all_operators_classified_global.csv` (`661,160` rows, `0` duplicate/null `review_id`), and `common_duration_summary.json` / `yearly_intelligence_trends.json` (`2016 = 438/126/744`, sum `= 655,649`); fix error string to `655649`.
2. **Module 2 (Gold Set Agreement & Independence):** Validate `blind_annotation_300_annotator1.csv` (`N=300`, 100/op) and `blind_annotation_200_annotator2.csv` (`N=200`), verify zero text/ID overlap against `N=4,500` seed reviews, verify IRR (`91.00%`, $\kappa=0.5762$, $\text{PABAK}=0.8650$ Sentiment; `95.41%`, $\kappa=0.7694$ Category), consensus (`N=182` Sent, `N=187` Cat), and active McNemar + Rogan-Gladen bounds.
3. **Module 3 (Model Deserialization, Schema Parity & Benchmark Consistency):** Verify all 7 core `ml/models/*.joblib` load cleanly, `dl/models/bilstm_vocab.json` loads via `dl.bilstm_artifacts.load_bilstm_vocab` (`2,864` tokens), `dl/models/cat_le.joblib` (alphabetical for BiLSTM) & `banglabert_finetuned_category/config.json` (`CATEGORY_LABEL_MAP`) & `sent_le.joblib` / `banglabert_finetuned_sentiment/config.json` match expected mappings, `paper_empirical_ground_truth.json` exists and matches live `category_voting_classifier` full-seed (`99.00% / 0.9883`, `V=29,843`) + Gold `N=300` predictions, and `ml/reports/linguistic_subcohort_benchmark.csv` sums to `N=4,500`.
4. **Module 4 (NSS Invariants & Additive Decomposition):** Tighten `atol=0.01` with exact targets (`64.85`, `65.91`, `53.04`, `62.70`) and assert exact additive identity across all `122` consecutive monthly intervals (`atol=1e-6`).
5. **Module 5 (Time-Series Continuity, CLT Floor, RMSSD/SSI & Surge Filtering):** Assert `122` gapless sector calendar months (`2016-08`..`2026-09`), enforce `month_diff == 1` via `pd.Period` arithmetic across full window (`345` `N>=30` transitions, `91` shocks) and modern `2020-01..2026-09` (`81` months per op, min `N >= 294 >= 30`, `240` transitions, `35` shocks), verify raw RMSSD (`6.28 / 5.61 / 13.61`), SSI (`93.72 / 94.39 / 86.39`), and surge-filtered RMSSD (`5.14 / 4.53 / 7.56`).
6. **Module 6 (Propositions 1 & 2 Statistical Tests & Priority Matrix):** Verify pooled 2x2 (`27/35` vs `91/205`, $\chi^2=12.83$, $\text{OR}=4.23$), non-surge 2x2 (`14/19` vs `82/189`, $\chi^2=6.38$, $\text{OR}=3.65$), per-operator asymmetry (BL `OR=10.00, p=0.0007`), Prop 1 regression ($R^2 = 0.5601$), and Priority Matrix (`N=88,181`, $\chi^2=11,027.60, V=0.3536$).
7. **Module 7 (Spring 2024 Counterfactual Telemetry & Case Study 2):** Verify BL `2024-03` (`+42.82`), `2024-04` (`+31.63`, `-11.18`), `2024-05` (`+64.42`, `+32.78`), BL `app_version` missingness (`51.82%`), `v11.8.0` (`N=158`, `NSS=-7.59` in Apr 2024; `N=198` Mar–Jun 2024), and BL `2025->2026` annual turnaround (`10,238->21,810`, `+15.54` = `+10.33` Gen + `+5.21` Tech).
8. **Module 8 (Anonymity, Manuscript Completeness, Deliverables & `--strict-paper`):** Check all blinded ESWA artifacts (`manuscript.tex`, `manuscript_twocolumn.tex`, `highlights.txt`, `references.bib`) for all 5 prohibited terms (`Ratul`, `rh61632`, `Leading University`, `Jashore`, `github.com`), check all 8 sections & 8 table/algorithm labels across both `.tex` files, validate non-empty PDFs & extract page counts via `pdfinfo` (`paper/manuscript.pdf`, `paper/manuscript_twocolumn.pdf`, and `paper/eswa_latex/*.pdf`), and emit `[WARN - Pending Phase 8/9]` (or hard-fail under `--strict-paper`) on raw `**` markdown tokens, PDF page budgets, PDF SHA256 sync, or missing `paper/JBA_Manuscript_Empirical_Calculations.xlsx`.

---

### Q3. `scripts/` Inventory: Retire to `archive/legacy_scripts/` vs. Repair In-Place & Cross-References

**Cross-Reference Audit Across Docs & Scripts:**
- `README.md:215,226,239,456-460,579-592` references ONLY `analyze_surges.py`, `audit_point1.py`, `audit_thresholds.py`, `check_version_bias.py`, and `audit_project_integrity.py`. (Zero references to any broken/JBA/docx/crop/patch scripts! Note: `README.md` must retain zero academic paper links per Phase 5/6 verification).
- `TODO.txt` contains zero references to any `scripts/*.py` or `scripts/*.ps1` files (`TODO.txt:1-126`).
- `.agent/workflows/install.md:156` and `.agents/skills/*/SKILL.md:94` reference only `scripts/` generically and `scripts/validate-agents.ps1/.sh`.
- `scripts/test_table_defs.py:3` reads `scripts/fix_table_formatting.py`; `scripts/reconstruct_master_manuscript.py:14` imports from `build_full_eswa_paper`.

**Retire to `archive/legacy_scripts/` (28 Scripts — Dead Targets / Superseded One-Off Helpers):**
1. *Broken JBA `.tex` / `.docx` Read-Only Auditors (3):* `audit_check.py:1` (`paper/journal_manuscript/...tex`), `audit_docx.py:3` (`paper/...JBA_Manuscript.docx`), `find_tables.py:3` (`paper/...JBA_Manuscript.docx`).
2. *Broken JBA `.tex` / `.docx` Mutators (14):* `apply_fixes.py:3`, `apply_jba_revisions.py:10`, `apply_peer_review_fixes.py:3`, `apply_reviewer_fixes_latex.py:4`, `build_jba_full_manuscript.py:28`, `build_jba_submission_docx.py:28`, `convert_latex_to_docx.py:13`, `generate_jba_latex.py:15`, `sync_latex_jba.py:17`, `test_float.py:1`, `test_width.py:1`, `update_fig_caption.py:3`, `build_paper_docx.py:28`, `build_concise_paper_docx.py:25`.
3. *Obsolete Word COM `.ps1` Page Checkers (3):* `check_pages.ps1:3`, `check_last_pages.ps1:3` (hardcode deleted `paper/journal_manuscript/...docx`), and `check_exact_pages.ps1:1` (defaults to deleted `paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx`).
4. *Broken Missing-Crop / Figure 1 Offset Helpers (4):* `check_crop.py:13`, `check_crop_wide.py:9`, `check_other_crops.py:7-15`, `test_figure1_offsets.py:122-150` (write stale `"July 2016"` + intermediate `crop_*_check.png`).
5. *Obsolete One-Off Script Self-Patchers (4):* `update_audit_integrity.py:3-6` (targets deleted blinded JBA file), `patch_audit_integrity.py:3-10`, `update_audit_completeness.py:3`, `patch_generate_global_viz.py:3`.
*(Note: Keep the 9 Phase-8/9 ESWA LaTeX/table/patch files or retire one-off ESWA patchers [`add_bib_entries.py`, `add_fontenc.py`, `apply_eswa_enhancements.py`, `apply_paper_reconciliations.py`, `fix_manuscript_latex.py`, `insert_linguistic_section.py`, `patch_base_tex.py`, `fix_table_formatting.py`, `test_table_defs.py`] only after confirming Phase 8 replaces `reconstruct_master_manuscript.py` + `build_full_eswa_paper.py`.)*

**Repair In-Place in Phase 7 (`REM-05`):**
- `scripts/audit_project_integrity.py` (all 8 modules, strict tolerances, `--strict-paper`).
- `scripts/verify_paper_complete.py:19,23,25,43` (fix hardcoded `"3,716 days"` -> `"3,713 days"`, `"20,678"` -> `"20,657"`, `"88,184"` -> `"88,181"`, validate against `paper_empirical_ground_truth.json`).
- `scripts/audit_paper_contradictions.py:23` (fix hardcoded `"88,184"` -> `"88,181"`, cross-check against `paper_empirical_ground_truth.json`).
- `scripts/validate-{skills,workflows,agents,templates,encoding}.ps1` and `scripts/*.sh` (see Q4).

**Keep Untouched / Defer to Phase 8–9 Ownership:**
- *Active Econometric / ML / DL Utilities (working `rc=0`):* `analyze_surges.py`, `audit_point1.py`, `audit_thresholds.py`, `check_banglabert_gold.py`, `check_full_window_shocks.py`, `check_shocks_threshold.py`, `check_version_bias.py`, `compute_empirical_todos.py`, `compute_global_language_distribution.py`, `compute_guideline_analyses.py`, `evaluate_linguistic_subcohorts.py`, `extract_shock_grievances.py`, `find_all_colors.py`, `point4_prop2_by_operator.py`, `print_table6_rows.py`, `reconcile_empirical_numbers.py`, `run_p4.py`, `tally_35_shocks.py`, `test_fig.py`, `test_milestone_space.py`, `upload_to_huggingface.py`, `verify_section42_stats.py`, plus `search_repo.{ps1,sh}`, `setup_search.{ps1,sh}`.
- *Phase 8 (`REM-06`, `REM-07`):* `generate_eswa_architecture_diagram.py`, `generate_paper_figures.py`, `generate_two_panel_figure.py`, `rebuild_figure3.py`, `reconstruct_master_manuscript.py`, `build_full_eswa_paper.py`.
- *Phase 9 (`REM-08`):* `build_paper_empirical_excel.py` (contains `g600` `82.0 / 0.6781` at `line 472` and reads global CSVs at `lines 71-80`), `build_paper_html.py`, `verify_html.py`, `check_equations.py` (`paper/index.html` only at `line 4`).

---

### Q4. Exact Edits for All 8 `scripts/*.sh` and `scripts/validate-*.ps1`

**1. All 8 `scripts/*.sh` Have 100% Windows CRLF (`\r\n`, 0 LF-only lines):**
Verified byte-level inspection:
- `scripts/search_repo.sh` (`58` CRLF), `scripts/setup_search.sh` (`103` CRLF), `scripts/validate-agents.sh` (`115` CRLF), `scripts/validate-all.sh` (`56` CRLF), `scripts/validate-encoding.sh` (`56` CRLF), `scripts/validate-skills.sh` (`65` CRLF), `scripts/validate-templates.sh` (`58` CRLF), `scripts/validate-workflows.sh` (`58` CRLF).
- **Required Edits:**
  - Convert all `\r\n` -> `\n` across all 8 `.sh` files (UTF-8 without BOM, `#!/bin/bash` at byte 0).
  - Also anchor the 4 bash child validators (`validate-workflows.sh:14`, `validate-skills.sh:13`, `validate-agents.sh:13,18,85`, `validate-templates.sh:14`) using `script_dir="$(cd "$(dirname "$0")" && pwd)"` and `repo_root="$(dirname "$script_dir")"`, anchor frontmatter `name:`/`description:` in `validate-skills.sh` & `validate-workflows.sh` inside the YAML block, and update `validate-encoding.sh` to check `*.sh` for `\r` bytes + BOM!

**2. Exact Edits to `scripts/validate-*.ps1` (preserving UTF-8 BOM on files with Unicode chars!):**
- `scripts/validate-workflows.ps1`:
  - Replace `line 13` (`Get-ChildItem ".agent/workflows/*.md"`) with `$repoRoot = Split-Path -Parent $PSScriptRoot`, `$workflowsDir = Join-Path $repoRoot ".agent/workflows"`, `Test-Path $workflowsDir` guard (`exit 1` if missing), and `Get-ChildItem $workflowsDir -Filter "*.md" -File`.
  - Replace `lines 21, 28` unanchored regexes (`"^---"`, `"description:"`) with anchored YAML frontmatter extraction (`if ($content -match "\A---\r?\n([\s\S]*?)\r?\n---")`) checking `$Matches[1] -match "(?m)^description:\s*\S+"`. Verified passing on all 27 `.agent/workflows/*.md` files.
- `scripts/validate-skills.ps1`:
  - Replace `line 13` (`Get-ChildItem ".agents/skills" -Directory`) with `$repoRoot = Split-Path -Parent $PSScriptRoot`, `$skillsDir = Join-Path $repoRoot ".agents/skills"`, `Test-Path $skillsDir` guard (`exit 1` if missing), and `Get-ChildItem $skillsDir -Directory`.
  - Replace `lines 30, 37, 44` unanchored checks (`"^---"`, `"name:"`, `"description:"`) with anchored frontmatter extraction (`\A---\r?\n([\s\S]*?)\r?\n---`) checking `(?m)^name:\s*\S+` and `(?m)^description:\s*\S+` inside `$Matches[1]`. Verified passing on all 12 `.agents/skills/*/SKILL.md` files.
- `scripts/validate-agents.ps1`:
  - Anchor `lines 12, 17` to `$repoRoot = Split-Path -Parent $PSScriptRoot` (`$agentsDir = Join-Path $repoRoot ".agents/agents"`), AND anchor `line 93` (`$skillPath = Join-Path (Join-Path $repoRoot ".agents") (Join-Path $ref.Groups[1].Value "SKILL.md")`)!
  - Anchor frontmatter parsing (`\A---\r?\n([\s\S]*?)\r?\n---`) before extracting `name`, `description`, `subagent`, `tools`, and `skills` references so body text (e.g., template examples) is never confused with YAML frontmatter.
  - **Critical Compatibility Finding (`lines 61-67`):** Live `.agents/agents/*.md` files (`gsd-{debugger,executor,planner,researcher,verifier}.md`) actually declare `view_file`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`, `list_dir`, `find_by_name`, `grep_search`, `read_url_content`, `search_web`, `run_command`, `send_message`. Keep those in `$knownTools` AND append native Antigravity tool names (`read_file`, `write_file`, `edit_file`, `manage_task`) rather than deleting the existing registry entries!
- `scripts/validate-templates.ps1`:
  - Replace `line 13` (`Get-ChildItem ".gsd/templates/*.md"`) with `$repoRoot = Split-Path -Parent $PSScriptRoot`, `$templatesDir = Join-Path $repoRoot ".gsd/templates"`, `Test-Path $templatesDir` guard (`exit 1` if missing), and `Get-ChildItem $templatesDir -Filter "*.md" -File`.
- `scripts/validate-encoding.ps1`:
  - Keep `*.ps1` UTF-8 BOM + `[System.Management.Automation.Language.Parser]::ParseFile(...)` checks (`lines 16-53`).
  - Add `*.sh` scan (`Get-ChildItem $PSScriptRoot -Filter "*.sh" -File | Sort-Object Name`): increment `$ScriptsChecked`, assert NO `\r` (`0x0D`) byte in `$bytes` (CRLF check), assert NO UTF-8 BOM (`$hasBom` must be `$false` so `#!/bin/bash` works at byte 0), and verify `#!/` shebang header!
- `scripts/validate-all.ps1`:
  - Already resolves child scripts via `$PSScriptRoot` (`line 14`) and guards missing child scripts (`lines 19-23`). Once the 5 child `.ps1` validators are anchored via `$PSScriptRoot`, running `powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1` from ANY working directory (repo root, `scripts/`, or `$env:TEMP`) will validate all 27 workflows, 12 skills, 5 subagents, 24 templates, and all `.ps1`/`.sh` scripts cleanly.

---

## Patterns to Follow
- **Single-Source Ground Truth JSON:** Emit all statistical/econometric ground truth once from `scripts/compute_statistical_tests.py` into `scraped_data_global/classified/paper_empirical_ground_truth.json`, and let `audit_project_integrity.py`, `verify_paper_complete.py`, `audit_paper_contradictions.py`, Phase 8 LaTeX generators, and Phase 9 Excel/HTML builders consume it.
- **Period-Safe Time-Series Differencing:** Always sort by `pd.Period(..., 'M')` and verify `(curr_period - prev_period).n == 1` plus `N >= 30` before computing $\Delta\text{NSS}$ or RMSSD.
- **Explicit `$PSScriptRoot` Anchoring & UTF-8 BOM Preservation:** In PowerShell 5.1, every validator script with Unicode symbols (`▶`, `✅`, `❌`, `━`, `╔`) MUST retain a UTF-8 BOM on write (`System.Text.UTF8Encoding($true)`), while `.sh` scripts MUST be UTF-8 without BOM and pure LF (`\n`).

## Anti-Patterns to Avoid
- **Never remove `view_file`/`write_to_file`/etc. from `validate-agents.ps1` `$knownTools`** while `.agents/agents/*.md` actively declare them — append native aliases instead.
- **Never test `df.isna().sum().sum() == 0` blindly on `all_operators_common_duration_classified.csv`** because `51` rows legitimately have null `review_text` (`0` nulls exist in `review_id`, `operator`, `review_date`, `predicted_sentiment`, `predicted_category`, `ym`).
- **Never assume `banglabert_finetuned_category/config.json` shares `cat_le.joblib` index order** — `cat_le.joblib` is alphabetical (for BiLSTM), whereas `config.json` follows `CATEGORY_LABEL_MAP` in `dl/finetune_banglabert.py:60-66`.
- **Never run `git commit` or overwrite `.safetensors`/`.pt`/`blind_annotation_*.csv`** (`ADR-003`), and never inject paper references into `README.md`.

---

## Dependencies Identified
| Package / Tool | Version / Availability | Purpose |
|---|---|---|
| `pandas`, `numpy`, `scipy`, `scikit-learn`, `joblib` | Installed (`Python 3.15.1`) | Live 5-fold CV, paired $t$-tests, McNemar, contingency, RMSSD, JSON generation |
| `openpyxl`, `python-docx`, `torch`, `matplotlib` | Installed | Available for workbook/DL checks (`transformers` is NOT installed) |
| `pdfinfo.exe`, `pdflatex.exe` | Installed (MiKTeX) | PDF page count & metadata verification in Module 8 |

## Risks
- **Runtime of Full 5-Fold CV (`~90–110s`):** `compute_statistical_tests.py` runs 5-fold CV over `FeatureUnion(word 12k + char 25k)` for both Category and Sentiment (`~55s + ~43s`), so `audit_project_integrity.py` must NOT re-run full 5-fold CV every time (`<10s` target in `README.md:579`); instead `audit_project_integrity.py` validates `paper_empirical_ground_truth.json` against quick full-seed/gold inference and model deserialization.
- **Row Concatenation Order Difference:** `ml/train_category.py:44-46` loads `[gp, bl, robi]` while `dl/finetune_banglabert.py:83-85` loads `[gp, robi, bl]`, so paired $t$-tests comparing live Category CV folds to recorded BanglaBERT folds should note fold-order caveat explicitly.

## Recommendations for Planning
1. **Plan 7.1 (`scripts/compute_statistical_tests.py`):** Implement canonical script covering all subparts (a)–(f), run it to generate `scraped_data_global/classified/paper_empirical_ground_truth.json`, and verify JSON completeness & exact invariants.
2. **Plan 7.2 (`scripts/audit_project_integrity.py` + `scripts/` Hygiene):** Complete all 8 modules in `audit_project_integrity.py` (with `--strict-paper` flag), retire the 28 dead/legacy scripts to `archive/legacy_scripts/` with `README.md`, and repair `verify_paper_complete.py` & `audit_paper_contradictions.py` in-place.
3. **Plan 7.3 (`.sh` LF Conversion & `validate-*.ps1` Hardening):** Convert all 8 `scripts/*.sh` CRLF -> LF (and anchor bash child validators), anchor all `validate-*.ps1` via `$PSScriptRoot` + YAML frontmatter regexes + `.sh` LF/no-BOM enforcement in `validate-encoding.ps1`, and empirically verify `validate-all.ps1` passes from both repo root and `scripts/` / `$env:TEMP`.
