---
phase: 3
plan: 2
wave: 2
depends_on:
  - "1-PLAN.md"
files_modified:
  - .gsd/phases/3/evidence/02_eswa_internal_contradictions_and_reconstruction_drift.md
  - .gsd/phases/3/evidence/02_eswa_figures_and_codebase_claims_audit.md
  - .gsd/phases/3/2-SUMMARY.md
autonomous: true
user_setup: []

must_haves:
  truths:
    - "Silent failure of 4 string replacements in scripts/reconstruct_master_manuscript.py against manuscript_base_1506.tex is documented with exact line numbers and clobbered fixes"
    - "Internal sample size, cohort arithmetic, and Table 3/4/5/6 contradictions (N=4,500 vs 4,499 vs 4,486; Table 3 precision/F1 typos; Table 5 overlapping 134M; Table 6 vs Case Studies 1 and 2) are empirically cataloged"
    - "Embedded PNG visual defects (Figure 1-4 hardcoded title offset due to Figure 0 insertion, Figure 4 title right-edge clipping, Figure 3 quadrant prevalence denominator mismatch) are documented"
    - "Contradictions between ESWA paper claims and live codebase/models/data (seed LLM Qwen model name, missing ZWNJ/lemmatization, BiLSTM GloVe/attention fiction, BanglaBERT hyperparameters, missing t-tests/McNemar, gold-set counts/agreement, 7 fabricated shocks) are documented"
  artifacts:
    - ".gsd/phases/3/evidence/02_eswa_internal_contradictions_and_reconstruction_drift.md"
    - ".gsd/phases/3/evidence/02_eswa_figures_and_codebase_claims_audit.md"
    - ".gsd/phases/3/2-SUMMARY.md"
  key_links:
    - "Reconstruction drift links scripts/reconstruct_master_manuscript.py and scripts/build_full_eswa_paper.py to paper/eswa_latex/manuscript.tex"
    - "Paper claim contradictions link paper/eswa_latex/manuscript.tex to Phase 1/Phase 2 model and data pipeline findings"
---

# Plan 3.2: ESWA Internal Contradictions, Pipeline Reconstruction Drift, Figure Defects & Model/Data Claims Audit

<objective>
Audit internal contradictions within `paper/eswa_latex/` and cross-check manuscript claims against the live codebase, serialized models, and data reports under ADR-001 (strictly read-only on project/paper/data files outside `.gsd/`; zero git commits). Empirically trace how `scripts/reconstruct_master_manuscript.py` clobbered earlier fixes via silent replacement misses, calculate exact arithmetic errors across Tables 3, 4, 5, and 6, visually audit embedded PNG figures for numbering shifts, title clipping, and quadrant denominator mismatches, and catalog all paper-vs-codebase contradictions (seed LLM, preprocessing, BiLSTM/BanglaBERT architectures, gold-set consensus, and 7 ungrounded shocks).
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- .gsd/REQUIREMENTS.md
- .gsd/ROADMAP.md
- .gsd/DECISIONS.md
- .gsd/phases/3/RESEARCH.md
- .gsd/phases/1/1-SUMMARY.md
- .gsd/phases/1/2-SUMMARY.md
- .gsd/phases/2/1-SUMMARY.md
- .gsd/phases/2/2-SUMMARY.md
- paper/eswa_latex/manuscript.tex
- paper/eswa_latex/manuscript_twocolumn.tex
- paper/eswa_latex/manuscript_base_1506.tex
- paper/eswa_latex/apply_full_review_fixes.py
- scripts/reconstruct_master_manuscript.py
- scripts/build_full_eswa_paper.py
- paper/eswa_latex/figures/figure0_system_architecture.png
- paper/eswa_latex/figures/figure1_monthly_nss_trajectory.png
- paper/eswa_latex/figures/figure2_yearly_leadership_strip.png
- paper/eswa_latex/figures/figure3_priority_matrix.png
- paper/eswa_latex/figures/figure4_banglalink_reversal_decomposition.png
- scraped_data_global/classified/nss_stability_and_shocks_summary.json
- scraped_data_global/classified/yearly_intelligence_trends.json
- data/gold_set/calculate_agreement.py
- ml/reports/category_classification_report.md
- dl/reports/banglabert_finetuning_report.txt
- dl/README.md
</context>

<tasks>

