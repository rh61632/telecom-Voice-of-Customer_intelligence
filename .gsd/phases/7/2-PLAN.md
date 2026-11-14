---
phase: 7
plan: 2
wave: 2
depends_on: ["1"]
files_modified:
  - archive/legacy_scripts/README.md
  - scripts/verify_paper_complete.py
  - scripts/audit_paper_contradictions.py
  - scripts/audit_project_integrity.py
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "28 dead/broken JBA, docx, Word-COM, crop-check, and self-patcher scripts are moved cleanly out of scripts/ into archive/legacy_scripts/ with an inventory README.md"
    - "verify_paper_complete.py reports 3,713 days (2016-08-01 to 2026-09-30), 20,657 early era reviews, and 88,181 functional reviews in 4 domains"
    - "audit_paper_contradictions.py reports 88,181 functional reviews in 4 domains"
    - "scripts/audit_project_integrity.py executes all 8 modules in under 10 seconds, passing cleanly (rc=0) with strict atol=0.01 tolerances"
    - "Module 1 validates common-duration N=655,649, global N=661,160, zero review_id dups/nulls, 51 text nulls allowed, and telemetry JSON alignment"
    - "Module 2 validates Gold N=300 and N=200, zero seed overlap, IRR kappa/PABAK, consensus N=182/187, and active McNemar & Rogan-Gladen bounds"
    - "Module 3 validates all 7 core joblib models deserialize, bilstm_vocab.json has 2,864 tokens, config.json mappings align, and paper_empirical_ground_truth.json matches live seed and gold predictions"
    - "Module 4 enforces strict atol=0.01 on GP 64.85, Robi 65.91, BL 53.04, Sector 62.70, and exact additive decomposition identity across all 122 months (atol=1e-6)"
    - "Module 5 enforces 122 consecutive sector months, month_diff==1 via pd.Period arithmetic, N>=30 CLT volume floor, 240 modern transitions, 35 shocks, raw RMSSD (6.28, 5.61, 13.61), SSI (93.72, 94.39, 86.39), and surge-filtered RMSSD (5.14, 4.53, 7.56)"
    - "Module 6 verifies pooled 2x2 (27/35 vs 91/205, chi2=12.83, OR=4.23), non-surge 2x2 (14/19 vs 82/189, chi2=6.38, OR=3.65), BL asymmetry (OR=10.00, p=0.0007), Prop 1 regression (R2=0.5601), and Priority Matrix (N=88,181, chi2=11,027.60, V=0.3536)"
    - "Module 7 verifies BL Spring 2024 counterfactual telemetry (2024-03 +42.82, 2024-04 +31.63 -11.18, 2024-05 +64.42 +32.78), BL missingness 51.82%, v11.8.0 telemetry, and BL 2025->2026 annual jump (+15.54 = +10.33 Gen + +5.21 Tech)"
    - "Module 8 checks all 5 prohibited terms (Ratul, rh61632, Leading University, Jashore, github.com) across manuscript.tex, manuscript_twocolumn.tex, highlights.txt, and references.bib; validates PDF existence; emits [WARN - Pending Phase 8/9] in default mode (rc=0) and enforces hard-fail when invoked with --strict-paper"
  artifacts:
    - "archive/legacy_scripts/ containing 28 retired scripts and an inventory README.md"
    - "scripts/verify_paper_complete.py repaired with exact 3,713 days and 88,181 functional reviews"
    - "scripts/audit_paper_contradictions.py repaired with exact 88,181 functional reviews"
    - "scripts/audit_project_integrity.py completed across all 8 modules with --strict-paper support"
---

# Plan 7.2: Complete Master Integrity Audit & Repair/Retire Scripts

