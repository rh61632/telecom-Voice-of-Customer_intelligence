---
phase: 7
plan: 1
wave: 1
depends_on: []
files_modified:
  - scripts/compute_statistical_tests.py
  - scraped_data_global/classified/paper_empirical_ground_truth.json
  - scraped_data_global/classified/paper_empirical_ground_truth.md
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "scripts/compute_statistical_tests.py executes autonomously and generates canonical scraped_data_global/classified/paper_empirical_ground_truth.json and companion .md"
    - "Live 5-fold CV replicates exact reference Category Soft-Voting (folds [0.7678, 0.7644, 0.7908, 0.8022, 0.7716], macro-F1 0.7794 ± 0.0146, Acc 87.33% ± 0.81%) and Sentiment Soft-Voting (CLI macro-F1 0.7820 ± 0.0213, Global Prod macro-F1 0.7688 ± 0.0186, Acc 87.44% ± 1.31%) with paired t-tests"
    - "Active Gold N=300 McNemar test and Rogan-Gladen Se/Sp are computed for both ensemble_voting_classifier (Se=0.5217, Sp=0.9747, N=300 Acc 89.00%, Consensus N=182 Acc 91.21%) and sentiment_voting_classifier (Se=0.4783, Sp=0.9711, N=300 Acc 83.67%, Consensus N=182 Acc 87.91%), explicitly documenting g600 retirement"
    - "Table 3 full-seed confusion matrix (N=4,500, Acc 0.9900, F1 0.9883) and complexity parameters (V=29,843, d_mean=109.72) are computed directly from category_voting_classifier.joblib"
    - "Table 1 deployed percentages sum exactly to 100.00% across N=655,649 (General 86.55%, Offers 5.04%, Login 4.99%, Network 2.46%, Billing 0.96%) and non-overlapping 122-month partitions A (17M+36M+24M+45M), B (17M+24M+36M+45M), and C (41M+12M+24M+45M) all sum to 122 months and 655,649 reviews"
    - "All 35 modern intra-era shocks (GP=6, Robi=7, BL=22) are decomposed, and both top10_by_abs_delta_nss and top10_curated_multi_operator are exported"
    - "Pooled 2x2 contingency (27/35 vs 91/205, chi2=12.83, OR=4.23), non-surge 2x2 (14/19 vs 82/189, chi2=6.38, OR=3.65), per-operator BL asymmetry (OR=10.00, p=0.0007), and Priority Matrix (N=88,181, chi2=11,027.60, V=0.3536, Billing OR=9.49, Login OR=6.44, Net OR=2.50) are computed and stored"
    - "Case Studies 1 & 2 include Spring 2024 monthly transitions, BL app_version missingness disclosure (51.82%), v11.8.0 telemetry (N=158, NSS=-7.59), and BL 2025->2026 turnaround (+15.54 NSS = +10.33 Gen + +5.21 Tech)"
    - "Table 7 & 8 decision framework thresholds record empirical p_base=0.044162, per-operator baselines, and exact 240-transition alert levels (Level 1: 147, Level 2: 58, Level 3: 15, Level 4: 13)"
  artifacts:
    - "scripts/compute_statistical_tests.py defining all statistical, econometric, ML CV, gold standard, time-series, and contingency routines"
    - "scraped_data_global/classified/paper_empirical_ground_truth.json containing structured empirical ground truth for all paper tables, tests, shocks, and case studies"
    - "scraped_data_global/classified/paper_empirical_ground_truth.md summarizing all key numbers for quick inspection"
---

# Plan 7.1: Canonical Statistical & Econometric Ground Truth Script

