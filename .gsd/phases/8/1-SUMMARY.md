# Plan 8.1 Summary: Publication Figures Remediation (REM-06, DISC-MAJ-13, DISC-HYG-04)

**Executed At:** `2026-11-12T00:58:00+06:00`  
**Phase:** 8 (Publication Figures, Active ESWA Manuscript & Compiled PDFs Remediation)  
**Plan:** 1 of 3 (`1-PLAN.md`)  
**Status:** Complete  
**Commits:** None (`ADR-003` policy: working-tree review without unsolicited git commits)  

---

## 1. Executive Summary

Plan 8.1 successfully remediated and regenerated all publication figures (`figure0` through `figure4`, plus longitudinal two-panel figures) across the repository. The update permanently eliminated hardcoded `"Figure 1:"` through `"Figure 4:"` bitmap prefixes, right-edge title/annotation clipping on `figure4`, quadrant boundary contradictions on `figure3` (aligning to 3.75% prevalence), ungrounded model/NLP claims on `figure0` (fictional Lemmatizer, Bayesian margin regularization, Multi-Head Attention replaced with live pipeline parameters), and divergent file aliases in `generate_two_panel_figure.py`.

All publication figures (`figure0` through `figure4` and compatibility aliases) now share **100% byte-for-byte SHA256 parity** across:
1. `paper/figures/`
2. `paper/eswa_latex/figures/`
3. `paper/telecommunications_policy_latex/figures/`

In addition, the two-panel figure files (`monthly_nss_trend_modern_era.png` and `monthly_nss_trend_2020_2026.png`) achieve **6-way SHA256 byte parity** across `paper/figures/`, `assets/plots/`, and `scraped_data_global/plots/`.

---

## 2. Tasks Completed

| Task | Name | Files Touched | Verification |
|---|---|---|---|
| 1 | Remediate `generate_eswa_architecture_diagram.py` and `generate_two_panel_figure.py` | `scripts/generate_eswa_architecture_diagram.py`, `scripts/generate_two_panel_figure.py`, `paper/eswa_latex/figures/figure0_system_architecture.png`, `paper/figures/figure0_system_architecture.png`, `paper/telecommunications_policy_latex/figures/figure0_system_architecture.png`, `paper/figures/monthly_nss_trend_modern_era.png`, `paper/figures/monthly_nss_trend_2020_2026.png`, `assets/plots/monthly_nss_trend_modern_era.png`, `assets/plots/monthly_nss_trend_2020_2026.png`, `scraped_data_global/plots/monthly_nss_trend_modern_era.png`, `scraped_data_global/plots/monthly_nss_trend_2020_2026.png` | `figure0` 3-way hash parity confirmed; two-panel 6-way alias hash parity confirmed (`b8d496436e1bf269...`) (`rc=0`) |
| 2 | Remediate `generate_paper_figures.py` and `rebuild_figure3.py` | `scripts/generate_paper_figures.py`, `scripts/rebuild_figure3.py`, `paper/figures/figure1_longitudinal_nss_trajectory.png`, `paper/figures/figure2_annual_leadership_strip.png`, `paper/figures/figure3_priority_matrix.png`, `paper/figures/figure4_banglalink_reversal_decomposition.png`, `paper/eswa_latex/figures/...`, `paper/telecommunications_policy_latex/figures/...` | Figures 1-4 verified identical across all 3 venue directories (`rc=0`) |
| 3 | Verify visual integrity, metadata invariants, and absence of hardcoded figure prefixes | `scripts/generate_paper_figures.py`, `scripts/rebuild_figure3.py`, all figure PNG files | Zero hardcoded Figure prefixes in titles; 3.75 threshold and 2.13x volume growth verified; all 15 publication figure files verified with non-zero size (`rc=0`) |

---

## 3. Detailed Remediation Actions

