---
phase: 8
plan: 1
wave: 1
depends_on: []
files_modified:
  - scripts/generate_eswa_architecture_diagram.py
  - scripts/generate_two_panel_figure.py
  - scripts/generate_paper_figures.py
  - scripts/rebuild_figure3.py
  - paper/figures/figure0_system_architecture.png
  - paper/figures/figure1_longitudinal_nss_trajectory.png
  - paper/figures/figure2_annual_leadership_strip.png
  - paper/figures/figure3_priority_matrix.png
  - paper/figures/figure4_banglalink_reversal_decomposition.png
  - paper/figures/monthly_nss_trend_modern_era.png
  - paper/figures/monthly_nss_trend_2020_2026.png
  - paper/eswa_latex/figures/figure0_system_architecture.png
  - paper/eswa_latex/figures/figure1_longitudinal_nss_trajectory.png
  - paper/eswa_latex/figures/figure2_annual_leadership_strip.png
  - paper/eswa_latex/figures/figure3_priority_matrix.png
  - paper/eswa_latex/figures/figure4_banglalink_reversal_decomposition.png
  - paper/telecommunications_policy_latex/figures/figure0_system_architecture.png
  - paper/telecommunications_policy_latex/figures/figure1_longitudinal_nss_trajectory.png
  - paper/telecommunications_policy_latex/figures/figure2_annual_leadership_strip.png
  - paper/telecommunications_policy_latex/figures/figure3_priority_matrix.png
  - paper/telecommunications_policy_latex/figures/figure4_banglalink_reversal_decomposition.png
  - assets/plots/monthly_nss_trend_modern_era.png
  - assets/plots/monthly_nss_trend_2020_2026.png
  - scraped_data_global/plots/monthly_nss_trend_modern_era.png
  - scraped_data_global/plots/monthly_nss_trend_2020_2026.png
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "scripts/generate_eswa_architecture_diagram.py replaces fictional Lemmatizer, Bayesian margin regularization, and Multi-Head Attention claims with exact live pipeline descriptions (word 1-2 + char 3-5 TF-IDF, Platt calibration, Single-Head Bahdanau attention, N=35 total / N=19 non-surge shocks)"
    - "scripts/generate_paper_figures.py removes hardcoded 'Figure 1..4:' bitmap headers, fixes figure4 canvas size and bbox_inches='tight' clipping, and aligns Case Study 2 annotation with empirical numbers (+15.54 turnaround: +10.33 General / +5.21 Technical, 2.13x volume growth)"
    - "Figure 3 priority matrix vertical prevalence threshold is set to 3.75% across both rebuild_figure3.py and generate_paper_figures.py, cleanly positioning all 3 App Login bubbles in Quadrant I (Urgent Crisis) and all 3 Offers bubbles in Quadrant IV (Commercial Friction), with BL Offers negativity aligned to 56.14%"
    - "scripts/generate_two_panel_figure.py synchronizes identical bytes across 6 paths (modern_era and 2020_2026 in paper/figures/, assets/plots/, and scraped_data_global/plots/)"
    - "All publication figures (figure0 through figure4) share identical SHA256 checksums across paper/figures/, paper/eswa_latex/figures/, and paper/telecommunications_policy_latex/figures/"
  artifacts:
    - "scripts/generate_eswa_architecture_diagram.py updated and producing synced figure0 across 3 directories"
    - "scripts/generate_paper_figures.py updated and producing synced figure1, figure2, figure3, figure4 across 3 directories"
    - "scripts/rebuild_figure3.py updated with 3.75% threshold, 56.14% BL negativity, and 3 output directories"
    - "scripts/generate_two_panel_figure.py updated with 6-way alias parity"
    - "Synchronized figure PNGs in paper/figures/, paper/eswa_latex/figures/, and paper/telecommunications_policy_latex/figures/"
---

# Plan 8.1: Publication Figures Remediation (REM-06, DISC-MAJ-13, DISC-HYG-04)

