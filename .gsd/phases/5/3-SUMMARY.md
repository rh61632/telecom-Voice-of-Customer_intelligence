# Plan 5.3 Summary: Documentation & Roadmap Remediation (README.md & TODO.txt)

## Summary

Successfully reconciled all empirical scorecard statistics, badges, 2016 volume counts, month counts, directory trees, and demo wording in `README.md` while keeping academic paper references strictly out of `README.md` per commit `4d5aaad`, and updated `TODO.txt` to fix model archive filenames, anonymize gold annotation references, correct seed counts to `N=4,500`, update corpus volume references to `655.6k` / `661.2k`, and mark the local Gradio demo implementation as completed.

## Tasks Completed

| Task | Description | Status | Evidence |
|---|---|---|---|
| Task 1 | Reconcile `README.md` badges, scorecards, longitudinal tables, and directory tree | Complete | Verified dual Cohen's Kappa badges (`Sentiment Kappa κ = 0.58`, `Category Kappa κ = 0.77`), 2016 `(Aug–Dec)` row counts (GP: 438, Robi: 126, BL: 744, BL NSS +45.3%, 63.2% positive), Banglalink scorecard common period NSS aligned to `+53.0%`, duration spans aligned to `122 Months` and `41 Months`, pipeline tree completed with `sync_post_classification.py` and `evaluate_nss_stability_and_shocks.py`, `demo/` tree added, Gradio web demo wording updated, and zero academic paper references present per commit `4d5aaad`. |
| Task 2 | Update `TODO.txt` filenames, corpus volume, seed count, and demo task status | Complete | Verified model archive filename corrected to `banglabert_finetuned_models.zip` (dropped stray ` (1)`), gold annotator filenames anonymized to `blind_annotation_300_annotator1.csv` and `blind_annotation_200_annotator2.csv`, seed count updated to `N = 4,500`, stale `398k` corpus references replaced with `655.6k common-window production corpus` and `661.2k master corpus`, and Section 4 Web Demo marked `[COMPLETED LOCALLY]`. |

## Verification Details

1. **README.md Verification:**
   ```powershell
   python -c "readme = open('README.md', encoding='utf-8').read(); assert '+53.0%' in readme and '+53.1%' not in readme, 'Banglalink scorecard mismatch'; assert 'Sentiment Kappa' in readme and 'Category Kappa' in readme, 'Dual kappa badges missing'; assert '(438)' in readme and '(744)' in readme and '(441)' not in readme, '2016 table volume mismatch'; assert '122 Months' in readme and '123 Months' not in readme, 'Month count mismatch'; assert 'Gradio' in readme, 'Gradio demo wording missing'; assert 'Expert Systems with Applications' not in readme, 'Paper reference leaked into README'; assert 'sync_post_classification.py' in readme, 'sync script missing from tree'; print('Task 1 verified: README.md empirical figures, badges, and layout confirmed.')"
   ```
   *Result:* Clean exit code 0 (`Task 1 verified: README.md empirical figures, badges, and layout confirmed.`).

2. **TODO.txt Verification:**
   ```powershell
   python -c "todo = open('TODO.txt', encoding='utf-8').read(); assert 'banglabert_finetuned_models.zip' in todo and 'banglabert_finetuned_models (1).zip' not in todo, 'Zip filename not updated'; assert 'blind_annotation_300_annotator1.csv' in todo and '_ratul.csv' not in todo, 'Annotator 1 not anonymized'; assert 'blind_annotation_200_annotator2.csv' in todo and '_friend.csv' not in todo, 'Annotator 2 not anonymized'; assert 'N = 4,500' in todo and 'N = 4,499' not in todo, 'Seed count mismatch'; assert '398k' not in todo, 'Stale 398k reference remains'; assert 'COMPLETED LOCALLY' in todo, 'Demo status not updated'; print('Task 2 verified: TODO.txt updated and verified.')"
   ```
   *Result:* Clean exit code 0 (`Task 2 verified: TODO.txt updated and verified.`).

3. **Consolidated Must-Haves Verification:**
   ```powershell
   python -c "
   readme = open('README.md', encoding='utf-8').read()
   assert 'Sentiment Kappa' in readme and '0.58' in readme
   assert 'Category Kappa' in readme and '0.77' in readme
   assert '+53.0%' in readme and '+53.1%' not in readme
   assert '(438)' in readme and '(126)' in readme and '(744)' in readme and '(441)' not in readme
   assert '122 Months' in readme and '41 Months' in readme
   assert 'sync_post_classification.py' in readme and 'evaluate_nss_stability_and_shocks.py' in readme
   assert 'demo/' in readme and 'app.py' in readme
   assert 'Gradio' in readme
   assert 'Expert Systems with Applications' not in readme and 'ESWA' not in readme

   todo = open('TODO.txt', encoding='utf-8').read()
   assert 'banglabert_finetuned_models.zip' in todo and 'banglabert_finetuned_models (1).zip' not in todo
   assert 'blind_annotation_300_annotator1.csv' in todo and '_ratul.csv' not in todo
   assert 'blind_annotation_200_annotator2.csv' in todo and '_friend.csv' not in todo
   assert 'N = 4,500' in todo and 'N = 4,499' not in todo
   assert '398k' not in todo
   assert 'COMPLETED LOCALLY' in todo

   print('ALL MUST-HAVES EMPIRICALLY CONFIRMED!')
   "
   ```
   *Result:* Clean exit code 0 (`ALL MUST-HAVES EMPIRICALLY CONFIRMED!`).

## Discrepancies Closed

- **`DISC-MIN-15`**: Scorecard discrepancy for Banglalink NSS (`+53.1%` vs canonical `+53.0%`).
- **`DISC-MIN-16`**: Single Cohen's Kappa badge in `README.md` replaced with dual badges for Sentiment (κ = 0.58) and Category (κ = 0.77).
- **`DISC-MAJ-16`**: 2016 volume table row in `README.md` reporting pre-cutoff 441 and 762 reviews updated to canonical August–December counts 438 and 744.
- **`DISC-MIN-17`**: Model checkpoint zip filename containing browser duplicate suffix `banglabert_finetuned_models (1).zip` corrected to `banglabert_finetuned_models.zip`.

## Deviations from Plan

None.

## Git Commits

None (`commits: none (ADR-003)`). Working tree preserved for staged inspection.
