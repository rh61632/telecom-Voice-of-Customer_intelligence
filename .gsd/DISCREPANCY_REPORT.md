# Canonical Discrepancy Catalog & Deduplication Report

> **Milestone:** Project & Paper Discrepancy Audit (v1.0.0)  
> **Status:** Authoritative / Complete  
> **Audit Date:** 2026-11-11  
> **Scope:** Full Repository (`scraped_data_global/`, `data/`, `ml/`, `dl/`, `demo/`, `scripts/`, `paper/`, `archive/`)  
> **Policy:** `ADR-001` (Strictly Read-Only, Zero Git Commits), `ADR-002` (Sequential `inherit` Workspace Execution)  

---

## 1. Executive Summary

This document constitutes the canonical, deduplicated discrepancy report across the entire Telecom Voice-of-Customer (VoC) Intelligence project and its accompanying academic manuscripts. 

Every reported discrepancy was independently discovered, empirically verified, and cross-reconciled against live datasets (`all_operators_common_duration_classified.csv`, `all_operators_classified_global.csv`, `all_operators_classified_with_language.csv`, seed CSVs, gold annotations), serialized machine learning models (`ml/models/*.joblib`, `dl/models/`), and LaTeX build artifacts across Phase 1 (Core Pipeline & Docs), Phase 2 (ML/DL & Empirical Scripts), Phase 3 (ESWA Manuscript & Cross-Venue Deliverables), and Phase 4.1 (Direct Quantitative Cross-Reconciliation).

Across the audit, **55 canonical deduplicated discrepancies** have been established, categorized under four standard severity tiers and three functional domains.

### Executive Discrepancy Matrix

| Severity Tier | Group A: Project Codebase & Pipeline | Group B: Research Paper Deliverables | Group C: Cross-Artifact Quantitative | Total |
|---|:---:|:---:|:---:|:---:|
| **Critical** | 2 | 2 | 4 | **8** |
| **Major** | 7 | 6 | 6 | **19** |
| **Minor** | 8 | 4 | 6 | **18** |
| **Hygiene** | 7 | 1 | 2 | **10** |
| **Total** | **24** | **13** | **18** | **55** |

---

## 2. Deduplication Methodology & Cluster Consolidation

Prior to synthesis, all findings across Phases 1–4 were evaluated against the 8 cross-phase duplicate clusters established in `RESEARCH.md` to guarantee zero double-counting:

1. **Cluster 1 (Dead Gold Benchmark Path):** Phase 1 `DISC-008` and Phase 2 `P2-ML-16` consolidated into `DISC-MAJ-01`.
2. **Cluster 2 (Seed Annotation LLM Identifier):** Phase 1 `DISC-009` and Phase 3 `P3-ESWA-12` consolidated into `DISC-MAJ-02`.
3. **Cluster 3 (Missing Runtime Dependencies):** Phase 1 `DISC-010`, `DISC-011`, and Phase 2 `P2-ML-20` consolidated into `DISC-MAJ-03`.
4. **Cluster 4 (Fictional DL Architecture Claims):** Phase 1 `DISC-005`, Phase 2 `P2-DL-07`, and Phase 3 `P3-ESWA-12` consolidated into `DISC-MAJ-04`.
5. **Cluster 5 (Voting Classifier Provenance & Soft Weights):** Phase 1 `DISC-006`, Phase 2 `P2-ML-13`, and Phase 3 `P3-ESWA-12` consolidated into `DISC-MAJ-05`.
6. **Cluster 6 (Seed Sample Drift & Symbolic Exclusions):** Phase 2 `P2-ML-12`, `P2-ML-18`, Phase 3 `P3-ESWA-06`, and `P3-ESWA-07` consolidated into `DISC-MAJ-06`.
7. **Cluster 7 (Stale/Broken Paper Scripts & Integrity Gaps):** Phase 2 `DISC-P2-22..28` and Phase 3 `P3-SCRIPTS-01..03` consolidated into `DISC-MAJ-07`.
8. **Cluster 8 (ESWA Title Prefix Inconsistency):** Phase 1 `DISC-017` and Phase 3 `P3-ESWA-04` consolidated into `DISC-MIN-01` with self-corrected ground truth (`manuscript.tex:32` and `title_page.tex:14` retain the prefix).

---

## 3. Tier 1: Critical Discrepancies (Integrity Breaches & Falsified Claims)

Critical discrepancies represent severe integrity breaches, silent data corruption hazards, fabricated statistics, or irreconcilable empirical contradictions that render the manuscript unfit for submission or endanger pipeline stability.

