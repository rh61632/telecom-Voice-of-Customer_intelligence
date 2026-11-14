import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path

BRAND_COLORS = {
    'Grameenphone': '#0090ff',
    'Robi': '#e60000',
    'Banglalink': '#ff7a00'
}

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
    xy=(4.31, 56.13), xytext=(3.3, 56.13),
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

# Save in all three venue figures directories with identical bytes
out_dirs = [
    Path('paper/figures'),
    Path('paper/eswa_latex/figures'),
    Path('paper/telecommunications_policy_latex/figures')
]

for d in out_dirs:
    d.mkdir(parents=True, exist_ok=True)

primary_path = out_dirs[0] / "figure3_priority_matrix.png"
fig.savefig(primary_path, bbox_inches='tight', pad_inches=0.12, dpi=300)
plt.close(fig)

b = primary_path.read_bytes()
for d in out_dirs[1:]:
    (d / "figure3_priority_matrix.png").write_bytes(b)

print('Successfully generated pristine figure3_priority_matrix.png across all 3 directories!')
