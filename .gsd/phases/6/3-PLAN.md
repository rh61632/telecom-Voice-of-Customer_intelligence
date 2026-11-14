---
phase: 6
plan: 3
wave: 2
depends_on: ["1", "2"]
files_modified:
  - data/processed/mygp_classified_reviews.csv
  - data/gold_set/ANNOTATION_RULEBOOK.md
  - data/gold_set/calculate_agreement.py
  - data/README.md
  - data/gold_set/comprehensive_benchmark_table.md
  - data/gold_set/gold_standard_evaluation_report.md
  - README.md
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "data/processed/mygp_classified_reviews.csv contains operator='Grameenphone' at column index 5, matching the 9-column schema of mybl and myrobi across all 1,500 rows"
    - "data/gold_set/blind_annotation_*.csv files remain strictly unmodified per ADR-003, with BLIND_106/BLIND_111 edge cases clarified in ANNOTATION_RULEBOOK.md"
    - "calculate_agreement.py is fully anonymized and outputs per-operator inter-annotator reliability metrics"
    - "All g600 prototype leakage (tables, 600-row confusion matrices, quotes) is completely retired from comprehensive_benchmark_table.md and gold_standard_evaluation_report.md"
    - "Benchmark reports and README.md lines 375–384 present verified live active g300 (N=300) and consensus (N=182 Sent, N=187 Cat) metrics and quotes"
  artifacts:
    - "data/processed/mygp_classified_reviews.csv with 9 columns, 1,500 rows, and operator='Grameenphone'"
    - "data/gold_set/calculate_agreement.py anonymized with per-operator agreement reporting"
    - "data/gold_set/comprehensive_benchmark_table.md reporting active g300 and consensus benchmarks"
    - "data/gold_set/gold_standard_evaluation_report.md reporting active g300 confusion matrices, Rogan-Gladen parameters, and active quotes"
    - "README.md lines 375–384 synchronized with active gold standard benchmark metrics"
---

# Plan 6.3: Ground Truth Schema, Gold Standard Benchmarks & README Gold Sync