<task type="auto">
  <name>Audit ESWA internal contradictions, silent reconstruction clobbering, and tabular arithmetic defects</name>
  <files>
    paper/eswa_latex/manuscript.tex
    paper/eswa_latex/manuscript_twocolumn.tex
    paper/eswa_latex/manuscript_base_1506.tex
    paper/eswa_latex/apply_full_review_fixes.py
    scripts/reconstruct_master_manuscript.py
    scripts/build_full_eswa_paper.py
    .gsd/phases/3/evidence/02_eswa_internal_contradictions_and_reconstruction_drift.md
  </files>
  <action>
    Perform an exhaustive read-only audit of internal text, table, equation, and reconstruction inconsistencies:
    1. Audit the pipeline reconstruction drift and silent failure of `.replace()` calls:
       - Inspect `scripts/reconstruct_master_manuscript.py:59-61,135-137,139-146,148-150`.
       - Test each of the four `.replace()` targets against `paper/eswa_latex/manuscript_base_1506.tex` (lines 275, 394, 432, 434-442) and empirically demonstrate that all 4 replacements silently failed to match due to subtle whitespace and formatting divergences.
       - Document how this silent failure preserved un-fixed base prose alongside patched tables from `scripts/build_full_eswa_paper.py`, clobbering earlier manual fixes from `apply_full_review_fixes.py`.
    2. Audit seed sample size and cohort arithmetic contradictions:
       - Contrast prose claims of `N = 4,500` (1,500 per operator) in lines 153, 254, 261 against `N = 4,499` (General = 2,730) in Table 1 (lines 149, 153), Table 2 (lines 266, 292), Table 3 (lines 316, 321), and Section 4.4 / Table 4 (lines 332, 357, 362).
       - In Table 4 (`tab:linguistic_benchmark`, lines 353-357), demonstrate that the sub-cohort counts sum to `1,091 + 390 + 3,005 = 4,486` (and `24.2% + 8.7% + 66.8% = 99.7%`), contradicting the reported total `4,499` (`100.0%`).
       - Document that Table 4 caption promises `"5-Fold Stratified Cross-Validation vs. Production Model"` but production model columns are omitted.
    3. Audit Table 3 (`tab:perclass`) arithmetic and reporting errors:
       - Recompute class metrics from the confusion matrix rows: show that $\mathcal{C}_1$ (App Login) column sum is 407 (400 TP, 7 FP), yielding true Precision = `400/407 = 0.9828` and F1 = `0.9913`, whereas Table 3 line 309 prints Precision = `0.9528` and F1 = `0.9912` (note harmonic mean of 0.9528 and 1.0 is 0.9758).
       - Show $\mathcal{C}_5$ Precision is printed as `0.9993` despite `2687/2687 = 1.0000`, and Macro Average Precision `0.9717` is computed from the erroneous values instead of `0.9779`.
       - Confirm Table 3 is never referenced anywhere in manuscript text.
    4. Audit Table 5 (`tab:eras`) window overlap and Era NSS contradictions:
       - Demonstrate that Table 5 lines 415-421 defines overlapping windows: `2018–2020 (36M)` and `2020–2022 (36M)`, whose month counts sum to `17 + 36 + 36 + 45 = 134` months (contradicting the 122-month corpus duration).
       - Compare Table 5 Era NSS numbers (`Era 1: GP -18.42, Robi -14.28, BL -22.15`; `Era 4: GP +41.20, Robi +36.85, BL +48.90`) against Section 5.1 prose lines 397-400 (`Era 1: GP -53.2, BL -55.8, Robi -57.9`; `Era 4: BL +40.1 to +81.9, Robi +78.6`).
    5. Audit Table 6 (`tab:shocks`) vs Case Study 1, Case Study 2, and feature/throughput claims:
       - Contrast Table 6 lines 451-452 (BL v11.8.0 crash in `2024-04`, `-11.2`, Login `-8.7`; v11.9.1 recovery in `2024-05`, `+32.8`, Login `+13.7`) with Case Study 1 line 506 (stating BL crashed in **May 2024** by `-32.8` from `+65.2` to `+32.4`, Login `-18.7`, then rebounded `+32.8`, Login `+17.8`).
       - Contrast Table 6 line 460 (BL `2026-01` `+15.5`, tech remediation `+5.21`, praise `+10.33`) with Case Study 2 lines 513-516 (`+6.95` General `57.4%` vs `42.6%` tech, omitting Billing `+0.36`).
       - Document feature N-gram contradictions: Eq (2) line 118 & Table 2 CNB/LR lines 278-279 (`Char (2–5) + Word (1–3)`) vs Table 2 Hero Ensemble line 282 & Section 4.4 line 365 (`Word (1–2) + Char (3–5)`).
       - Document latency/throughput contradictions: `1.42 ms/review` in line 282 (implies `704 rev/s`, `1000/1.42`) vs stated `450 reviews/sec` (which corresponds to `2.22 ms`, as in `update_paper.py:145`).
       - Document Section 6.1 canary contradiction: adaptive window `W in [30, 100]` reviews (lines 536, 550) vs Decision Rule 3 line 528 claiming `"initial 5% phased rollout"`.
       - Document unreferenced labels: `tab:perclass` (Table 3), `tab:decision_matrix`/`tab:executive_matrix` (Table 8), and `eq:shock_threshold` (Equation 8), plus Table 7 captioned `Algorithm 1:`.
    6. Save findings to `.gsd/phases/3/evidence/02_eswa_internal_contradictions_and_reconstruction_drift.md`.

    AVOID: Modifying any `.tex` file or running mutating scripts.
    USE: Read-only Python verification checks that inspect lines, compute arithmetic, and test string matching.
  </action>
  <verify>
    python -c "import pathlib; p = pathlib.Path('.gsd/phases/3/evidence/02_eswa_internal_contradictions_and_reconstruction_drift.md'); assert p.exists() and p.stat().st_size > 1000, f'File missing or too small: {p}'; print('Internal contradictions evidence verified successfully')"
  </verify>
  <done>
    `.gsd/phases/3/evidence/02_eswa_internal_contradictions_and_reconstruction_drift.md` exists and contains empirical proof of the 4 failed string replacements, exact N=4500 vs 4499 vs 4486 citations, Table 3 math recomputations, Table 5 month sum of 134M, and Table 6 vs Case Study contradictions.
  </done>
