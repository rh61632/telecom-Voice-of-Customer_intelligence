---
phase: 1
plan: 3
wave: 3
depends_on:
  - "2-PLAN.md"
files_modified:
  - .gsd/phases/1/evidence/03_demo_application_audit.md
  - .gsd/phases/1/evidence/03_documentation_and_drift_audit.md
  - .gsd/phases/1/3-SUMMARY.md
autonomous: true
user_setup: []

must_haves:
  truths:
    - "demo/app.py layout definition, output mapping, and return tuple are audited and the missing out_cat wiring is documented"
    - "demo/app.py claims (655.6k training vs inference) and line 114 paper title citation are verified"
    - "All quantitative claims and badges across README.md, data/README.md, and TODO.txt are verified against ground-truth data"
    - "All 39 modified tracked files and untracked artifacts from git status -s are cataloged with exact drift rationales"
  artifacts:
    - ".gsd/phases/1/evidence/03_demo_application_audit.md"
    - ".gsd/phases/1/evidence/03_documentation_and_drift_audit.md"
    - ".gsd/phases/1/3-SUMMARY.md"
  key_links:
    - "demo/app.py imports ml.predict and ml.language_detector which depends on undeclared nltk from 2-PLAN.md"
    - "common_duration_summary.json from 1-PLAN.md is reconciled against README.md performance scorecard"
---

# Plan 1.3: Documentation, Live Demo & Working-Tree Drift Audit

<objective>
Audit the Gradio interactive demo in `demo/app.py` (specifically UI component wiring, output mapping bug, runtime imports, and claims), verify all metrics, scorecards, and links in `README.md`, `data/README.md`, and `TODO.txt` against underlying data, and comprehensively catalog pre-existing uncommitted working-tree drift across the repository.
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- .gsd/ARCHITECTURE.md
- .gsd/DECISIONS.md
- demo/app.py
- demo/requirements.txt
- README.md
- data/README.md
- TODO.txt
- scraped_data_global/classified/common_duration_summary.json
- .gsd/phases/1/evidence/01_merge_sync_telemetry_audit.md
- .gsd/phases/1/evidence/02_archive_and_dependencies_audit.md
</context>

<tasks>

<task type="auto">
  <name>Audit demo/app.py UI wiring, runtime imports, and demo documentation</name>
  <files>
    demo/app.py
    demo/requirements.txt
    ml/predict.py
    ml/language_detector.py
    .gsd/phases/1/evidence/03_demo_application_audit.md
  </files>
  <action>
    Perform a strict read-only audit of the interactive Gradio demo application:
    1. Audit UI wiring bug in `demo/app.py`:
       - Line 97 defines `out_cat = gr.Textbox(label="Operational Domain", interactive=False)`.
       - Line 38 computes `category_label = f"{res['category']} ({res['category_confidence'] * 100:.1f}%)"`.
       - Line 54 returns a 5-element tuple: `lang_badge, sentiment_label, res["probabilities"], cat_probs, diagnostic_summary` (omitting `category_label`).
       - Line 108 defines `outputs=[out_lang, out_sent, out_sent_probs, out_cat_probs, out_diag]` (omitting `out_cat`).
       - Consequence: The `out_cat` textbox in the UI remains permanently empty regardless of input review. Document exact lines and proposed fix.
    2. Audit training claim inaccuracy:
       - Line 67 asserts: `"Trained on 655,649 longitudinal customer reviews across Grameenphone, Robi Axiata, and Banglalink (2016–2026)."`.
       - Reconcile against ground truth: The production Ensemble model was trained on `N=4,500` seed reviews (`data/processed/`), while `655,649` is the size of the scored common-window evaluation corpus.
    3. Audit paper title leakage:
       - Line 114 embeds the full research paper title (*“With Great Reviews Comes Great Responsibility...”*).
       - Evaluate whether this conflicts with repo hygiene and commit `4d5aaad` which decoupled research paper deliverables to `paper/`.
    4. Audit demo dependencies and model loading:
       - Verify `demo/requirements.txt` vs runtime requirements: `demo/app.py` imports `ml.language_detector` which requires `nltk` (not in `demo/requirements.txt`).
       - Verify model loading calls at lines 17-18: `load_model("ensemble")` -> `ml/models/ensemble_voting_classifier.joblib` and `load_category_model()` -> `ml/models/category_voting_classifier.joblib`.
    5. Save structured audit findings with exact line citations and code excerpts to `.gsd/phases/1/evidence/03_demo_application_audit.md`.

    AVOID: Running `demo.launch()` or launching long-running web servers. Do NOT edit `demo/app.py`.
    USE: Read-only Python AST or script inspection verifying function signatures and component references.
  </action>
  <verify>
    python -c "import os; assert os.path.exists('.gsd/phases/1/evidence/03_demo_application_audit.md'), 'Evidence file missing'; print('Demo application audit evidence successfully verified')"
  </verify>
  <done>
    `.gsd/phases/1/evidence/03_demo_application_audit.md` exists and contains detailed code analysis of the `out_cat` wiring bug, exact line citations for the training volume claim error, paper title citation analysis, and dependency gap audit.
  </done>
