#!/usr/bin/env python3
"""
Generate Publication-Quality Visualizations for Common Duration VoC Dataset (Oct 2023 - Sep 2026).
Continuous Shared Window: 1,072 Days, N = 248,501 Verified Reviews across Grameenphone, Robi, and Banglalink.
Strict Operator Serial:
  1. Grameenphone (GP, #0090ff)
  2. Robi (Robi, #e60000)
  3. Banglalink (BL, #ff7a00)

Plots generated (all at 300 DPI):
  1. operator_sentiment_distribution_bars.png   — Grouped sentiment share per operator
  2. net_sentiment_score_comparison_bars.png     — NSS bar chart (incl. industry avg)
  3. monthly_sentiment_trend_line.png            — Yearly NSS trajectory (2023–2026)
  4. multi_year_sentiment_trend_line.png         — Same as #3 (alt filename for README)
  5. operator_category_complaint_distribution_bars.png — Complaint rates by category
  6. category_sentiment_stacked_bars.png         — Sentiment mix within each category
  7. monthly_nss_trend_line.png                  — Monthly-granularity NSS (48 pts, Oct 2023–Sep 2026)
"""

import os
import sys
from pathlib import Path

# Add system packages for matplotlib
sys.path.append("/usr/lib/python3/dist-packages")
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib_cache"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Matplotlib configuration
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib_cache"
plt.rcParams.update({
    "font.sans-serif": "DejaVu Sans",
    "font.family": "sans-serif",
    "figure.titlesize": 14,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.autolayout": False,
})

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GLOBAL_DIR = REPO_ROOT / "scraped_data_global_2020_2026"
CLASSIFIED_CSV = GLOBAL_DIR / "classified" / "all_operators_common_duration_classified.csv"

PLOTS_DIR = GLOBAL_DIR / "plots"
ASSETS_PLOTS_DIR = REPO_ROOT / "assets" / "plots"

PLOTS_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# Strict Serial: Grameenphone, Robi, Banglalink
OPERATOR_SERIAL = ["Grameenphone", "Robi", "Banglalink"]
OPERATOR_LABELS = ["Grameenphone (MyGP)", "Robi (MyRobi)", "Banglalink (MyBL)"]

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


def load_dataset():
    print(f"Loading master classified dataset: {CLASSIFIED_CSV.name}...")
    df = pd.read_csv(
        CLASSIFIED_CSV,
        usecols=["operator", "review_date", "predicted_sentiment", "predicted_category", "rating"]
    )
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    df["year"] = df["review_date"].dt.year
    df["ym"] = df["review_date"].dt.strftime("%Y-%m")
    print(f"Loaded {len(df):,d} records across {df['operator'].nunique()} operators.\n")
    return df