</task>

<task type="auto">
  <name>Audit embedded figures vs prose/captions and cross-check paper claims against codebase, models, and data reports</name>
  <files>
    paper/eswa_latex/figures/figure0_system_architecture.png
    paper/eswa_latex/figures/figure1_monthly_nss_trajectory.png
    paper/eswa_latex/figures/figure2_yearly_leadership_strip.png
    paper/eswa_latex/figures/figure3_priority_matrix.png
    paper/eswa_latex/figures/figure4_banglalink_reversal_decomposition.png
    paper/eswa_latex/manuscript.tex
    scraped_data_global/classified/nss_stability_and_shocks_summary.json
    scraped_data_global/classified/yearly_intelligence_trends.json
    ml/reports/category_classification_report.md
    dl/reports/banglabert_finetuning_report.txt
    dl/README.md
    data/gold_set/calculate_agreement.py
    .gsd/phases/3/evidence/02_eswa_figures_and_codebase_claims_audit.md
    .gsd/phases/3/2-SUMMARY.md
  </files>
  <action>
    Perform an exhaustive read-only audit of figure visuals/captions and paper claims vs codebase reality:
    1. Audit embedded figures visual defects and caption alignment:
       - Numbering offset defect: verify that because `figure0_system_architecture.png` was included as LaTeX `Figure 1` (`\caption{VoC-Intelligence pipeline architecture...}`), LaTeX numbers `figure1` as `Figure 2`, `figure2` as `Figure 3`, `figure3` as `Figure 4`, and `figure4` as `Figure 5`. Yet the image files themselves have hardcoded title banners reading `"Figure 1: Monthly Net Sentiment Score..."`, `"Figure 2: Yearly Telecom Leadership..."`, `"Figure 3: Category Priority Matrix..."`, and `"Figure 4: Banglalink Turnaround..."`, creating contradictory double-numbering in the PDF.
       - Figure 4 title clipping: inspect the header banner of `figure4_banglalink_reversal_decomposition.png` and document the right-edge truncation where `"(+15.54 Point"` cuts off `"s)"`.
       - Priority matrix quadrant mismatch: analyze `figure3_priority_matrix.png` vs `manuscript.tex:490-493`. The prose claims all App Login complaints fall in Quadrant I (`4.8%–11.5%`) and all Offers in Quadrant IV (`11.5%–24.0%`) based on within-operator prevalence. But `figure3` plots total-corpus prevalence (`0.78%–8.12%`), visually placing `GP App Login` (`3.88%`) into Quadrant II and `BL Offers` (`4.31%`) into Quadrant III.
    2. Audit ESWA paper claims against live codebase, models, and reports:
       - Seed LLM claim: paper claims `Qwen-2.5-32B` (line 254), whereas `archive/seed_pipeline_groq/src/02_classify_reviews_mygp.py:50` uses `model="qwen/qwen3.8-27b"` (documented in Phase 1 2-SUMMARY.md).
       - Preprocessing & lemmatization claim: paper claims ZWNJ stripping and Banglish lemmatization (`faltu`/`fal2`/`faaltu`) in lines 112-120; confirm zero ZWNJ or Banglish lemmatizers exist in `ml/`, `dl/`, or `scraped_data_global/`.
       - Model architectures & hyperparameters:
         - Paper claims BiLSTM with GloVe 300d embeddings and multi-head attention (line 280, Fig 0). Reality: code uses random 128d embeddings without GloVe, and either Bahdanau single-head attention or Char-CNN (Phase 2 1-SUMMARY.md).
         - Paper claims voting classifier weights `[2, 2, 1]`, whereas production models in Colab and Joblib files use `[2.0, 2.5, 1.0]`.
         - Paper claims BanglaBERT finetuning used `max_len=128, batch=16, epochs=5` (from `update_banglabert.py:29`), whereas `dl/finetune_banglabert.py:331-339` specifies `max_length=96, batch_size=32, epochs=4`.
         - Paper reports paired CV $t$-tests ($t(4)=4.82, 7.15, 48.3$) and McNemar $\chi^2(1)=21.64$; verify that zero scripts in the repository compute or log these statistical tests.
         - Paper reports CNB Macro-F1 `0.7418` and BanglaBERT Macro-F1 `0.7611`, neither of which appears in any `ml/` or `dl/` report (Phase 2 1-SUMMARY.md & 2-SUMMARY.md).
       - Gold standard and human agreement:
         - Paper claims $N=300$ dual-annotated, raw agreement $87.0\%$ Cat / $81.0\%$ Sent, $N=261$ consensus, PABAK $0.8650$, Rogan-Gladen $Se=0.711, Sp=0.942$.
         - Live reality in `data/gold_set/calculate_agreement.py`: Sent overlap is $N=200$ ($91.0\%$, $\kappa=0.5762$), Cat overlap is $N=196$ ($95.41\%$, $\kappa=0.7694$), consensus is $N=182$ Sent ($87.91\%$) and $N=187$ Cat ($94.12\%$). PABAK and Rogan-Gladen prevalence adjustment are completely unimplemented.
       - Table 6 Shocks vs Ground Truth:
         - Cross-check the 10 shock rows in Table 6 against `scraped_data_global/classified/nss_stability_and_shocks_summary.json`: show that 7 of the 10 shock rows do not exist in the 35 identified shocks.
         - Row 10 (BL `2026-01` `+15.5`) conflates the multi-month/annual turnaround `2025->2026` (`+15.54`) with the single monthly jump `2025-12 -> 2026-01` (`+48.15`).
       - Repository URL:
         - Paper title page line 37 specifies `https://github.com/ratulhasan/telecom-Voice-of-Customer_intelligence` whereas `git remote -v` is `https://github.com/rh61632/telecom-Voice-of-Customer_intelligence.git`.
    3. Write detailed evidence to `.gsd/phases/3/evidence/02_eswa_figures_and_codebase_claims_audit.md` and synthesize `.gsd/phases/3/2-SUMMARY.md`.

    AVOID: Re-running image generation scripts or modifying figures or code.
    USE: Read-only Python scripts inspecting PNG metadata/dimensions, JSON reports, and code lines.
  </action>
  <verify>
    python -c "import pathlib; p1 = pathlib.Path('.gsd/phases/3/evidence/02_eswa_figures_and_codebase_claims_audit.md'); p2 = pathlib.Path('.gsd/phases/3/2-SUMMARY.md'); assert p1.exists() and p1.stat().st_size > 1000, f'Evidence missing: {p1}'; assert p2.exists() and p2.stat().st_size > 1000, f'Summary missing: {p2}'; print('Figures, codebase claims, and 2-SUMMARY verified successfully')"
  </verify>
  <done>
    `.gsd/phases/3/evidence/02_eswa_figures_and_codebase_claims_audit.md` and `.gsd/phases/3/2-SUMMARY.md` exist and contain visual inspection evidence of figure numbering offsets and clipping, priority matrix quadrant calculations, and comprehensive table-by-table discrepancies between ESWA claims and codebase reality.
  </done>
</task>

</tasks>

<verification>
After all tasks, verify:
- [ ] Evidence document `02_eswa_internal_contradictions_and_reconstruction_drift.md` documents 4 silent replacement failures, N=4,500 vs 4,499 vs 4,486, Table 3 math, Table 5 134M sum, and Table 6 vs Case Study 1/2
- [ ] Evidence document `02_eswa_figures_and_codebase_claims_audit.md` documents figure numbering offset, title clipping, priority matrix quadrant mismatch, and paper vs codebase model/shock discrepancies
- [ ] Summary file `2-SUMMARY.md` is complete with all observed internal and cross-artifact discrepancies
</verification>

<success_criteria>
- [ ] All tasks verified passing with exit code 0
- [ ] Must-haves confirmed
- [ ] Zero project source, data, or paper files modified outside `.gsd/`
- [ ] Zero git commits created
</success_criteria>
