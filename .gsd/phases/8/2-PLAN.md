---
phase: 8
plan: 2
wave: 2
depends_on: ["1"]
files_modified:
  - archive/legacy_scripts/eswa_patchers/apply_full_review_fixes.py
  - archive/legacy_scripts/eswa_patchers/update_banglabert.py
  - archive/legacy_scripts/eswa_patchers/update_paper.py
  - archive/legacy_scripts/eswa_patchers/manuscript_base_1506.tex
  - archive/legacy_scripts/eswa_patchers/manuscript_twocolumn_base_1508.tex
  - archive/legacy_scripts/eswa_patchers/test_reconstruct.tex
  - archive/legacy_scripts/eswa_patchers/test_up.tex
  - archive/legacy_scripts/eswa_patchers/reconstruct_master_manuscript.py
  - archive/legacy_scripts/eswa_patchers/build_full_eswa_paper.py
  - scripts/compute_statistical_tests.py
  - scraped_data_global/classified/paper_empirical_ground_truth.json
  - scraped_data_global/classified/paper_empirical_ground_truth.md
  - paper/eswa_latex/references.bib
  - paper/eswa_latex/title_page.tex
  - paper/eswa_latex/manuscript.tex
  - scripts/sync_eswa_twocolumn.py
  - paper/eswa_latex/manuscript_twocolumn.tex
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "Brittle patchers and legacy .tex backups in paper/eswa_latex/ and scripts/ are archived to archive/legacy_scripts/eswa_patchers/ in favor of deterministic single-source manuscript generation"
    - "scripts/compute_statistical_tests.py:818 uses .get('overall_distribution', {}) to fully populate 661k global language breakdown in paper_empirical_ground_truth.json"
    - "references.bib has cohen1960coefficient:289 year set to 1960, cambria2017senticnet renamed and updated to AAAI-18 proceedings with DOI 10.1609/aaai.v32i1.11559, retains cited feinstein1990high & byrt1993bias, and prunes 13 uncited orphans (0 uncited orphan entries)"
    - "title_page.tex updates GitHub URL to rh61632, includes xurl to resolve 15.62pt overfull hbox, sets hypersetup author/title metadata, and unifies the formal title matching demo/app.py without 'With Great Reviews...' prefix"
    - "paper/eswa_latex/manuscript.tex has every reported metric, table (Tables 1-8), equation (Eqs 1-12), and case study (1 & 2) aligned to live empirical ground truth (V=29,843, 87.33% Cat / 87.44% Sent CV, N=4,500, +15.54 BL turnaround), ungrounded 28% ARPU / 3.5x-5.0x SAC / lemmatizer claims removed, unlogged Colab metrics recorded as '—' / 'GPU (Colab T4)', and contains zero raw markdown '**...**' tokens"
    - "scripts/sync_eswa_twocolumn.py generates paper/eswa_latex/manuscript_twocolumn.tex with byte-identical body parity (lines 25-end) to manuscript.tex, preserving double-blind anonymity and all 8 sections and 8 key labels"
  artifacts:
    - "archive/legacy_scripts/eswa_patchers/ containing archived patchers and stale .tex drafts"
    - "paper/eswa_latex/references.bib with corrected years, valid AAAI-18 SenticNet DOI, and zero orphan entries"
    - "paper/eswa_latex/title_page.tex with rh61632 remote, xurl package, hypersetup, and unified title"
    - "paper/eswa_latex/manuscript.tex updated with 100% empirical ground truth and zero markdown bold tokens"
    - "scripts/sync_eswa_twocolumn.py deterministic synchronization script"
    - "paper/eswa_latex/manuscript_twocolumn.tex updated with byte-identical body parity"
---

# Plan 8.2: ESWA Manuscript, BibTeX, Title Page & Patcher Architecture Remediation (REM-07)