## Objective
Remediate and regenerate all publication figures (`figure0` through `figure4`) to eliminate hardcoded `"Figure 1..4:"` bitmap prefixes, right-edge title/annotation clipping on `figure4`, quadrant-boundary contradictions on `figure3`, fictional model/NLP claims on `figure0`, and divergent aliases in `generate_two_panel_figure.py`. Synchronize all figures with byte-for-byte SHA256 parity across `paper/figures/`, `paper/eswa_latex/figures/`, and `paper/telecommunications_policy_latex/figures/`.

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-06`)
- `.gsd/phases/8/RESEARCH.md` (Sections 1.1, 1.2, 1.3)
- `scraped_data_global/classified/paper_empirical_ground_truth.json`
- `scripts/generate_eswa_architecture_diagram.py`
- `scripts/generate_paper_figures.py`
- `scripts/rebuild_figure3.py`
- `scripts/generate_two_panel_figure.py`

## Tasks

<task type="auto">
  <name>Remediate generate_eswa_architecture_diagram.py and generate_two_panel_figure.py</name>
  <files>
    scripts/generate_eswa_architecture_diagram.py
    scripts/generate_two_panel_figure.py
    paper/eswa_latex/figures/figure0_system_architecture.png
    paper/figures/figure0_system_architecture.png
    paper/telecommunications_policy_latex/figures/figure0_system_architecture.png
    paper/figures/monthly_nss_trend_modern_era.png
    paper/figures/monthly_nss_trend_2020_2026.png
    assets/plots/monthly_nss_trend_modern_era.png
    assets/plots/monthly_nss_trend_2020_2026.png
    scraped_data_global/plots/monthly_nss_trend_modern_era.png
    scraped_data_global/plots/monthly_nss_trend_2020_2026.png
  </files>
  <action>
    1. In `scripts/generate_eswa_architecture_diagram.py`:
       - Update Stage 1 `Code-Mixed NLP Processor` inner card (line 61): replace `"Phonetic Banglish Normalizer"`, `"Sub-word Char N-grams (2-5)"`, `"Word N-grams (1-3)"` with `["Trilingual / Code-Mixed Engine", "Lowercase & Whitespace Norm.", "Sub-word Char N-grams (3-5)", "Word N-grams (1-2) + Sublinear TF"]` to match production `category_voting_classifier.joblib` and `sentiment_voting_classifier.joblib` ($V=29,843$).
       - Update Stage 1 `Dual Ground-Truth Sets` (line 63): replace `"Human Gold Set: N = 300"`, `"Blind Dual-Annotated Truth"` with `["Seed Dataset: N = 4,500", "Human Gold Set: N = 300", "Dual-Annotated Subset: N = 200", "Inter-Rater Kappa Benchmarks"]`.
       - Update Stage 2 `Production Voting Ensemble` (line 68): replace `"87.5% CV Acc / 450 rev/sec"` with `["Soft-Voting Tri-Classifier", "Calibrated LinearSVC (Platt)", "Complement Naive Bayes", "Balanced Multinomial LR", "87.3% Cat / 87.4% Sent CV Acc", "122-177 rev/sec (Single CPU)"]`.
       - Update Stage 2 `Deep Learning Benchmarks` (line 70): replace `"BiLSTM + Multi-Head Attention"` with `"BiLSTM + Single-Head Attention"`.
       - Update Stage 2 `Statistical Calibration` (line 72): replace `"Bayesian Margin Regularization"`, `"Star-Rating Inversion Filter"` with `["Rogan-Gladen True Prevalence", "Platt Sigmoid Calibration", "McNemar & Paired t-Tests"]`.
       - Update Stage 3 `Rule 2: Changepoint & Surges` (line 79): replace `"Isolates Real Crises (N=35)"` with `["Dual-Track Volatility Filter", "Flags Shocks (N=35 Total)", "Filters Promo Surges (≥ 50%)", "Separates Campaign Noise", "Isolates Non-Surge (N=19)"]`.
       - Update output saving (lines 106-108): write identically with `dpi=300, bbox_inches='tight'` to ALL THREE figure directories:
         - `paper/eswa_latex/figures/figure0_system_architecture.png`
         - `paper/figures/figure0_system_architecture.png`
         - `paper/telecommunications_policy_latex/figures/figure0_system_architecture.png`
         (Ensure parent directories exist via `Path.mkdir(parents=True, exist_ok=True)`).

    2. In `scripts/generate_two_panel_figure.py`:
       - Enforce 6-way alias parity (lines 168-174): save both `monthly_nss_trend_modern_era.png` and `monthly_nss_trend_2020_2026.png` with `dpi=300, bbox_inches='tight'` across:
         - `paper/figures/`
         - `assets/plots/`
         - `scraped_data_global/plots/`
       - Ensure all 6 target files receive identical bytes.
       - Verify Panel B hardcoded telemetry values (lines 80-157) match `paper_empirical_ground_truth.json` (`v11.8.0` `-7.59`, Mar `42.82`, Apr `-11.18`, May `+32.78`, May hotfix `+71.71` / `+77.0`).

    3. Execute both scripts:
       - `python scripts/generate_eswa_architecture_diagram.py`
       - `python scripts/generate_two_panel_figure.py`

    AVOID: Altering color schemes or visual aesthetics outside the discrepancy list.
    AVOID: Leaving any of the 3 venue figure folders with stale or missing figure0 files.
  </action>
  <verify>
    python -c "import hashlib, pathlib; p1=pathlib.Path('paper/eswa_latex/figures/figure0_system_architecture.png'); p2=pathlib.Path('paper/figures/figure0_system_architecture.png'); p3=pathlib.Path('paper/telecommunications_policy_latex/figures/figure0_system_architecture.png'); assert p1.exists() and p2.exists() and p3.exists(), 'figure0 missing in a venue'; h1,h2,h3 = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (p1,p2,p3)]; assert h1==h2==h3, f'figure0 hash mismatch: {h1}, {h2}, {h3}'; m1=pathlib.Path('paper/figures/monthly_nss_trend_modern_era.png'); m2=pathlib.Path('paper/figures/monthly_nss_trend_2020_2026.png'); m3=pathlib.Path('assets/plots/monthly_nss_trend_modern_era.png'); m4=pathlib.Path('assets/plots/monthly_nss_trend_2020_2026.png'); m5=pathlib.Path('scraped_data_global/plots/monthly_nss_trend_modern_era.png'); m6=pathlib.Path('scraped_data_global/plots/monthly_nss_trend_2020_2026.png'); mh=[hashlib.sha256(p.read_bytes()).hexdigest() for p in (m1,m2,m3,m4,m5,m6)]; assert len(set(mh))==1, f'6-way alias mismatch: {mh}'; print('✓ figure0 and two-panel figure verified with identical hashes!')"
  </verify>
  <done>
    figure0_system_architecture.png generated with accurate NLP/ML claims and synced across 3 directories. monthly_nss_trend_modern_era.png and monthly_nss_trend_2020_2026.png synced with identical bytes across all 6 target locations.
  </done>
</task>

<task type="auto">
  <name>Remediate generate_paper_figures.py and rebuild_figure3.py</name>
  <files>
    scripts/generate_paper_figures.py
    scripts/rebuild_figure3.py
    paper/figures/figure1_longitudinal_nss_trajectory.png
    paper/figures/figure2_annual_leadership_strip.png
    paper/figures/figure3_priority_matrix.png
    paper/figures/figure4_banglalink_reversal_decomposition.png
    paper/eswa_latex/figures/figure1_longitudinal_nss_trajectory.png
    paper/eswa_latex/figures/figure2_annual_leadership_strip.png
    paper/eswa_latex/figures/figure3_priority_matrix.png
    paper/eswa_latex/figures/figure4_banglalink_reversal_decomposition.png
    paper/telecommunications_policy_latex/figures/figure1_longitudinal_nss_trajectory.png
    paper/telecommunications_policy_latex/figures/figure2_annual_leadership_strip.png
    paper/telecommunications_policy_latex/figures/figure3_priority_matrix.png
    paper/telecommunications_policy_latex/figures/figure4_banglalink_reversal_decomposition.png
  </files>
  <action>
    1. In `scripts/generate_paper_figures.py`:
       - Remove hardcoded `"Figure N:"` bitmap titles (DISC-MAJ-13):
         - Line 158: change `'Figure 1: Ten-Year Monthly Net Sentiment Score (NSS) Trajectory across Bangladeshi Operators'` to `'Ten-Year Monthly Net Sentiment Score (NSS) Trajectory across Bangladeshi Operators'`.
         - Line 206: change `'Figure 2: Annual Voice-of-Customer Leadership Strip (2016–2026 Highest Yearly NSS Leader)'` to `'Annual Voice-of-Customer Leadership Strip (2016–2026 Highest Yearly NSS Leader)'`.
         - Line 298: change `'Figure 3: Strategic VoC Priority Matrix (Prevalence vs Dissatisfaction Intensity)'` to `'Strategic VoC Priority Matrix (Prevalence vs. Dissatisfaction Intensity)'`.
         - Line 346: change `'Figure 4: Additive Domain Decomposition of Banglalink\'s 2025–2026 NSS Reversal (+15.54 Points)'` to `'Additive Domain Decomposition of Banglalink\'s 2025–2026 NSS Reversal (+15.54 Points)'`.
       - Fix Figure 4 right-edge clipping and annotation (DISC-MAJ-13):
         - Line 307: expand canvas `figsize=(9.5, 5.2)` to `figsize=(10.5, 5.4)`.
         - Line 346: set title `fontsize=11.5`.
         - Line 348: pass `bbox_inches='tight', pad_inches=0.15` to `fig.savefig(...)`.
         - Line 338: update takeaway annotation text to `'Key Takeaway (Proposition 1):\n66.5% of Banglalink\'s turnaround\n(+10.33 of +15.54 pts) was driven by\na 2.13x volume growth (21,810 vs. 10,238 reviews),\nwhile real login bug fixes added +2.80 pts.'`.
       - Harmonize Figure 3 layout and parameters:
         - Line 219: fix `BL Offers & Packs` negativity from `56.13` to `56.14` (`3,321 / 5,916 = 56.1359%`).
         - Lines 238-245: change vertical prevalence threshold from `4.5` to `3.75` (`ax.axvline(3.75)` and corresponding quadrant background spans `ax.axvspan(0, 3.75, ...)` and `ax.axvspan(3.75, 9.6, ...)`).
         - Adopt the cleaner unified Billing card and horizontal bottom legend from `rebuild_figure3.py`.
       - Update save operations for all figures (lines 160, 208, 300, 348):
         - Pass `bbox_inches='tight', pad_inches=0.12` on `figure1`, `figure2`, `figure3`, and `pad_inches=0.15` on `figure4`.
         - Save each figure to all three directories: `paper/figures/`, `paper/eswa_latex/figures/`, and `paper/telecommunications_policy_latex/figures/`.

    2. In `scripts/rebuild_figure3.py`:
       - Line 175: change title to `'Strategic VoC Priority Matrix (Prevalence vs. Dissatisfaction Intensity)'` (removing `'Figure 3: '` prefix).
       - Lines 16-23: change vertical threshold from `4.5` to `3.75` (updating `ax.axvline(3.75)`, `ax.axvspan(0, 3.75, ...)`, and `ax.axvspan(3.75, 9.6, ...)`).
       - Line 57: fix `BL Offers & Packs` negativity to `56.14`.
       - Lines 179-183: update output destinations to write `figure3_priority_matrix.png` to ALL THREE directories (`paper/figures/`, `paper/eswa_latex/figures/`, and `paper/telecommunications_policy_latex/figures/`).

    3. Execute both scripts:
       - `python scripts/generate_paper_figures.py`
       - `python scripts/rebuild_figure3.py`

    AVOID: Reintroducing `ax.axvline(4.5)` which incorrectly pushed GP App Login into QII and BL Offers into QIII.
    AVOID: Missing `bbox_inches='tight'` which leads to clipped titles in LaTeX figures.
  </action>
  <verify>
    python -c "import hashlib, pathlib; dirs=['paper/figures', 'paper/eswa_latex/figures', 'paper/telecommunications_policy_latex/figures']; figs=['figure1_longitudinal_nss_trajectory.png', 'figure2_annual_leadership_strip.png', 'figure3_priority_matrix.png', 'figure4_banglalink_reversal_decomposition.png']; [assert len({hashlib.sha256((pathlib.Path(d)/f).read_bytes()).hexdigest() for d in dirs})==1, f'Mismatch in {f}' for f in figs]; print('✓ Figures 1-4 SHA256 verified identical across all 3 venue directories!')"
  </verify>
  <done>
    All publication figures 1-4 regenerated without hardcoded Figure prefixes, figure4 clipping eliminated, figure3 quadrant threshold aligned to 3.75%, and identical PNG files stored across all three paper directories.
  </done>
</task>

<task type="auto">
  <name>Verify visual integrity, metadata invariants, and absence of hardcoded figure prefixes</name>
  <files>
    scripts/generate_paper_figures.py
    scripts/rebuild_figure3.py
  </files>
  <action>
    1. Verify that `generate_paper_figures.py` and `rebuild_figure3.py` contain zero occurrences of literal `'Figure 1:'`, `'Figure 2:'`, `'Figure 3:'`, or `'Figure 4:'` inside `plt.title` calls.
    2. Verify that the vertical quadrant boundary in both `generate_paper_figures.py` and `rebuild_figure3.py` is `3.75` (`3.75%`).
    3. Verify that `figure4` in `generate_paper_figures.py` contains `2.13x` volume growth and `+15.54` pts decomposition (`+10.33` General / `+5.21` Technical).
    4. Verify that all 5 publication figure files (`figure0` through `figure4`) exist and have non-zero size in `paper/figures/`, `paper/eswa_latex/figures/`, and `paper/telecommunications_policy_latex/figures/`.
  </action>
  <verify>
    python -c "import re, pathlib; s1=pathlib.Path('scripts/generate_paper_figures.py').read_text(encoding='utf-8'); s2=pathlib.Path('scripts/rebuild_figure3.py').read_text(encoding='utf-8'); assert not re.search(r'title\(.*Figure [1-4]:', s1), 'Found Figure N: prefix in generate_paper_figures.py'; assert not re.search(r'title\(.*Figure [1-4]:', s2), 'Found Figure N: prefix in rebuild_figure3.py'; assert '3.75' in s1 and '3.75' in s2, 'Missing 3.75 threshold in figure3 generator'; assert '2.13x' in s1, 'Missing 2.13x in figure4 annotation'; print('✓ Figure scripts free of hardcoded prefixes, aligned with 3.75 threshold and 2.13x volume!')"
  </verify>
  <done>
    Source scripts verified clean of hardcoded bitmap headers, aligned to 3.75% prevalence boundary and 2.13x Case Study 2 volume growth, and cross-venue PNG files confirmed synchronized.
  </done>
</task>

## Must-Haves
After all tasks complete, verify:
- [ ] `figure0_system_architecture.png` replaces unverified NLP/Bayesian/Multi-head claims with live pipeline parameters
- [ ] Hardcoded `"Figure 1:"`–`"Figure 4:"` titles are removed from bitmap images
- [ ] `figure4` canvas is expanded and saved with `bbox_inches='tight'`, preventing right-edge text clipping
- [ ] `figure3` vertical threshold is `3.75%`, placing all App Login bubbles in QI and Offers in QIV
- [ ] `monthly_nss_trend_modern_era.png` and `monthly_nss_trend_2020_2026.png` maintain 6-way byte parity
- [ ] `figure0` through `figure4` have identical SHA256 hashes across `paper/figures/`, `paper/eswa_latex/figures/`, and `paper/telecommunications_policy_latex/figures/`

## Success Criteria
- [ ] All tasks verified passing
- [ ] Must-haves confirmed
- [ ] Zero uncommitted git changes required (`ADR-003`)