## Objective
Harmonize the primary ground truth schema, anonymize agreement evaluation tooling, retire all historical prototype `g600` leakage in favor of active `N=300` / `N=200` gold benchmarks, and synchronize repository documentation: add `operator="Grameenphone"` at column index 5 to `data/processed/mygp_classified_reviews.csv` so all three operator datasets share an identical 9-column schema; preserve `blind_annotation_*.csv` annotations strictly verbatim while clarifying `[BLIND_106]` / `[BLIND_111]` taxonomy boundary cases in `ANNOTATION_RULEBOOK.md`; anonymize `data/gold_set/calculate_agreement.py` and add per-operator agreement outputs; replace leaked `g600` tables, matrices, and quotes in `comprehensive_benchmark_table.md` and `gold_standard_evaluation_report.md` with verified active `g300` ($N=300$) and consensus ($N=182$ Sentiment, $N=187$ Category) data; and update `data/README.md` and `README.md` lines 375–384.

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-04`)
- `.gsd/DECISIONS.md` (`ADR-002`, `ADR-003`)
- `.gsd/phases/6/RESEARCH.md`
- `data/processed/mygp_classified_reviews.csv`
- `data/gold_set/ANNOTATION_RULEBOOK.md`
- `data/gold_set/calculate_agreement.py`
- `data/gold_set/comprehensive_benchmark_table.md`
- `data/gold_set/gold_standard_evaluation_report.md`
- `README.md`

## Tasks

<task type="auto">
  <name>Align mygp_classified_reviews.csv schema and document BLIND_106 in ANNOTATION_RULEBOOK.md</name>
  <files>
    data/processed/mygp_classified_reviews.csv
    data/gold_set/ANNOTATION_RULEBOOK.md
  </files>
  <action>
    1. Update `data/processed/mygp_classified_reviews.csv`:
       - Insert column `operator` with value `"Grameenphone"` at column index 5 (between `thumbs_up` and `category`).
       - Ensure the new column header is exactly:
         `user_name,rating,review_date,review_text,thumbs_up,operator,category,sentiment,english_summary`
       - Preserve all 1,500 rows, 0 nulls, and all existing values intact.
       - Confirm the schema matches `mybl_classified_reviews.csv` and `myrobi_classified_reviews.csv` (9 columns).
    2. Update `data/gold_set/ANNOTATION_RULEBOOK.md`:
       - CRITICAL: Do NOT edit `blind_annotation_300_annotator1.csv` or `blind_annotation_200_annotator2.csv` (`ADR-003`).
       - In Section 2 (Operational Category Guidelines) and the Cheat Sheet:
         - Add an explicit **Edge-Case Disambiguation Note (`[BLIND_106]` / `[BLIND_111]`):**
           - Explain that explicit data-pack / tariff pricing complaints (*"MB package dam beshi"*) map to `Offers & Data Packs`.
           - Explain that generic uncontextualized cost complaints (*"Good but price is some high"*, `[BLIND_106]`; *"khali tk besi 🫠"*, `[BLIND_111]`) sit on the boundary between `Billing & Airtime Deductions` and `Offers & Data Packs` (or `General Appreciation / Other` when mixed with general praise).
           - Note that historical blind annotations in `blind_annotation_*.csv` are preserved verbatim per `ADR-003` without post-hoc modification to maintain empirical audit integrity.

    AVOID: Modifying any cell or label in `blind_annotation_300_annotator1.csv` or `blind_annotation_200_annotator2.csv`.
    AVOID: Shifting column orders or introducing nulls in `mygp_classified_reviews.csv`.
    USE: Exact column index 5 insertion for `operator`.
  </action>
  <verify>
    python -c "import pandas as pd; df=pd.read_csv('data/processed/mygp_classified_reviews.csv'); assert len(df)==1500; assert list(df.columns)[5]=='operator'; assert (df['operator']=='Grameenphone').all(); s=open('data/gold_set/ANNOTATION_RULEBOOK.md', encoding='utf-8').read(); assert 'BLIND_106' in s; print('✓ GP schema and ANNOTATION_RULEBOOK verified!')"
  </verify>
  <done>
    mygp_classified_reviews.csv has 9 columns with operator='Grameenphone' at index 5 across 1,500 rows; ANNOTATION_RULEBOOK.md contains the BLIND_106/BLIND_111 boundary note.
  </done>
</task>

<task type="auto">
  <name>Anonymize data/gold_set/calculate_agreement.py and sync data/README.md</name>
  <files>
    data/gold_set/calculate_agreement.py
    data/README.md
  </files>
  <action>
    1. Update `data/gold_set/calculate_agreement.py`:
       - Anonymize the script completely:
         - Replace references to specific individuals in docstrings and comments (e.g. line 3) with `"Annotator 1"` and `"Annotator 2"`.
         - Clean `resolve_files()` candidates: remove filenames with individual names (`ratul`/`friend`), looking strictly for `blind_annotation_300_annotator1.csv` and `blind_annotation_200_annotator2.csv`.
         - Rename internal variables: `ratul_*` and `friend_*` to `ann1_*` and `ann2_*`.
         - Update all console print messages to refer to `"Annotator 1"` and `"Annotator 2"`.
       - Enhance the script to compute and print the per-operator inter-annotator agreement breakdown:
         - Grameenphone ($N=67$): agreement `89.55%`, $\kappa = 0.6921$
         - Banglalink ($N=67$): agreement `94.03%`, $\kappa = 0.4846$
         - Robi ($N=66$): agreement `89.39%`, $\kappa = 0.3400$
       - Keep overall agreement calculations (`Sentiment: 91.00% / 0.5762`, `Category: 95.41% / 0.7694` on valid pairs) functioning identically.
    2. Update `data/README.md`:
       - Lines 23-24: Update file references from `blind_annotation_300_ratul.csv` and `blind_annotation_200_friend.csv` to `blind_annotation_300_annotator1.csv` and `blind_annotation_200_annotator2.csv`.
       - Line 25: Fix broken math formatting by replacing `κ = 0.7694$` with `Sentiment $\kappa = 0.5762$, Category $\kappa = 0.7694$`.
       - Ensure all references to human annotators use `"Annotator 1"` and `"Annotator 2"`.

    AVOID: Altering the underlying agreement calculation math or Cohen's Kappa formula.
    USE: Clean variable names `ann1` and `ann2`.
  </action>
  <verify>
    python -c "s=open('data/gold_set/calculate_agreement.py', encoding='utf-8').read(); assert 'Ratul' not in s and 'Friend' not in s and 'ratul' not in s and 'friend' not in s, 'Non-anonymized name found!'; s_readme=open('data/README.md', encoding='utf-8').read(); assert 'annotator1' in s_readme and 'annotator2' in s_readme; print('✓ calculate_agreement.py and data/README.md verified!')"
  </verify>
  <done>
    calculate_agreement.py is completely anonymized and prints per-operator breakdowns; data/README.md links to annotator1 and annotator2 files with corrected math formatting.
  </done>
</task>

<task type="auto">
  <name>Rebuild gold benchmark reports on active g300/consensus data and sync README.md</name>
  <files>
    data/gold_set/comprehensive_benchmark_table.md
    data/gold_set/gold_standard_evaluation_report.md
    README.md
  </files>
  <action>
    1. Rebuild `data/gold_set/comprehensive_benchmark_table.md`:
       - Section 1: Keep inter-annotator agreement metrics (`91.00% / 0.5762` Sentiment, `95.41% / 0.7694` Category, per-operator breakdown).
       - Section 2: Completely retire leaked `g600` tables (`82.00% / 0.6781`, etc.). Insert verified active `g300` ($N=300$) and Consensus ($N=182$ Sentiment, $N=187$ Category) benchmark tables for both Sentiment and Category models:
         - Sentiment on `g300`:
           - `ensemble_voting_classifier`: `89.00%` Acc / `0.6089` Macro-F1 / `0.8820` Wtd-F1 / `0.5150` $\kappa$
           - `sentiment_voting_classifier`: `83.67%` Acc / `0.5625` Macro-F1 / `0.8638` Wtd-F1 / `0.4670` $\kappa$
           - `challenger_linearsvc`: `89.00%` Acc / `0.6330` Macro-F1 / `0.8862` Wtd-F1 / `0.5366` $\kappa$
           - `primary_logistic_regression`: `82.67%` Acc / `0.5836` Macro-F1 / `0.8577` Wtd-F1 / `0.4624` $\kappa$
           - `bilstm_attention_model` (Word+Char-CNN): `79.67%` Acc / `0.5790` Macro-F1 / `0.8409` Wtd-F1
           - `bilstm_sentiment_model` (Colab Word-only): `78.67%` Acc / `0.5364` Macro-F1 / `0.8297` Wtd-F1
           - Star-Rating Heuristic: `86.67%` Acc / `0.5438` Macro-F1 / `0.8539` Wtd-F1 / `0.4244` $\kappa$
         - Category on `g300`:
           - `category_voting_classifier`: `91.33%` Acc / `0.4919` Macro-F1 / `0.9098` Wtd-F1 / `0.5046` $\kappa$
           - `category_linearsvc`: `91.00%` Acc / `0.4904` Macro-F1 / `0.9051` Wtd-F1 / `0.4679` $\kappa$
           - `category_logistic_regression`: `89.33%` Acc / `0.4760` Macro-F1 / `0.8985` Wtd-F1 / `0.4385` $\kappa$
           - `bilstm_category_model` (Colab Word-only): `91.33%` Acc / `0.5154` Macro-F1 / `0.9132` Wtd-F1
         - Consensus metrics ($N=182$ Sentiment, $N=187$ Category):
           - `ensemble_voting`: `91.21%` Acc / `0.4589` (3-cls) / `0.6884` (2-cls)
           - `sentiment_voting`: `87.91%` Acc / `0.4769` (3-cls) / `0.7153` (2-cls)
           - `challenger_linearsvc`: `91.21%` Acc / `0.4519` (3-cls)
           - `primary_logistic_regression`: `85.71%` Acc / `0.4560` (3-cls)
           - Star-Rating Heuristic: `92.86%` Acc / `0.5282` (3-cls)
           - `category_voting`: `94.12%` Acc / `0.5166`
           - `category_linearsvc`: `94.12%` Acc / `0.5166`
           - `category_logistic_regression`: `92.51%` Acc / `0.5181`
           - `bilstm_category_model`: `94.12%` Acc / `0.6153`
         - Clearly explain the $N=182$ Sentiment Consensus 0-Neutral artifact (Annotator 2 assigned 0 Neutral labels, depressing 3-class Macro-F1 whenever Neutral is predicted).
       - Section 3: Anonymize links to `blind_annotation_300_annotator1.csv` and `blind_annotation_200_annotator2.csv`.
    2. Rebuild `data/gold_set/gold_standard_evaluation_report.md`:
       - Header: Replace `g600` `200 reviews per operator` with `100 reviews per operator` random stratified draw from Aug 2025 – Sep 2026 common window with zero seed overlap; anonymize annotators.
       - Line 14: Update links; note relative link `../../archive/scraped_data_2020/gold_set/archived_600_plan/` and clarify that early `g600` prototype numbers were retired in favor of active $N=300$ / $N=200$.
       - Sections 1–3: Retire all `g600` tables, `200/200/200` splits, and 600-row confusion matrices. Replace with active $N=300$ and consensus metrics, $3\times 3$ confusion matrices on $N=300$ (`[[12, 3, 8], [5, 5, 9], [2, 6, 250]]` for `ensemble_voting_classifier` and `[[11, 12, 0], [8, 7, 4], [0, 25, 233]]` for `sentiment_voting_classifier`), and active Rogan-Gladen parameters (`Se = 0.5217, Sp = 0.9747` for `ensemble_voting`; `Se = 0.4783, Sp = 0.9711` for `sentiment_voting`).
       - Section 4: Replace leaked `g600` quotes with verified active `g300` examples (`BLIND_085` 5★ Negative, `BLIND_238` 1★ Positive, `BLIND_325` Banglish contraction).
       - Section 5: Anonymize annotator references and document `[BLIND_106]` boundary case.
       - Section 6: Retire `82.00% / 0.6781`, replace with active $N=300$ and consensus figures, and fix missing opening `$` on $\kappa$ tokens.
    3. Update `README.md` lines 375–384 (Gold Standard Benchmark table and Key Takeaway):
       - Align table rows with verified active $N=300$ / $N=182$ consensus metrics:
         - Line 376: Challenger LinearSVC Category `91.00%` ($N=300$) | `94.12%` ($N=187$) | `0.4679`
         - Line 377: Primary Logistic Regression Category `89.33%` ($N=300$) | `92.51%` ($N=187$) | `0.4385`
         - Line 379: Challenger LinearSVC Sentiment `89.00%` ($N=300$) | `91.21%` ($N=182$, was `92.31%`) | `0.5366`
         - Line 380: Primary Logistic Regression Sentiment `82.67%` ($N=300$) | `85.71%` ($N=182$, was `86.81%`) | `0.4624`
         - Line 381: Naive Star-Rating Baseline `86.67%` ($N=300$, was `80.17%`) | `92.86%` ($N=182$, was `84.62%`) | `0.4244` (was `0.4102`)
       - Keep Key Takeaway and surrounding notes perfectly consistent with these active numbers.

    AVOID: Retaining any leaked g600 numbers (82.00%, 0.6781, 80.17%, 84.62%, 92.31%, VOC_0035, VOC_0014, VOC_0010).
    USE: Empirical values computed on live blind_annotation_300_annotator1.csv and blind_annotation_200_annotator2.csv.
  </action>
  <verify>
    python -c "s_rep=open('data/gold_set/gold_standard_evaluation_report.md', encoding='utf-8').read(); assert '82.00%' not in s_rep and '0.6781' not in s_rep and 'VOC_0035' not in s_rep, 'Leaked g600 content found in report!'; s_bench=open('data/gold_set/comprehensive_benchmark_table.md', encoding='utf-8').read(); assert '82.00%' not in s_bench and '0.6781' not in s_bench, 'Leaked g600 content found in benchmark table!'; s_readme=open('README.md', encoding='utf-8').read(); assert '80.17%' not in s_readme and '84.62%' not in s_readme and '86.67%' in s_readme and '92.86%' in s_readme, 'README gold table mismatch!'; print('✓ g600 retirement and active gold synchronization verified!')"
  </verify>
  <done>
    comprehensive_benchmark_table.md and gold_standard_evaluation_report.md are completely cleansed of g600 leakage and present active g300 and consensus benchmarks; README.md lines 375-384 display active gold standard numbers.
  </done>
</task>

## Must-Haves
After all tasks complete, verify:
- [ ] `data/processed/mygp_classified_reviews.csv` has 9 columns with `operator="Grameenphone"` at index 5 across 1,500 rows
- [ ] `data/gold_set/blind_annotation_*.csv` files are completely untouched
- [ ] `data/gold_set/ANNOTATION_RULEBOOK.md` documents `[BLIND_106]` and `[BLIND_111]` taxonomy boundaries
- [ ] `data/gold_set/calculate_agreement.py` is anonymized and outputs per-operator agreement
- [ ] `data/gold_set/comprehensive_benchmark_table.md` presents verified active $N=300$ and consensus metrics with $g600$ retired
- [ ] `data/gold_set/gold_standard_evaluation_report.md` contains active $N=300$ confusion matrices, Rogan-Gladen parameters, and active quotes
- [ ] `README.md` lines 375–384 reflect active $g300$ and consensus metrics (no $g600$ leakage)

## Success Criteria
- [ ] All tasks verified passing with single-command PowerShell checks
- [ ] No git commits created (`ADR-003`)
- [ ] Zero changes to human ground-truth annotations in `data/gold_set/blind_annotation_*.csv`
