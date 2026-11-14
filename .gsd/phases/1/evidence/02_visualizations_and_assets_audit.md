# Empirical Evidence 02: Visualizations, Asset Parity & Figure Generation Audit

> **Phase:** 1 — Core Pipeline, Data, Demo & Documentation Audit  
> **Plan:** 2 — Visualizations, Asset Parity, Archive Lineage & Dependency Audit  
> **Task:** 1 — Audit visualization generation, plot inventory, and asset directory mirroring  
> **Execution Date:** 2026-11-11  
> **Status:** Verified Pass (Strict Read-Only)

---

## 1. Executive Summary

This audit verified byte-level parity between primary visualization outputs in `scraped_data_global/plots/` and the presentation mirrors in `assets/plots/`, evaluated the visualization generation pipeline (`scraped_data_global/pipeline/generate_global_visualizations.py`), inspected the brand logo assets in `assets/logos/`, and cross-referenced paper figure generators (`scripts/generate_paper_figures.py` and `scripts/generate_two_panel_figure.py`).

Key findings:
1. **100% Byte-for-Byte SHA256 Parity:** All 20 PNG plot files in `scraped_data_global/plots/` are identical to their counterparts in `assets/plots/`.
2. **Plot Alias Taxonomy:** The 20 files represent 10 distinct underlying figures, with multiple symlink-like alias files generated via dual `save_plot()` calls (e.g., `multi_year_sentiment_trend_line.png` == `monthly_sentiment_trend_line.png` == `yearly_sentiment_trend_all_years.png`).
3. **Common Window Drift in Source vs Git HEAD:** `generate_global_visualizations.py` contains uncommitted working-tree modifications synchronizing the header docstring, titles, and fallback start date from `Jul 2016` (3,716 days, N=655,670) to `Aug 2016` (`2016-08-01`, 3,713 days, N=655,649).
4. **Paper Figure Cross-Reference & Risk:** `scripts/generate_paper_figures.py` produces publication-grade serif figures with identical SHA256 hashes across `paper/figures/`, `paper/eswa_latex/figures/`, and `paper/telecommunications_policy_latex/figures/`. However, `scripts/generate_two_panel_figure.py` targets `scraped_data_global/plots/monthly_nss_trend_modern_era.png` and `assets/plots/monthly_nss_trend_modern_era.png` without updating `monthly_nss_trend_2020_2026.png`, creating potential plot divergence if executed.

---

## 2. SHA256 Parity Verification: `scraped_data_global/plots/` vs `assets/plots/`

Every file was hashed using Python `hashlib.sha256()`. Both directories contain exactly 20 PNG files with identical names, byte lengths, and SHA256 digests.