## Objective
Remediate the active *Expert Systems with Applications* (ESWA) manuscript suite (`manuscript.tex`, `manuscript_twocolumn.tex`, `title_page.tex`, and `references.bib`). Retire brittle `.replace()` string patchers and stale `.tex` backups to `archive/legacy_scripts/eswa_patchers/`. Fix `references.bib` citation years, DOIs, and orphan entries. Update `title_page.tex` repository URL and formatting. Replace all drifted, unverified, or fabricated metrics across Sections 1–8, Tables 1–8, Equations 1–12, and Case Studies 1–2 with exact empirical ground truth from `paper_empirical_ground_truth.json`. Implement a deterministic synchronization script ensuring byte-level body parity between single-column and two-column manuscripts.

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-07`)
- `.gsd/phases/8/RESEARCH.md` (Sections 2.1, 2.2, 2.4, 3.1, 3.2)
- `scraped_data_global/classified/paper_empirical_ground_truth.json`
- `paper/eswa_latex/references.bib`
- `paper/eswa_latex/title_page.tex`
- `paper/eswa_latex/manuscript.tex`
- `paper/eswa_latex/manuscript_twocolumn.tex`
- `scripts/compute_statistical_tests.py`

## Tasks

<task type="auto">
  <name>Archive brittle patchers, fix compute_statistical_tests.py:818, and remediate references.bib & title_page.tex</name>
  <files>
    archive/legacy_scripts/eswa_patchers/apply_full_review_fixes.py
    archive/legacy_scripts/eswa_patchers/update_banglabert.py
    archive/legacy_scripts/eswa_patchers/update_paper.py
    archive/legacy_scripts/eswa_patchers/manuscript_base_1506.tex
    archive/legacy_scripts/eswa_patchers/manuscript_twocolumn_base_1508.tex
    archive/legacy_scripts/eswa_patchers/test_reconstruct.tex
    archive/legacy_scripts/eswa_patchers/test_up.tex
    archive/legacy_scripts/eswa_patchers/reconstruct_master_manuscript.py
    archive/legacy_scripts/eswa_patchers/build_full_eswa_paper.py
    scripts/compute_statistical_tests.py
    scraped_data_global/classified/paper_empirical_ground_truth.json
    scraped_data_global/classified/paper_empirical_ground_truth.md
    paper/eswa_latex/references.bib
    paper/eswa_latex/title_page.tex
  </files>
  <action>
    1. Retire brittle patchers and legacy `.tex` drafts to `archive/legacy_scripts/eswa_patchers/`:
       - Create `archive/legacy_scripts/eswa_patchers/`.
       - Move the following files from `paper/eswa_latex/`:
         - `apply_full_review_fixes.py`
         - `update_banglabert.py`
         - `update_paper.py`
         - `manuscript_base_1506.tex`
         - `manuscript_twocolumn_base_1508.tex`
         - `test_reconstruct.tex`
         - `test_up.tex`
       - Move the following scripts from `scripts/`:
         - `reconstruct_master_manuscript.py`
         - `build_full_eswa_paper.py`

    2. Fix `scripts/compute_statistical_tests.py:818`:
       - Change `json.load(f).get("language_breakdown", {})` to `json.load(f).get("overall_distribution", {})` to match key structure in `ml/reports/global_language_distribution.json`.
       - Re-run `python scripts/compute_statistical_tests.py` and confirm `scraped_data_global/classified/paper_empirical_ground_truth.json` has `global_corpus_language_distribution_661k` populated with English (77.12%), Romanized Banglish (11.27%), and Bangla (9.42%).

    3. Remediate `paper/eswa_latex/references.bib` (DISC-MAJ-12):
       - Change `cohen1960coefficient` year (:289) from `{2020}` to `{1960}`.
       - Rename and update `cambria2017senticnet` (:20-28) to `cambria2018senticnet`:
         ```bibtex
         @inproceedings{cambria2018senticnet,
           title={SenticNet 5: Discovering conceptual primitives for sentiment analysis by means of deep feature review filtering},
           author={Cambria, Erik and Poria, Soujanya and Hazarika, Devamanyu and Kwok, Kenneth},
           booktitle={Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence (AAAI-18)},
           pages={1795--1802},
           year={2018},
           doi={10.1609/aaai.v32i1.11559}
         }
         ```
       - Retain `feinstein1990high` and `byrt1993bias` (cited in Sections 4.2 & 7.2 for PABAK and the Kappa Paradox).
       - Retain `platt1999probabilistic` (cited in Section 3.2 for Platt scaling) and `landis1977measurement` (cited in Section 4.2 for Kappa interpretation).
       - Prune the 13 uncited orphan entries: `hirschman1970exit`, `smith1999model`, `parasuraman1985conceptual`, `oliver1980cognitive`, `chevalier2006effect`, `mudambi2010what`, `bitner2000technology`, `hasan2020sentiment`, `falch2018regulation`, `guzman2014users`, `pagano2013user`, `martin2017survey`, and `kazmaier2022power` (and `qwen2024` if Groq model ID `qwen/qwen3.8-27b` cited directly). Ensure 0 uncited orphan BibTeX entries remain.

    4. Remediate `paper/eswa_latex/title_page.tex`:
       - Update repository URL at line 37: replace `https://github.com/ratulhasan/telecom-Voice-of-Customer_intelligence` with `https://github.com/rh61632/telecom-Voice-of-Customer_intelligence`.
       - Add `\usepackage{xurl}` (after `\usepackage{hyperref}`) to eliminate the `15.62 pt` overfull `\hbox` on the GitHub URL.
       - Add `\hypersetup{pdfauthor={Ratul Hasan}, pdftitle={An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling}}` to eliminate `hyperref` warnings and trailing `; ` in `pdfinfo`.
       - Set the formal title at line 14 matching `demo/app.py`: `\title{An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling}` (removing `"With Great Reviews Comes Great Responsibility: "` prefix).

    AVOID: Keeping duplicate or stale `.tex` drafts in `paper/eswa_latex/`.
    AVOID: Leaving broken DOIs or incorrect years in `references.bib`.
  </action>
  <verify>
    python -c "import pathlib, json; p_bib=pathlib.Path('paper/eswa_latex/references.bib').read_text(encoding='utf-8'); assert '1960' in p_bib and '10.1609/aaai.v32i1.11559' in p_bib, 'BibTeX missing 1960 or AAAI DOI'; assert 'hirschman1970exit' not in p_bib, 'Orphan bib entry not pruned'; p_tp=pathlib.Path('paper/eswa_latex/title_page.tex').read_text(encoding='utf-8'); assert 'rh61632' in p_tp, 'Missing rh61632 URL'; assert 'xurl' in p_tp, 'Missing xurl in title_page'; assert 'With Great Reviews' not in p_tp, 'Old title prefix remains in title_page'; gt=json.load(open('scraped_data_global/classified/paper_empirical_ground_truth.json', encoding='utf-8')); assert len(gt['table4_linguistic_subcohorts']['global_corpus_language_distribution_661k']) > 0, '661k lang breakdown empty'; print('✓ references.bib, title_page.tex, and compute_statistical_tests verified!')"
  </verify>
  <done>
    Legacy patchers archived to archive/legacy_scripts/eswa_patchers/. compute_statistical_tests.py:818 fixed and executed. references.bib and title_page.tex fully remediated.
  </done>