def save_plot(fig, filename: str):
    p1 = PLOTS_DIR / filename
    p2 = ASSETS_PLOTS_DIR / filename
    fig.savefig(p1, dpi=300, bbox_inches="tight")
    fig.savefig(p2, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ Saved: {filename} (in {PLOTS_DIR.name}/ and {ASSETS_PLOTS_DIR.parent.name}/{ASSETS_PLOTS_DIR.name}/)")


def plot_operator_sentiment_distribution(df):
    """Plot 1: Grouped bar chart of Sentiment Distribution per Operator (Serial: GP, Robi, BL)"""
    print("Generating Plot 1: Operator Sentiment Distribution...")
    
    # Calculate distributions following strict serial
    data = {}
    for op in OPERATOR_SERIAL:
        op_df = df[df["operator"] == op]
        tot = len(op_df)
        counts = op_df["predicted_sentiment"].value_counts()
        data[op] = {
            "Positive": (counts.get("Positive", 0) / tot) * 100,
            "Neutral": (counts.get("Neutral", 0) / tot) * 100,
            "Negative": (counts.get("Negative", 0) / tot) * 100,
        }

    x = np.arange(len(OPERATOR_SERIAL))
    w = 0.24

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    
    pos_vals = [data[op]["Positive"] for op in OPERATOR_SERIAL]
    neu_vals = [data[op]["Neutral"] for op in OPERATOR_SERIAL]
    neg_vals = [data[op]["Negative"] for op in OPERATOR_SERIAL]

    r1 = ax.bar(x - w, pos_vals, w, label="Positive", color=SENTIMENT_COLORS["Positive"], edgecolor="black", alpha=0.9)
    r2 = ax.bar(x, neu_vals, w, label="Neutral", color=SENTIMENT_COLORS["Neutral"], edgecolor="black", alpha=0.9)
    r3 = ax.bar(x + w, neg_vals, w, label="Negative", color=SENTIMENT_COLORS["Negative"], edgecolor="black", alpha=0.9)

    ax.set_title("Customer Sentiment Distribution by Operator\n(Continuous 1,072-Day Common Period: Oct 2023 – Sep 2026, N=248,501)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(OPERATOR_LABELS, fontweight="bold", fontsize=11)
    
    # Color tick labels by brand
    for tick_label, op in zip(ax.get_xticklabels(), OPERATOR_SERIAL):
        tick_label.set_color(BRAND_COLORS[op])

    ax.set_ylabel("Share of Reviews (%)", fontweight="bold")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(frameon=True, loc="upper right")

    for r in r1:
        h = r.get_height()
        ax.annotate(f"{h:.1f}%", xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 2),
                    textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")
    for r in r2:
        h = r.get_height()
        ax.annotate(f"{h:.1f}%", xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 2),
                    textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")
    for r in r3:
        h = r.get_height()
        ax.annotate(f"{h:.1f}%", xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 2),
                    textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    save_plot(fig, "operator_sentiment_distribution_bars.png")


def plot_net_sentiment_score(df):
    """Plot 2: Net Sentiment Score (NSS) comparison across operators (Serial: GP, Robi, BL + Industry)"""
    print("Generating Plot 2: Net Sentiment Score Comparison...")
    
    nss_vals = []
    labels = []
    colors = []

    for op, label in zip(OPERATOR_SERIAL, OPERATOR_LABELS):
        op_df = df[df["operator"] == op]
        tot = len(op_df)
        pos = (op_df["predicted_sentiment"] == "Positive").sum()
        neg = (op_df["predicted_sentiment"] == "Negative").sum()
        nss = ((pos - neg) / tot) * 100
        nss_vals.append(nss)
        labels.append(label)
        colors.append(BRAND_COLORS[op])

    # Industry benchmark
    ind_pos = (df["predicted_sentiment"] == "Positive").sum()
    ind_neg = (df["predicted_sentiment"] == "Negative").sum()
    ind_nss = ((ind_pos - ind_neg) / len(df)) * 100
    nss_vals.append(ind_nss)
    labels.append("Industry Benchmark\n(248.5k Reviews)")
    colors.append("#5D6D7E")

    fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)
    bars = ax.bar(labels, nss_vals, color=colors, edgecolor="black", width=0.55, alpha=0.9)

    ax.set_title("Lifetime Net Sentiment Score (NSS = % Positive − % Negative)\nAcross 248,501 Verified Reviews (Oct 2023 – Sep 2026 Common Period)", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax.set_ylim(40, 95)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for bar, val in zip(bars, nss_vals):
        h = bar.get_height()
        ax.annotate(f"+{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                    textcoords="offset points", ha="center", va="bottom", fontsize=11, fontweight="bold")

    plt.tight_layout()
    save_plot(fig, "net_sentiment_score_comparison_bars.png")


def plot_yearly_sentiment_trajectory(df):
    """Plot 3: Multi-Year Longitudinal NSS Trajectory (2023 - 2026) (Serial: GP, Robi, BL)"""
    print("Generating Plot 3: Multi-Year Sentiment Trajectory...")
    
    # Calculate yearly NSS for each operator
    yearly_data = {}
    years = sorted([int(y) for y in df["year"].dropna().unique()])

    for op in OPERATOR_SERIAL:
        yearly_data[op] = {}
        for y in years:
            sub = df[(df["operator"] == op) & (df["year"] == y)]
            if len(sub) >= 500:  # Threshold for statistical validity
                pos = (sub["predicted_sentiment"] == "Positive").sum()
                neg = (sub["predicted_sentiment"] == "Negative").sum()
                nss = ((pos - neg) / len(sub)) * 100
                yearly_data[op][y] = nss

    fig, ax = plt.subplots(figsize=(11, 5.8), dpi=300)
    
    # Serial: Grameenphone, Robi, Banglalink
    markers = {"Grameenphone": "^", "Robi": "s", "Banglalink": "o"}
    styles = {"Grameenphone": "-", "Robi": "-", "Banglalink": "-"}

    offset_map = {
        ("Grameenphone", 2023): (0, 8),
        ("Banglalink", 2023): (0, 8),
        ("Robi", 2023): (0, -14),
        ("Grameenphone", 2024): (0, 8),
        ("Banglalink", 2024): (0, 8),
        ("Robi", 2024): (0, -14),
        ("Robi", 2025): (0, 8),
        ("Grameenphone", 2025): (0, 8),
        ("Banglalink", 2025): (0, -14),
        ("Banglalink", 2026): (0, 8),
        ("Robi", 2026): (0, -14),
        ("Grameenphone", 2026): (0, -14),
    }

    for op in OPERATOR_SERIAL:
        op_years = sorted(yearly_data[op].keys())
        op_nss = [yearly_data[op][y] for y in op_years]
        ax.plot(
            op_years,
            op_nss,
            marker=markers[op],
            linestyle=styles[op],
            linewidth=2.8,
            markersize=8,
            label=f"{op} ({'MyGP' if op=='Grameenphone' else 'MyRobi' if op=='Robi' else 'MyBL'})",
            color=BRAND_COLORS[op],
        )
        for y, val in zip(op_years, op_nss):
            xytext = offset_map.get((op, y), (0, 8))
            ax.annotate(
                f"{val:+.1f}%",
                xy=(y, val),
                xytext=xytext,
                textcoords="offset points",
                ha="center",
                fontsize=9,
                fontweight="bold",
                color=BRAND_COLORS[op],
            )

    ax.set_title("Longitudinal Net Sentiment Score (NSS) Trajectory (2023 – 2026)\nContinuous Multi-Operator Benchmark Across 1,072 Shared Days (Oct 2023 – Sep 2026)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Year", fontweight="bold")
    ax.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax.set_xlim(2022.7, 2026.3)
    ax.set_ylim(35, 95)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.6)
    
    # Highlight inflection annotations
    ax.axvspan(2023.7, 2024.3, color="#E74C3C", alpha=0.08, label="2023-24 Robi/BL VAS & Network Hurdles")
    ax.axvspan(2025.7, 2026.3, color="#2ECC71", alpha=0.08, label="2026 Banglalink Surge / GP App Fatigue")

    ax.legend(frameon=True, facecolor="white", edgecolor="gray", loc="lower left")

    plt.tight_layout()
    save_plot(fig, "monthly_sentiment_trend_line.png")
    # Also save as multi_year_sentiment_trend_line.png
    save_plot(fig, "multi_year_sentiment_trend_line.png")


def plot_operator_category_complaints(df):
    """Plot 4: Grouped Bar Chart of Actionable Complaint Categories (Serial: GP, Robi, BL)"""
    print("Generating Plot 4: Operator Complaint Category Distribution...")

    complaint_cats = [
        "Offers & Data Packs",
        "App Login & Technical Bugs",
        "Network Speed & 4G Latency",
        "Billing & Airtime Deductions",
    ]

    cat_data = {c: [] for c in complaint_cats}
    for c in complaint_cats:
        for op in OPERATOR_SERIAL:
            sub = df[df["operator"] == op]
            pct = (sub["predicted_category"] == c).mean() * 100
            cat_data[c].append(pct)

    x = np.arange(len(complaint_cats))
    w = 0.25

    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)

    # Plot in strict serial: Grameenphone, Robi, Banglalink
    gp_vals = [cat_data[c][0] for c in complaint_cats]
    robi_vals = [cat_data[c][1] for c in complaint_cats]
    bl_vals = [cat_data[c][2] for c in complaint_cats]

    r1 = ax.bar(x - w, gp_vals, w, label="Grameenphone (MyGP)", color=BRAND_COLORS["Grameenphone"], edgecolor="black", alpha=0.9)
    r2 = ax.bar(x, robi_vals, w, label="Robi (MyRobi)", color=BRAND_COLORS["Robi"], edgecolor="black", alpha=0.9)
    r3 = ax.bar(x + w, bl_vals, w, label="Banglalink (MyBL)", color=BRAND_COLORS["Banglalink"], edgecolor="black", alpha=0.9)

    ax.set_title("Operational Complaint Rate Across Bangladesh Telecom Operators\n(Relative Prevalence in 1,072-Day Common Period: Oct 2023 – Sep 2026, N=248,501)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels([c.replace(" & ", "\n& ") for c in complaint_cats], fontweight="bold", fontsize=10.5)
    ax.set_ylabel("Share of Total Reviews (%)", fontweight="bold")
    ax.set_ylim(0, 7.5)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(frameon=True, loc="upper right")

    for r in r1:
        h = r.get_height()
        ax.annotate(f"{h:.2f}%", xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 2),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    for r in r2:
        h = r.get_height()
        ax.annotate(f"{h:.2f}%", xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 2),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    for r in r3:
        h = r.get_height()
        ax.annotate(f"{h:.2f}%", xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 2),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    plt.tight_layout()
    save_plot(fig, "operator_category_complaint_distribution_bars.png")


def plot_category_sentiment_stacked(df):
    """Plot 5: Sentiment composition stacked within each operational category"""
    print("Generating Plot 5: Category Sentiment Composition...")

    categories = [
        "Offers & Data Packs",
        "App Login & Technical Bugs",
        "Network Speed & 4G Latency",
        "Billing & Airtime Deductions",
        "General Appreciation / Other",
    ]

    breakdown = []
    for c in categories:
        sub = df[df["predicted_category"] == c]
        tot = len(sub)
        p = (sub["predicted_sentiment"] == "Positive").sum() / tot * 100
        u = (sub["predicted_sentiment"] == "Neutral").sum() / tot * 100
        n = (sub["predicted_sentiment"] == "Negative").sum() / tot * 100
        breakdown.append({"Category": c, "Positive": p, "Neutral": u, "Negative": n, "Total": tot})

    b_df = pd.DataFrame(breakdown)

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    y = np.arange(len(categories))
    h = 0.55

    ax.barh(y, b_df["Positive"], h, label="Positive", color=SENTIMENT_COLORS["Positive"], edgecolor="black", alpha=0.9)
    ax.barh(y, b_df["Neutral"], h, left=b_df["Positive"], label="Neutral", color=SENTIMENT_COLORS["Neutral"], edgecolor="black", alpha=0.9)
    ax.barh(y, b_df["Negative"], h, left=b_df["Positive"] + b_df["Neutral"], label="Negative", color=SENTIMENT_COLORS["Negative"], edgecolor="black", alpha=0.9)

    ax.set_title("Sentiment Breakdown by Operational Category (Common Period N=248,501)", fontsize=13, fontweight="bold", pad=12)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{c} (N={n:,d})" for c, n in zip(categories, b_df["Total"])], fontweight="bold")
    ax.set_xlabel("Proportion of Category (%)", fontweight="bold")
    ax.set_xlim(0, 100)
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.legend(frameon=True, loc="lower right")

    for i in range(len(categories)):
        pos_v = b_df["Positive"].iloc[i]
        neg_v = b_df["Negative"].iloc[i]
        if pos_v > 15:
            ax.text(pos_v / 2, i, f"{pos_v:.1f}%", ha="center", va="center", color="white", fontweight="bold", fontsize=9)
        if neg_v > 15:
            ax.text(100 - neg_v / 2, i, f"{neg_v:.1f}%", ha="center", va="center", color="white", fontweight="bold", fontsize=9)

    plt.tight_layout()
    save_plot(fig, "category_sentiment_stacked_bars.png")


def plot_monthly_nss_trend(df):
    """Plot 6: Monthly-granularity Net Sentiment Score (Oct 2023 – Sep 2026).

    Produces ~36 monthly data points per operator across the 1,072-day common
    window, exposing intra-year signals such as Eid offer surges, app-update
    friction windows, and post-holiday churn spikes that annual averages hide.

    Thresholds:
      - min_reviews = 30  — months with fewer reviews are skipped (sparse data)
    Eid windows shaded (approximate):
      - Eid ul-Fitr 2024: Apr 2024
      - Eid ul-Adha 2024: Jun 2024
      - Eid ul-Fitr 2025: Mar 2025
      - Eid ul-Adha 2025: Jun 2025
      - Eid ul-Fitr 2026: Mar 2026
    """
    print("Generating Plot 6: Monthly-Granularity NSS Trend (Oct 2023 – Sep 2026)...")

    MIN_REVIEWS = 30  # skip months with too few data points to be meaningful

    # Build sorted list of all year-month labels in the common window
    all_ym = sorted(df["ym"].dropna().unique())

    monthly = {}  # op -> list of (ym_label, nss)
    for op in OPERATOR_SERIAL:
        op_df = df[df["operator"] == op]
        pts = []
        for ym in all_ym:
            sub = op_df[op_df["ym"] == ym]
            if len(sub) < MIN_REVIEWS:
                continue
            pos = (sub["predicted_sentiment"] == "Positive").sum()
            neg = (sub["predicted_sentiment"] == "Negative").sum()
            nss = ((pos - neg) / len(sub)) * 100
            pts.append((ym, nss))
        monthly[op] = pts

    # Convert ym strings to matplotlib-friendly x positions
    # Use a global sorted index of all ym that appear for at least one operator
    seen_yms = sorted({ym for pts in monthly.values() for ym, _ in pts})
    ym_to_x = {ym: i for i, ym in enumerate(seen_yms)}

    # Eid window shading: (start_ym_idx, end_ym_idx) approximate
    EID_WINDOWS = [
        ("2024-04", "2024-04", "Eid ul-Fitr '24"),
        ("2024-06", "2024-06", "Eid ul-Adha '24"),
        ("2025-03", "2025-03", "Eid ul-Fitr '25"),
        ("2025-06", "2025-06", "Eid ul-Adha '25"),
        ("2026-03", "2026-03", "Eid ul-Fitr '26"),
    ]

    markers = {"Grameenphone": "^", "Robi": "s", "Banglalink": "o"}

    fig, ax = plt.subplots(figsize=(16, 6), dpi=300)

    # Shade Eid windows
    eid_labeled = False
    for eid_start, eid_end, label in EID_WINDOWS:
        if eid_start in ym_to_x:
            x0 = ym_to_x[eid_start] - 0.4
            x1 = ym_to_x.get(eid_end, ym_to_x[eid_start]) + 0.4
            ax.axvspan(
                x0, x1,
                color="#F39C12", alpha=0.13,
                label="Eid Window (approx.)" if not eid_labeled else "_nolegend_"
            )
            eid_labeled = True
            ax.text(
                (x0 + x1) / 2, 92, label,
                ha="center", va="top", fontsize=7, color="#b7770d",
                rotation=90, style="italic"
            )

    # Plot each operator line
    for op in OPERATOR_SERIAL:
        pts = monthly[op]
        if not pts:
            continue
        xs = [ym_to_x[ym] for ym, _ in pts]
        ys = [nss for _, nss in pts]
        ax.plot(
            xs, ys,
            marker=markers[op],
            linewidth=1.8,
            markersize=5,
            alpha=0.9,
            label=f"{op} ({'MyGP' if op == 'Grameenphone' else 'MyRobi' if op == 'Robi' else 'MyBL'})",
            color=BRAND_COLORS[op],
        )

    # X-axis: show one tick label per quarter to avoid crowding
    quarter_ticks = [i for i, ym in enumerate(seen_yms) if ym.endswith(("-01", "-04", "-07", "-10"))]
    quarter_labels = [seen_yms[i] for i in quarter_ticks]
    ax.set_xticks(quarter_ticks)
    ax.set_xticklabels(quarter_labels, rotation=35, ha="right", fontsize=8.5)

    ax.set_title(
        "Monthly Net Sentiment Score (NSS) Trajectory — Common Period (Oct 2023 – Sep 2026)\n"
        "Continuous 1,072-Day Benchmark · 248,501 Reviews · Grameenphone | Robi | Banglalink",
        fontsize=13, fontweight="bold", pad=12
    )
    ax.set_xlabel("Month (Year-Month)", fontweight="bold")
    ax.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax.set_ylim(25, 100)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(frameon=True, facecolor="white", edgecolor="gray", loc="lower left", fontsize=9)

    plt.tight_layout()
    save_plot(fig, "monthly_nss_trend_line.png")


def main():
    print("=" * 75)
    print("GENERATING GLOBAL COMMON PERIOD PUBLICATION PLOTS (N=248,501)")
    print("Strict Operator Serial: Grameenphone, Robi, Banglalink")
    print("=" * 75)
    df = load_dataset()
    plot_operator_sentiment_distribution(df)
    plot_net_sentiment_score(df)
    plot_yearly_sentiment_trajectory(df)
    plot_operator_category_complaints(df)
    plot_category_sentiment_stacked(df)
    plot_monthly_nss_trend(df)
    print("\n✓ ALL 6 MASTER VISUALIZATIONS GENERATED AT 300 DPI SUCCESSFULLY!")


if __name__ == "__main__":
    main()