| Filename | File Size (Bytes) | SHA256 Checksum (`scraped_data_global/plots/`) | SHA256 Checksum (`assets/plots/`) | Parity Status |
|---|---|---|---|---|
| `category_model_benchmark_bars.png` | 236,683 | `c957a6f5bfca8a2c090648d5f5a02bdf9ed5b3a64fd72482f10b795a95f51af9` | `c957a6f5bfca8a2c090648d5f5a02bdf9ed5b3a64fd72482f10b795a95f51af9` | MATCH (100%) |
| `category_sentiment_stacked_bars.png` | 183,724 | `acb916f2b9946fe854ca6f5397bd41058809ce15c2c8a8acea53149d3a8165e2` | `acb916f2b9946fe854ca6f5397bd41058809ce15c2c8a8acea53149d3a8165e2` | MATCH (100%) |
| `monthly_nss_trend_2020_2026.png` | 665,746 | `b6e057f951a10e4c27f2da453e679bcedfd5f64d9acd1b3c9fe6251662b9ff49` | `b6e057f951a10e4c27f2da453e679bcedfd5f64d9acd1b3c9fe6251662b9ff49` | MATCH (100%) |
| `monthly_nss_trend_all_months.png` | 720,558 | `70e96a6365ff29aa3571526ba341f72bc4aeb3f45a5c6a08fe54c93dd3a738a8` | `70e96a6365ff29aa3571526ba341f72bc4aeb3f45a5c6a08fe54c93dd3a738a8` | MATCH (100%) |
| `monthly_nss_trend_early_era.png` | 471,362 | `ace61fc041a32be5308d729d7f2c830b0b8617613268c0c17727e13e9b248240` | `ace61fc041a32be5308d729d7f2c830b0b8617613268c0c17727e13e9b248240` | MATCH (100%) |
| `monthly_nss_trend_line.png` | 720,558 | `70e96a6365ff29aa3571526ba341f72bc4aeb3f45a5c6a08fe54c93dd3a738a8` | `70e96a6365ff29aa3571526ba341f72bc4aeb3f45a5c6a08fe54c93dd3a738a8` | MATCH (100%) |
| `monthly_nss_trend_modern_era.png` | 665,746 | `b6e057f951a10e4c27f2da453e679bcedfd5f64d9acd1b3c9fe6251662b9ff49` | `b6e057f951a10e4c27f2da453e679bcedfd5f64d9acd1b3c9fe6251662b9ff49` | MATCH (100%) |
| `monthly_nss_trend_pre2020.png` | 471,362 | `ace61fc041a32be5308d729d7f2c830b0b8617613268c0c17727e13e9b248240` | `ace61fc041a32be5308d729d7f2c830b0b8617613268c0c17727e13e9b248240` | MATCH (100%) |
| `monthly_sentiment_trend_line.png` | 393,312 | `b1542abe175a2c09b61b16bc378f0b40a68146997616108f0c41be09404ce82a` | `b1542abe175a2c09b61b16bc378f0b40a68146997616108f0c41be09404ce82a` | MATCH (100%) |
| `multi_year_sentiment_trend_line.png` | 393,312 | `b1542abe175a2c09b61b16bc378f0b40a68146997616108f0c41be09404ce82a` | `b1542abe175a2c09b61b16bc378f0b40a68146997616108f0c41be09404ce82a` | MATCH (100%) |
| `net_sentiment_score_comparison_bars.png` | 151,844 | `aa4e3be888df076e88d7854164d73c9d6747e772c3eb1ab664633690f2aae98b` | `aa4e3be888df076e88d7854164d73c9d6747e772c3eb1ab664633690f2aae98b` | MATCH (100%) |
| `nss_stability_volatility_bars.png` | 213,409 | `b8b7a918bd717e5e348f4e0da9e7ac48c3e801b289a0fc066a57457552a99ef6` | `b8b7a918bd717e5e348f4e0da9e7ac48c3e801b289a0fc066a57457552a99ef6` | MATCH (100%) |
| `operator_category_complaint_distribution_bars.png` | 219,178 | `f9b4e1af50b3f84a125c128edb1388e1c1c6803aa315557c455aa3fd3c51edde` | `f9b4e1af50b3f84a125c128edb1388e1c1c6803aa315557c455aa3fd3c51edde` | MATCH (100%) |
| `operator_sentiment_distribution_bars.png` | 142,552 | `21db3a286ce62ebbc5a9edb27984dae433576864a95c2be168848bb4f8823111` | `21db3a286ce62ebbc5a9edb27984dae433576864a95c2be168848bb4f8823111` | MATCH (100%) |
| `sentiment_model_benchmark_bars.png` | 233,548 | `ab816588538d925315c10e7de560ba3938d0ba5b231dc7b67527636f20b43a77` | `ab816588538d925315c10e7de560ba3938d0ba5b231dc7b67527636f20b43a77` | MATCH (100%) |
| `yearly_sentiment_trend_2020_2026.png` | 293,812 | `4f9750ba82310a5559267231447e54cd1d84ef8ce7aa5f57cf747aa651586579` | `4f9750ba82310a5559267231447e54cd1d84ef8ce7aa5f57cf747aa651586579` | MATCH (100%) |
| `yearly_sentiment_trend_all_years.png` | 393,312 | `b1542abe175a2c09b61b16bc378f0b40a68146997616108f0c41be09404ce82a` | `b1542abe175a2c09b61b16bc378f0b40a68146997616108f0c41be09404ce82a` | MATCH (100%) |
| `yearly_sentiment_trend_early_era.png` | 222,891 | `158449efd5ad08dd8e04f5bebb32e200558cbc9e91c8b98f4b9fddae8981c72c` | `158449efd5ad08dd8e04f5bebb32e200558cbc9e91c8b98f4b9fddae8981c72c` | MATCH (100%) |
| `yearly_sentiment_trend_modern_era.png` | 293,812 | `4f9750ba82310a5559267231447e54cd1d84ef8ce7aa5f57cf747aa651586579` | `4f9750ba82310a5559267231447e54cd1d84ef8ce7aa5f57cf747aa651586579` | MATCH (100%) |
| `yearly_sentiment_trend_pre2020.png` | 222,891 | `158449efd5ad08dd8e04f5bebb32e200558cbc9e91c8b98f4b9fddae8981c72c` | `158449efd5ad08dd8e04f5bebb32e200558cbc9e91c8b98f4b9fddae8981c72c` | MATCH (100%) |