</task>

<task type="auto">
  <name>Full empirical remediation of paper/eswa_latex/manuscript.tex</name>
  <files>
    paper/eswa_latex/manuscript.tex
  </files>
  <action>
    Apply the complete line-by-line empirical remediation from `RESEARCH.md` Table 3.2 to `paper/eswa_latex/manuscript.tex`:

    1. **Preamble & Title (lines 1–35):**
       - Add `\hypersetup{pdfauthor={Anonymous}, pdftitle={An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling}}`.
       - Change `\doublespacing` (line 23) to `\onehalfspacing` (and ensure tight float placement `[t!]`) to reduce `manuscript.pdf` page count from 37 pages down below 35 (`<= 35`).
       - Set formal title (line 32): `\title{An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling}` (removing `"With Great Reviews Comes Great Responsibility: "` prefix).

    2. **Abstract & Section 1 (lines 36–70):**
       - Line 37: change to `87.44\% sentiment and 87.33\% category cross-validation accuracy`; retain `94.12\%` category ($N=187$) and `87.91\%` sentiment ($N=182$) blind consensus agreement; replace `450 reviews/second` with `122.4--145.2 reviews/second single-review CPU throughput` (`176.5 rps` CLI); Woolf `95\% CI: [1.83, 9.75]` + BL asymmetry footnote (`OR=10.00, p=0.0007`).
       - Line 63: replace phonetic lemmatizer / Bayesian regularization with `code-mixed text preprocessing, a calibrated soft-voting ensemble classifier, deep transformer verification anchors, and Rogan-Gladen misclassification adjustment`.

    3. **Sections 2 & 3 (lines 71–235):**
       - Line 78: cite `\citep{cambria2018senticnet, zhang2018deep}`.
       - Lines 94, 101-102: align with updated `figure0` text (code-mixed preprocessing, Rogan-Gladen prevalence calibration).
       - Lines 110-120 (Eqs 1–2): replace ZWNJ/lemmatizer formulas with actual code pipeline (`ml/train_category.py:62,90-102`, `category_voting_classifier.joblib`): whitespace/case normalization (repeated-char collapse in BiLSTM) + `FeatureUnion` $\mathbf{x}_i = [\mathbf{x}_{i,\text{word}(1-2)} \;\|\; \mathbf{x}_{i,\text{char}(3-5)}]$ (`max_features = 12,000` word + `25,000` char, `sublinear_tf=True`), noting CLI sentiment model uses `char_wb(2-5)`.
       - Lines 141-153 (Table 1 `tab:taxonomy`): General Seed $N=2{,}731$; 2-decimal Seed % = `8.89\%, 8.09\%, 4.82\%, 17.51\%, 60.69\%` (**100.00%**); 2-decimal Deployed % = `4.99\%, 2.46\%, 0.96\%, 5.04\%, 86.55\%` (**100.00%**); Note `Seed N = 4{,}500` (1,500 per operator).
       - Line 158: cite `\citep{platt1999probabilistic, niculescu2005predicting}`.
       - Line 170 (Eq 4): production voting weights $\boldsymbol{\omega} = [0.364, 0.455, 0.182]$ (`[2.0, 2.5, 1.0]` for LR, LinearSVC, CNB), noting CLI uses `[2, 2, 1]`.
       - Line 173 (Sec 3.2.1): exact fitted Category model `$V = 29{,}843$` (4,843 word + 25,000 char), empirical mean density `$d = 109.72$` (median `59.0`, range `[0, 1199]`; Sentiment CLI `$V = 18{,}027$`, `$d = 110.86$`); single-review CPU latency `8.17 ms` (`122.4 rev/sec`, or `18.2k rev/s` batched).
       - Line 205: reference `(Equation~\ref{eq:shock_threshold})`.
       - Lines 209-211 (Eq 10): move `(\ge +50\% \text{ volume growth})` out of display math into following prose or wrap in `multline` to eliminate the 32 pt overfull box.
       - Lines 221-230: explicit prevalence split `P(C_k) \ge 3.75\%` and negativity split `I(C_k) \ge 75\%` (extreme churn $\ge 85\%$ in QII).

    4. **Section 4: Experiments & Validation (lines 236–380):**
       - Lines 239-241: `48.83\%, 30.26\%, 20.92\%`, eliminate 1.10 pt overfull box with `\sloppy` or abbreviated `Grameenphone Ltd.\ (GP)`.
       - Line 249: replace `"largest longitudinal..."` claim with `"substantial longitudinal telecom text dataset spanning a decade of consumer feedback"`.
       - Lines 254-258: Groq `qwen/qwen3.8-27b`; primary blind gold set $N=300$ (Annotator 1) with dual-annotated overlap $N=200$ ($N=196$ valid category pairs); Category IRR agreement **`95.41\%`** ($187/196$, $\kappa = 0.7694$), Sentiment IRR agreement **`91.00\%`** ($182/200$, $\kappa = 0.5762$, 3-class PABAK = `0.8650`); cite `\citep{cohen1960coefficient, landis1977measurement, feinstein1990high, byrt1993bias}`; consensus subsets $N=187$ (Category) and $N=182$ (Sentiment).
       - Lines 263-293 (Table 2 `tab:model_leaderboard`): Caption `$N=4{,}500$`.
         - Dummy: `0.1511 \pm 0.0001` / `0.4584` / `60.69\% \pm 0.04\%` / `CPU (<0.01 ms)`
         - CNB: `0.6934 \pm 0.0191` / `0.8160` / `81.47\% \pm 1.37\%` / `CPU`
         - Balanced LogReg: `0.7845 \pm 0.0135` / `0.8730` / `87.16\% \pm 0.86\%` / `CPU`
         - Calibrated LinearSVC: `0.7664 \pm 0.0160` / `0.8654` / `86.91\% \pm 0.74\%` / `CPU`
         - Hero Ensemble: `0.7794 \pm 0.0146` / `0.8717` / `87.33\% \pm 0.81\%` / `CPU (8.17 ms / 122.4 rps)`
         - Hybrid BiLSTM + Attn: Feature=`128d Word Emb + 1-Head Attn`, `0.7106` / `—` / `80.84\%` / `GPU (Colab T4)`
         - BanglaBERT (Frozen): `0.6253` / `—` / `74.88\%` / `GPU (Colab T4)`
         - BanglaBERT (Fine-Tuned): `0.7624 \pm 0.0179` / `—` / `85.27\% \pm 1.14\%` / `GPU (Colab T4)`
         - Multilingual MiniLM: `0.7247` / `—` / `81.15\%` / `GPU (Colab T4)`
         - Table 2 Notes (line 292): weights `[2.0, 2.5, 1.0]`; paired $t$-tests on Category 5-fold CV (Hero vs Dummy $t(4)=85.77, p<0.0001$; vs CNB $t(4)=12.24, p=0.0003$; vs BanglaBERT $t(4)=3.07, p=0.0372$; vs LinearSVC $t(4)=1.81, p=0.1442$; vs LogReg $t(4)=-2.02, p=0.1130$); Active Gold $N=300$ McNemar tests vs star heuristic: Category Hero $91.33\%$ Acc ($94.12\%$ consensus $N=187$), Global Prod Sentiment $83.67\%$ ($87.91\%$ consensus $N=182$, McNemar $\chi^2_c=1.25, p=0.2626$; CLI Ensemble $89.00\%$/$91.21\%$, $\chi^2_c=0.97, p=0.3239$). Unlogged metrics set to `—`.
       - Lines 295-322 (Table 3 `tab:perclass`): exact full-seed $N=4,500$ performance (`paper_empirical_ground_truth.json:3049-3122`):
         - $\mathcal{C}_1$ (App Login): `0.9804 / 1.0000 / 0.9901`, row `[400, 0, 0, 0, 0]`, support `400`
         - $\mathcal{C}_2$ (Network): `0.9504 / 1.0000 / 0.9746`, row `[0, 364, 0, 0, 0]`, support `364`
         - $\mathcal{C}_3$ (Billing): `0.9909 / 1.0000 / 0.9954`, row `[0, 0, 217, 0, 0]`, support `217`
         - $\mathcal{C}_4$ (Offers): `0.9813 / 0.9987 / 0.9899`, row `[0, 0, 0, 787, 1]`, support `788`
         - $\mathcal{C}_5$ (General): `0.9996 / 0.9839 / 0.9917`, row `[8, 19, 2, 15, 2687]`, support `2,731`
         - Macro Avg: `0.9805 / 0.9965 / 0.9883`; Weighted Avg: `0.9903 / 0.9900 / 0.9900`, Total `4,500`.
       - Line 324: reference `Table~\ref{tab:perclass}` explicitly, update BanglaBERT delta (`+0.1371` Macro-F1, `74.88% -> 85.27%`), single-review CPU latency `122.4 rps` (`8.17 ms`).
       - Lines 332-365 (Table 4 `tab:linguistic_benchmark`): Add 4th row `Symbolic / Emoticons` (`N=14`, `0.3%`); update all rows:
         - Bangla (`1,091`, `24.2%`): Cat `80.11% / 0.7503`, Sent `82.68% / 0.7835`
         - Banglish (`390`, `8.7%`): Cat `85.13% / 0.7305`, Sent `79.23% / 0.7567`
         - English (`3,005`, `66.8%`): Cat `90.18% / 0.7900`, Sent `90.82% / 0.7671`
         - Symbolic (`14`, `0.3%`): Cat `100.00% / 1.0000`, Sent `92.86% / 0.4815`
         - Overall (`4,500`, `100.0%`): Cat `87.33% / 0.7794`, Sent `87.84% / 0.7823`
         - Caption: `(5-Fold Stratified Cross-Validation Across N = 4,500)`.
       - Line 367: clarify scope of unconstrained global scraped archive ($N=661,160$) vs common-window ($N=655,649$).
       - Lines 372, 377: consensus benchmarks $N=187$ (Category) and $N=182$ (Sentiment).

    5. **Sections 5 & 6: Deployment, Shocks & Case Studies (lines 381–610):**
       - Lines 397-400 (Four Eras prose): Era 1 (`17M`, GP `+8.78`, BL `+45.46`, Robi `-52.54`), Era 2 (`36M`, GP `+42.44`, Robi `+54.98`, BL `+32.82`), Era 3 (`24M`, GP `+62.69`, Robi `+66.25`, BL `+50.64`), Era 4 (`45M`, GP `+69.44`, Robi `+70.64`, BL `+63.33`).
       - Lines 403-427 (Table 5 `tab:eras`): Partition A (`17M + 36M + 24M + 45M = 122M`). Fix note (:426) to report pooled era NSS over 122 calendar months ($N=655,649$), removing the false Rogan-Gladen note.
       - Line 437: reference `Equation~(\ref{eq:shock_threshold})`.
       - Lines 439-466 (Table 6 `tab:shocks`): populate with all 10 verified rows of `top10_curated_multi_operator` (`paper_empirical_ground_truth.json:1958-2219`), with purely empirical telemetry signatures (GP `2020-04` `+31.24`, GP `2021-05` `-13.75`, GP `2021-09` `+13.57`, GP `2025-09` `-18.54`, Robi `2023-01` `-16.61`, Robi `2023-02` `+10.67`, Robi `2023-12` `+10.00`, BL `2021-05` `-16.43`, BL `2024-04` `-11.18`, BL `2024-05` `+32.78`).
       - Lines 468-478 (Contingency): replace raw markdown `**...**` tokens with `\textbf{...}`. Report pooled 35 shocks ($27/35 = 77.1\%$ vs $91/205 = 44.4\%$, $\chi^2(1)=12.83, p=0.0003$, Fisher $\text{OR}=4.23, p=0.0004$, Woolf 95% CI `[1.83, 9.75]`, Yates $\chi^2(1)=11.55, p=0.0007, \text{RR}=1.74$; non-surge $\chi^2(1)=6.38, p=0.0116, \text{OR}=3.65$). Disclose Banglalink-driven asymmetry ($20/22$ shocks, $\text{OR}=10.00, p=0.0007$).
       - Lines 488-494 (Priority Matrix): Billing (`0.78% to 1.11%` prev, `89.77% to 92.89%` neg, $\text{OR}=9.49$ `[8.64, 10.42]`), App Login (`3.88% to 8.12%` prev, `87.10% to 89.28%` neg, $\text{OR}=6.44$ `[6.18, 6.70]`), Network (`1.88% to 3.64%` prev, `74.01% to 76.37%` neg, $\text{OR}=2.50$ `[2.40, 2.61]`), Offers (`4.31% to 5.27%` prev, `50.26% to 56.62%` neg).
       - Line 506 (Case Study 1): April 2024 drop $\Delta\text{NSS} = -11.18$ (`+42.82` $\to$ `+31.63`; App Login `-8.74` pp), May 2024 rebound $\Delta\text{NSS} = +32.78$ (`+31.63` $\to$ `+64.42`; App Login `+13.73` pp, General `+17.38` pp). Disclose `51.82%` null `app_version` across Banglalink, `v11.8.0` telemetry ($N=158$ in Apr 2024, NSS `-7.59`), and `v11.9.1` telemetry ($N=905$, NSS `+71.71`).
       - Lines 509-516 (Case Study 2): Annual 2025 ($N=10,238$, NSS `+66.39`) $\to$ 2026 ($N=21,810$, NSS `+81.93`, `2.13x` volume growth) turnaround $\Delta\text{NSS} = +15.54$ pts (acute Dec 2025 $\to$ Jan 2026 jump of $+48.15$ pts). Track A (4 Technical Domains) = `+5.21` pts (`33.5%`) (`App Login +2.80`, `Network +1.07`, `Offers +0.98`, `Billing +0.36`); Track B (General Appreciation) = `+10.33` pts (`66.5%`). Remove `Toffee` and remove old unverified numbers.
       - Lines 528, 536: align canary rollout ($W \in [30, 100]$) and reference `Table~\ref{alg:canary}`.
       - Lines 538-574 (Table 7 `alg:canary`): caption `\caption{Real-Time Canary Release Gating and Automated Rollback Protocol (Algorithm 1)}`; line 550 $p_{\text{base}} = 0.0442$ (noting GP `0.0345`, Robi `0.0401`, BL `0.0725`); remove unverified simulation note.
       - Lines 579-609 (Sec 6.2 & Table 8 `tab:decision_matrix`): remove unsubstantiated `3.5x–5.0x SAC` and `28% higher ARPU` claims (`ADR-003`), replacing with qualitative CLV framing grounded in app-login shock severity ($\text{OR}=4.23$). Cite `Table~\ref{tab:decision_matrix}` and report 240-transition alert counts (`Level 1: 147`, `Level 2: 58`, `Level 3: 15`, `Level 4: 13`). Use `>{\raggedright\arraybackslash}` to clear overfull boxes.

    6. **Sections 7 & 8: Discussion & Conclusion (lines 611–668):**
       - Lines 612-617: remove duplicate `%% 7. DISCUSSION` banner.
       - Lines 627-633: active Rogan-Gladen parameters for Global Production Sentiment model $\mathrm{Se} = 0.4783, \mathrm{Sp} = 0.9711$ (CLI model $\mathrm{Se} = 0.5217, \mathrm{Sp} = 0.9747$), active gold $N=300$ / consensus $N=187$ / $N=182$. Cite `\citep{feinstein1990high, byrt1993bias}` for $\kappa = 0.5762$ vs PABAK = $0.8650$. Update Woolf CI `[1.83, 9.75]`.
       - Line 652: conclusion CV accuracy `87.33%` category and `87.44%` global production sentiment, `94.12%` category and `87.91%` sentiment consensus agreement, single-review CPU latency `5.67--8.17 ms/review` (`122.4--176.5 reviews/sec`), and Banglalink-driven shock asymmetry (`OR=4.23, p=0.0004`, Yates $\chi^2(1)=11.55, \text{RR}=1.74$).

    AVOID: Leaving any raw markdown `**...**` bold syntax in the file.
    AVOID: Reintroducing unverified commercial numbers (`28% ARPU`, `3.5x-5.0x SAC`).
  </action>
  <verify>
    python -c "import pathlib, re; m=pathlib.Path('paper/eswa_latex/manuscript.tex').read_text(encoding='utf-8'); assert '**' not in m, 'Raw markdown bold found in manuscript.tex'; assert '87.33' in m and '87.44' in m, 'Missing 87.33% / 87.44% in manuscript.tex'; assert '29,843' in m or '29{,}843' in m, 'Missing V=29843 in manuscript.tex'; assert '15.54' in m and '10.33' in m, 'Missing Case Study 2 numbers'; assert 'cambria2018senticnet' in m, 'Missing cambria2018senticnet cite'; assert 'feinstein1990high' in m, 'Missing feinstein1990high cite'; assert 'With Great Reviews' not in m, 'Old title prefix remains in manuscript.tex'; print('✓ manuscript.tex verified free of markdown and aligned with empirical ground truth!')"
  </verify>
  <done>
    manuscript.tex fully updated with verified empirical ground truth, zero raw markdown syntax, and all Section 1-8 / Table 1-8 / Eq 1-12 discrepancies resolved.
  </done>
