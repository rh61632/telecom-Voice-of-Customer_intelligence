from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from PIL import Image

out_dir = Path("paper/figures")
out_dir.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['DejaVu Serif', 'Times New Roman', 'Cambria', 'Georgia']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12.5
plt.rcParams['xtick.labelsize'] = 9.5
plt.rcParams['ytick.labelsize'] = 9.5

BRAND_COLORS = {
    'Grameenphone': '#0090ff',  # GP Electric Blue
    'Robi': '#e60000',          # Robi Vibrant Red
    'Banglalink': '#ff7a00',    # BL Vibrant Orange
    'Industry': '#333333'       # Dark Slate
}

df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['ym'] = df['review_date'].str[:7]

monthly = df.groupby(['operator', 'ym'])['predicted_sentiment'].apply(
    lambda x: ((x == 'Positive').sum() - (x == 'Negative').sum()) / len(x) * 100.0 if len(x) >= 30 else np.nan
).unstack(level='operator')

all_months = sorted(df['ym'].unique())
monthly = monthly.reindex(all_months)

fig, ax = plt.subplots(figsize=(14.0, 6.8), dpi=300)

# Plot lines
for op, style, marker in [('Grameenphone', '-', 'o'), 
                          ('Robi', '--', 's'), 
                          ('Banglalink', '-.', '^')]:
    series = monthly[op]
    valid_idx = series.dropna().index
    x_indices = [all_months.index(m) for m in valid_idx]
    y_values = series.dropna().values
    
    ax.plot(x_indices, y_values, label=f"{op}", color=BRAND_COLORS[op],
            linestyle=style, linewidth=2.2, marker=marker, markersize=4.2, alpha=0.92, zorder=3)

# Baseline
ax.axhline(0, color='#64748b', linestyle=':', linewidth=1.2, alpha=0.8, zorder=2)

# Milestones configuration:
milestones = [
    {
        'ym': '2018-02',
        'label': '4G Commercial Launch\n(19 Feb 2018)',
        'xy': (all_months.index('2018-02'), 32),
        'xytext': (all_months.index('2018-02'), 82),
        'ha': 'center', 'va': 'center',
        'fc': '#eff6ff', 'ec': '#3b82f6', 'tc': '#1e3a8a'
    },
    {
        'ym': '2020-03',
        'label': 'COVID-19 Onset\n(Mar 2020)',
        'xy': (all_months.index('2020-03'), 15),
        'xytext': (all_months.index('2020-03'), -48),
        'ha': 'center', 'va': 'center',
        'fc': '#ecfdf5', 'ec': '#10b981', 'tc': '#065f46'
    },
    {
        'ym': '2024-04',
        'label': 'BL v11.8 Crash & Hotfix\n(Apr–May 2024)',
        'xy': (all_months.index('2024-04'), 25),
        'xytext': (all_months.index('2024-04'), -48),
        'ha': 'center', 'va': 'center',
        'fc': '#fff7ed', 'ec': '#ea580c', 'tc': '#9a3412'
    },
    {
        'ym': '2025-09',
        'label': '5G Commercial Launch\n(1 Sep 2025)',
        'xy': (all_months.index('2025-09'), 75),
        'xytext': (all_months.index('2025-09'), 104),
        'ha': 'center', 'va': 'center',
        'fc': '#f5f3ff', 'ec': '#8b5cf6', 'tc': '#4c1d95'
    }
]

for m_info in milestones:
    idx = all_months.index(m_info['ym'])
    ax.axvline(idx, color='#94a3b8', linestyle='--', linewidth=1.1, alpha=0.65, zorder=1)
    
    ax.annotate(
        m_info['label'],
        xy=m_info['xy'],
        xytext=m_info['xytext'],
        fontsize=8.8, fontweight='bold', color=m_info['tc'],
        ha=m_info['ha'], va=m_info['va'],
        bbox=dict(boxstyle='round,pad=0.38', facecolor=m_info['fc'], edgecolor=m_info['ec'], lw=1.2, alpha=0.96),
        arrowprops=dict(arrowstyle='->', color=m_info['ec'], lw=1.3, shrinkA=3, shrinkB=3),
        zorder=5
    )

# Place legend outside at top, centered between title and plot
ax.legend(
    loc='lower center',
    bbox_to_anchor=(0.5, 1.01),
    ncol=3,
    frameon=True, framealpha=0.96,
    edgecolor='#94a3b8',
    facecolor='white',
    fontsize=9.8,
    borderpad=0.5
)

# Formatting X ticks
tick_indices = [i for i, m in enumerate(all_months) if m.endswith('-01') or i == 0 or i == len(all_months)-1]
tick_labels = [all_months[i] for i in tick_indices]
ax.set_xticks(tick_indices)
ax.set_xticklabels(tick_labels, rotation=35, ha='right', fontsize=9.5)

ax.set_xlabel('Calendar Month (July 2016 to September 2026, N >= 30 Monthly Floor)', labelpad=8)
ax.set_ylabel('Net Sentiment Score (NSS)', labelpad=8)
ax.set_ylim(-75, 126)
ax.grid(True, linestyle=':', alpha=0.5, zorder=1)

plt.title('Figure 1: Ten-Year Monthly Net Sentiment Score (NSS) Trajectory across Bangladeshi Operators', pad=32, fontweight='bold', fontsize=12.5)
plt.tight_layout()
fig.savefig(out_dir / "figure1_monthly_nss_trajectory.png")
plt.close(fig)
print("Successfully regenerated Figure 1 with external top legend and clean offsets!")

# Crop checks
img = Image.open('paper/figures/figure1_monthly_nss_trajectory.png')
w, h = img.size

# 4G
crop_4g = img.crop((int(0.12 * w), int(0.10 * h), int(0.32 * w), int(0.40 * h)))
crop_4g.save('paper/figures/crop_4g_check.png')

# COVID
crop_covid = img.crop((int(0.30 * w), int(0.68 * h), int(0.46 * w), int(0.96 * h)))
crop_covid.save('paper/figures/crop_covid_check.png')

# BL
crop_bl = img.crop((int(0.68 * w), int(0.68 * h), int(0.86 * w), int(0.96 * h)))
crop_bl.save('paper/figures/crop_bl_check.png')

# 5G
crop_5g = img.crop((int(0.80 * w), int(0.08 * h), int(0.98 * w), int(0.35 * h)))
crop_5g.save('paper/figures/crop_5g_check.png')

print("All crop checks saved.")