### 3.1 Figure 0: Architecture Diagram (`scripts/generate_eswa_architecture_diagram.py`)
- **Stage 1 (Code-Mixed NLP Processor):** Removed fictional `"Phonetic Banglish Normalizer"` and replaced with verified live pipeline cards: `["Trilingual / Code-Mixed Engine", "Lowercase & Whitespace Norm.", "Sub-word Char N-grams (3-5)", "Word N-grams (1-2) + Sublinear TF"]` ($V=29,843$).
- **Stage 1 (Ground Truth Sets):** Clarified dual ground truth configuration: `["Seed Dataset: N = 4,500", "Human Gold Set: N = 300", "Dual-Annotated Subset: N = 200", "Inter-Rater Kappa Benchmarks"]`.
- **Stage 2 (Production Voting Ensemble):** Replaced fictional 450 rev/sec with empirically benchmarked CPU latency: `["Soft-Voting Tri-Classifier", "Calibrated LinearSVC (Platt)", "Complement Naive Bayes", "Balanced Multinomial LR", "87.3% Cat / 87.4% Sent CV Acc", "122-177 rev/sec (Single CPU)"]`.
- **Stage 2 (Deep Learning Benchmarks):** Fixed `"BiLSTM + Multi-Head Attention"` to `"BiLSTM + Single-Head Attention"` (Bahdanau attention anchor).
- **Stage 2 (Statistical Calibration):** Replaced fictional `"Bayesian Margin Regularization"` and `"Star-Rating Inversion Filter"` with `"Rogan-Gladen True Prevalence"`, `"Platt Sigmoid Calibration"`, and `"McNemar & Paired t-Tests"`.
- **Stage 3 (Rule 2: Changepoint & Surges):** Replaced vague crisis label with exact empirical shock counts: `["Dual-Track Volatility Filter", "Flags Shocks (N=35 Total)", "Filters Promo Surges (≥ 50%)", "Separates Campaign Noise", "Isolates Non-Surge (N=19)"]`.
- **Export Synchronization:** Directly saves and writes identical bytes across `paper/eswa_latex/figures/`, `paper/figures/`, and `paper/telecommunications_policy_latex/figures/`.

### 3.2 Two-Panel Longitudinal Figures (`scripts/generate_two_panel_figure.py`)
- Standardized byte-for-byte synchronization across all 6 targets:
  - `paper/figures/monthly_nss_trend_modern_era.png`
  - `paper/figures/monthly_nss_trend_2020_2026.png`
  - `assets/plots/monthly_nss_trend_modern_era.png`
  - `assets/plots/monthly_nss_trend_2020_2026.png`
  - `scraped_data_global/plots/monthly_nss_trend_modern_era.png`
  - `scraped_data_global/plots/monthly_nss_trend_2020_2026.png`
- Verified Panel B build telemetry annotations: v11.8.0 crash (`-7.59`), March baseline (`42.82`), April shock (`-11.18`), May rebound (`+32.78`), May hotfix (`+77.0`, Mar-Jun `+71.71`), and volume totals (`1,093`, `1,315`, `2,265`).

### 3.3 Publication Figures 1–4 (`scripts/generate_paper_figures.py` & `scripts/rebuild_figure3.py`)
- **Bitmap Prefix Removal (DISC-MAJ-13):**
  - Figure 1: `'Figure 1: Ten-Year Monthly...'` $\rightarrow$ `'Ten-Year Monthly Net Sentiment Score (NSS) Trajectory across Bangladeshi Operators'`.
  - Figure 2: `'Figure 2: Annual Voice-of-Customer...'` $\rightarrow$ `'Annual Voice-of-Customer Leadership Strip (2016–2026 Highest Yearly NSS Leader)'`.
  - Figure 3: `'Figure 3: Strategic VoC Priority Matrix...'` $\rightarrow$ `'Strategic VoC Priority Matrix (Prevalence vs. Dissatisfaction Intensity)'`.
  - Figure 4: `'Figure 4: Additive Domain Decomposition...'` $\rightarrow$ `'Additive Domain Decomposition of Banglalink\'s 2025–2026 NSS Reversal (+15.54 Points)'`.
- **Figure 4 Canvas & Right-Edge Clipping:**
  - Expanded canvas from `figsize=(9.5, 5.2)` to `figsize=(10.5, 5.4)` with title `fontsize=11.5`.
  - Exported with `bbox_inches='tight', pad_inches=0.15` to ensure callouts and axis labels never clip.
  - Aligned annotation with empirical data: `2.13x` volume growth (21,810 vs. 10,238 reviews) driving `+10.33` pts of `+15.54` turnaround (66.5%), and `+2.80` pts from login bug fixes.
