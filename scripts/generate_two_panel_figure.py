import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# Set style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Times']
plt.rcParams['mathtext.fontset'] = 'cm'

# 1. Load data
df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['ym'] = df['review_date'].str[:7]
modern = df[df['ym'].between('2020-01', '2026-09')].copy()

# Compute monthly NSS
monthly = modern.groupby(['operator', 'ym'])['predicted_sentiment'].value_counts().unstack(fill_value=0)
for col in ['Positive', 'Negative', 'Neutral']:
    if col not in monthly.columns: monthly[col] = 0
monthly['total'] = monthly['Positive'] + monthly['Negative'] + monthly['Neutral']
monthly['nss'] = ((monthly['Positive'] - monthly['Negative']) / monthly['total']) * 100.0

months = sorted(modern['ym'].unique())
gp_nss = [monthly.loc[('Grameenphone', m)]['nss'] if ('Grameenphone', m) in monthly.index else np.nan for m in months]
robi_nss = [monthly.loc[('Robi', m)]['nss'] if ('Robi', m) in monthly.index else np.nan for m in months]
bl_nss = [monthly.loc[('Banglalink', m)]['nss'] if ('Banglalink', m) in monthly.index else np.nan for m in months]

# 2. Setup Figure with 2 Panels (Panel A top, Panel B bottom with 2 subplots)
# Compact height: 5.9 inches
fig = plt.figure(figsize=(11.5, 5.9), dpi=300)
gs = GridSpec(2, 2, height_ratios=[1.05, 0.95], hspace=0.38, wspace=0.22)

ax_a = fig.add_subplot(gs[0, :])
ax_b1 = fig.add_subplot(gs[1, 0])
ax_b2 = fig.add_subplot(gs[1, 1])

# -------------------------------------------------------------
# PANEL A: Longitudinal Monthly NSS (2020-2026)
# -------------------------------------------------------------
c_gp = '#0072B2'   # Blue
c_robi = '#D55E00' # Vermillion / Red
c_bl = '#E69F00'   # Amber / Orange

xs = np.arange(len(months))
ax_a.plot(xs, robi_nss, color=c_robi, lw=1.6, marker='s', markersize=3.2, label='Robi (My Robi · RMSSD = 5.61)', alpha=0.9)
ax_a.plot(xs, gp_nss, color=c_gp, lw=1.6, marker='o', markersize=3.2, label='Grameenphone (MyGP · RMSSD = 6.28)', alpha=0.9)
ax_a.plot(xs, bl_nss, color=c_bl, lw=2.0, marker='^', markersize=3.8, label='Banglalink (MyBL · RMSSD = 13.61)', alpha=0.95)