## Objective
Clean up the `scripts/` directory by archiving 28 obsolete, dead, or superseded scripts (JBA LaTeX/docx builders, Word-COM page checkers, crop debuggers, and script self-patchers) into `archive/legacy_scripts/` with an explanatory inventory `README.md`. Repair `scripts/verify_paper_complete.py` (updating `3,716 -> 3,713 days`, `20,678 -> 20,657 reviews`, `88,184 -> 88,181 reviews`) and `scripts/audit_paper_contradictions.py` (`88,184 -> 88,181 reviews`) in-place. Fully implement and harden all 8 modules of `scripts/audit_project_integrity.py` (restoring missing Modules 2, 3, and 7; tightening NSS `atol=0.01`; enforcing `month_diff == 1` and $N \ge 30$; validating against `paper_empirical_ground_truth.json`; and adding `--strict-paper` gate separation for Phase 8/9 paper artifacts).

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-05`)
- `.gsd/DECISIONS.md` (`ADR-002`, `ADR-003`)
- `.gsd/phases/7/RESEARCH.md`
- `scripts/audit_project_integrity.py`
- `scripts/verify_paper_complete.py`
- `scripts/audit_paper_contradictions.py`
- `scraped_data_global/classified/paper_empirical_ground_truth.json`

## Tasks

<task type="auto">
  <name>Archive 28 legacy scripts with inventory README and repair verify scripts in-place</name>
  <files>
    archive/legacy_scripts/README.md
    scripts/verify_paper_complete.py
    scripts/audit_paper_contradictions.py
  </files>
  <action>
    1. Create directory `archive/legacy_scripts/` if not present.
    2. Move the 28 identified dead/superseded scripts from `scripts/` into `archive/legacy_scripts/`:
       - JBA LaTeX/docx read-only auditors (3): `audit_check.py`, `audit_docx.py`, `find_tables.py`
       - JBA LaTeX/docx mutators (14): `apply_fixes.py`, `apply_jba_revisions.py`, `apply_peer_review_fixes.py`, `apply_reviewer_fixes_latex.py`, `build_jba_full_manuscript.py`, `build_jba_submission_docx.py`, `convert_latex_to_docx.py`, `generate_jba_latex.py`, `sync_latex_jba.py`, `test_float.py`, `test_width.py`, `update_fig_caption.py`, `build_paper_docx.py`, `build_concise_paper_docx.py`
       - Obsolete Word COM .ps1 page checkers (3): `check_pages.ps1`, `check_last_pages.ps1`, `check_exact_pages.ps1`
       - Stale crop/offset helpers (4): `check_crop.py`, `check_crop_wide.py`, `check_other_crops.py`, `test_figure1_offsets.py`
       - Script self-patchers (4): `update_audit_integrity.py`, `patch_audit_integrity.py`, `update_audit_completeness.py`, `patch_generate_global_viz.py`
    3. Create `archive/legacy_scripts/README.md` cataloging each of the 28 moved scripts, explaining why each was retired (e.g., superseded by ESWA submission pipeline, targets deleted JBA .docx/.tex files, obsolete Word COM automation, temporary crop debuggers), and noting that active production and evaluation scripts remain in `scripts/`.
    4. Repair `scripts/verify_paper_complete.py` in-place:
       - Update line 19: change reference from `3,716 days` to `3,713 days`.
       - Update line 25: change early era reviews count reference from `20,678` to `20,657`.
       - Update line 43: change total in 4 domains from `88,184` to `88,181`.
       - Cross-check against `scraped_data_global/classified/paper_empirical_ground_truth.json` if present.
    5. Repair `scripts/audit_paper_contradictions.py` in-place:
       - Update line 23: change total reviews in 4 domains from `88,184` to `88,181`.
       - Confirm execution produces 0 assertion errors.

    AVOID: Archiving scripts owned by Phase 8/9 (`reconstruct_master_manuscript.py`, `build_full_eswa_paper.py`, `generate_paper_figures.py`, `build_paper_empirical_excel.py`, etc.).
    AVOID: Introducing paper references into `README.md`.
  </action>
  <verify>
    python -c "import os; assert not os.path.exists('scripts/apply_fixes.py'), 'apply_fixes still in scripts'; assert os.path.exists('archive/legacy_scripts/apply_fixes.py'), 'apply_fixes not in archive'; assert os.path.exists('archive/legacy_scripts/README.md'), 'archive README missing'; import subprocess; subprocess.run(['python', 'scripts/verify_paper_complete.py'], check=True); subprocess.run(['python', 'scripts/audit_paper_contradictions.py'], check=True); print('✓ Script archiving and verify script repair verified!')"
  </verify>
  <done>
    All 28 legacy scripts are moved to archive/legacy_scripts/ with README.md inventory; verify_paper_complete.py and audit_paper_contradictions.py execute cleanly with 3,713 days and 88,181 functional reviews.
  </done>
</task>

<task type="auto">
  <name>Complete all 8 modules in scripts/audit_project_integrity.py with strict tolerances and --strict-paper</name>
  <files>
    scripts/audit_project_integrity.py
  </files>
  <action>
    Complete `scripts/audit_project_integrity.py` to restore all missing modules (2, 3, 7) and harden existing modules (1, 4, 5, 6, 8) to run in under 10 seconds:

    1. **Command-Line Arguments & Configuration:**
       - Support `--strict-paper` flag: in default mode, Module 8 emits visible `[WARN - Pending Phase 8/9]` on pending manuscript defects (raw `**`, PDF SHA256 sync, PDF page limits, missing Excel) and exits 0; under `--strict-paper`, pending defects cause exit 1.

    2. **Module 1 (Data Integrity):**
       - Validate `scraped_data_global/classified/all_operators_common_duration_classified.csv`:
         - Exact count: `655,649` rows (fix error message from `655670` to `655649`).
         - Operator breakdown: GP `320,140`, Robi `198,378`, BL `137,131`.
         - Date range: `2016-08-01` to `2026-09-30`.
         - Zero duplicate `review_id` values.
         - Zero nulls in `review_id`, `operator`, `review_date`, `predicted_sentiment`, `predicted_category`, `ym`.
         - Null count in `review_text` must equal exactly `51` (do not fail blindly on `df.isna()`).
       - Validate `scraped_data_global/classified/all_operators_classified_global.csv`:
         - Exact count: `661,160` rows.
         - Zero duplicate `review_id` values.
       - Validate `common_duration_summary.json` and `yearly_intelligence_trends.json`:
         - Yearly counts sum to `655,649` (`2016 = 438/126/744`).

    3. **Module 2 (Gold Set Agreement & Independence):**
       - Validate `data/gold_set/blind_annotation_300_annotator1.csv` ($N=300$, exactly 100/op) and `data/gold_set/blind_annotation_200_annotator2.csv` ($N=200$, 67 GP, 67 BL, 66 Robi).
       - Verify zero text or review ID overlap between Gold sets and seed $N=4,500$ dataset.
       - Verify IRR metrics:
         - Sentiment ($N=200$): Raw agreement `91.00%` (182/200), Cohen's $\kappa = 0.5762 \pm 0.001$, 3-class $\text{PABAK} = 0.8650$.
         - Category ($N=196$ valid pairs): Raw agreement `95.41%` (187/196), Cohen's $\kappa = 0.7694 \pm 0.001$.
       - Verify active Gold $N=300$ and consensus $N=182/187$ accuracy bounds for `ensemble_voting_classifier` ($89.00\% / 91.21\%$) and `sentiment_voting_classifier` ($83.67\% / 87.91\%$).

    4. **Module 3 (Model Deserialization, Schema Parity & Benchmark Consistency):**
       - Verify clean deserialization of all 7 core `ml/models/*.joblib`: `category_voting_classifier.joblib`, `sentiment_voting_classifier.joblib`, `ensemble_voting_classifier.joblib`, `primary_logistic_regression.joblib`, `challenger_linearsvc.joblib`, `complement_nb.joblib`, `calibrated_svc.joblib`.
       - Verify `dl/models/bilstm_vocab.json` loads via `dl.bilstm_artifacts.load_bilstm_vocab` with exactly `2,864` tokens.
       - Verify `dl/models/cat_le.joblib` has 5 alphabetical classes (for BiLSTM) and `dl/models/banglabert_finetuned_category/config.json` has `CATEGORY_LABEL_MAP` (`0: General` .. `4: Billing`).
       - Verify `scraped_data_global/classified/paper_empirical_ground_truth.json` exists and matches live full-seed evaluation (`category_voting_classifier.joblib` $N=4,500$ Acc `0.9900`, F1 `0.9883`, $V=29,843$).
       - Verify `ml/reports/linguistic_subcohort_benchmark.csv` subcohort counts sum to $N=4,500$.

    5. **Module 4 (Mathematical Invariants of NSS & Additive Decomposition):**
       - Tighten tolerance to `atol=0.01`:
         - GP: `64.85`
         - Robi: `65.91`
         - BL: `53.04` (assert `53.04`, correcting previous `53.05`)
         - Sector: `62.70`
       - Assert exact additive decomposition identity $\sum \Delta C_k = \Delta\text{NSS}$ across all 122 consecutive monthly sector transitions at `atol=1e-6`.

    6. **Module 5 (Time Series Aggregation, CLT Floor, RMSSD & Surge Filtering):**
       - Assert 122 gapless sector calendar months (`2016-08` through `2026-09`).
       - Enforce `month_diff == 1` via `pd.Period` arithmetic for all consecutive transitions (never assume row indexing).
       - In modern era (`2020-01`..`2026-09`): assert 81 months per operator, minimum monthly volume $\ge 294 \gg 30$ (CLT floor satisfied), 240 transitions, exactly 35 shocks ($|\Delta\text{NSS}| \ge 10.0$: GP 6, Robi 7, BL 22).
       - Verify raw RMSSD (GP `6.28`, Robi `5.61`, BL `13.61`), SSI (GP `93.72`, Robi `94.39`, BL `86.39`), and non-surge filtered RMSSD ($|\text{vol\_pct}| < 50\%$: GP `5.14`, Robi `4.53`, BL `7.56`).

    7. **Module 6 (Proposition 1 & 2 Statistical Tests & Priority Matrix):**
       - Verify pooled $2\times 2$ contingency: Shocks `27/35` vs Non-shocks `91/205`, $\chi^2(1) = 12.83$ (`atol=0.01`), Fisher $\text{OR} = 4.23$ (`atol=0.01`).
       - Verify non-surge $2\times 2$: Shocks `14/19` vs Non-shocks `82/189`, $\chi^2(1) = 6.38$, Fisher $\text{OR} = 3.65$.
       - Verify per-operator asymmetry: BL $\text{OR} = 10.00 (p = 0.0007)$.
       - Verify Prop 1 surge regression across 35 shocks: $R^2 = 0.5601$, slope `11.52`.
       - Verify Priority Matrix ($N=88,181$ in 4 operational domains): omnibus $\chi^2(3) = 11,027.60$, $V = 0.3536$, Billing $\text{OR} = 9.49$, Login $\text{OR} = 6.44$, Network $\text{OR} = 2.50$.

    8. **Module 7 (Spring 2024 Counterfactual Telemetry & Case Study 2):**
       - Banglalink Spring 2024 transitions: `2024-03` ($N=1,093$, NSS `+42.82`), `2024-04` ($N=1,315$, NSS `+31.63`, $\Delta\text{NSS} = -11.18$), `2024-05` ($N=2,265$, NSS `+64.42`, $\Delta\text{NSS} = +32.78$).
       - Banglalink `app_version` missingness rate: `51.82%` (71,068 nulls).
       - `v11.8.0` telemetry: Apr 2024 ($N=158$, NSS `-7.59`), Mar-Jun 2024 ($N=198$, NSS `+10.61`).
       - Case Study 2 annual turnaround: 2025 ($N=10,238$, NSS `+66.39`) to 2026 ($N=21,810$, NSS `+81.93`), $\Delta\text{NSS} = +15.54$, General component `+10.33 (66.5%)`, Technical component `+5.21 (33.5%)`.

    9. **Module 8 (Anonymity, Manuscript Completeness & Deliverables):**
       - Check double-blind anonymity across `paper/eswa_latex/manuscript.tex`, `paper/eswa_latex/manuscript_twocolumn.tex`, `paper/eswa_latex/highlights.txt`, and `paper/eswa_latex/references.bib` for all 5 prohibited identifiers: `Ratul`, `rh61632`, `Leading University`, `Jashore`, `github.com`.
       - Check all 8 expected academic sections in both manuscript files.
       - Check all 8 expected table/algorithm labels in both manuscript files (`tab:taxonomy`, `tab:model_leaderboard` or `tab:leaderboard`, `tab:perclass`, `tab:linguistic_benchmark`, `tab:eras`, `tab:shocks`, `alg:canary`, `tab:decision_matrix`).
       - Validate PDF existence: `paper/manuscript.pdf`, `paper/manuscript_twocolumn.pdf`, and `paper/eswa_latex/*.pdf`.
       - Extract PDF page counts via `pdfinfo.exe` (or `pypdf` if available).
       - Phase 8/9 Gated Checks:
         - Inspect for raw markdown tokens (`\*\*`) in `.tex` files.
         - Check single-column page count ($\le 35$ target) and two-column page count ($\le 15$ target).
         - Check PDF SHA256 synchronization between `paper/` and `paper/eswa_latex/`.
         - Check existence of `paper/JBA_Manuscript_Empirical_Calculations.xlsx`.
         - In default mode: if any Phase 8/9 gated check fails, emit `[WARN - Pending Phase 8/9: ...]` without failing the audit (`exit 0`).
         - Under `--strict-paper`: fail immediately (`exit 1`) on any pending Phase 8/9 defect.

    AVOID: Re-running full 5-fold CV in `audit_project_integrity.py` (which takes ~100s); validate deserialized models and `paper_empirical_ground_truth.json` instead to maintain `<10s` runtime.
    AVOID: Failing Phase 7 verification on uncompiled Phase 8 LaTeX / Excel artifacts.
    USE: Exact `atol=0.01` and `pd.Period` arithmetic throughout.
  </action>
  <verify>
    python scripts/audit_project_integrity.py
  </verify>
  <done>
    scripts/audit_project_integrity.py runs all 8 modules cleanly in under 10 seconds, passes with exit code 0, and reports 100% of empirical checks verified.
  </done>
</task>

## Must-Haves
After all tasks complete, verify:
- [ ] 28 dead/broken scripts are moved into `archive/legacy_scripts/` with an inventory `README.md`
- [ ] `scripts/verify_paper_complete.py` and `scripts/audit_paper_contradictions.py` execute cleanly with 3,713 days and 88,181 functional reviews
- [ ] `scripts/audit_project_integrity.py` runs all 8 modules (including restored Modules 2, 3, 7) and exits 0 in under 10 seconds
- [ ] Strict tolerances (`atol=0.01`) and `month_diff == 1` time-series arithmetic pass
- [ ] `--strict-paper` option correctly flags pending Phase 8/9 deliverables while default mode passes cleanly

## Success Criteria
- [ ] All tasks verified passing
- [ ] Must-haves confirmed
- [ ] No regressions in tests
