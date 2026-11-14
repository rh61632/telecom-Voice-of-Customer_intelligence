import pathlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_system_architecture_diagram():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Background subtle styling
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Color palette
    c_blue = '#1f77b4'
    c_teal = '#17becf'
    c_orange = '#ff7f0e'
    c_green = '#2ca02c'
    c_red = '#d62728'
    c_purple = '#9467bd'
    c_dark = '#2c3e50'
    c_box_bg = '#f8f9fa'

    # Title Banner
    ax.text(7.0, 8.65, "VoC-Intelligence: Intelligent Decision Support & Expert System Architecture", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1a252f')
    ax.text(7.0, 8.35, "Cross-Layer Subsystem Root Cause Diagnostics & Decoupling Pipeline for Telecommunications", 
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#566573')

    # 4 Main Columns / Stages
    # Stage 1: Data Ingestion & Preprocessing (x: 0.6 to 3.2)
    # Stage 2: Multi-Model Inference & Calibration (x: 3.8 to 6.8)
    # Stage 3: Expert Rules & Decoupling Engine (x: 7.4 to 10.4)
    # Stage 4: Decision Support & Triage (x: 11.0 to 13.6)

    def draw_stage_box(x, y, w, h, title, color):
        # Header banner
        rect_bg = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                        facecolor=c_box_bg, edgecolor='#bdc3c7', linewidth=1.2)
        ax.add_patch(rect_bg)
        rect_hdr = patches.FancyBboxPatch((x, y + h - 0.55), w, 0.55, boxstyle="round,pad=0.08,rounding_size=0.15",
                                         facecolor=color, edgecolor=color, linewidth=1)
        ax.add_patch(rect_hdr)
        ax.text(x + w/2, y + h - 0.28, title, ha='center', va='center', fontsize=11, fontweight='bold', color='white')

    def draw_inner_card(x, y, w, h, title, items, badge_col):
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.1",
                                     facecolor='white', edgecolor='#d5dbdb', linewidth=1)
        ax.add_patch(card)
        ax.text(x + 0.15, y + h - 0.22, title, ha='left', va='center', fontsize=9.5, fontweight='bold', color=badge_col)
        curr_y = y + h - 0.45
        for item in items:
            ax.text(x + 0.15, curr_y, f"• {item}", ha='left', va='center', fontsize=8.2, color='#2c3e50')
            curr_y -= 0.22

    # Draw Stage 1: Ingestion & Normalization
    draw_stage_box(0.5, 0.6, 2.9, 7.4, "Stage 1: Ingestion & NLP", c_blue)
    draw_inner_card(0.65, 5.5, 2.6, 1.7, "Data Ingestion Pipeline", 
                    ["Automated Scraper Daemon", "N = 655,649 Real Reviews", "10-Year Horizon (2016-2026)", "App Versions & Timestamps"], c_blue)
    draw_inner_card(0.65, 3.4, 2.6, 1.8, "Code-Mixed NLP Processor", 
                    ["Trilingual / Code-Mixed Engine", "Lowercase & Whitespace Norm.", "Sub-word Char N-grams (3-5)", "Word N-grams (1-2) + Sublinear TF"], c_blue)
    draw_inner_card(0.65, 0.9, 2.6, 2.2, "Dual Ground-Truth Sets", 
                    ["Seed Dataset: N = 4,500", "Human Gold Set: N = 300", "Dual-Annotated Subset: N = 200", "Inter-Rater Kappa Benchmarks"], c_blue)

    # Draw Stage 2: Inference & Calibration
    draw_stage_box(3.8, 0.6, 3.2, 7.4, "Stage 2: Model Inference", c_teal)
    draw_inner_card(3.95, 5.2, 2.9, 2.0, "Production Voting Ensemble", 
                    ["Soft-Voting Tri-Classifier", "Calibrated LinearSVC (Platt)", "Complement Naive Bayes", "Balanced Multinomial LR", "87.3% Cat / 87.4% Sent CV Acc", "122-177 rev/sec (Single CPU)"], c_teal)
    draw_inner_card(3.95, 2.8, 2.9, 2.1, "Deep Learning Benchmarks", 
                    ["BUET BanglaBERT (Transformer)", "BiLSTM + Single-Head Attention", "BERT Macro-F1 = 0.8598", "Inference Latency Tradeoff", "Offline Verification Anchor"], c_teal)
    draw_inner_card(3.95, 0.9, 2.9, 1.6, "Statistical Calibration", 
                    ["Rogan-Gladen True Prevalence", "Platt Sigmoid Calibration", "McNemar & Paired t-Tests"], c_teal)

    # Draw Stage 3: Expert Rules & Decoupling Engine
    draw_stage_box(7.4, 0.6, 3.2, 7.4, "Stage 3: Expert Inference", c_orange)
    draw_inner_card(7.55, 5.3, 2.9, 1.9, "Rule 1: Diagnostic Decoupling", 
                    ["Cross-Layer Attribution", "Client Software vs. Core RF", "App Crashes vs. Cell Latency", "Chi-Square Contingency Proof", "OR = 4.23 (p = 0.0003)"], c_orange)
    draw_inner_card(7.55, 3.1, 2.9, 1.9, "Rule 2: Changepoint & Surges", 
                    ["Dual-Track Volatility Filter", "Flags Shocks (N=35 Total)", "Filters Promo Surges (≥ 50%)", "Separates Campaign Noise", "Isolates Non-Surge (N=19)"], c_orange)
    draw_inner_card(7.55, 0.9, 2.9, 1.9, "Rule 3: Priority Matrix Engine", 
                    ["Prevalence vs Severity Index", "Toxicity Odds Ratio Engine", "Billing: Quad II (Latent Churn)", "App Bugs: Quad I (Urgent Crisis)"], c_orange)

    # Draw Stage 4: Decision Support & Executive Triage
    draw_stage_box(11.0, 0.6, 2.5, 7.4, "Stage 4: Decision Support", c_green)
    draw_inner_card(11.15, 5.5, 2.2, 1.7, "Automated Alerting", 
                    ["Real-Time Anomaly Flag", "Subsystem Attribution", "Automated CTO Alert", "Hotfix Rollback Advice"], c_green)
    draw_inner_card(11.15, 3.4, 2.2, 1.8, "Executive Dashboard", 
                    ["Longitudinal NSS Engine", "Operator Parity Index", "Market Share Benchmark", "Four-Era Trajectory"], c_green)
    draw_inner_card(11.15, 0.9, 2.2, 2.2, "Managerial Protocols", 
                    ["Rule 1: SLA Decoupling", "Rule 2: Dual Dashboards", "Rule 3: Auth Telemetry", "Rule 4: Prompt Regulation"], c_green)

    # Connecting Flow Arrows between Stages
    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor='#34495e', edgecolor='#34495e', width=2.5, headwidth=8, headlength=8))
        if label:
            ax.text((x1+x2)/2, y1 + 0.15, label, ha='center', va='bottom', fontsize=8, fontweight='bold', color='#2c3e50')

    draw_arrow(3.4, 6.2, 3.8, 6.2, "Clean Text")
    draw_arrow(3.4, 4.2, 3.8, 4.2, "Features")
    draw_arrow(7.0, 6.2, 7.4, 6.2, "Predictions")
    draw_arrow(7.0, 2.0, 7.4, 2.0, "Calibrated")
    draw_arrow(10.6, 6.2, 11.0, 6.2, "Root Causes")
    draw_arrow(10.6, 4.0, 11.0, 4.0, "Triaged")

    plt.tight_layout()
    out_paths = [
        pathlib.Path('paper/eswa_latex/figures/figure0_system_architecture.png'),
        pathlib.Path('paper/figures/figure0_system_architecture.png'),
        pathlib.Path('paper/telecommunications_policy_latex/figures/figure0_system_architecture.png')
    ]
    for p in out_paths:
        p.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_paths[0], dpi=300, bbox_inches='tight')
    plt.close()
    
    # Ensure byte-for-byte identity across all venue directories
    img_bytes = out_paths[0].read_bytes()
    for p in out_paths[1:]:
        p.write_bytes(img_bytes)

    print(f"Architecture diagram generated successfully and synchronized to {len(out_paths)} directories!")

if __name__ == '__main__':
    create_system_architecture_diagram()