## Objective
Implement and execute `scripts/compute_statistical_tests.py` to establish the canonical, reproducible empirical ground truth for the entire paper and verification suite. This script computes live 5-fold stratified cross-validation and paired $t$-tests on classical ML models, active Gold $N=300$ McNemar tests and Rogan-Gladen parameters for both classifiers, Table 3 confusion matrix and feature complexity ($V=29,843$, $d=109.72$), Table 4 linguistic subcohorts, Table 1 deployed percentages summing to $100.00\%$, non-overlapping 122-month era NSS partitions ($17\text{M}+36\text{M}+24\text{M}+45\text{M}$, $17\text{M}+24\text{M}+36\text{M}+45\text{M}$, $41\text{M}+12\text{M}+24\text{M}+45\text{M}$), all 35 modern shocks and both top-10 lists, pooled and per-operator $2\times 2$ contingency tables, the Priority Matrix ($N=88,181$, $\chi^2=11,027.60$, $V=0.3536$), Case Studies 1 & 2 telemetry, and Table 7/8 decision thresholds. Outputs `paper_empirical_ground_truth.json` and `paper_empirical_ground_truth.md`.

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-05`)
- `.gsd/DECISIONS.md` (`ADR-002`, `ADR-003`)
- `.gsd/phases/7/RESEARCH.md`
- `ml/train_category.py`
- `ml/train_sentiment.py`
- `ml/train_ensemble.py`
- `data/gold_set/calculate_agreement.py`
- `scripts/point4_prop2_by_operator.py`
- `scripts/verify_section42_stats.py`
- `scripts/analyze_surges.py`

## Tasks

<task type="auto">
  <name>Implement scripts/compute_statistical_tests.py with all statistical, econometric & ML routines</name>
  <files>
    scripts/compute_statistical_tests.py
  </files>
  <action>
    Implement `scripts/compute_statistical_tests.py` using Python 3, `scipy.stats`, `sklearn`, `pandas`, `numpy`, and `joblib`. Structure the script into clean modular functions:

    1. **Metadata & GPU DL Provenance:**
       - Record execution metadata (timestamp, python version, dataset paths).
       - Explicitly document recorded GPU Deep Learning benchmarks from `dl/telecom_voc_banglabert_finetuning_colab.ipynb` (cell 6), `dl/reports/results.txt:20-42`, and `ml/reports/category_benchmark_summary.csv:1-5` (BanglaBERT Sentiment Macro-F1 `0.8598 ± 0.0102`, Acc `91.60% ± 0.74%`; BanglaBERT Category Macro-F1 `0.7624 ± 0.0179`, Acc `85.27% ± 1.14%`; BiLSTM+Char-CNN Sentiment Macro-F1 `0.8229`, Category Macro-F1 `0.7259`; MiniLM Sentiment Macro-F1 `0.7915`, Category Macro-F1 `0.7102`).
       - Note row concatenation ordering difference caveat between `ml/train_category.py` (`[gp, bl, robi]`) and `dl/finetune_banglabert.py` (`[gp, robi, bl]`).
       - Benchmark live single-review CPU inference latency (`ms/review`, `reviews/sec`) for `category_voting_classifier.joblib`, `sentiment_voting_classifier.joblib`, and `ensemble_voting_classifier.joblib`.

    2. **Live 5-Fold Stratified CV & Paired $t$-Tests ($N = 4,500$):**
       - Load `data/processed/{mygp,mybl,myrobi}_classified_reviews.csv` in `[gp, bl, robi]` concatenation order (`N = 4,500`).
       - Run `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` across:
         - Category: `DummyClassifier(strategy='most_frequent')`, `ComplementNB(alpha=0.5, norm=False)`, `LogisticRegression(C=2.5, class_weight='balanced', max_iter=1000, random_state=42)`, `CalibratedClassifierCV(LinearSVC(C=1.0, class_weight='balanced', max_iter=2000, random_state=42), cv=3)`, and Soft-Voting Hero Ensemble (`VotingClassifier(voting='soft', weights=[2.0, 2.5, 1.0])` over `FeatureUnion(word_tfidf max_features=12000 + char_tfidf max_features=25000)`). Target fold scores: `[0.7678, 0.7644, 0.7908, 0.8022, 0.7716]` (Mean Macro-F1 `0.7794 ± 0.0146`, Weighted-F1 `0.8717`, Acc `87.33% ± 0.81%`).
         - Sentiment: Dummy, ComplementNB, Balanced LogReg, Calibrated LinearSVC, CLI Soft-Voting (`ensemble_voting_classifier` architecture, char_wb 2-5, weights `[2, 2, 1]`, folds `[0.8001, 0.7646, 0.8114, 0.7798, 0.7542]`, Macro-F1 `0.7820 ± 0.0213`), and Global Prod Soft-Voting (`sentiment_voting_classifier` architecture, word+char FeatureUnion, folds `[0.7674, 0.7547, 0.7990, 0.7774, 0.7457]`, Macro-F1 `0.7688 ± 0.0186`, Acc `87.44% ± 1.31%`).
       - Compute paired two-tailed $t$-tests (`scipy.stats.ttest_rel`, `df=4`) for all model pairs (Hero vs Dummy, Hero vs CNB, Hero vs LogReg, Hero vs LinearSVC; CLI Ensemble vs Dummy/CNB; Prod Ensemble vs Dummy/CNB).

    3. **Active Gold Standard ($N = 300$ / $N = 200$), Consensus, IRR, McNemar & Rogan-Gladen:**
       - Load `data/gold_set/blind_annotation_300_annotator1.csv` ($N=300$) and `data/gold_set/blind_annotation_200_annotator2.csv` ($N=200$).
       - Compute Inter-Rater Reliability:
         - Sentiment ($N=200$): Raw agreement `91.00%` (182/200), Cohen's $\kappa = 0.5762$, 3-class $\text{PABAK} = 0.8650$, and per-operator breakdowns (GP `89.55%`, BL `94.03%`, Robi `89.39%`).
         - Category ($N=196$ valid pairs): Raw agreement `95.41%` (187/196), Cohen's $\kappa = 0.7694$.
       - Evaluate classifiers on $N=300$ and consensus subsets ($N=182$ Sentiment, $N=187$ Category):
         - Star-rating heuristic benchmark (`1-2★=Negative, 3★=Neutral, 4-5★=Positive`): $N=300$ Acc `86.67%`, $N=182$ Acc `92.86%`.
         - `ensemble_voting_classifier.joblib`: $N=300$ Acc `89.00%` / Macro-F1 `0.6089`; Consensus $N=182$ Acc `91.21%` (166/182); McNemar vs heuristic ($b=22, c=15$): uncorrected $\chi^2(1) = 1.3243 (p = 0.2498)$, continuity-corrected $\chi^2(1) = 0.9730 (p = 0.3239)$, exact binomial $p = 0.3240$; Rogan-Gladen binary negative parameters: $\text{TP}=12, \text{FN}=11, \text{TN}=270, \text{FP}=7 \implies \mathrm{Se} = 0.5217, \mathrm{Sp} = 0.9747$.
         - `sentiment_voting_classifier.joblib`: $N=300$ Acc `83.67%` / Macro-F1 `0.5625`; Consensus $N=182$ Acc `87.91%` (160/182); McNemar vs heuristic ($b=21, c=30$): uncorrected $\chi^2(1) = 1.5882 (p = 0.2076)$, continuity-corrected $\chi^2(1) = 1.2549 (p = 0.2626)$, exact binomial $p = 0.2624$; Rogan-Gladen parameters: $\text{TP}=11, \text{FN}=12, \text{TN}=269, \text{FP}=8 \implies \mathrm{Se} = 0.4783, \mathrm{Sp} = 0.9711$.
         - `category_voting_classifier.joblib`: $N=300$ Acc `91.33%` / Macro-F1 `0.4919`; Consensus $N=187$ Acc `94.12%` (176/187).
         - Challenger Logistic Regression & LinearSVC metrics.
         - Explicit disclosure of deprecated `g600` retirement (`Se=0.711, Sp=0.942` provenance traced to deleted `g600` files).

    4. **Table 3 Full-Seed Confusion Matrix & Complexity ($V, d$) & Table 4 Linguistic Subcohorts:**
       - Evaluate `category_voting_classifier.joblib` on full seed $N=4,500$: Accuracy `0.9900`, Macro Prec `0.9805`, Macro Rec `0.9965`, Macro-F1 `0.9883`.
       - Compute exact $5\times 5$ confusion matrix in standard class order (`General [2731], Offers [788], Login [400], Network [364], Billing [217]`).
       - Compute feature vocabulary size $V$ and active features per review $d$ via vectorizer transforms:
         - `category_voting_classifier.joblib`: $V = 29,843$ (`word_tfidf` 4,843 + `char_tfidf` 25,000), $d_{\text{mean}} = 109.72$, $d_{\text{median}} = 59.0$, $d_{\min} = 0$, $d_{\max} = 1,199$.
         - `ensemble_voting_classifier.joblib`: $V = 18,027$, $d_{\text{mean}} = 110.86$, $d_{\text{median}} = 64.0$.
       - Table 4 Linguistic subcohort metrics: compute from `data/processed/all_operators_classified_with_language.csv` ($N=4,500$, including `Symbolic / Emoticons` $N=14$), outputting both held-out and OOF metrics matching `ml/reports/linguistic_subcohort_benchmark.csv`, plus global language distributions for $N=661,160$ and $N=655,649$.

    5. **Table 1 Deployed %, Non-Overlapping 4-Era 122M NSS & Decade Scorecard:**
       - From `scraped_data_global/classified/all_operators_common_duration_classified.csv` ($N=655,649$):
         - Table 1 proportions: General `567,468 (86.55%)`, Offers `33,077 (5.04%)`, Login `32,701 (4.99%)`, Network `16,108 (2.46%)`, Billing `6,295 (0.96%)`. Sum of 2-decimal rounded percentages $= 100.00\%$. Include per-operator distributions and seed $N=4,500$ counts.
         - Decade Scorecard: GP `320,140 (48.83%, NSS +64.85%, 95% CI [64.61%, 65.09%])`, Robi `198,378 (30.26%, NSS +65.91%, 95% CI [65.61%, 66.21%])`, BL `137,131 (20.92%, NSS +53.04%, 95% CI [52.63%, 53.45%])`, Sector `655,649 (+62.70%)`.
         - Non-overlapping 4-Era Partitions (all summing to 122 months and 655,649 reviews):
           - Partition A (`17M + 36M + 24M + 45M = 122M`): Era 1 (`2016-08..2017-12`, $N=4,780$, GP agg `+8.78`, Robi `-52.54`, BL `+45.46`), Era 2 (`2018-01..2020-12`, $N=93,348$, GP `+42.44`, Robi `+54.98`, BL `+32.82`), Era 3 (`2021-01..2022-12`, $N=197,864$, GP `+62.69`, Robi `+66.25`, BL `+50.64`), Era 4 (`2023-01..2026-09`, $N=359,657$, GP `+69.44`, Robi `+70.64`, BL `+63.33`).
           - Partition B (`17M + 24M + 36M + 45M = 122M`, DISCREPANCY_REPORT:72): Era 1 ($N=4,780$), Era 2 (`2018-01..2019-12`, $N=15,877$, GP `+12.38`, Robi `+4.96`, BL `+19.69`), Era 3 (`2020-01..2022-12`, $N=275,335$, GP `+58.57`, Robi `+65.38`, BL `+47.27`), Era 4 ($N=359,657$).
           - Partition C (`41M + 12M + 24M + 45M = 122M`, Telecom Policy): Era 1 ($N=20,657$), Era 2 ($N=77,471$), Era 3 ($N=197,864$), Era 4 ($N=359,657$).
         - Annual 2016-2026 NSS, review counts, and Rogan-Gladen adjusted negative prevalence $p^* = (p_{\text{obs}} + \mathrm{Sp} - 1) / (\mathrm{Se} + \mathrm{Sp} - 1)$ under `sentiment_voting_classifier` ($\mathrm{Se}=0.4783, \mathrm{Sp}=0.9711$).

    6. **All 35 Modern Shocks, Prominent Top-10 Lists, Contingency Tests & Priority Matrix:**
       - Modern era transitions (`2020-01` to `2026-09`, 240 transitions = 80/operator):
         - Verify 35 shocks ($|\Delta\text{NSS}| \ge 10.0$): GP 6, Robi 7, BL 22; 20 positive, 15 negative; leading operational driver counts: Login 27, Network 4, Offers 4, Billing 0.
         - Compute full transition records for all 35 shocks (operator, prev/curr month, volumes, $d_{\ln(\text{vol})}$, $\Delta\text{NSS}$, 5-class diffs, leading domain, recovery months).
         - Output two verified top-10 lists: `top10_by_abs_delta_nss` (magnitude-ranked, dominated by BL) and `top10_curated_multi_operator` (balanced 4 GP, 3 Robi, 3 BL across 3 operational domains, matching `scripts/print_table6_rows.py`), plus top-4-per-operator lists.
       - Contingency & Surge Analysis:
         - Pooled $2\times 2$ (240 transitions): Shocks `27/35 (77.14%)` vs Non-shocks `91/205 (44.39%)`, Pearson $\chi^2(1) = 12.8317 (p = 0.000341)$, Yates $\chi^2(1) = 11.5547 (p = 0.000676)$, Fisher $\text{OR} = 4.2280 (p = 0.000404)$, Woolf 95% CI `[1.79, 9.98]`, $\text{RR} = 1.7378$.
         - Non-surge $2\times 2$ ($|\text{vol\_pct}| < 50\%$, 208 transitions): Shocks `14/19 (73.68%)` vs Non-shocks `82/189 (43.39%)`, $\chi^2(1) = 6.38 (p = 0.0116)$, Fisher $\text{OR} = 3.65 (p = 0.0150)$.
         - Per-operator asymmetry: GP `3/6` vs `30/74` ($\text{OR}=1.47$), Robi `4/7` vs `32/73` ($\text{OR}=1.71$), BL `20/22` vs `29/58` ($\text{OR}=10.00, p=0.0007$; non-surge $\text{OR}=11.41, p=0.0088$).
         - Prop 1 surge regression: `Gen/Other diff` vs $d_{\ln(\text{vol})}$ ($R^2 = 0.5601$, slope `11.52`, $p = 2.35\times 10^{-7}$); RMSSD raw (GP `6.28`, Robi `5.61`, BL `13.61`) and non-surge filtered (GP `5.14`, Robi `4.53`, BL `7.56`).
       - Priority Matrix ($N = 88,181$ in 4 functional domains):
         - Omnibus $\chi^2(3) = 11,027.60, p < 0.0001, V = 0.3536$.
         - Domain negativity & OR vs Offers (`54.56%`, $N=33,077$): Billing `91.93%` ($N=6,295$, $\text{OR}=9.49$ `[8.64, 10.42]`), Login `88.54%` ($N=32,701$, $\text{OR}=6.44$ `[6.18, 6.70]`), Network `75.01%` ($N=16,108$, $\text{OR}=2.50$ `[2.40, 2.61]`); Login vs Network $\text{OR}=2.57$ `[2.45, 2.70]`.
         - Per-operator negativity bounds: Billing `[89.77%, 92.89%]`, Login `[87.10%, 89.28%]`, Network `[74.01%, 76.37%]`, Offers `[50.26%, 56.62%]`.

    7. **Case Studies 1 & 2 Telemetry & Decision Framework Tables 7 & 8:**
       - Case Study 1 (Banglalink Spring 2024):
         - Transitions: `2024-03` ($N=1,093$, NSS `+42.82`), `2024-04` ($N=1,315$, NSS `+31.63`, $\Delta\text{NSS}=-11.18$, $\Delta\text{Login}=-8.74$), `2024-05` ($N=2,265$, NSS `+64.42`, $\Delta\text{NSS}=+32.78$, $\Delta\text{Login}=+13.73$, $\Delta\text{Gen}=+17.38$), `2024-06` ($N=4,528$, NSS `+79.55`, $\Delta\text{NSS}=+15.13$).
         - BL `app_version` missingness rate: `51.82%` (71,068 null of 137,131).
         - Version telemetry: `v11.8.0` in Apr 2024 ($N=158$, NSS `-7.59`), `v11.8.0` Mar-Jun 2024 ($N=198$, NSS `+10.61`), `v11.9.1` ($N=905$, NSS `+71.71`).
         - Corpus version reporting bias: rated reviews with version ($N=492,224$, NSS `+65.43%`) vs without version ($N=163,425$, NSS `+54.47%`, difference `+10.96 pp`).
       - Case Study 2 (Banglalink 2025 -> 2026 Turnaround):
         - Annual: 2025 ($N=10,238$, NSS `+66.39`) to 2026 ($N=21,810$, NSS `+81.93`, 2.13x volume growth), $\Delta\text{NSS} = +15.54$, decomposed into General `+10.33 (66.5%)` + 4-Domain Technical `+5.21 (33.5%)` (Login `+2.80`, Network `+1.07`, Offers `+0.98`, Billing `+0.36`).
         - Monthly transition: `2025-12` ($N=689$, NSS `+37.01`) to `2026-01` ($N=4,644$, NSS `+85.16`, $\Delta\text{NSS} = +48.15$).
       - Table 7 & 8 Decision Framework:
         - Empirical $p_{\text{base}} = P(\text{App Login \& Negative}) = 28,955 / 655,649 = 0.044162$ (`4.42%`), per-operator baselines: GP `0.03454` (11,058/320,140), Robi `0.04008` (7,951/198,378), BL `0.07253` (9,946/137,131).
         - Table 8 alert counts across 240 modern transitions: Level 1 (`|\Delta\text{NSS}| < 5.0`) = 147 (61.25%), Level 2 (`5.0 <= |\Delta\text{NSS}| < 10.0`) = 58 (24.17%), Level 3 (`\Delta\text{NSS} <= -10.0`) = 15 (6.25%), Level 4 (`\text{vol\_pct} >= 50%` & `\Delta\text{Gen} >= 5.0 pp`) = 13 (5.42%).

    8. Output formatting:
       - Save all computed structures to `scraped_data_global/classified/paper_empirical_ground_truth.json` with `indent=2`, UTF-8 encoding, deterministic key sorting.
       - Also emit human-readable companion Markdown report to `scraped_data_global/classified/paper_empirical_ground_truth.md` for fast developer and paper-auditing inspection.

    AVOID: Altering any model `.safetensors` weights or `.joblib` files on disk.
    AVOID: Re-introducing deprecated `g600` metrics as active performance.
    USE: Exact live data from disk CSVs and `.joblib` pipelines with `pd.Period` arithmetic for time-series.
  </action>
  <verify>
    python -c "import ast; ast.parse(open('scripts/compute_statistical_tests.py', encoding='utf-8').read()); print('✓ scripts/compute_statistical_tests.py parses cleanly')"
  </verify>
  <done>
    scripts/compute_statistical_tests.py is fully written, syntactically valid, and defines all required statistical and econometric routines.
  </done>
</task>

<task type="auto">
  <name>Execute scripts/compute_statistical_tests.py and verify ground-truth JSON and companion MD</name>
  <files>
    scraped_data_global/classified/paper_empirical_ground_truth.json
    scraped_data_global/classified/paper_empirical_ground_truth.md
  </files>
  <action>
    1. Run `python scripts/compute_statistical_tests.py` from repository root.
    2. Confirm successful generation of `scraped_data_global/classified/paper_empirical_ground_truth.json` and `scraped_data_global/classified/paper_empirical_ground_truth.md`.
    3. Assert all critical invariant numbers in `paper_empirical_ground_truth.json`:
       - `metadata`: contains timestamp and explicit DL provenance note.
       - `table1_taxonomy`: deployed percentages sum to `100.00%` (General `86.55`, Offers `5.04`, Login `4.99`, Network `2.46`, Billing `0.96`).
       - `model_cv_and_ttests`: Category Hero ensemble fold scores are `[0.7678, 0.7644, 0.7908, 0.8022, 0.7716]`, Mean Macro-F1 `0.7794 ± 0.0146`, Acc `87.33% ± 0.81%`; CLI Sentiment ensemble Macro-F1 `0.7820 ± 0.0213`; Prod Sentiment Macro-F1 `0.7688 ± 0.0186`; paired $t$-tests present for all model pairs.
       - `gold_and_irr`: Active Gold $N=300$ `ensemble_voting_classifier` Acc `89.00%`, Consensus $N=182$ Acc `91.21%`, McNemar continuity-corrected $\chi^2(1) = 0.9730$, active Rogan-Gladen $\mathrm{Se} = 0.5217, \mathrm{Sp} = 0.9747$; `sentiment_voting_classifier` Acc `83.67%`, Consensus $N=182$ Acc `87.91%`, Rogan-Gladen $\mathrm{Se} = 0.4783, \mathrm{Sp} = 0.9711$; IRR raw agreement `91.00%`, $\kappa = 0.5762$, PABAK `0.8650`.
       - `table3_seed_and_complexity`: $N=4,500$ full-seed Category Acc `0.9900`, F1 `0.9883`, $V=29,843$, $d=109.72$.
       - `table5_eras_and_annual`: Partitions A, B, and C each contain exactly 122 months and sum to 655,649 reviews.
       - `shocks_and_contingency`: exactly 35 shocks (GP=6, Robi=7, BL=22, 27 Login-led); pooled $\chi^2 = 12.83, \text{OR} = 4.23$; non-surge $\chi^2 = 6.38, \text{OR} = 3.65$; BL asymmetry $\text{OR} = 10.00$; Prop 1 $R^2 = 0.5601$; both `top10_by_abs_delta_nss` and `top10_curated_multi_operator` contain 10 verified items.
       - `priority_matrix`: $N=88,181$, omnibus $\chi^2 = 11,027.60$, $V = 0.3536$, Billing $\text{OR} = 9.49$, Login $\text{OR} = 6.44$, Network $\text{OR} = 2.50$.
       - `case_studies`: Case Study 1 BL Spring 2024 $\Delta\text{NSS} = -11.18$ (Apr) and $+32.78$ (May), missingness `51.82%`, `v11.8.0` telemetry; Case Study 2 BL annual $\Delta\text{NSS} = +15.54$ ($+10.33$ Gen, $+5.21$ Tech).
       - `decision_framework_tables7_8`: empirical $p_{\text{base}} = 0.044162$, alert level counts: Level 1 `147`, Level 2 `58`, Level 3 `15`, Level 4 `13`.
  </action>
  <verify>
    python -c "import json; d=json.load(open('scraped_data_global/classified/paper_empirical_ground_truth.json', encoding='utf-8')); assert sum(d['table1_taxonomy']['percentages'].values()) == 100.0, 'Table 1 sum != 100'; assert d['table3_seed_and_complexity']['vocabulary_size'] == 29843, 'V != 29843'; assert len(d['shocks_and_contingency']['all_35_shocks']) == 35, 'Shocks != 35'; assert d['priority_matrix']['total_functional_reviews'] == 88181, 'Priority N != 88181'; assert round(d['priority_matrix']['cramers_v'], 4) == 0.3536, 'V != 0.3536'; print('✓ paper_empirical_ground_truth.json verified complete and invariant-compliant!')"
  </verify>
  <done>
    scraped_data_global/classified/paper_empirical_ground_truth.json and companion markdown exist, reflect live calculations from disk datasets, and pass all verification assertions.
  </done>
</task>

## Must-Haves
After all tasks complete, verify:
- [ ] `scripts/compute_statistical_tests.py` runs end-to-end and produces valid UTF-8 JSON and Markdown companion
- [ ] Table 1 deployed percentages sum exactly to 100.00% across $N=655,649$
- [ ] Live 5-fold CV macro-F1, paired $t$-tests, McNemar tests, and Rogan-Gladen parameters match verified values
- [ ] Table 3 confusion matrix ($N=4,500$) and complexity parameters ($V=29,843, d=109.72$) match live models
- [ ] All 35 shocks, pooled/per-operator contingency, Priority Matrix ($N=88,181, \chi^2=11,027.60, V=0.3536$), and Case Studies 1 & 2 are accurately recorded

## Success Criteria
- [ ] All tasks verified passing
- [ ] Must-haves confirmed
- [ ] No regressions in tests
