---
phase: 1
plan: 2
wave: 2
depends_on:
  - "1-PLAN.md"
files_modified:
  - .gsd/phases/1/evidence/02_visualizations_and_assets_audit.md
  - .gsd/phases/1/evidence/02_archive_and_dependencies_audit.md
  - .gsd/phases/1/2-SUMMARY.md
autonomous: true
user_setup: []

must_haves:
  truths:
    - "Byte-for-byte SHA256 parity between scraped_data_global/plots/ and assets/plots/ is verified across all 20 charts"
    - "generate_global_visualizations.py window parameters, operator color hexes, and DPI settings are verified"
    - "All 5 archive/ subdirectories are cataloged and dead code references into archive are mapped with exact line citations"
    - "Repo-wide Python imports are reconciled against requirements.txt, demo/requirements.txt, ml/, and dl/ manifests"
  artifacts:
    - ".gsd/phases/1/evidence/02_visualizations_and_assets_audit.md"
    - ".gsd/phases/1/evidence/02_archive_and_dependencies_audit.md"
    - ".gsd/phases/1/2-SUMMARY.md"
  key_links:
    - "Common window parameters from 1-PLAN.md link to generate_global_visualizations.py:98 COMMON_START"
    - "Archive directory structure links to broken path in ml/train_filtered_experiments.py:19"
---

# Plan 1.2: Visualizations, Asset Parity, Archive Lineage & Dependency Audit

<objective>
Audit the project's visual reporting artifacts across `scraped_data_global/plots/` and `assets/plots/`, inspect historical lineage across all 5 subdirectories in `archive/` (including dead file references), evaluate repo-wide Python package imports against all declared `requirements.txt` manifests, and inspect the GSD harness configuration.
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- .gsd/ARCHITECTURE.md
- .gsd/STACK.md
- .gsd/DECISIONS.md
- scraped_data_global/pipeline/generate_global_visualizations.py
- requirements.txt
- demo/requirements.txt
- ml/requirements.txt
- dl/requirements.txt
- ml/train_filtered_experiments.py
- archive/seed_pipeline_groq/src/02_classify_reviews_mygp.py
</context>

<tasks>

<task type="auto">
  <name>Audit visualization generation, plot inventory, and asset directory mirroring</name>
  <files>
    scraped_data_global/pipeline/generate_global_visualizations.py
    scraped_data_global/plots/
    assets/plots/
    assets/logos/
    scripts/generate_paper_figures.py
    scripts/generate_two_panel_figure.py
    .gsd/phases/1/evidence/02_visualizations_and_assets_audit.md
  </files>
  <action>
    Perform a strict read-only audit of visualization code and generated image assets:
    1. Parity hash check: compute SHA256 hashes of all 20 PNG plot files in `scraped_data_global/plots/` and compare against corresponding files in `assets/plots/`. Verify whether all 20 charts are byte-for-byte identical.
    2. Inspect `generate_global_visualizations.py`:
       - Verify start date filter at line 98 (`COMMON_START = "2016-08-01"` in uncommitted diff vs original `2016-07-28`).
       - Verify operator color hex codes: Grameenphone `#0090ff`, Robi `#e60000`, Banglalink `#ff7a00`.
       - Verify target image resolution (`dpi=300`), output paths, and plot taxonomy.
    3. Asset inventory: inspect `assets/logos/` (`gp.png`, `robi.png`, `banglalink.png`), verifying image dimensions and readability for README presentation.
    4. Paper figure generation cross-reference: inspect `scripts/generate_paper_figures.py` and `scripts/generate_two_panel_figure.py` to identify any shared plots, duplicate naming, or styling differences compared to `generate_global_visualizations.py`.
    5. Save structured empirical evidence, SHA256 comparison tables, and line citations to `.gsd/phases/1/evidence/02_visualizations_and_assets_audit.md`.

    AVOID: Re-running visualization generation scripts or regenerating PNGs. Do NOT touch image files.
    USE: Read-only Python script computing SHA256 hashes via `hashlib` and inspecting source code lines.
  </action>
  <verify>
    python -c "import os; assert os.path.exists('.gsd/phases/1/evidence/02_visualizations_and_assets_audit.md'), 'Evidence file missing'; print('Visualizations and assets audit evidence successfully verified')"
  </verify>
  <done>
    `.gsd/phases/1/evidence/02_visualizations_and_assets_audit.md` exists and contains complete SHA256 comparison table of all 20 plot pairs, verification of operator color codes and DPI, and audit of COMMON_START date in `generate_global_visualizations.py`.
  </done>
