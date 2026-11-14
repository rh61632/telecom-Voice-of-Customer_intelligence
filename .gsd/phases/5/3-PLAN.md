---
phase: 5
plan: 3
wave: 2
depends_on:
  - 5.1
  - 5.2
files_modified:
  - README.md
  - TODO.txt
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "README.md features dual Cohen's Kappa badges for Sentiment (κ = 0.58) and Category (κ = 0.77)"
    - "README.md line 120 displays 2016 (Aug–Dec) volumes as GP=438, Robi=126, BL=744 with +45.3% NSS and 63.2% positive reviews"
    - "README.md line 416 displays Banglalink Common Period NSS as +53.0%"
    - "README.md lines 432-433 display 122 Months and 41 Months matching canonical common duration"
    - "README.md directory tree includes sync_post_classification.py, evaluate_nss_stability_and_shocks.py, and demo/"
    - "README.md Section 9 mentions interactive Gradio web demo and fixes stray math delimiters"
    - "README.md strictly avoids academic paper references per commit 4d5aaad"
    - "TODO.txt fixes zip filename, anonymizes annotator filenames, corrects seed count to N=4,500, updates corpus volume to 655.6k, and marks demo completed locally"
  artifacts:
    - "README.md with empirical scorecards, dual badges, and verified tables"
    - "TODO.txt with updated task status and accurate filenames"
---

# Plan 5.3: Documentation & Roadmap Remediation (README.md & TODO.txt)