### `DISC-CRIT-01`: Gold Standard Benchmark Provenance Contradiction & Deprecated `g600` Leakage
- **Traceability:** `[Phase 2: P2-GOLD-21, Phase 3: P3-XLSX-FIG, P3-ESWA-12, Phase 4.1: Evidence 03 §5, §6]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `data/gold_set/comprehensive_benchmark_table.md:30-36`, `data/gold_set/gold_standard_evaluation_report.md:18-58`, `archive/scraped_data_2020/gold_set/archived_600_plan/gold_set_verified.csv`, `scripts/build_paper_empirical_excel.py:84`, `paper/eswa_latex/manuscript.tex:627`
- **Empirical Proof:** Evaluating `ensemble_voting_classifier.joblib` on the archived 600-sample dataset yields **82.00% Accuracy / 0.6781 Macro-F1**, matching the published benchmark reports to 4 decimal places. However, evaluating the same model on the active, author-verified 300-sample ground truth (`data/gold_set/blind_annotation_300_annotator1.csv`) yields **89.00% Accuracy / 0.6089 Macro-F1** (a -0.0692 Macro-F1 collapse). Furthermore, the paper's claimed Rogan-Gladen screening parameters (**$Se = 0.711, Sp = 0.942$**) were traced directly to `g600`: on `g600`, `pred_ensemble` Negative Sensitivity is $54/76 = 0.7105 \implies \mathbf{0.711}$, and `pred_bilstm` Negative Specificity is $494/524 = 0.9427 \implies \mathbf{0.942}$. The published parameters are a cherry-picked composite across two different models from a leaked, supposedly unexecuted dataset.
- **Impact Assessment:** Scientific integrity violation. Benchmark tables publish results from a deprecated test set while claiming it was never executed, concealing the active model's true performance on verified human annotations.
- **Actionable Remediation:** Retract all $N=600$ benchmark tables. Re-evaluate and publish model metrics exclusively against active human consensus ground truth ($N=182$ Sentiment, $N=187$ Category). Recompute Rogan-Gladen parameters using empirical sensitivity and specificity derived from verified active ground truth.

### `DISC-CRIT-02`: Table 6 Fabricated Shocks & Monthly Transition Conflation
- **Traceability:** `[Phase 3: P3-ESWA-12, Phase 4.1: Evidence 02 §1]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:451-460`, `scraped_data_global/classified/all_operators_common_duration_classified.csv`
- **Empirical Proof:** Ground-truth calculation across all 240 modern monthly transitions confirms that exactly 7 of 10 rows in Table 6 (Rows 3 through 9) are **phantom shocks**: their actual monthly transitions had $|\Delta\text{NSS}| < 10.0$ pp (ranging from $-7.46$ to $+9.06$ pp). Furthermore, Row 10 (Banglalink `2026-01` $+15.54$) conflated an annual/partial recovery figure into a single-month transition whose actual $\Delta\text{NSS}$ was $+48.15$ pp.
- **Impact Assessment:** Direct empirical falsification. Over 70% of the prominent econometric shock case studies presented in Table 6 do not exist in the underlying data.
- **Actionable Remediation:** Re-populate Table 6 strictly from the verified 35 intra-era modern shocks cataloged in `nss_significant_shocks.csv` and `02_shocks_priority_matrix_and_cases_reconciliation.md`. Correct Row 10 to reflect the true monthly $\Delta\text{NSS} = +48.15$ pp or clearly relabel it as an annualized turnaround decomposition.

### `DISC-CRIT-03`: Table 5 Longitudinal Era Overlap Arithmetic & NSS Contradictions
- **Traceability:** `[Phase 3: P3-ESWA-08, Phase 4.1: Evidence 01 §2]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:397-400, 415-426`, `scraped_data_global/classified/all_operators_common_duration_classified.csv`
- **Empirical Proof:** Table 5 defines four eras claiming $24\text{M} + 36\text{M} + 36\text{M} + 38\text{M} = 134\text{ months}$, whereas the calendar covers only 122 months. Table 5 double-counts the entire year 2020 in both Era 2 and Era 3, overstates Era 1 by 7 months (actual: 17M), and truncates Era 4 by 7 months (actual: 45M). Table 5 NSS values (e.g., GP $-18.42$, Robi $-14.28$) directly contradict Section 5.1 narrative claims (GP $-53.2$, Robi $-57.9$) and live data (GP $-24.16$, Robi $-29.28$).
- **Impact Assessment:** Basic arithmetic failure and irreconcilable internal narrative contradictions that undermine peer-review credibility.
- **Actionable Remediation:** Restructure Table 5 to cover non-overlapping calendar intervals summing to 122 months (Era 1: 2016-08..2017-12, 17M; Era 2: 2018-01..2019-12, 24M; Era 3: 2020-01..2022-12, 36M; Era 4: 2023-01..2026-09, 45M). Recompute empirical NSS and standard errors directly from live classified data.

### `DISC-CRIT-04`: Case Study 1 Crash vs Surge Inversion & Version Telemetry Absence
- **Traceability:** `[Phase 3: P3-ESWA-09, Phase 4.1: Evidence 02 §3]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:506`, `scraped_data_global/classified/all_operators_common_duration_classified.csv`
- **Empirical Proof:** Case Study 1 narrative claims Banglalink suffered a $-32.8$ point crash in May 2024 due to `v11.8.0`. Empirical recomputation reveals that May 2024 was actually a **$+32.8$ point surge** ($+32.4$ to $+65.2$); the crash occurred in April 2024 and was only $-11.2$ points ($+43.6$ to $+32.4$). Additionally, 51.8% of Banglalink reviews have null `app_version`, and `v11.8.0` accounts for only 198 reviews across the entire history, invalidating causal attribution claims.
- **Impact Assessment:** Severe narrative inversion. A major case study in the paper describes a customer sentiment surge as a catastrophic crash.
- **Actionable Remediation:** Rewrite Case Study 1 to accurately document the April 2024 $-11.2$ point drop and subsequent May 2024 $+32.8$ point rebound. Disclose `app_version` missingness rates and qualify causal claims regarding release `v11.8.0`.

### `DISC-CRIT-05`: McNemar Test Falsification & Unexecuted Paired $t$-Tests
- **Traceability:** `[Phase 3: P3-ESWA-12, Phase 4.1: Evidence 03 §4]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:292`, `data/gold_set/blind_annotation_300_annotator1.csv`, `ml/models/*.joblib`
- **Empirical Proof:** Table 2 notes assert that McNemar's test on Gold $N=300$ vs the star-rating heuristic yields $\chi^2(1) = 21.64, p < 0.0001$. Executing the true contingency test on active Gold $N=300$ yields McNemar $\chi^2(1) = \mathbf{1.59}, p = \mathbf{0.2076}$ (the star heuristic actually had fewer misclassifications than the model: 25 vs 33). Furthermore, zero repository scripts implement paired $t$-tests or McNemar's test, proving the reported values were fabricated.
- **Impact Assessment:** Fabrication of inferential test statistics in Table 2 notes.
- **Actionable Remediation:** Implement a reproducible evaluation script (`scripts/compute_statistical_tests.py`) that computes exact McNemar and paired $t$-test statistics across CV folds. Update Table 2 with true empirical test values.

### `DISC-CRIT-06`: Master Manuscript Silent Reconstruction Clobbering
- **Traceability:** `[Phase 3: P3-ESWA-05]`
- **Domain:** Group B (Research Paper Deliverables)
- **Exact Location:** `scripts/reconstruct_master_manuscript.py:59-61, 135-150`, `paper/eswa_latex/manuscript.tex:468, 478`
- **Empirical Proof:** All four string replacements in `reconstruct_master_manuscript.py` failed silently against `manuscript_base_1506.tex` due to minor whitespace and formatting mismatches. As a result, newly injected tables were placed adjacent to obsolete, contradictory legacy prose, and unparsed Markdown bolding (`**27 of the 35...**`, `**acute public customer...**`) was baked directly into compiled LaTeX PDFs.
- **Impact Assessment:** Automated paper build pipeline introduces syntax corruption and maintains mutually contradictory text within the primary submission document.
- **Actionable Remediation:** Replace brittle literal `.replace()` string substitution with robust AST-based or section-delimited templating in paper build scripts. Cleanse all raw Markdown syntax from LaTeX source files.

### `DISC-CRIT-07`: BanglaBERT Class Index Misalignment Hazard (80% Label Corruption)
- **Traceability:** `[Phase 2: P2-DL-08, Phase 1: DISC-021]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `dl/models/banglabert_finetuned_{sentiment,category}/config.json`, `dl/models/cat_le.joblib`
- **Empirical Proof:** The uncommitted patch in `banglabert_finetuned_category/config.json` mapped label indices as `0: General Appreciation`, `1: Offers`, `2: App Login`, `3: Network Speed`, `4: Billing`. In contrast, scikit-learn's label encoder `cat_le.joblib` uses alphabetical ordering: `0: App Login`, `1: Billing`, `2: General Appreciation`, `3: Network Speed`, `4: Offers`. Passing raw model logits into `cat_le.inverse_transform()` corrupts 4 of 5 classes (80% corruption rate).
- **Impact Assessment:** Severe runtime silent corruption risk in deep learning inference pipelines.
- **Actionable Remediation:** Synchronize `config.json` `id2label` mappings to match scikit-learn label encoders exactly, or enforce explicit dictionary-based label conversion during inference.

### `DISC-CRIT-08`: Raw Review Schema-Dropping Overwrite Hazard
- **Traceability:** `[Phase 1: DISC-001]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `scraped_data_global/pipeline/scraper_worker.py:49-57, 137-140, 203-211`, `scraped_data_global/pipeline/merge_and_sync_all_datasets.py:272`, `scripts/check_version_bias.py:6`
- **Empirical Proof:** Raw review scrapers collect 12 columns (`review_id`, `user_name`, `rating`, `review_date`, `review_text`, `thumbs_up`, `operator`, `app_version`, `user_image`, `developer_reply`, `developer_reply_date`, `is_enriched`). However, lines 49-57 of `scraper_worker.py` and line 272 of `merge_and_sync_all_datasets.py` hardcode a 7-column write mask, dropping `app_version` and metadata. Re-running the scraper permanently strips metadata and causes downstream `scripts/check_version_bias.py:6` to crash with `KeyError: 'app_version'`.
- **Impact Assessment:** Permanent data loss during pipeline re-execution, breaking downstream bias and econometric analysis scripts.
- **Actionable Remediation:** Update `scraper_worker.py` and `merge_and_sync_all_datasets.py` to preserve all 12 raw columns in storage and write masks.

---

## 4. Tier 2: Major Discrepancies (Reproducibility & Model Drift)

Major discrepancies represent significant flaws affecting model reproducibility, paper compilation, econometric claims, or missing software dependencies.

### `DISC-MAJ-01`: Dead Gold Path Silent Zero Return (Cluster 1)
- **Traceability:** `[Phase 1: DISC-008, Phase 2: P2-ML-16]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `ml/train_filtered_experiments.py:19, 138-140`
- **Empirical Proof:** `GOLD_CSV` references `scraped_data_2020/gold_set/gold_set_verified.csv`, a non-existent path. The script catches the `FileNotFoundError` and silently returns `(0.0, 0.0)` for accuracy and macro-F1, masking evaluation failures during experiment runs.
- **Impact Assessment:** Silently breaks ablation and experimental evaluation routines.
- **Actionable Remediation:** Update `GOLD_CSV` path to `data/gold_set/blind_annotation_300_annotator1.csv` and remove silent exception swallowing.

### `DISC-MAJ-02`: Seed Annotation LLM Identifier Mismatch (Cluster 2)
- **Traceability:** `[Phase 1: DISC-009, Phase 3: P3-ESWA-12]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `archive/seed_pipeline_groq/src/02_llm_zero_shot_classification.py:50`, `paper/eswa_latex/manuscript.tex:254`
- **Empirical Proof:** The Groq pipeline script explicitly targets `qwen/qwen3.8-27b`, whereas the manuscript claims `Qwen-2.5-32B` was used for zero-shot seed pseudo-labeling.
- **Impact Assessment:** Factual inaccuracy regarding the generative model used in the data generation methodology.
- **Actionable Remediation:** Reconcile manuscript text to cite `qwen/qwen3.8-27b` or clarify the provenance of zero-shot annotations.

### `DISC-MAJ-03`: Missing Runtime Dependencies Across Manifests & Demo Crash (Cluster 3)
- **Traceability:** `[Phase 1: DISC-010, DISC-011, Phase 2: P2-ML-20]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `demo/requirements.txt:1-5`, `requirements.txt:1-40`, `ml/requirements.txt:1-10`, `demo/app.py:13`
- **Empirical Proof:** `demo/requirements.txt` omits `nltk` and `pandas`. Executing `python demo/app.py` in an environment configured strictly from `demo/requirements.txt` crashes immediately with `ModuleNotFoundError: No module named 'nltk'`. Furthermore, root `requirements.txt` omits `nltk`, `python-docx`, `openpyxl`, `Pillow`, and `huggingface_hub`.
- **Impact Assessment:** Prevents turnkey deployment and breaks clean virtual environment setup.
- **Actionable Remediation:** Add `nltk>=3.8.1` and `pandas>=2.0.0` to `demo/requirements.txt`. Add all missing runtime libraries to root and subproject requirements manifests.

### `DISC-MAJ-04`: Fictional DL Architecture Claims (Char-CNN, GloVe, Multi-Head) (Cluster 4)
- **Traceability:** `[Phase 1: DISC-005, Phase 2: P2-DL-07, Phase 3: P3-ESWA-12]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `classify_global_dataset.py:24-67`, `dl/predict_dl.py:25-60`, `dl/README.md:12, 62`, `master_unified_colab.ipynb:486-504`, `paper/eswa_latex/manuscript.tex:284-292`
- **Empirical Proof:** The paper and documentation assert the BiLSTM architecture integrates `Char-CNN` embeddings, pre-trained `GloVe 300d` vectors, and multi-head Bahdanau attention. The codebase implementation (`HybridBiLSTMAttention`) contains randomly initialized 128d word embeddings, single-head attention, and zero character-level convolutional layers.
- **Impact Assessment:** Severe peer-review vulnerability. Architecture diagrams and methodology text claim complex features absent from actual code.
- **Actionable Remediation:** Revise manuscript Section 4.2 to accurately describe the word-level BiLSTM with single-head attention, removing all claims of Char-CNN, GloVe, and multi-head attention.

### `DISC-MAJ-05`: Model Provenance & Voting Classifier Soft Weight Divergence (Cluster 5)
- **Traceability:** `[Phase 1: DISC-006, Phase 2: P2-ML-13, Phase 3: P3-ESWA-12]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `classify_global_dataset.py:78`, `ml/predict.py:21`, `ml/models/category_voting_classifier.joblib`, `ml/train_category.py:84-133`, `paper/eswa_latex/manuscript.tex:278-282`
- **Empirical Proof:** Production model `category_voting_classifier.joblib` was generated in Google Colab Cell 7 using `weights=[2.0, 2.5, 1.0]`, `LR C=2.5`, and dual TF-IDF vectorizers (`char 25k + word 12k`). Local training script `ml/train_category.py` specifies `weights=[2, 2, 1]`, `LR C=1.0`, and single `char_wb` vectorizer. The paper claims local hyperparameters while deploying the Colab model.
- **Impact Assessment:** Pipeline irreproducibility; running local training overwrites production models with lower-performing weights.
- **Actionable Remediation:** Update `ml/train_category.py` to match the exact Colab pipeline configuration (`weights=[2.0, 2.5, 1.0]`, dual vectorizers) and synchronize manuscript reporting.

### `DISC-MAJ-06`: Seed Corpus Sample Count Drift & 14 Symbolic Exclusions (Cluster 6)
- **Traceability:** `[Phase 2: P2-ML-12, P2-ML-18, Phase 3: P3-ESWA-06, P3-ESWA-07, Phase 4.1: Evidence 03 §3]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `data/processed/my{gp,bl,robi}_classified_reviews.csv`, `scripts/evaluate_linguistic_subcohorts.py:81`, `paper/eswa_latex/manuscript.tex:141-153, 334-365`, `ml/reports/category_classification_report.md`
- **Empirical Proof:** Ground-truth seed reviews total exactly $N=4,500$ (1,500 per operator, 2,731 General Appreciation). Paper Tables 1, 2, and 3 cite $N=4,499$ (2,730 General Appreciation). Furthermore, Table 4 sub-cohorts sum to $4,486$ ($1,091 + 390 + 3,005$) because `evaluate_linguistic_subcohorts.py` silently dropped 14 `Symbolic / Emoticons` reviews.
- **Impact Assessment:** Unreconciled sample sizes across consecutive tables in the methodology section.
- **Actionable Remediation:** Update all tables to cite the true ground-truth total of $N=4,500$. Explicitly document the 14 symbolic/emoticon reviews in Table 4.

### `DISC-MAJ-07`: Stale/Broken Paper Scripts & Integrity Script Gaps (Cluster 7)
- **Traceability:** `[Phase 2: DISC-P2-22..28, Phase 3: P3-SCRIPTS-01..03]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `scripts/audit_check.py`, `scripts/audit_docx.py`, `scripts/find_tables.py`, `scripts/audit_project_integrity.py`
- **Empirical Proof:** 18 scripts in `scripts/` target obsolete `paper/journal_manuscript/` or `.docx` paths, crashing on invocation (`FileNotFoundError`, `PackageNotFoundError`). In `audit_project_integrity.py`, Modules 2, 3, and 7 are completely unexecuted, and loose tolerances (`atol=0.05`) mask data drift.
- **Impact Assessment:** Repository contains broken audit tooling and gives false assurance of project integrity.
- **Actionable Remediation:** Archive or update stale scripts in `scripts/`. Implement missing verification modules in `audit_project_integrity.py` and enforce strict equality assertions.

### `DISC-MAJ-08`: Gradio Demo Layout `out_cat` Disconnected Wiring Bug
- **Traceability:** `[Phase 1: DISC-015]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `demo/app.py:31, 38, 54, 97, 108`
- **Empirical Proof:** `out_cat = gr.Textbox(label="Operational Domain")` is defined in layout (line 97), and `category_label` is computed (line 38). However, lines 31 and 54 return 5-element tuples omitting `category_label`, and line 108 callback output registers only 5 outputs. In the running UI, the "Operational Domain" box remains permanently empty.
- **Impact Assessment:** Core interactive demonstration UI feature is broken for users.
- **Actionable Remediation:** Update return statements and Gradio event listeners in `demo/app.py` to include `category_label` in outputs.

### `DISC-MAJ-09`: Complement Naive Bayes (CNB) Macro-F1 Overstatement (+8 pp)
- **Traceability:** `[Phase 4.1: Evidence 03 §1]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:278`, `ml/reports/category_classification_report.md`
- **Empirical Proof:** Table 2 claims CNB achieves Macro-F1 = $0.7418 \pm 0.018$ and Weighted-F1 = $0.8412$. Live 5-fold Stratified Cross-Validation on $N=4,500$ proves CNB achieves only Macro-F1 = **$0.6641$** (Config A) or **$0.6481$** (Config B), overstated by $+7.8$ to $+9.4$ percentage points.
- **Impact Assessment:** Distorts baseline comparisons in Table 2 benchmark evaluation.
- **Actionable Remediation:** Recompute and update Table 2 with empirical CNB cross-validation scores ($0.6641$).

### `DISC-MAJ-10`: Vocabulary Complexity & Non-Zero Feature Density Drift
- **Traceability:** `[Phase 4.1: Evidence 03 §2]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:173`, `ml/models/category_voting_classifier.joblib`
- **Empirical Proof:** The manuscript claims vocabulary size $V \approx 50,000$ and non-zero feature density $d \approx 20\text{--}45$. Deserializing `category_voting_classifier.joblib` reveals actual feature dimension $V = 29,843$ features, and empirical non-zero density across seed and production samples is $d = 109.72$ features/review.
- **Impact Assessment:** Technical complexity claims diverge by more than 2x from production model parameters.
- **Actionable Remediation:** Correct Section 3.2 complexity metrics to reflect $V \approx 30,000$ and mean density $d \approx 110$.

### `DISC-MAJ-11`: Unreferenced Tables, Ghost Equations & Caption Defects
- **Traceability:** `[Phase 3: P3-ESWA-02]`
- **Domain:** Group B (Research Paper Deliverables)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:198, 267, 299, 541-543, 590-591`
- **Empirical Proof:** Table 3 (`tab:perclass`) and Table 8 (`tab:decision_matrix`) have zero citations in manuscript prose. Equation 8 (`eq:shock_threshold`) has zero references. Table 7 is captioned `"Algorithm 1: Canary Deployment Gating..."` inside a floating `table*` environment, rendering as `"Table 7 Algorithm 1: ..."`.
- **Impact Assessment:** Professional typesetting defects and unreferenced content violating journal formatting standards.
- **Actionable Remediation:** Add explicit prose discussions citing Table 3, Table 8, and Equation 8. Fix Table 7 captioning to follow standard algorithm or table environments.

### `DISC-MAJ-12`: BibTeX Chronological Errors & 17 Uncited Orphan Entries
- **Traceability:** `[Phase 3: P3-ESWA-03]`
- **Domain:** Group B (Research Paper Deliverables)
- **Exact Location:** `paper/eswa_latex/references.bib:26, 289`, `manuscript.bbl:52-64`
- **Empirical Proof:** `cohen1960coefficient` line 289 has `year = {2020}`, compiling as `Cohen (2020)` for Jacob Cohen's foundational 1960 paper. `cambria2017senticnet` line 26 has `year = {2018}`. Furthermore, exactly 17 of 49 BibTeX entries are uncited orphans.
- **Impact Assessment:** Academic attribution errors and citation bloat.
- **Actionable Remediation:** Correct publication years in `references.bib` (`1960` for Cohen, `2017` for Cambria). Remove or cite orphan bibliography entries.

### `DISC-MAJ-13`: Embedded Figures Clipping, Dual Numbering & Quadrant Inversion
- **Traceability:** `[Phase 3: P3-ESWA-11]`
- **Domain:** Group B (Research Paper Deliverables)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:94, 389, 431, 482`, `paper/eswa_latex/figures/figure{1..4}*.png`
- **Empirical Proof:** Prepending `figure0` caused Figures 1–4 to render with contradictory numbers (LaTeX caption says Figure 2, but embedded raster banner says Figure 1). In `figure4_banglalink_reversal_decomposition.png`, the title text clips at column 2849 of 2850 px canvas, truncating `"s)"` from `"(+15.54 Points)"`. In `figure3_priority_matrix.png`, plotting total-corpus prevalence (0.78%–8.12%) placed GP Login in Q2 and BL Offers in Q3, contradicting prose descriptions.
- **Impact Assessment:** Graphic presentation flaws and visual contradiction of narrative findings.
- **Actionable Remediation:** Regenerate raster figures without burned-in "Figure X" headers. Re-export Figure 4 with adequate canvas margins. Re-plot Figure 3 using within-domain prevalence.

### `DISC-MAJ-14`: Missing Empirical Workbook `paper/JBA_Manuscript_Empirical_Calculations.xlsx`
- **Traceability:** `[Phase 3: P3-XLSX-FIG]`
- **Domain:** Group B (Research Paper Deliverables)
- **Exact Location:** `paper/JBA_Manuscript_Empirical_Calculations.xlsx`, `scripts/build_paper_empirical_excel.py`
- **Empirical Proof:** The referenced empirical Excel workbook does not exist on disk (zero `.xlsx` files exist in the repository). The build script was retargeted to `paper/` but never executed, and contains hardcoded leaked `g600` metrics.
- **Impact Assessment:** Deliverable promised in documentation and methodology is missing from the repository.
- **Actionable Remediation:** Execute `build_paper_empirical_excel.py` using verified active ground-truth metrics to generate the canonical spreadsheet.

### `DISC-MAJ-15`: Cross-Venue LaTeX Drift & Equation 9 Algebraic Sign Inversion
- **Traceability:** `[Phase 3: P3-TP-01..07]`
- **Domain:** Group B (Research Paper Deliverables)
- **Exact Location:** `paper/telecommunications_policy_latex/{manuscript,manuscript_twocolumn,title_page}.tex`
- **Empirical Proof:** In `telecommunications_policy_latex/manuscript.tex:213`, Equation 9 inverts the sign of the False Positive Rate ($+FPR-1$). Line 179 script review counts sum to 655,598 (-51 review deficit). Compiled PDFs retain pre-sync counts.
- **Impact Assessment:** Severe algebraic error in secondary venue submission deliverable.
- **Actionable Remediation:** Correct Equation 9 algebra to $1 - FPR$, synchronize review counts, and recompile secondary manuscript PDFs.

### `DISC-MAJ-16`: Common-Window Boundary Divergence & 21-Review JSON Leakage
- **Traceability:** `[Phase 1: DISC-003, Phase 3: P3-HTML-02, Phase 4.1: Evidence 01 §3]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `merge_and_sync_all_datasets.py:290`, `sync_post_classification.py:58`, `yearly_intelligence_trends.json:4, 28`
- **Empirical Proof:** Classified common-duration dataset starts `2016-08-01` ($N=655,649$, 3,713 days). `sync_post_classification.py` uses `2016-07-28` ($N=655,676$, 3,716 days). `yearly_intelligence_trends.json` retained 21 reviews scraped between July 28 and July 31, 2016, reporting 2016 volume as 1,329 ($N=655,670$).
- **Impact Assessment:** Pipeline scripts yield conflicting row counts depending on which sync script is executed.
- **Actionable Remediation:** Standardize all pipeline and reporting scripts to enforce the canonical `2016-08-01` boundary ($N=655,649$). Regenerate `yearly_intelligence_trends.json`.

### `DISC-MAJ-17`: Unsubstantiated Commercial Claims (`28% ARPU` & `3.5x-5.0x SAC`)
- **Traceability:** `[Phase 4.1: Evidence 03 §7]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:242, 581`
- **Empirical Proof:** The manuscript claims that resolved VoC issues result in "28% higher ARPU" (line 581) and cites a "3.5x–5.0x Subscriber Acquisition Cost ratio" (line 242). Zero repository datasets, telemetry logs, scripts, or cited papers substantiate these figures.
- **Impact Assessment:** Commercial ROI claims presented as empirical facts without supporting evidence.
- **Actionable Remediation:** Provide formal academic citations for industry benchmark figures or explicitly qualify them as illustrative assumptions.

### `DISC-MAJ-18`: Uncommitted Working-Tree Drift (39 Tracked Files + Untracked Dirs)
- **Traceability:** `[Phase 1: DISC-021]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** Git working tree (39 modified tracked files across root, `dl/`, `paper/`, plus untracked `demo/`, `ml/reports/`, `scripts/`)
- **Empirical Proof:** Git status inspection reveals 39 modified tracked files (common-window shifts, regenerated plots, model configs) and large untracked directories that have never been committed to version control.
- **Impact Assessment:** High risk of work loss and deployment divergence; working tree differs substantially from git `HEAD`.
- **Actionable Remediation:** Post-audit, commit all validated changes under clean semantic commit messages.

### `DISC-MAJ-19`: PyTorch & Joblib Deserialization Failures under Python 3.15.1
- **Traceability:** `[Phase 2: P2-DL-11]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `dl/models/bilstm_vocab.joblib`, `dl/predict_dl.py:68, 104`
- **Empirical Proof:** Running `joblib.load('dl/models/bilstm_vocab.joblib')` crashes with `AttributeError: module '__main__' has no attribute 'Vocabulary'` due to unpickling module scoping. Running `python dl/predict_dl.py --model transformer` crashes with `ModuleNotFoundError: No module named 'transformers'`.
- **Impact Assessment:** Breaks standalone inference scripts in clean runtime environments.
- **Actionable Remediation:** Decouple vocabulary serialization from `__main__` by saving word-to-index mappings as standard JSON dictionaries. Add appropriate dependency guards.

---

## 5. Tier 3: Minor Discrepancies (Stylistic & Documentation Drift)

Minor discrepancies represent localized typographical errors, rounding divergences, unanchored regexes, or documentation inconsistencies that do not compromise core integrity.

### `DISC-MIN-01`: ESWA Title Prefix Inconsistency Across Artifacts (Cluster 8)
- **Traceability:** `[Phase 1: DISC-017, Phase 3: P3-ESWA-04]`
- **Domain:** Group B (Research Paper Deliverables)
- **Exact Location:** `demo/app.py:114`, `paper/eswa_latex/manuscript.tex:32`, `paper/eswa_latex/title_page.tex:14`, `paper/eswa_latex/manuscript_base_1506.tex:28`
- **Empirical Proof:** `demo/app.py:114`, `manuscript.tex:32`, and `title_page.tex:14` retain the informal prefix *"With Great Reviews Comes Great Responsibility: ..."*, whereas `manuscript_base_1506.tex:28` and `telecommunications_policy_latex/title_page.tex:18` dropped it.
- **Actionable Remediation:** Adopt a single, uniform academic title across all manuscript, code, and demo files.

### `DISC-MIN-02`: Table 1 Deployed Percentage Rounding Error (Sums to 100.1%)
- **Traceability:** `[Phase 4.1: Evidence 01 §1]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:141-153`
- **Empirical Proof:** Table 1 deployed percentages ($86.6\% + 5.0\% + 5.0\% + 2.5\% + 1.0\%$) sum to $100.1\%$. Unrounded values sum to exactly $100.0000\%$ ($86.55\%, 5.04\%, 4.99\%, 2.46\%, 0.96\%$).
- **Actionable Remediation:** Adjust rounding in Table 1 to ensure components sum to $100.0\%$.

### `DISC-MIN-03`: Table 3 Confusion Matrix Precision/F1 Typographical Errors
- **Traceability:** `[Phase 3: P3-ESWA-07, Phase 4.1: Evidence 03 §1]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:309-316`
- **Empirical Proof:** Table 3 reports $\mathcal{C}_1$ Precision $0.9528$ (true $0.9828$), $\mathcal{C}_1$ F1 $0.9912$ (true $0.9913$), $\mathcal{C}_5$ Precision $0.9993$ (true $1.0000$), and Macro Precision $0.9717$ (true $0.9779$).
- **Actionable Remediation:** Update Table 3 precision and F1 entries to match true confusion matrix arithmetic.

### `DISC-MIN-04`: Inter-Rater Sentiment Agreement Typo ($81.0\%$ vs $91.0\%$) & PABAK Derivation
- **Traceability:** `[Phase 4.1: Evidence 03 §5]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:258, 629`
- **Empirical Proof:** Line 258 claims sentiment agreement is $81.0\%$, while line 629 reports PABAK $= 0.8650$. The PABAK formula $(3 \times 0.9100 - 1)/2 = 0.8650$ proves line 258 was a typo for $91.00\%$.
- **Actionable Remediation:** Correct line 258 to report true sentiment percentage agreement of $91.0\%$.

### `DISC-MIN-05`: Case Study 2 Category Contribution Contradiction
- **Traceability:** `[Phase 3: P3-ESWA-09, Phase 4.1: Evidence 02 §3]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `paper/eswa_latex/manuscript.tex:509-516`
- **Empirical Proof:** Case Study 2 reports $+6.95$ Gen ($57.4\%$ vs $42.6\%$ technical) and omits Billing $+0.36$, contradicting Table 6 Row 10 and Figure 4 ($+15.54$: $+10.33$ Gen $66.5\%$ vs $+5.21$ Tech $33.5\%$).
- **Actionable Remediation:** Reconcile Case Study 2 prose with Figure 4 and Table 6 decompositions.

### `DISC-MIN-06`: Summary JSON Schema Inconsistency Between Pipelines
- **Traceability:** `[Phase 1: DISC-004]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `merge_and_sync_all_datasets.py:317-324`, `sync_post_classification.py:86-96`, `common_duration_summary.json`
- **Empirical Proof:** `merge_and_sync` omits sentiment category counts, whereas `sync_post` includes them.
- **Actionable Remediation:** Standardize JSON summary schemas across all pipeline scripts.

### `DISC-MIN-07`: Stale Benchmark Results Report in DL Directory
- **Traceability:** `[Phase 2: P2-DL-01]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `dl/reports/results.txt:4, 11-13, 58-59`
- **Empirical Proof:** Stale report from commit `60cf0f4` cites obsolete class counts and points to non-existent `colab_bilstm_attention.pt`.
- **Actionable Remediation:** Delete or regenerate `results.txt` from current model checkpoints.

### `DISC-MIN-08`: BanglaBERT Positive Banglish Review Misclassification
- **Traceability:** `[Phase 2: P2-DL-03]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `dl/telecom_voc_banglabert_finetuning_colab.ipynb:904-906`
- **Empirical Proof:** Notebook Cell 10 misclassifies `"Onk shundor app shob offer e discount pai"` as Negative with 94.7% confidence.
- **Actionable Remediation:** Document known tokenizer/vocabulary limitations on Latin-script Banglish in deep learning models.

### `DISC-MIN-09`: Missing `operator` Column in Seed CSV
- **Traceability:** `[Phase 2: P2-DL-02]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `data/processed/mygp_classified_reviews.csv:1`, `banglabert_finetuning_colab.ipynb:225`
- **Empirical Proof:** `mygp_classified_reviews.csv` contains 8 columns lacking `operator`, causing Colab to print `"across 2 operators"`.
- **Actionable Remediation:** Add `operator="Grameenphone"` column to `mygp_classified_reviews.csv`.

### `DISC-MIN-10`: `train_category.py` Standard Deviation Duplication Bug
- **Traceability:** `[Phase 2: P2-ML-15]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `ml/train_category.py:247`
- **Empirical Proof:** Formats string as `{m['mean_macro_f1']:.4f} ± {m['mean_macro_f1']:.4f}`, duplicating the mean instead of printing the standard deviation.
- **Actionable Remediation:** Change second format token to `{m['std_macro_f1']:.4f}`.

### `DISC-MIN-11`: Short-Text Ablation Study Table vs Prose Contradiction
- **Traceability:** `[Phase 2: P2-ML-17]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `ml/reports/short_text_filtering_ablation_study.md:12-19, 37`
- **Empirical Proof:** Table line 12 reports Macro-F1 rising from $0.6737 \to 0.7318$, while prose line 19 claims $0.6781 \to 0.7436$ with malformed LaTeX `(≥ 3$ words)`.
- **Actionable Remediation:** Reconcile narrative text to match table data and correct LaTeX syntax.

### `DISC-MIN-12`: Language Detector Effective English Threshold Fallthrough
- **Traceability:** `[Phase 2: P2-ML-19]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `ml/language_detector.py:6, 86, 147-156`
- **Empirical Proof:** Line 153 falls through to `elif english_ratio >= 0.60`, lowering the effective English threshold to 60% vs the documented 70%.
- **Actionable Remediation:** Align implementation with Gambäck & Das 70% threshold or update documentation.

### `DISC-MIN-13`: Global Language Distribution Date Span Ambiguity
- **Traceability:** `[Phase 2: P2-ML-20]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `ml/reports/global_language_distribution.md:3`, `ml/reports/global_language_distribution.json`
- **Empirical Proof:** Prose claims 2016–2026, but underlying data covers 2014–2026 (including 1,093 reviews from 2014–2015).
- **Actionable Remediation:** Clarify date boundaries in the report title and header.

### `DISC-MIN-14`: Gradio Demo Factual Training Volume Claim
- **Traceability:** `[Phase 1: DISC-016]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `demo/app.py:67`
- **Empirical Proof:** UI banner claims model was trained on 655,649 reviews instead of 4,500 seed reviews.
- **Actionable Remediation:** Update banner text to state: "Demonstrating models trained on 4,500 expert-labeled seed reviews, evaluated on 655,649 longitudinal customer reviews."

### `DISC-MIN-15`: README Internal Banglalink Scorecard Contradiction
- **Traceability:** `[Phase 1: DISC-018]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `README.md:416` vs `README.md:51`
- **Empirical Proof:** Line 416 states Banglalink NSS is `+53.1%` (legacy 3,716-day rounding) vs Section 1 Scorecard `+53.0%`.
- **Actionable Remediation:** Update line 416 to `+53.0%`.

### `DISC-MIN-16`: README Badge Sentiment Kappa Omission
- **Traceability:** `[Phase 1: DISC-019]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `README.md:20`
- **Empirical Proof:** Displays Category Kappa $\kappa = 0.77$ only, omitting Sentiment Kappa $\kappa = 0.5762$.
- **Actionable Remediation:** Add companion badge for Sentiment Kappa.

### `DISC-MIN-17`: TODO.txt Stale 398k References & Task Status
- **Traceability:** `[Phase 1: DISC-020]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `TODO.txt:63`
- **Empirical Proof:** Cites obsolete "398k production corpus" and marks Web Demo open despite `demo/app.py` existing.
- **Actionable Remediation:** Update corpus volume to 655.6k and mark Web Demo task completed.

### `DISC-MIN-18`: HTML Deliverable Word Count Inflation & KaTeX Defects
- **Traceability:** `[Phase 3: P3-HTML-01..04]`
- **Domain:** Group B (Research Paper Deliverables)
- **Exact Location:** `paper/index.html`, `paper/paper.html`
- **Empirical Proof:** HUD claims $\sim 3,206$ words; actual is 3,843 (+20.1%). Exactly 7 `<TAB>ext` and 2 `<TAB>imes` escape sequences corrupt KaTeX math blocks.
- **Actionable Remediation:** Update HUD word count and replace corrupted tab-escaped math blocks with standard LaTeX syntax.

---

## 6. Tier 4: Hygiene Discrepancies (Dead Code & Environment Cleanup)

Hygiene discrepancies represent environmental portability risks, dead code paths, unanchored regexes, and test harness maintenance items.

### `DISC-HYG-01`: Non-Portable Hardcoded POSIX Python Interpreter
- **Traceability:** `[Phase 1: DISC-002]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `scraped_data_global/pipeline/run_parallel_scrapers.py:22`
- **Empirical Proof:** Hardcodes `dl/.venv/bin/python`, failing on Windows systems.
- **Actionable Remediation:** Use `sys.executable` to dynamically resolve the current Python environment.

### `DISC-HYG-02`: Unused Heavy Dependencies Declared in Manifests
- **Traceability:** `[Phase 1: DISC-012]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `requirements.txt:36-37`, `dl/requirements.txt:6-7`
- **Empirical Proof:** Declares `torchvision>=0.17.0` and `torchaudio>=2.2.0`, which are never imported in the project.
- **Actionable Remediation:** Remove unused dependencies from requirements manifests.

### `DISC-HYG-03`: `scikit-learn` Version Specifier Floor Conflict
- **Traceability:** `[Phase 1: DISC-013]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `demo/requirements.txt:2`, `requirements.txt:30`
- **Empirical Proof:** Specifies `>=1.3.0` in demo vs `>=1.4.0` in root requirements.
- **Actionable Remediation:** Align scikit-learn floor across all manifests to `>=1.4.0`.

### `DISC-HYG-04`: Two-Panel Figure Generator Alias Parity Break Risk
- **Traceability:** `[Phase 1: DISC-014]`
- **Domain:** Group B (Research Paper Deliverables)
- **Exact Location:** `scripts/generate_two_panel_figure.py:171-173`
- **Empirical Proof:** Saves `monthly_nss_trend_modern_era.png` without updating alias `monthly_nss_trend_2020_2026.png`.
- **Actionable Remediation:** Update generator script to write to both alias targets simultaneously.

### `DISC-HYG-05`: Raw Review Scraper Configuration & Duplicate Row
- **Traceability:** `[Phase 1: P1-EVID-01]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `scraped_data_global/pipeline/scraper_worker.py:33, 39, 45`, `scraped_data_global/raw/myrobi_global.csv`
- **Empirical Proof:** Hardcodes `country="us"` and `lang="en"`; exactly 1 duplicate/null `review_id` row in `myrobi_global.csv` (200,651 unique out of 200,652).
- **Actionable Remediation:** Deduplicate raw CSV and parameterize scraper language/country options.

### `DISC-HYG-06`: BanglaBERT Zip Archive Stale Tokenizer & Config Files
- **Traceability:** `[Phase 2: P2-DL-09]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `banglabert_finetuned_models.zip`
- **Empirical Proof:** Weights match disk (`b566cc09...`, `dc85d60c...`), but zip archive retains pre-patch `LABEL_0..` in `config.json`.
- **Actionable Remediation:** Re-pack zip archive with patched `config.json` files.

### `DISC-HYG-07`: PyTorch BiLSTM Training Vocabulary Off-by-One
- **Traceability:** `[Phase 2: P2-DL-10]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `dl/train_bilstm_category.py:311-312, 342-377`
- **Empirical Proof:** `bilstm_category_vocab.json` missing on disk; `+1` padding token index calculation off-by-one.
- **Actionable Remediation:** Correct vocabulary index offset and persist serialized JSON vocabulary mapping.

### `DISC-HYG-08`: Gold Standard Rulebook Violation & Author De-Anonymization
- **Traceability:** `[Phase 2: P2-GOLD-21]`
- **Domain:** Group C (Cross-Artifact Quantitative)
- **Exact Location:** `data/gold_set/calculate_agreement.py:13, 22`, `data/gold_set/ANNOTATION_RULEBOOK.md:122`
- **Empirical Proof:** Script prints de-anonymized author names `"Ratul CSV"` and `"Friend CSV"`. Sample `[BLIND_106]` violates `ANNOTATION_RULEBOOK.md:122` by classifying a price complaint under Billing. Missing `$` on `\kappa` in `data/README.md:25`.
- **Actionable Remediation:** Anonymize script print statements to `"Annotator 1"` and `"Annotator 2"`. Re-label sample `[BLIND_106]` under Offers & Data Packs.

### `DISC-HYG-09`: Windows CRLF Line Endings in All 8 Bash Scripts
- **Traceability:** `[Phase 2: DISC-P2-30]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `scripts/*.sh` (all 8 files), `scripts/validate-encoding.ps1:16`
- **Empirical Proof:** All 8 `.sh` scripts contain Windows `\r\n` line endings, causing syntax errors under POSIX bash. `validate-encoding.ps1` ignores `.sh` files.
- **Actionable Remediation:** Convert line endings of all shell scripts to LF (`\n`) and extend `validate-encoding.ps1` to audit `*.sh`.

### `DISC-HYG-10`: Harness Validator CWD Path Fragility & Unanchored Regexes
- **Traceability:** `[Phase 2: DISC-P2-29, 31, 32]`
- **Domain:** Group A (Project Codebase & Pipeline)
- **Exact Location:** `scripts/validate-{skills,workflows,agents,templates}.ps1`, `scripts/validate-all.ps1`
- **Empirical Proof:** Invoking validator scripts from outside repo root causes silent false-positive pass ("0 checked, 0 errors, All valid!"). Regexes use unanchored substring matching.
- **Actionable Remediation:** Anchor all validator scripts to script root using `$PSScriptRoot` and replace substring regexes with structured YAML frontmatter parsing.

---

## 7. Master Discrepancy Index & Traceability Cross-Reference

| Canonical ID | Severity | Domain | Primary File & Line | Summary Description | Source Audit IDs |
|---|:---:|:---:|---|---|---|
| `DISC-CRIT-01` | Critical | Group C | `data/gold_set/comprehensive_benchmark_table.md:30` | Gold benchmark table originates from deprecated `g600` (82.00%/0.6781) vs active `g300` (89.00%/0.6089); Rogan-Gladen $Se/Sp$ cherry-picked from `g600` | P2-GOLD-21, P3-XLSX-FIG, P3-ESWA-12, Phase 4.1 |
| `DISC-CRIT-02` | Critical | Group C | `paper/eswa_latex/manuscript.tex:451-460` | 7 of 10 rows in Table 6 are phantom shocks ($|\Delta\text{NSS}| < 10$); Row 10 conflated annual into monthly | P3-ESWA-12, Phase 4.1 |
| `DISC-CRIT-03` | Critical | Group C | `paper/eswa_latex/manuscript.tex:415-426` | Table 5 defines overlapping eras summing to 134M vs 122M calendar; NSS values contradict narrative | P3-ESWA-08, Phase 4.1 |
| `DISC-CRIT-04` | Critical | Group C | `paper/eswa_latex/manuscript.tex:506` | CS1 inverts May 2024 $+32.8$ surge into a crash; 51.8% of BL reviews lack `app_version` | P3-ESWA-09, Phase 4.1 |
| `DISC-CRIT-05` | Critical | Group C | `paper/eswa_latex/manuscript.tex:292` | McNemar test on Gold falsified ($\chi^2=1.59, p=0.2076$ vs claimed $21.64$); paired $t$-tests unexecuted | P3-ESWA-12, Phase 4.1 |
| `DISC-CRIT-06` | Critical | Group B | `scripts/reconstruct_master_manuscript.py:59` | 4/4 string replacements failed silently; unparsed Markdown bolding baked into LaTeX | P3-ESWA-05 |
| `DISC-CRIT-07` | Critical | Group A | `dl/models/banglabert_finetuned_category/config.json` | BanglaBERT class index order conflicts with `cat_le.joblib`, corrupting 80% of predictions | P2-DL-08, DISC-021 |
| `DISC-CRIT-08` | Critical | Group A | `scraped_data_global/pipeline/scraper_worker.py:49` | Scrapers overwrite 12 cols with 7 cols, permanently stripping `app_version` and metadata | DISC-001 |
| `DISC-MAJ-01` | Major | Group A | `ml/train_filtered_experiments.py:19` | Dead gold path causes `evaluate_on_gold_standard()` to silently return `(0.0, 0.0)` | DISC-008, P2-ML-16 |
| `DISC-MAJ-02` | Major | Group C | `archive/seed_pipeline_groq/src/02_*.py:50` | Seed LLM mismatch: code uses `qwen/qwen3.8-27b`, paper claims `Qwen-2.5-32B` | DISC-009, P3-ESWA-12 |
| `DISC-MAJ-03` | Major | Group A | `demo/requirements.txt:1` | Missing `nltk` in demo crashes app on launch; root/ml manifests omit 5 runtime libraries | DISC-010, DISC-011, P2-ML-20 |
| `DISC-MAJ-04` | Major | Group C | `master_unified_colab.ipynb:486` | Fictional DL claims: code is word-only BiLSTM; zero Char-CNN, GloVe, or multi-head attention | DISC-005, P2-DL-07, P3-ESWA-12 |
| `DISC-MAJ-05` | Major | Group C | `ml/models/category_voting_classifier.joblib` | Model produced by Colab Cell 7 (`[2.0, 2.5, 1.0]`) vs local `train_category.py` (`[2, 2, 1]`) | DISC-006, P2-ML-13, P3-ESWA-12 |
| `DISC-MAJ-06` | Major | Group C | `paper/eswa_latex/manuscript.tex:141` | Seed count drift ($N=4,499$ vs $4,500$); Table 4 drops 14 symbolic reviews ($4,486$) | P2-ML-12, P2-ML-18, P3-ESWA-06, P3-ESWA-07 |
| `DISC-MAJ-07` | Major | Group A | `scripts/audit_check.py` | 18 scripts broken targeting deleted docx/manuscript paths; integrity script omits Modules 2, 3, 7 | DISC-P2-22..28, P3-SCRIPTS-01..03 |
| `DISC-MAJ-08` | Major | Group A | `demo/app.py:97, 108` | `out_cat` component defined but omitted from return tuples, leaving box permanently blank | DISC-015 |
| `DISC-MAJ-09` | Major | Group C | `paper/eswa_latex/manuscript.tex:278` | CNB Macro-F1 overstated in Table 2 by +8 pp ($0.7418$ claimed vs $0.6641$ empirical CV) | Phase 4.1 |
| `DISC-MAJ-10` | Major | Group C | `paper/eswa_latex/manuscript.tex:173` | Claimed vocabulary $V \approx 50\text{k}$ vs actual $29,843$; density $d \approx 20\text{--}45$ vs actual $109.7$ | Phase 4.1 |
| `DISC-MAJ-11` | Major | Group B | `paper/eswa_latex/manuscript.tex:198, 267` | Tables 3 & 8 and Eq 8 have 0 references in prose; Table 7 captioned `"Algorithm 1:"` | P3-ESWA-02 |
| `DISC-MAJ-12` | Major | Group B | `paper/eswa_latex/references.bib:289` | Cohen (2020) and Cambria (2018) year errors; 17 uncited orphan BibTeX entries | P3-ESWA-03 |
| `DISC-MAJ-13` | Major | Group B | `paper/eswa_latex/figures/figure1..4*.png` | Figure 0 insertion offsets numbering; Figure 4 title clipped; Figure 3 quadrant misplacement | P3-ESWA-11 |
| `DISC-MAJ-14` | Major | Group B | `paper/JBA_Manuscript_Empirical_Calculations.xlsx` | Workbook missing from repository; generator script contains leaked `g600` metrics | P3-XLSX-FIG |
| `DISC-MAJ-15` | Major | Group B | `paper/telecommunications_policy_latex/manuscript.tex:213` | Eq 9 inverts false positive sign ($+FPR-1$); line 179 has 51-review deficit; stale PDFs | P3-TP-01..07 |
| `DISC-MAJ-16` | Major | Group C | `merge_and_sync_all_datasets.py:290` | Common-window cutoff conflict (`2016-08-01` vs `2016-07-28`); 21 July 2016 reviews in JSON | DISC-003, P3-HTML-02, Phase 4.1 |
| `DISC-MAJ-17` | Major | Group C | `paper/eswa_latex/manuscript.tex:242, 581` | Commercial claims of "28% higher ARPU" and "3.5x-5.0x SAC" have 0 supporting data | Phase 4.1 |
| `DISC-MAJ-18` | Major | Group A | Git working tree | 39 modified tracked files and untracked directories represent uncommitted drift | DISC-021 |
| `DISC-MAJ-19` | Major | Group A | `dl/models/bilstm_vocab.joblib` | Vocabulary unpickling crashes (`AttributeError: Vocabulary`); CLI lacks transformers | P2-DL-11 |
| `DISC-MIN-01` | Minor | Group B | `demo/app.py:114`, `manuscript.tex:32` | Informal title prefix *"With Great Reviews..."* retained in ESWA vs dropped in TP | DISC-017, P3-ESWA-04 |
| `DISC-MIN-02` | Minor | Group C | `paper/eswa_latex/manuscript.tex:141-153` | Table 1 deployed percentages sum to $100.1\%$ vs unrounded $100.0000\%$ | Phase 4.1 |
| `DISC-MIN-03` | Minor | Group C | `paper/eswa_latex/manuscript.tex:309-316` | Table 3 confusion matrix typographical errors in $\mathcal{C}_1$ and $\mathcal{C}_5$ precision and F1 | P3-ESWA-07, Phase 4.1 |
| `DISC-MIN-04` | Minor | Group C | `paper/eswa_latex/manuscript.tex:258, 629` | Line 258 claims sentiment agreement $81.0\%$ vs true $91.00\%$ used in PABAK ($0.8650$) | Phase 4.1 |
| `DISC-MIN-05` | Minor | Group C | `paper/eswa_latex/manuscript.tex:509-516` | CS2 reports $+6.95$ Gen ($57.4\%$) vs Table 6 / Fig 4 ($+15.54$, $+10.33$ Gen, $66.5\%$) | P3-ESWA-09, Phase 4.1 |
| `DISC-MIN-06` | Minor | Group A | `merge_and_sync_all_datasets.py:317` | Summary JSON schema divergence (omits vs includes sentiment counts) | DISC-004 |
| `DISC-MIN-07` | Minor | Group A | `dl/reports/results.txt:4` | Stale DL report from commit `60cf0f4` cites obsolete counts and missing checkpoint | P2-DL-01 |
| `DISC-MIN-08` | Minor | Group A | `dl/telecom_voc_banglabert_finetuning_colab.ipynb:904` | Cell 10 misclassifies positive Banglish review as Negative with 94.7% confidence | P2-DL-03 |
| `DISC-MIN-09` | Minor | Group A | `data/processed/mygp_classified_reviews.csv` | Missing `operator` column causes Colab to print `"across 2 operators"` | P2-DL-02 |
| `DISC-MIN-10` | Minor | Group A | `ml/train_category.py:247` | Formatting bug duplicates mean macro-F1 instead of printing standard deviation | P2-ML-15 |
| `DISC-MIN-11` | Minor | Group A | `ml/reports/short_text_filtering_ablation_study.md:12` | Table ($0.6737 \to 0.7318$) contradicts prose ($0.6781 \to 0.7436$) with broken LaTeX | P2-ML-17 |
| `DISC-MIN-12` | Minor | Group A | `ml/language_detector.py:153` | Fallthrough `elif english_ratio >= 0.60` lowers English threshold from 70% to 60% | P2-ML-19 |
| `DISC-MIN-13` | Minor | Group A | `ml/reports/global_language_distribution.md:3` | Prose claims 2016–2026, but underlying JSON and data span 2014–2026 | P2-ML-20 |
| `DISC-MIN-14` | Minor | Group A | `demo/app.py:67` | UI banner claims model was trained on 655,649 reviews instead of 4,500 seed reviews | DISC-016 |
| `DISC-MIN-15` | Minor | Group A | `README.md:416` | Line 416 states BL NSS `+53.1%` vs Section 1 Scorecard `+53.0%` | DISC-018 |
| `DISC-MIN-16` | Minor | Group A | `README.md:20` | README badge displays Category Kappa $\kappa = 0.77$ only, omitting Sentiment Kappa | DISC-019 |
| `DISC-MIN-17` | Minor | Group A | `TODO.txt:63` | Stale "398k corpus" reference; Web Demo task marked open despite existing demo | DISC-020 |
| `DISC-MIN-18` | Minor | Group B | `paper/index.html` | HUD claims 3,206 words vs 3,843 actual; 9 tab-escaped math blocks corrupt KaTeX | P3-HTML-01..04 |
| `DISC-HYG-01` | Hygiene | Group A | `scraped_data_global/pipeline/run_parallel_scrapers.py:22` | Hardcoded POSIX interpreter path `dl/.venv/bin/python` fails on Windows | DISC-002 |
| `DISC-HYG-02` | Hygiene | Group A | `requirements.txt:36-37` | Declares unused packages `torchvision` and `torchaudio` | DISC-012 |
| `DISC-HYG-03` | Hygiene | Group A | `demo/requirements.txt:2` | Version specifier floor conflict for scikit-learn (`>=1.3.0` vs `>=1.4.0`) | DISC-013 |
| `DISC-HYG-04` | Hygiene | Group B | `scripts/generate_two_panel_figure.py:171` | Saves modern era figure without updating 2020-2026 alias, breaking parity | DISC-014 |
| `DISC-HYG-05` | Hygiene | Group A | `scraped_data_global/pipeline/scraper_worker.py:33` | Hardcoded `country="us"` and `lang="en"`; 1 duplicate `review_id` row in Robi CSV | P1-EVID-01 |
| `DISC-HYG-06` | Hygiene | Group A | `banglabert_finetuned_models.zip` | Zip archive retains pre-patch `LABEL_0..` in `config.json` | P2-DL-09 |
| `DISC-HYG-07` | Hygiene | Group A | `dl/train_bilstm_category.py:311` | Vocabulary JSON missing; `+1` padding calculation off-by-one | P2-DL-10 |
| `DISC-HYG-08` | Hygiene | Group C | `data/gold_set/calculate_agreement.py:13` | Author names de-anonymized in script; `[BLIND_106]` violates rulebook | P2-GOLD-21 |
| `DISC-HYG-09` | Hygiene | Group A | `scripts/*.sh` | Windows CRLF endings break POSIX bash execution; ignored by encoding validator | DISC-P2-30 |
| `DISC-HYG-10` | Hygiene | Group A | `scripts/validate-skills.ps1` | CWD-relative paths cause silent false-positive pass; unanchored regexes | DISC-P2-29, 31, 32 |

---

*End of Canonical Discrepancy Catalog (`.gsd/DISCREPANCY_REPORT.md`)*