</task>

<task type="auto">
  <name>Audit archive lineage, dependency declarations vs codebase imports, and repo harness integrity</name>
  <files>
    archive/seed_pipeline_groq/
    archive/scraped_data_2020/
    archive/robi_backfill/
    archive/early_dl_experiments/
    archive/powerbi_dashboard/
    ml/train_filtered_experiments.py
    archive/seed_pipeline_groq/src/02_classify_reviews_mygp.py
    requirements.txt
    demo/requirements.txt
    ml/requirements.txt
    dl/requirements.txt
    VERSION
    scripts/validate-all.ps1
    scripts/validate-all.sh
    .gsd/phases/1/evidence/02_archive_and_dependencies_audit.md
  </files>
  <action>
    Perform a strict read-only audit of repository historical archives, package dependencies, and harness files:
    1. Historical archive catalog: inspect each of the 5 subdirectories in `archive/`:
       - `archive/seed_pipeline_groq/`: record file count, Groq model used (`qwen/qwen3.8-27b` in `02_classify_reviews_mygp.py:50` vs manuscript's `Qwen-2.5-32B`).
       - `archive/scraped_data_2020/`: record file count, 402-day common window review count (`N=83,417`), iOS probe (`N=1,199`), and archived gold standard.
       - `archive/robi_backfill/`: record review count (`37.1k` backfill) and script roles.
       - `archive/early_dl_experiments/`: record early BanglaBERT Colab notebook and archived models.
       - `archive/powerbi_dashboard/`: record GIF assets of discarded prototype.
    2. Broken references to archive: inspect live codebase for references to moved/archived paths, specifically `ml/train_filtered_experiments.py:19` referencing non-existent `scraped_data_2020/gold_set/gold_set_verified.csv`.
    3. Comprehensive dependency reconciliation:
       - Parse all declared dependencies in `requirements.txt`, `demo/requirements.txt`, `ml/requirements.txt`, and `dl/requirements.txt`.
       - Scan all Python scripts across `ml/`, `dl/`, `demo/`, `scraped_data_global/`, `scripts/`, `data/` for imported modules.
       - Document undeclared dependencies imported in code: `nltk`, `python-docx`, `openpyxl`, `Pillow`, `huggingface_hub`.
       - Document unused dependencies declared in requirements: `torchvision`, `torchaudio`.
       - Document version specifier conflicts (e.g., `scikit-learn>=1.4.0` in root vs `>=1.3.0` in `demo/requirements.txt`).
    4. Repo harness validation: verify `VERSION` (`1.6.0`), `.gsd/` file integrity, and inspect validation rules in `scripts/validate-all.ps1` and `scripts/validate-all.sh`.
    5. Save structured audit tables and line citations to `.gsd/phases/1/evidence/02_archive_and_dependencies_audit.md`.

    AVOID: Modifying any requirements files or attempting `pip install`.
    USE: Read-only Python AST or regex analysis to extract imports and compare against requirement manifests.
  </action>
  <verify>
    python -c "import os; assert os.path.exists('.gsd/phases/1/evidence/02_archive_and_dependencies_audit.md'), 'Evidence file missing'; print('Archive and dependency audit evidence successfully verified')"
  </verify>
  <done>
    `.gsd/phases/1/evidence/02_archive_and_dependencies_audit.md` exists and contains inventory of all 5 archive dirs, exact line citation of broken archive path in `train_filtered_experiments.py`, full audit of undeclared/unused dependencies, and repo harness integrity verification.
  </done>
</task>

</tasks>

<verification>
After all tasks complete, verify:
- [ ] `.gsd/phases/1/evidence/02_visualizations_and_assets_audit.md` exists and documents SHA256 parity across all 20 charts, color constants, and COMMON_START.
- [ ] `.gsd/phases/1/evidence/02_archive_and_dependencies_audit.md` exists and documents archive subdirectories, dead paths, undeclared/unused dependencies, and harness status.
- [ ] `.gsd/phases/1/2-SUMMARY.md` is generated summarizing all Plan 2 findings and discrepancies.
</verification>

<success_criteria>
- [ ] All tasks verified passing with exit code 0
- [ ] No project source, data, or paper files outside `.gsd/` were modified
- [ ] No git commands (`git add`, `git commit`) were executed
</success_criteria>