</task>

<task type="auto">
  <name>Implement scripts/sync_eswa_twocolumn.py and sync manuscript_twocolumn.tex with byte body parity</name>
  <files>
    scripts/sync_eswa_twocolumn.py
    paper/eswa_latex/manuscript_twocolumn.tex
  </files>
  <action>
    1. Implement `scripts/sync_eswa_twocolumn.py`:
       - Reads `paper/eswa_latex/manuscript.tex`.
       - Extracts body content starting from line 25 (`\journal{Expert Systems with Applications}`) through end of file.
       - Assembles the 19-line twocolumn preamble:
         ```latex
         \documentclass[final,5p,times,twocolumn,authoryear]{elsarticle}

         %% =========================================================================
         %% PACKAGES & PREAMBLE
         %% =========================================================================
         \usepackage[T1]{fontenc}
         \usepackage{amsmath,amssymb}
         \usepackage{booktabs}
         \usepackage{array}
         \usepackage{tabularx}
         \usepackage{multirow}
         \usepackage{float}
         \usepackage{caption}
         \usepackage{graphicx}
         \usepackage{microtype}
         \usepackage{hyperref}
         \usepackage{url}
         \usepackage{xcolor}
         \usepackage{setspace}
         \setlength{\bibsep}{2pt plus 0.3ex}
         \captionsetup{skip=4pt}
         ```
       - Concatenates the twocolumn preamble with the identical manuscript body lines.
       - Writes `paper/eswa_latex/manuscript_twocolumn.tex`.
       - Validates that body lines (lines 20-end in twocolumn vs lines 25-end in single-column) match byte-for-byte.

    2. Execute `python scripts/sync_eswa_twocolumn.py`.

    3. Verify that both `manuscript.tex` and `manuscript_twocolumn.tex`:
       - Contain zero raw markdown `**...**` tokens.
       - Contain zero case-insensitive occurrences of double-blind prohibited terms: `["Ratul", "rh61632", "Leading University", "Jashore", "github.com"]`.
       - Contain all 8 required `\section{...}` headers and 8 required `\label{...}` entries.
  </action>
  <verify>
    python -c "import pathlib, re; s=pathlib.Path('paper/eswa_latex/manuscript.tex').read_text(encoding='utf-8'); t=pathlib.Path('paper/eswa_latex/manuscript_twocolumn.tex').read_text(encoding='utf-8'); assert not re.findall(r'\*\*[^*]+\*\*', s), 'Markdown in manuscript.tex'; assert not re.findall(r'\*\*[^*]+\*\*', t), 'Markdown in twocolumn.tex'; terms = ['Ratul', 'rh61632', 'Leading University', 'Jashore', 'github.com']; [assert not re.search(re.escape(term), s, re.I) for term in terms]; [assert not re.search(re.escape(term), t, re.I) for term in terms]; s_lines = s.splitlines()[24:]; t_lines = t.splitlines()[19:]; assert s_lines == t_lines, 'Body lines diverged between single-column and two-column'; print('✓ Both manuscripts verified: zero markdown, full anonymity, byte-level body parity!')"
  </verify>
  <done>
    scripts/sync_eswa_twocolumn.py written and executed. manuscript_twocolumn.tex synchronized with byte-exact body parity to manuscript.tex.
  </done>
</task>

## Must-Haves
After all tasks complete, verify:
- [ ] Brittle patchers and legacy `.tex` files are safely archived in `archive/legacy_scripts/eswa_patchers/`
- [ ] `references.bib` has 1960 for Cohen, valid AAAI-18 SenticNet DOI, and zero orphan entries
- [ ] `title_page.tex` contains rh61632 URL, xurl package, hypersetup, and unified formal title
- [ ] `manuscript.tex` has all empirical figures, tables, equations, and case studies aligned to ground truth
- [ ] `manuscript.tex` and `manuscript_twocolumn.tex` have zero raw markdown `**...**` tokens
- [ ] Both manuscripts preserve double-blind anonymity and have byte-identical body parity

## Success Criteria
- [ ] All tasks verified passing
- [ ] Must-haves confirmed
- [ ] Zero uncommitted git changes required (`ADR-003`)
