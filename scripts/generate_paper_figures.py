"""
generate_paper_figures.py
Generates the 4 publication-grade figures for the JBA paper:
1. Figure 1: Ten-Year Monthly Net Sentiment Score Trajectory (Jul 2016 - Sep 2026)
2. Figure 2: Annual Voice-of-Customer Leadership Strip (2016-2026)
3. Figure 3: Strategic VoC Priority Matrix (Prevalence vs Dissatisfaction Intensity)
4. Figure 4: Additive Domain Decomposition of Banglalink 2025-2026 NSS Reversal

Colors strictly follow official project standards:
- Grameenphone: #0090ff (GP Electric Blue)
- Robi: #e60000 (Robi Vibrant Red)
- Banglalink: #ff7a00 (BL Vibrant Orange)
- Sentiment Positive: #2ECC71 (Emerald Green)
- Sentiment Neutral: #F39C12 (Sun Orange)
- Sentiment Negative: #E74C3C (Crimson Red)
- Industry / Neutral: #333333 / #666666
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

output_dirs = [
    Path("paper/figures"),
    Path("paper/eswa_latex/figures"),
    Path("paper/telecommunications_policy_latex/figures")
]
for d in output_dirs:
    d.mkdir(parents=True, exist_ok=True)

def save_figure_to_all(fig, filename_primary, filename_alias=None, pad_inches=0.12):
    p0 = output_dirs[0] / filename_primary
    fig.savefig(p0, bbox_inches='tight', pad_inches=pad_inches, dpi=300)
    plt.close(fig)
    img_b = p0.read_bytes()
    for d in output_dirs:
        (d / filename_primary).write_bytes(img_b)
        if filename_alias:
            (d / filename_alias).write_bytes(img_b)

# Typography & styling
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['DejaVu Serif', 'Times New Roman', 'Cambria', 'Georgia']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12.5
plt.rcParams['xtick.labelsize'] = 9.5
plt.rcParams['ytick.labelsize'] = 9.5
plt.rcParams['legend.fontsize'] = 9.8

# Official Project Brand Colors (from README.md & generate_global_visualizations.py)
BRAND_COLORS = {
    'Grameenphone': '#0090ff',  # GP Electric Blue
    'Robi': '#e60000',          # Robi Vibrant Red
    'Banglalink': '#ff7a00',    # BL Vibrant Orange
    'Industry': '#333333'       # Dark Slate Industry Benchmark
}

SENTIMENT_COLORS = {
    'Positive': '#2ECC71',      # Emerald Green
    'Neutral': '#F39C12',       # Sun Orange
    'Negative': '#E74C3C'       # Crimson Red
}

# -------------------------------------------------------------
# 1. Figure 1: Monthly NSS Trajectory (2016-2026) with Shocks
# -------------------------------------------------------------
print("Generating Figure 1: Monthly NSS Trajectory (Strict Project Brand Colors & Zero-Collision Offsets)...")
df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['ym'] = df['review_date'].str[:7]

monthly = df.groupby(['operator', 'ym'])['predicted_sentiment'].apply(
    lambda x: ((x == 'Positive').sum() - (x == 'Negative').sum()) / len(x) * 100.0 if len(x) >= 30 else np.nan
).unstack(level='operator')

all_months = sorted(df['ym'].unique())
monthly = monthly.reindex(all_months)

fig, ax = plt.subplots(figsize=(14.0, 6.8), dpi=300)

# Plot lines with official project colors
for op, style, marker in [('Grameenphone', '-', 'o'), 
                          ('Robi', '--', 's'), 
                          ('Banglalink', '-.', '^')]:
    series = monthly[op]
    valid_idx = series.dropna().index
    x_indices = [all_months.index(m) for m in valid_idx]
    y_values = series.dropna().values
    
    ax.plot(x_indices, y_values, label=f"{op}", color=BRAND_COLORS[op],
            linestyle=style, linewidth=2.2, marker=marker, markersize=4.2, alpha=0.92, zorder=3)

# Zero line
ax.axhline(0, color='#64748b', linestyle=':', linewidth=1.2, alpha=0.8, zorder=2)

# Zero-collision milestone callouts
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

ax.set_xlabel('Calendar Month (August 2016 to September 2026, N >= 30 Monthly Floor)', labelpad=8)
ax.set_ylabel('Net Sentiment Score (NSS)', labelpad=8)
ax.set_ylim(-75, 126)
ax.grid(True, linestyle=':', alpha=0.5, zorder=1)

plt.title('Ten-Year Monthly Net Sentiment Score (NSS) Trajectory across Bangladeshi Operators', pad=32, fontweight='bold', fontsize=12.5)
plt.tight_layout()
save_figure_to_all(fig, "figure1_longitudinal_nss_trajectory.png", filename_alias="figure1_monthly_nss_trajectory.png", pad_inches=0.12)

# -------------------------------------------------------------
# 2. Figure 2: Decade Leadership Timeline (2016 - 2026)
# -------------------------------------------------------------
print("Generating Figure 2: Decade Leadership Strip (Strict Project Colors & Anti-Collision)...")
fig, ax = plt.subplots(figsize=(12.5, 2.8), dpi=300)

leaders = [
    (2016, 'Banglalink', '+45.3', BRAND_COLORS['Banglalink']),
    (2017, 'Banglalink', '+45.5', BRAND_COLORS['Banglalink']),
    (2018, 'Banglalink', '+22.3', BRAND_COLORS['Banglalink']),
    (2019, 'GP (Grameenphone)', '+19.6', BRAND_COLORS['Grameenphone']),
    (2020, 'Robi Axiata', '+63.6', BRAND_COLORS['Robi']),
    (2021, 'Robi Axiata', '+63.8', BRAND_COLORS['Robi']),
    (2022, 'Robi Axiata', '+68.4', BRAND_COLORS['Robi']),
    (2023, 'GP (Grameenphone)', '+69.8', BRAND_COLORS['Grameenphone']),
    (2024, 'GP (Grameenphone)', '+70.6', BRAND_COLORS['Grameenphone']),
    (2025, 'Robi Axiata', '+78.6', BRAND_COLORS['Robi']),
    (2026, 'Banglalink', '+81.9', BRAND_COLORS['Banglalink']),
]

for i, (yr, leader, nss_str, col) in enumerate(leaders):
    box = patches.FancyBboxPatch((i * 1.05 + 0.05, 0.15), 0.95, 0.72,
                                 boxstyle="round,pad=0.03,rounding_size=0.08",
                                 facecolor=col, edgecolor='#1a202c', linewidth=1.2, alpha=0.92)
    ax.add_patch(box)
    
    # Year
    ax.text(i * 1.05 + 0.525, 0.67, f"{yr}", ha='center', va='center', color='white', fontweight='bold', fontsize=10.5)
    
    # Multiline text layout for operator names preventing any card clipping
    if 'Grameenphone' in leader:
        ax.text(i * 1.05 + 0.525, 0.47, "Grameen-\nphone", ha='center', va='center', color='white', fontsize=8.0, fontweight='bold', linespacing=0.9)
    elif 'Robi' in leader:
        ax.text(i * 1.05 + 0.525, 0.47, "Robi\nAxiata", ha='center', va='center', color='white', fontsize=8.0, fontweight='bold', linespacing=0.9)
    else:
        ax.text(i * 1.05 + 0.525, 0.47, f"{leader}", ha='center', va='center', color='white', fontsize=8.5, fontweight='bold')
        
    # NSS badge
    ax.text(i * 1.05 + 0.525, 0.27, f"NSS {nss_str}", ha='center', va='center', color='#fff9c4', fontsize=8.0, fontweight='bold')

ax.set_xlim(-0.1, 11.6)
ax.set_ylim(0, 1.0)
ax.axis('off')
plt.title('Annual Voice-of-Customer Leadership Strip (2016–2026 Highest Yearly NSS Leader)', pad=10, fontweight='bold', fontsize=12)
plt.tight_layout()
save_figure_to_all(fig, "figure2_annual_leadership_strip.png", filename_alias="figure2_yearly_leadership_strip.png", pad_inches=0.12)

# -------------------------------------------------------------
# -------------------------------------------------------------
# 3. Figure 3: Strategic VoC Priority Matrix
# -------------------------------------------------------------
print("Generating Figure 3: VoC Priority Matrix (Strict Brand Colors & Anti-Collision)...")
fig, ax = plt.subplots(figsize=(12, 7.6), dpi=300)

# 1. Subtle, pastel Quadrant Background Color Fills
ax.axvspan(0, 3.75, 75/100, 1.0, color='#fff7ed', alpha=0.45, zorder=0)  # Top Left: Severe Latent Churn
ax.axvspan(3.75, 9.6, 75/100, 1.0, color='#fef2f2', alpha=0.55, zorder=0)  # Top Right: Urgent Crisis
ax.axvspan(0, 3.75, 45/100, 75/100, color='#f0fdf4', alpha=0.45, zorder=0) # Bottom Left: Secondary Operational
ax.axvspan(3.75, 9.6, 45/100, 75/100, color='#f0f9ff', alpha=0.45, zorder=0) # Bottom Right: Commercial Friction

# 2. Dividing Benchmark Lines
ax.axvline(3.75, color='#94a3b8', linestyle='--', linewidth=1.3, zorder=1)
ax.axhline(75.0, color='#94a3b8', linestyle='--', linewidth=1.3, zorder=1)

# 3. Clean Quadrant Headers placed strictly in the outer corners (Zero collision)
ax.text(9.4, 98.8, 'QUADRANT I: URGENT CRISIS\nHigh Prevalence / Severe Negativity (>75%)',
        ha='right', va='top', fontsize=8.5, fontweight='bold', color='#991b1b',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#fee2e2', edgecolor='#f87171', lw=0.8, alpha=0.9))

ax.text(0.18, 98.8, 'QUADRANT II: SEVERE LATENT CHURN\nLow Prevalence / Extreme Negativity (>85%)',
        ha='left', va='top', fontsize=8.5, fontweight='bold', color='#9a3412',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffedd5', edgecolor='#fb923c', lw=0.8, alpha=0.9))

ax.text(9.4, 45.8, 'QUADRANT IV: COMMERCIAL FRICTION\nHigh Prevalence / Moderate Negativity (<75%)',
        ha='right', va='bottom', fontsize=8.5, fontweight='bold', color='#075985',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#e0f2fe', edgecolor='#38bdf8', lw=0.8, alpha=0.9))

ax.text(0.18, 45.8, 'QUADRANT III: SECONDARY OPERATIONAL\nLow Prevalence / Moderate Negativity (<75%)',
        ha='left', va='bottom', fontsize=8.5, fontweight='bold', color='#166534',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#dcfce7', edgecolor='#4ade80', lw=0.8, alpha=0.9))

# --- PLOT BUBBLES ---
bubbles = [
    # Billing
    {'op': 'Grameenphone', 'prev': 1.11, 'neg': 92.89, 'n': 3307, 'col': BRAND_COLORS['Grameenphone']},
    {'op': 'Banglalink', 'prev': 0.86, 'neg': 91.87, 'n': 1085, 'col': BRAND_COLORS['Banglalink']},
    {'op': 'Robi', 'prev': 0.78, 'neg': 89.77, 'n': 1395, 'col': BRAND_COLORS['Robi']},
    # Network
    {'op': 'Grameenphone', 'prev': 1.88, 'neg': 74.01, 'n': 4453, 'col': BRAND_COLORS['Grameenphone']},
    {'op': 'Robi', 'prev': 2.57, 'neg': 76.37, 'n': 3895, 'col': BRAND_COLORS['Robi']},
    {'op': 'Banglalink', 'prev': 3.64, 'neg': 74.83, 'n': 3735, 'col': BRAND_COLORS['Banglalink']},
    # Login
    {'op': 'Grameenphone', 'prev': 3.88, 'neg': 88.95, 'n': 11058, 'col': BRAND_COLORS['Grameenphone']},
    {'op': 'Robi', 'prev': 4.60, 'neg': 87.10, 'n': 7951, 'col': BRAND_COLORS['Robi']},
    {'op': 'Banglalink', 'prev': 8.12, 'neg': 89.28, 'n': 9946, 'col': BRAND_COLORS['Banglalink']},
    # Offers
    {'op': 'Banglalink', 'prev': 4.31, 'neg': 56.14, 'n': 3321, 'col': BRAND_COLORS['Banglalink']},
    {'op': 'Grameenphone', 'prev': 5.27, 'neg': 56.62, 'n': 9557, 'col': BRAND_COLORS['Grameenphone']},
    {'op': 'Robi', 'prev': 5.18, 'neg': 50.26, 'n': 5168, 'col': BRAND_COLORS['Robi']},
]

for b in bubbles:
    bubble_size = b['n'] / 22.0
    ax.scatter(b['prev'], b['neg'], s=bubble_size, color=b['col'],
               alpha=0.72, edgecolors='#0f172a', linewidth=1.3, zorder=3)

# --- INDIVIDUAL CALLOUTS WITH SURGICAL CLEARANCE ---

# 1. Unified Elegant Billing Card (Top-Left)
billing_text = "Billing & Deductions (>90% Dissatisfaction)\n• GP: 92.9% neg (N=3,307)\n• BL: 91.9% neg (N=1,085)\n• Ro: 89.8% neg (N=1,395)"
ax.annotate(
    billing_text,
    xy=(0.95, 91.5),
    xytext=(1.60, 91.5),
    ha='left', va='center',
    fontsize=7.8, fontweight='medium',
    bbox=dict(boxstyle='round,pad=0.35', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.96, lw=0.8),
    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.9, shrinkA=4, shrinkB=6),
    zorder=4
)
# Add auxiliary arrows to the other two billing bubbles from the unified card
ax.annotate('', xy=(1.11, 92.89), xytext=(1.60, 92.8),
            arrowprops=dict(arrowstyle='->', color=BRAND_COLORS['Grameenphone'], lw=0.9, shrinkA=0, shrinkB=4), zorder=4)
ax.annotate('', xy=(0.78, 89.77), xytext=(1.60, 90.2),
            arrowprops=dict(arrowstyle='->', color=BRAND_COLORS['Robi'], lw=0.9, shrinkA=0, shrinkB=4), zorder=4)

# 2. Network Latency Callouts (Mid-Left)
ax.annotate(
    "GP: Network Latency\n(74.0% neg, N=4,453)",
    xy=(1.88, 74.01), xytext=(1.88, 67.5),
    ha='center', va='top', fontsize=7.8, fontweight='medium',
    bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.96, lw=0.7),
    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.8, shrinkA=3, shrinkB=4), zorder=4
)
ax.annotate(
    "Ro: Network Latency\n(76.4% neg, N=3,895)",
    xy=(2.57, 76.37), xytext=(2.57, 81.8),
    ha='center', va='bottom', fontsize=7.8, fontweight='medium',
    bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.96, lw=0.7),
    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.8, shrinkA=3, shrinkB=4), zorder=4
)
ax.annotate(
    "BL: Network Latency\n(74.8% neg, N=3,735)",
    xy=(3.64, 74.83), xytext=(3.64, 67.5),
    ha='center', va='top', fontsize=7.8, fontweight='medium',
    bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.96, lw=0.7),
    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.8, shrinkA=3, shrinkB=4), zorder=4
)

# 3. App Login & Bugs Callouts (Top-Right)
ax.annotate(
    "GP: App Login & Bugs\n(89.0% neg, N=11,058)",
    xy=(3.88, 88.95), xytext=(4.1, 95.2),
    ha='left', va='bottom', fontsize=7.8, fontweight='medium',
    bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.96, lw=0.7),
    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.8, shrinkA=3, shrinkB=4), zorder=4
)
ax.annotate(
    "Ro: App Login & Bugs\n(87.1% neg, N=7,951)",
    xy=(4.60, 87.10), xytext=(5.85, 86.0),
    ha='left', va='center', fontsize=7.8, fontweight='medium',
    bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.96, lw=0.7),
    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.8, shrinkA=3, shrinkB=4), zorder=4
)
ax.annotate(
    "BL: App Login & Bugs\n(89.3% neg, N=9,946)",
    xy=(8.12, 89.28), xytext=(8.12, 83.0),
    ha='center', va='top', fontsize=7.8, fontweight='medium',
    bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.96, lw=0.7),
    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.8, shrinkA=3, shrinkB=4), zorder=4
)

# 4. Offers & Packs Callouts (Bottom-Right)
ax.annotate(
    "BL: Offers & Packs\n(56.1% neg, N=3,321)",
    xy=(4.31, 56.14), xytext=(3.3, 56.14),
    ha='right', va='center', fontsize=7.8, fontweight='medium',
    bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.96, lw=0.7),
    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.8, shrinkA=3, shrinkB=4), zorder=4
)
ax.annotate(
    "GP: Offers & Packs\n(56.6% neg, N=9,557)",
    xy=(5.27, 56.62), xytext=(6.5, 58.5),
    ha='left', va='center', fontsize=7.8, fontweight='medium',
    bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.96, lw=0.7),
    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.8, shrinkA=3, shrinkB=4), zorder=4
)
ax.annotate(
    "Ro: Offers & Packs\n(50.3% neg, N=5,168)",
    xy=(5.18, 50.26), xytext=(6.5, 51.5),
    ha='left', va='center', fontsize=7.8, fontweight='medium',
    bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.96, lw=0.7),
    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.8, shrinkA=3, shrinkB=4), zorder=4
)

# 5. Dedicated clean horizontal legend below the plot
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Grameenphone (GP, #0090ff)',
           markerfacecolor=BRAND_COLORS['Grameenphone'], markersize=10, markeredgecolor='#0f172a', markeredgewidth=1.2),
    Line2D([0], [0], marker='o', color='w', label='Robi Axiata (Ro, #e60000)',
           markerfacecolor=BRAND_COLORS['Robi'], markersize=10, markeredgecolor='#0f172a', markeredgewidth=1.2),
    Line2D([0], [0], marker='o', color='w', label='Banglalink (BL, #ff7a00)',
           markerfacecolor=BRAND_COLORS['Banglalink'], markersize=10, markeredgecolor='#0f172a', markeredgewidth=1.2),
    Line2D([0], [0], marker='o', color='w', label='Bubble Area $\\propto$ Absolute Negative Volume',
           markerfacecolor='#94a3b8', markersize=7, markeredgecolor='#0f172a', markeredgewidth=0.8),
]
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.11),
          ncol=4, frameon=True, framealpha=0.95, edgecolor='#cbd5e1', fontsize=8.5)

ax.set_xlabel('Domain Prevalence (% of Total Operator Review Corpus)', fontsize=10.5, labelpad=8)
ax.set_ylabel('Within-Category Negativity Rate (% Negative Reviews in Domain)', fontsize=10.5, labelpad=8)
ax.set_xlim(0, 9.6)
ax.set_ylim(44.5, 100.5)
ax.grid(True, linestyle=':', alpha=0.45)
plt.title('Strategic VoC Priority Matrix (Prevalence vs. Dissatisfaction Intensity)', pad=12, fontweight='bold', fontsize=12)
plt.tight_layout()
save_figure_to_all(fig, "figure3_priority_matrix.png", pad_inches=0.12)

# -------------------------------------------------------------
# 4. Figure 4: Additive Decomposition of Banglalink 2025->2026
# -------------------------------------------------------------
print("Generating Figure 4: Additive Decomposition (Strict Project Colors & Anti-Collision)...")
fig, ax = plt.subplots(figsize=(10.5, 5.4), dpi=300)

components = [
    ('General Appreciation\n(Volume Surge)', +10.33, SENTIMENT_COLORS['Positive']),  # #2ECC71 Emerald Green
    ('App Login &\nTechnical Bugs', +2.80, BRAND_COLORS['Grameenphone']),             # #0090ff
    ('Network Speed &\n4G Latency', +1.07, '#0284c7'),                                # Sky Blue
    ('Offers &\nData Packs', +0.98, SENTIMENT_COLORS['Neutral']),                     # #F39C12 Amber
    ('Billing &\nAirtime Deductions', +0.36, SENTIMENT_COLORS['Negative']),           # #E74C3C Crimson Red
    ('Net 2025->2026\nTurnaround', +15.54, BRAND_COLORS['Banglalink'])                # #ff7a00 Banglalink Orange!
]

labels = [c[0] for c in components]
vals = [c[1] for c in components]
bar_cols = [c[2] for c in components]

x_pos = np.arange(len(components))
bars = ax.bar(x_pos, vals, color=bar_cols, width=0.55, edgecolor='#1e293b', linewidth=1.2, alpha=0.92)

for bar, v in zip(bars, vals):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.35, f"+{v:.2f}",
            ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#1e293b')

ax.set_xticks(x_pos)
ax.set_xticklabels(labels, fontsize=9.0)
ax.set_ylabel('Additive Contribution to Delta NSS (Percentage Points)', labelpad=8)
ax.set_ylim(0, 19.5)
ax.axhline(0, color='#1e293b', linewidth=1.0)
ax.grid(True, axis='y', linestyle=':', alpha=0.55)

ax.annotate(
    'Key Takeaway (Proposition 1):\n66.5% of Banglalink\'s turnaround\n(+10.33 of +15.54 pts) was driven by\na 2.13x volume growth (21,810 vs. 10,238 reviews),\nwhile real login bug fixes added +2.80 pts.',
    xy=(0, 10.33),
    xytext=(2.6, 14.8),
    fontsize=9.0, fontweight='semibold', color='#14532d', ha='center',
    bbox=dict(boxstyle='round,pad=0.45', facecolor='#f0fdf4', edgecolor='#86efac', lw=1.2),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.15', color='#16a34a', lw=1.4)
)

plt.title('Additive Domain Decomposition of Banglalink\'s 2025–2026 NSS Reversal (+15.54 Points)', pad=14, fontweight='bold', fontsize=11.5)
plt.tight_layout()
save_figure_to_all(fig, "figure4_banglalink_reversal_decomposition.png", pad_inches=0.15)

print("All 4 figures successfully regenerated with zero-collision offsets!")

print("All 4 figures successfully regenerated with zero-collision offsets!")