- **Figure 3 Priority Matrix Harmonization:**
  - Adjusted vertical prevalence boundary from `4.5%` to `3.75%` across both scripts.
  - Positioning verification:
    - GP App Login (`3.88%`, `88.95%`), Robi App Login (`4.60%`, `87.10%`), and BL App Login (`8.12%`, `89.28%`) all cleanly reside in **Quadrant I: Urgent Crisis** ($>3.75\%$ prevalence, $>75\%$ negativity).
    - BL Offers (`4.31%`, `56.14%`), Robi Offers (`5.18%`, `50.26%`), and GP Offers (`5.27%`, `56.62%`) all cleanly reside in **Quadrant IV: Commercial Friction** ($>3.75\%$ prevalence, $<75\%$ negativity).
  - Aligned BL Offers negativity to exact ground truth: `56.14%` ($3,321 / 5,916$).
  - Adopted unified Billing card and horizontal bottom legend layout.
- **3-Venue Figure Parity & Backward Compatibility:**
  - Added multi-venue export function ensuring Figure 1, 2, 3, and 4 are written identically across `paper/figures/`, `paper/eswa_latex/figures/`, and `paper/telecommunications_policy_latex/figures/`.
  - Maintained LaTeX graphic aliases (`figure1_monthly_nss_trajectory.png` and `figure2_yearly_leadership_strip.png`) with identical bytes so existing LaTeX manuscripts compile seamlessly.

---

## 4. Empirical Proof & Checksums

### 4.1 Publication Figure SHA256 Checksums (Identical across all 3 venues)
| Figure File | SHA256 Checksum (Prefix) | Size (bytes) | Status |
|---|---|---|---|
| `figure0_system_architecture.png` | `17092544561c9774...` | 717,376 | Synchronized across 3 venues |
| `figure1_longitudinal_nss_trajectory.png` | `b3c0d02aaedc66be...` | 677,943 | Synchronized across 3 venues |
| `figure1_monthly_nss_trajectory.png` (alias) | `b3c0d02aaedc66be...` | 677,943 | Synchronized across 3 venues |
| `figure2_annual_leadership_strip.png` | `905cb27c4487d93e...` | 191,113 | Synchronized across 3 venues |
| `figure2_yearly_leadership_strip.png` (alias) | `905cb27c4487d93e...` | 191,113 | Synchronized across 3 venues |
| `figure3_priority_matrix.png` | `81a14d54c0a5c64b...` | 515,264 | Synchronized across 3 venues |
| `figure4_banglalink_reversal_decomposition.png` | `620339a28ec76fea...` | 250,329 | Synchronized across 3 venues |

### 4.2 Two-Panel Figure 6-Way Parity Checksums
| File Path | SHA256 Checksum (Prefix) | Status |
|---|---|---|
| `paper/figures/monthly_nss_trend_modern_era.png` | `b8d496436e1bf269...` | Verified match |
| `paper/figures/monthly_nss_trend_2020_2026.png` | `b8d496436e1bf269...` | Verified match |
| `assets/plots/monthly_nss_trend_modern_era.png` | `b8d496436e1bf269...` | Verified match |
| `assets/plots/monthly_nss_trend_2020_2026.png` | `b8d496436e1bf269...` | Verified match |
| `scraped_data_global/plots/monthly_nss_trend_modern_era.png` | `b8d496436e1bf269...` | Verified match |
| `scraped_data_global/plots/monthly_nss_trend_2020_2026.png` | `b8d496436e1bf269...` | Verified match |

---

## 5. Deviations from Plan

None. Execution followed all instructions in `1-PLAN.md` with zero deviations. (Note: in the verify block of Task 2, `assert` inside a list comprehension was replaced with `all(...)` to adhere to standard Python syntax while executing the exact identical assertion check).

---

## 6. Next Steps

Proceed to Phase 8 Plan 2 (`2-PLAN.md`):
- Active ESWA manuscript text, tables, and econometric/statistical reconciliation.
- Aligning manuscript claims with `paper_empirical_ground_truth.json`.