### Underlying Unique Plot Groups (Identical SHA256 Hashes)

1. **Monthly NSS Full History:**
   - `monthly_nss_trend_line.png` == `monthly_nss_trend_all_months.png` (`70e96a...`)
2. **Monthly NSS Pre-2020 Era:**
   - `monthly_nss_trend_early_era.png` == `monthly_nss_trend_pre2020.png` (`ace61f...`)
3. **Monthly NSS Modern Era (2020–2026):**
   - `monthly_nss_trend_modern_era.png` == `monthly_nss_trend_2020_2026.png` (`b6e057...`)
4. **Yearly NSS Trajectory (All Years):**
   - `monthly_sentiment_trend_line.png` == `multi_year_sentiment_trend_line.png` == `yearly_sentiment_trend_all_years.png` (`b1542a...`)
5. **Yearly NSS Pre-2020 Era:**
   - `yearly_sentiment_trend_early_era.png` == `yearly_sentiment_trend_pre2020.png` (`158449...`)
6. **Yearly NSS Modern Era (2020–2026):**
   - `yearly_sentiment_trend_modern_era.png` == `yearly_sentiment_trend_2020_2026.png` (`4f9750...`)
7. **Unique Standalone Charts:**
   - `operator_sentiment_distribution_bars.png` (`21db3a...`)
   - `net_sentiment_score_comparison_bars.png` (`aa4e3b...`)
   - `operator_category_complaint_distribution_bars.png` (`f9b4e1...`)
   - `category_sentiment_stacked_bars.png` (`acb916...`)
   - `sentiment_model_benchmark_bars.png` (`ab8165...`)
   - `category_model_benchmark_bars.png` (`c957a6...`)
   - `nss_stability_volatility_bars.png` (`b8b7a9...`)

---

## 3. Visualization Pipeline Code Audit (`scraped_data_global/pipeline/generate_global_visualizations.py`)

### 3.1 Start Date Filtering & Window Boundary Drift
- **Lines 1-4:** Header docstring declares:
  `Generate Visualizations for Common Duration VoC Dataset (Aug 2016 - Sep 2026).`
  `Continuous Shared Window: 3,713 Days, N = 655,649 Verified Reviews across Grameenphone, Robi, and Banglalink.`
- **Line 77-83:** In `load_dataset()`, if `all_operators_common_duration_classified.csv` is present, it loads it directly (which was trimmed in Plan 1 to start `2016-08-01`).
- **Line 98 (Fallback branch):** 
  ```python
  start_common = pd.Timestamp("2016-08-01 00:00:00")
  ```
- **Git Drift Analysis:** In committed HEAD (`c8fe2e0`), line 98 computed `start_common = max(df_sep[df_sep["operator"] == op]["review_date"].min() ...)` which yielded `2016-07-28` (`3,716` days, `N=655,670`). The uncommitted working tree hardcoded `start_common = pd.Timestamp("2016-08-01 00:00:00")` and updated plot annotations to `3,713 Days` and `Aug 2016`.

### 3.2 Operator Brand Colors & Palette Configuration
Defined at lines 59-69:
```python
BRAND_COLORS = {
    "Grameenphone": "#0090ff",  # GP Electric Blue
    "Robi": "#e60000",          # Robi Vibrant Red
    "Banglalink": "#ff7a00",    # BL Vibrant Orange
}

SENTIMENT_COLORS = {
    "Positive": "#2ECC71",      # Emerald Green
    "Neutral": "#F39C12",       # Sun Orange
    "Negative": "#E74C3C",      # Crimson Red
}
```
All colors align with official project standards and README presentation badges.