# Highlight Spring 2024 shock
m_mar24_idx = months.index('2024-03')
m_may24_idx = months.index('2024-05')
ax_a.axvspan(m_mar24_idx - 0.4, m_may24_idx + 0.4, color='#FFDD88', alpha=0.35, zorder=1)
ax_a.annotate('Spring 2024 Shock Episode\n(v11.8.0 Crash & Hotfix Surge)', 
            xy=(m_mar24_idx + 0.5, 33), xytext=(m_mar24_idx - 14, 20),
            arrowprops=dict(arrowstyle='->', lw=0.9, color='#B86200'),
            fontsize=8.0, fontweight='bold', color='#8A4B00',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF7E6', edgecolor='#E69F00', alpha=0.9))

# Styling Panel A
ax_a.set_title('(a) Monthly Net Sentiment Score (NSS) by Operator, 2020–2026 (81 Months, N = 634,992)', 
               fontsize=9.8, fontweight='bold', loc='left', pad=4)
ax_a.set_ylabel('NSS (%)', fontsize=8.8, fontweight='bold')
ax_a.set_ylim(15, 95)
ax_a.set_xlim(-0.8, len(months) - 0.2)

# X ticks every 6 months
tick_step = 6
tick_indices = list(range(0, len(months), tick_step))
if tick_indices[-1] != len(months) - 1:
    tick_indices.append(len(months) - 1)
ax_a.set_xticks(tick_indices)
ax_a.set_xticklabels([months[i] for i in tick_indices], rotation=0, fontsize=8.0)
ax_a.grid(True, linestyle=':', alpha=0.55)
ax_a.legend(loc='lower left', ncol=3, frameon=True, facecolor='white', framealpha=0.9, edgecolor='#CCCCCC', fontsize=8.0)

# -------------------------------------------------------------
# PANEL B1: Banglalink Spring 2024 Build Version Telemetry
# -------------------------------------------------------------
b1_data = [
    ('v11.7.1', 'Mar', 42.9, 30.5, 55.4, '#2B7A78', 'o'),
    ('Other', 'Mar', 42.0, 31.2, 52.7, '#888888', 's'),
    ('Unversioned', 'Mar', 43.0, 37.0, 49.0, '#3AAFA9', '^'),
    
    ('v11.8.0 (Crash)', 'Apr', -7.6, -22.3, 7.1, '#D90429', 'X'),
    ('v11.9.1 (Early)', 'Apr', 40.5, 25.5, 55.5, '#457B9D', 'D'),
    ('Other', 'Apr', 42.7, 31.2, 54.2, '#888888', 's'),
    ('Unversioned', 'Apr', 35.3, 29.4, 41.1, '#3AAFA9', '^'),
    
    ('v11.9.1 (Hotfix)', 'May', 77.0, 72.9, 81.0, '#1D3557', 'D'),
    ('v11.10.x', 'May', 22.1, 6.1, 38.2, '#E76F51', 'p'),
    ('Other', 'May', 56.8, 42.7, 70.8, '#888888', 's'),
    ('Unversioned', 'May', 62.3, 58.4, 66.1, '#3AAFA9', '^'),
]

month_groups = {'Mar': 0.8, 'Apr': 2.3, 'May': 3.8}
x_offsets = {
    'Mar': [-0.25, 0.0, 0.25],
    'Apr': [-0.36, -0.12, 0.12, 0.36],
    'May': [-0.36, -0.12, 0.12, 0.36]
}

idx_m = {'Mar': 0, 'Apr': 0, 'May': 0}
for label, m, nss, ci_l, ci_h, col, marker in b1_data:
    x_pos = month_groups[m] + x_offsets[m][idx_m[m]]
    idx_m[m] += 1
    
    err_low = nss - ci_l
    err_high = ci_h - nss
    
    ax_b1.errorbar(x_pos, nss, yerr=[[err_low], [err_high]], fmt=marker, color=col,
                   ecolor=col, elinewidth=1.4, capsize=3.0, capthick=1.2, markersize=5.5, zorder=4)

ax_b1.axhline(0, color='#333333', linestyle='--', lw=0.8, alpha=0.7)
ax_b1.axhspan(-26, 0, color='#FFEAEA', alpha=0.4, zorder=1)

ax_b1.annotate('v11.8.0 Crash\n-7.6 [-22, +7]', 
               xy=(month_groups['Apr'] - 0.36, -7.6), xytext=(0.5, -22),
               arrowprops=dict(arrowstyle='->', lw=0.9, color='#D90429'),
               fontsize=7.2, fontweight='bold', color='#D90429',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF0F0', edgecolor='#D90429', alpha=0.9))

ax_b1.annotate('v11.9.1 Hotfix: +77.0\nParallel Rebound (+57 to +62)', 
               xy=(month_groups['May'] - 0.36, 77.0), xytext=(1.8, 79),
               arrowprops=dict(arrowstyle='->', lw=0.9, color='#1D3557'),
               fontsize=7.2, fontweight='bold', color='#1D3557',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0F4F8', edgecolor='#1D3557', alpha=0.9))

ax_b1.set_title('(b) Build Telemetry: v11.8.0 Crash vs. Hotfix (NSS [95% CI])', 
                fontsize=8.8, fontweight='bold', loc='left', pad=4)
ax_b1.set_xticks([0.8, 2.3, 3.8])
ax_b1.set_xticklabels(['March 2024\n(+42.8 baseline)', 'April 2024\n(-11.2 shock)', 'May 2024\n(+32.8 rebound)'], fontsize=8.0)
ax_b1.set_ylabel('Cohort NSS (%)', fontsize=8.5, fontweight='bold')
ax_b1.set_ylim(-26, 95)
ax_b1.set_xlim(0.3, 4.3)
ax_b1.grid(True, linestyle=':', alpha=0.55)

# -------------------------------------------------------------
# PANEL B2: Review Volume Confound & Cohort Shares
# -------------------------------------------------------------
months_b2 = ['March 2024', 'April 2024', 'May 2024']
vol_unversioned = [718, 851, 1317]
vol_focal_build = [170, 158 + 121, 708 + 122]
vol_legacy = [205, 185, 118]

x_b2 = np.arange(len(months_b2))
bar_w = 0.48

p1 = ax_b2.bar(x_b2, vol_unversioned, bar_w, label='Unversioned Cohort (58–66%)', color='#3AAFA9', alpha=0.85, edgecolor='white')
p2 = ax_b2.bar(x_b2, vol_focal_build, bar_w, bottom=vol_unversioned, label='Focal Builds (v11.8.0 / v11.9.1)', color='#1D3557', alpha=0.85, edgecolor='white')
bottom_legacy = [vol_unversioned[i] + vol_focal_build[i] for i in range(3)]
p3 = ax_b2.bar(x_b2, vol_legacy, bar_w, bottom=bottom_legacy, label='Other Active Versions', color='#AAAAAA', alpha=0.85, edgecolor='white')

totals = [1093, 1315, 2265]
for i, tot in enumerate(totals):
    surge_lbl = "\n(+72.2% surge)" if i == 2 else ("\n(+20.3%)" if i == 1 else "\n(Baseline)")
    ax_b2.text(i, tot + 30, f"N={tot:,}{surge_lbl}", ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#222222')

ax_b2.set_title('(c) Volume Surge Confound: Monthly Review Distribution', 
                fontsize=8.8, fontweight='bold', loc='left', pad=4)
ax_b2.set_xticks(x_b2)
ax_b2.set_xticklabels(months_b2, fontsize=8.0)
ax_b2.set_ylabel('Review Count (N)', fontsize=8.5, fontweight='bold')
ax_b2.set_ylim(0, 2750)
ax_b2.grid(True, linestyle=':', alpha=0.55, axis='y')
ax_b2.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9, edgecolor='#CCCCCC', fontsize=7.2)

fig_path = 'paper/journal_manuscript/figures/monthly_nss_trend_modern_era.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
# Also save backward-compatible copy and update assets/plots
plt.savefig('paper/journal_manuscript/figures/monthly_nss_trend_2020_2026.png', dpi=300, bbox_inches='tight')
plt.savefig('assets/plots/monthly_nss_trend_modern_era.png', dpi=300, bbox_inches='tight')
plt.savefig('scraped_data_global/plots/monthly_nss_trend_modern_era.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"Compact two-panel figure saved to: {fig_path}")