</task>

<task type="auto">
  <name>Audit README.md, data/README.md, TODO.txt, and catalog pre-existing uncommitted working-tree drift</name>
  <files>
    README.md
    data/README.md
    TODO.txt
    scraped_data_global/classified/common_duration_summary.json
    .gsd/phases/1/evidence/03_documentation_and_drift_audit.md
  </files>
  <action>
    Perform a strict read-only audit of project documentation and catalog all pre-existing uncommitted git drift:
    1. Documentation metric cross-check:
       - Compare `README.md:43-56` (Performance Scorecard) and `data/README.md` against `scraped_data_global/classified/common_duration_summary.json`:
         * Total reviews: `655,649` (Grameenphone: `320,140`, Robi: `198,378`, Banglalink: `137,131`).
         * Percentages: GP (77.0% pos, 10.9% neu, 12.1% neg, NSS +64.9%), Robi (77.9% pos, 10.2% neu, 12.0% neg, NSS +65.9%), BL (70.4% pos, 12.3% neu, 17.3% neg, NSS +53.0%), Industry (75.9% pos, 10.9% neu, 13.2% neg, NSS +62.7%).
         * Duration dates: August 1, 2016 – September 30, 2026 (3,713 Days).
         * Master corpus: `661,160` reviews.
       - Check badges in `README.md:12-22` for any stale numbers or broken URLs.
       - Scan for any leftover references to old window parameters (`3,716` days or `655,670` reviews) across documentation files.
    2. Audit `TODO.txt` against actual project state:
       - Item 1 (Model Checkpoint Hosting): check whether Hugging Face upload script exists (`scripts/upload_to_huggingface.py`) and whether hub models are pushed or pending.
       - Item 2 (Gold Standard Expansion): verify [COMPLETED] status and metrics against `data/gold_set/gold_standard_evaluation_report.md` (Sentiment Kappa 0.5762, Category Kappa 0.7694).
       - Item 3 (Filtered vs Unfiltered): check ablation study references and current production model usage.
       - Items 4-6: document status of remaining deferred roadmap items.
    3. Catalog uncommitted working-tree drift:
       - Run read-only `git status -s` and `git diff --stat` to capture all 39 modified tracked files and all untracked paths.
       - Categorize each modification: (a) Common window shift `2016-07-28` -> `2016-08-01` (`3,716` -> `3,713` days, `655,670` -> `655,649` reviews), (b) Regenerated plot PNGs (30 plots), (c) Model config updates (`banglabert_finetuned_*/config.json`), (d) Excel builder path update.
       - Catalog untracked assets: `demo/`, `ml/reports/`, `scripts/`, `.gsd/`.
    4. Save structured audit report with full metric comparison tables and git drift categorization to `.gsd/phases/1/evidence/03_documentation_and_drift_audit.md`.

    AVOID: Running `git add`, `git commit`, `git checkout`, `git reset`, or any modifying git commands.
    USE: Read-only Python subprocess executing `git status -s` and `git diff --stat` to capture working tree state.
  </action>
  <verify>
    python -c "import os; assert os.path.exists('.gsd/phases/1/evidence/03_documentation_and_drift_audit.md'), 'Evidence file missing'; print('Documentation and drift audit evidence successfully verified')"
  </verify>
  <done>
    `.gsd/phases/1/evidence/03_documentation_and_drift_audit.md` exists and contains verified documentation metric table vs ground truth, comprehensive audit of `TODO.txt` items, and an exhaustive categorized inventory of all 39 uncommitted modified files and untracked directories.
  </done>
</task>

</tasks>

<verification>
After all tasks complete, verify:
- [ ] `.gsd/phases/1/evidence/03_demo_application_audit.md` exists and documents demo wiring, training claims, and paper leakage.
- [ ] `.gsd/phases/1/evidence/03_documentation_and_drift_audit.md` exists and documents README scorecard verification, TODO status, and working-tree drift.
- [ ] `.gsd/phases/1/3-SUMMARY.md` is generated summarizing all Plan 3 findings and discrepancies.
</verification>

<success_criteria>
- [ ] All tasks verified passing with exit code 0
- [ ] No project source, data, or paper files outside `.gsd/` were modified
- [ ] No git commands (`git add`, `git commit`) were executed
</success_criteria>