## Objective
Reconcile all empirical scorecard statistics, badges, 2016 volume counts, month counts, directory trees, and demo wording in `README.md` while keeping academic paper references strictly out of `README.md` per commit `4d5aaad`, and update `TODO.txt` to fix model archive filenames, anonymize gold annotation references, correct seed counts to `N=4,500`, and mark local Gradio demo implementation as completed.

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/DECISIONS.md` (`ADR-002`, `ADR-003`)
- `.gsd/phases/5/RESEARCH.md`
- `README.md`
- `TODO.txt`
- `scraped_data_global/classified/common_duration_summary.json`
- `scraped_data_global/classified/yearly_intelligence_trends.json`

## Tasks

<task type="auto">
  <name>Reconcile README.md badges, scorecards, longitudinal tables, and directory tree</name>
  <files>
    README.md
  </files>
  <action>
    In `README.md`:
    1. Dual Inter-Annotator Reliability Badges (`DISC-MIN-16`):
       Update badge line 20 to present both Sentiment Kappa and Category Kappa:
       ```markdown
       [![Sentiment Reliability: Cohen's Kappa](https://img.shields.io/badge/Sentiment%20Kappa-%CE%BA%20%3D%200.58%20(Moderate)-blueviolet.svg)](data/gold_set/gold_standard_evaluation_report.md)
       [![Category Reliability: Cohen's Kappa](https://img.shields.io/badge/Category%20Kappa-%CE%BA%20%3D%200.77%20(Substantial)-blueviolet.svg)](data/gold_set/gold_standard_evaluation_report.md)
       ```
    2. Year 2016 Trajectory Table Row (line 120) (`DISC-MAJ-16`):
       Under the canonical August 1, 2016 cutoff (`N=655,649`), update the 2016 row from:
       ```markdown
       | **2016** *(Jul–Dec)* | **+2.5%** (441) | **-57.9%** (126) | **+46.3%** (762) | Early app deployment; Robi experienced high negative sentiment (72.2% negative), while Banglalink launched with 63.8% positive reviews. |
       ```
       to:
       ```markdown
       | **2016** *(Aug–Dec)* | **+2.5%** (438) | **-57.9%** (126) | **+45.3%** (744) | Early app deployment; Robi experienced high negative sentiment (72.2% negative), while Banglalink launched with 63.2% positive reviews. |
       ```
       *(Counts 438, 126, 744 match `yearly_intelligence_trends.json` and eliminate the 21 July 2016 reviews).*
    3. Banglalink Scorecard Consistency (line 416) (`DISC-MIN-15`):
       Update line 416 to match Section 1 Scorecard (line 52) and `common_duration_summary.json:38` (`53.04`):
       Change `* **Common Period NSS:** \`+53.1%\` (137,131 reviews)` to `* **Common Period NSS:** \`+53.0%\` (137,131 reviews)`.
    4. Month Count Consistency (lines 432-433):
       Change `(123 Months)` to `(122 Months)` and `(42 Months)` to `(41 Months)` (matching lines 97 and 107 for the August 2016 – September 2026 common duration window).
    5. Directory Tree Completion (lines 478-484):
       - In `scraped_data_global/pipeline/`, add `sync_post_classification.py` and `evaluate_nss_stability_and_shocks.py`.
       - Add `demo/` with `app.py` and `requirements.txt` to the directory tree.
    6. Section 9 Roadmap Text (line 590):
       Change `interactive Streamlit web demos` to `interactive Gradio web demo`, and clean up stray `$` characters:
       ```markdown
       For active tracking of deferred milestones, model checkpoint hosting on Hugging Face Model Hub, and interactive Gradio web demo, see **[TODO.txt](TODO.txt)**. Multi-annotator reliability verification (Cohen's Kappa κ = 0.5762 on Sentiment, κ = 0.7694 on Categories) is completed and documented in [`gold_standard_evaluation_report.md`](data/gold_set/gold_standard_evaluation_report.md).
       ```
    7. Preservation of Academic Paper Boundary (commit `4d5aaad`):
       Strictly keep academic paper titles, ESWA journal references, and peer-review text OUT of `README.md`. Keep the existing `@misc` bibtex citation at line 599.
    
    AVOID: Altering the validated scorecard metrics (+64.9%, +65.9%, +53.0%, total 655,649).
    AVOID: Re-introducing academic journal references or arXiv/ESWA manuscript text into `README.md`.
  </action>
  <verify>
    python -c "readme = open('README.md', encoding='utf-8').read(); assert '+53.0%' in readme and '+53.1%' not in readme, 'Banglalink scorecard mismatch'; assert 'Sentiment Kappa' in readme and 'Category Kappa' in readme, 'Dual kappa badges missing'; assert '(438)' in readme and '(744)' in readme and '(441)' not in readme, '2016 table volume mismatch'; assert '122 Months' in readme and '123 Months' not in readme, 'Month count mismatch'; assert 'Gradio' in readme, 'Gradio demo wording missing'; assert 'Expert Systems with Applications' not in readme, 'Paper reference leaked into README'; assert 'sync_post_classification.py' in readme, 'sync script missing from tree'; print('Task 1 verified: README.md empirical figures, badges, and layout confirmed.')"
  </verify>
  <done>
    `README.md` includes dual Kappa badges, +53.0% Banglalink NSS, August–December 2016 counts 438/126/744, 122 months, complete tree, Gradio wording, and zero paper references.
  </done>
</task>

<task type="auto">
  <name>Update TODO.txt filenames, corpus volume, seed count, and demo task status</name>
  <files>
    TODO.txt
  </files>
  <action>
    In `TODO.txt`:
    1. Correct Model Checkpoint Zip Name (lines 16, 32) (`DISC-MIN-17`):
       Change `banglabert_finetuned_models (1).zip` to `banglabert_finetuned_models.zip` (matching actual root archive name).
    2. Anonymize Annotator Filenames (lines 49-50):
       Change:
       - `data/gold_set/blind_annotation_300_ratul.csv` -> `data/gold_set/blind_annotation_300_annotator1.csv`
       - `data/gold_set/blind_annotation_200_friend.csv` -> `data/gold_set/blind_annotation_200_annotator2.csv`
    3. Correct Seed Dataset Count (line 61):
       Change `Full-dataset model (N = 4,499)` to `Full-dataset model (N = 4,500)` (matching actual seed corpus).
    4. Update Corpus Volume References (lines 63, 69):
       Replace stale references to `398k production corpus` and `398k corpus` with `655.6k common-window production corpus` and `661.2k master corpus`.
    5. Update Web Demo Task Status (Section 4, lines 76-89):
       Update status to:
       ```text
       --------------------------------------------------------------------------------
       4. INTERACTIVE LIVE WEB DEMO (GRADIO ON HUGGING FACE SPACES) [COMPLETED LOCALLY]
       --------------------------------------------------------------------------------
       Status: COMPLETED LOCALLY (Gradio app in demo/app.py with demo/requirements.txt);
               Hugging Face Spaces deployment pending public account configuration.
       ```
    
    AVOID: Modifying future research roadmap items in Section 5 (calibration curves) or Section 6 (refresh cadence).
    USE: Exact filenames matching disk and anonymized naming conventions.
  </action>
  <verify>
    python -c "todo = open('TODO.txt', encoding='utf-8').read(); assert 'banglabert_finetuned_models.zip' in todo and 'banglabert_finetuned_models (1).zip' not in todo, 'Zip filename not updated'; assert 'blind_annotation_300_annotator1.csv' in todo and '_ratul.csv' not in todo, 'Annotator 1 not anonymized'; assert 'blind_annotation_200_annotator2.csv' in todo and '_friend.csv' not in todo, 'Annotator 2 not anonymized'; assert 'N = 4,500' in todo and 'N = 4,499' not in todo, 'Seed count mismatch'; assert '398k' not in todo, 'Stale 398k reference remains'; assert 'COMPLETED LOCALLY' in todo, 'Demo status not updated'; print('Task 2 verified: TODO.txt updated and verified.')"
  </verify>
  <done>
    `TODO.txt` reflects actual zip filename, anonymized annotator filenames, N=4,500 seed count, 655.6k/661.2k corpus, and local completion of Gradio web demo.
  </done>
</task>

</tasks>

## Must-Haves
After all tasks complete, verify:
- [ ] `README.md` features dual Kappa badges (Sentiment 0.58, Category 0.77)
- [ ] `README.md` displays `+53.0%` for Banglalink Common Period NSS
- [ ] `README.md` 2016 table row reports `*(Aug–Dec)*` with counts `(438)`, `(126)`, `(744)`
- [ ] `README.md` reports `(122 Months)` and `(41 Months)` for duration spans
- [ ] `README.md` contains zero academic paper / ESWA journal references (per commit `4d5aaad`)
- [ ] `TODO.txt` references `banglabert_finetuned_models.zip` and anonymized gold filenames
- [ ] `TODO.txt` marks Web Demo as `[COMPLETED LOCALLY]` and replaces `398k` with `655.6k`/`661.2k`

## Success Criteria
- [ ] Both tasks verified passing with single-command PowerShell checks
- [ ] Must-haves confirmed
- [ ] Zero unsolicited git commits generated (`ADR-003`)