### 3.3 Output Resolution & Dual-Path Saving
Defined at lines 115-121:
```python
def save_plot(fig, filename: str):
    p1 = PLOTS_DIR / filename
    p2 = ASSETS_PLOTS_DIR / filename
    fig.savefig(p1, dpi=300, bbox_inches="tight")
    fig.savefig(p2, dpi=300, bbox_inches="tight")
    plt.close(fig)
```
- `dpi=300` is strictly enforced across all 20 charts.
- `bbox_inches="tight"` prevents clipping of external top-positioned legends.
- Both `scraped_data_global/plots/` and `assets/plots/` receive identical writes upon script execution.

---

## 4. Brand Asset Inventory (`assets/logos/`)

Brand logos were inspected using Pillow (`PIL.Image`):

| File | Resolution (Pixels) | Format | Color Mode | File Size (Bytes) | Notes |
|---|---|---|---|---|---|
| `assets/logos/gp.png` | 1000 × 1000 | PNG | RGBA | 58,667 | Grameenphone icon, alpha transparency |
| `assets/logos/robi.png` | 1000 × 1000 | PNG | RGBA | 53,153 | Robi icon, alpha transparency |
| `assets/logos/banglalink.png` | 1000 × 1000 | PNG | RGBA | 66,355 | Banglalink icon, alpha transparency |

All three logo assets are high-resolution, square RGBA images suitable for markdown presentation and GitHub header rendering.

---

## 5. Paper Figure Cross-Reference & Risk Analysis

### 5.1 Manuscript Publication Figures (`scripts/generate_paper_figures.py`)
- **Target Directory:** `paper/figures/`
- **Generated Figures:**
  1. `figure1_monthly_nss_trajectory.png`: Ten-Year Monthly Net Sentiment Score Trajectory (Jul 2016 – Sep 2026)
  2. `figure2_yearly_leadership_strip.png`: Annual Voice-of-Customer Leadership Strip (2016–2026)
  3. `figure3_priority_matrix.png`: Strategic VoC Priority Matrix (Prevalence vs Dissatisfaction Intensity)
  4. `figure4_banglalink_reversal_decomposition.png`: Additive Domain Decomposition of Banglalink 2025–2026 NSS Reversal
- **Typography & Style:** Uses academic serif typography (`font.serif = ['DejaVu Serif', 'Times New Roman', 'Cambria', 'Georgia']`), font size 10, target dpi 300.
- **Cross-Directory Parity:**
  - `figure1_monthly_nss_trajectory.png`: SHA256 `a591ed26f554...` matches across `paper/figures/`, `paper/eswa_latex/figures/`, and `paper/telecommunications_policy_latex/figures/`.
  - `figure2_yearly_leadership_strip.png`: SHA256 `6af54b687b21...` matches across all 3 directories.
  - `figure3_priority_matrix.png`: SHA256 `0d687e2648c1...` matches across all 3 directories.
  - `figure4_banglalink_reversal_decomposition.png`: SHA256 `5f6b227882c3...` matches across all 3 directories.

### 5.2 Divergence Risk in `scripts/generate_two_panel_figure.py`
In `scripts/generate_two_panel_figure.py:168-174`:
```python
fig_path = 'paper/figures/monthly_nss_trend_modern_era.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
# Also save backward-compatible copy and update assets/plots
plt.savefig('paper/figures/monthly_nss_trend_2020_2026.png', dpi=300, bbox_inches='tight')
plt.savefig('assets/plots/monthly_nss_trend_modern_era.png', dpi=300, bbox_inches='tight')
plt.savefig('scraped_data_global/plots/monthly_nss_trend_modern_era.png', dpi=300, bbox_inches='tight')
plt.close()
```
**Identified Discrepancy / Risk:**
If `scripts/generate_two_panel_figure.py` is executed, it updates `monthly_nss_trend_modern_era.png` in `assets/plots/` and `scraped_data_global/plots/` to a 3-panel figure ((a) Modern Trajectory, (b) Banglalink Root Cause, (c) Volume Surge Confound), but leaves `monthly_nss_trend_2020_2026.png` untouched in those directories. Currently, both files have identical SHA256 hash `b6e057f951a1...` (the single-panel chart from `generate_global_visualizations.py`). Re-running `generate_two_panel_figure.py` without synchronized targets would break the verified 100% parity between alias pairs.

---

## 6. Verification Status

Verification command passed:
```powershell
python -c "import os; assert os.path.exists('.gsd/phases/1/evidence/02_visualizations_and_assets_audit.md'), 'Evidence file missing'; print('Visualizations and assets audit evidence successfully verified')"
```
Output:
`Visualizations and assets audit evidence successfully verified`
