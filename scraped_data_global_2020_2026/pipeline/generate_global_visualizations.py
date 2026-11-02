#!/usr/bin/env python3
"""
Generate Publication-Quality Visualizations for Common Duration VoC Dataset (Oct 2023 - Sep 2026).
Continuous Shared Window: 1,072 Days, N = 285,111 Verified Reviews across Grameenphone, Robi, and Banglalink.
Strict Cutoff: September 30, 2026.
Strict Operator Serial:
  1. Grameenphone (GP, #0090ff)
  2. Robi (Robi, #e60000)
  3. Banglalink (BL, #ff7a00)

Plots generated (all at 300 DPI, zero-collision legends positioned cleanly above plots):
  1. operator_sentiment_distribution_bars.png   — Grouped sentiment share per operator
  2. net_sentiment_score_comparison_bars.png     — NSS bar chart (incl. industry avg)
  3. monthly_sentiment_trend_line.png            — Yearly NSS trajectory (2023–2026)
  4. multi_year_sentiment_trend_line.png         — Same as #3 (alt filename for README)
  5. operator_category_complaint_distribution_bars.png — Complaint rates by category
  6. category_sentiment_stacked_bars.png         — Sentiment mix within each category
  7. monthly_nss_trend_line.png                  — Monthly-granularity NSS (clean, no Eid noise)
  8. sentiment_model_benchmark_bars.png          — 3-Class Sentiment model benchmark (Acc & Macro-F1)
  9. category_model_benchmark_bars.png           — 5-Class Operational Category model benchmark (Acc & Macro-F1)
"""

import os
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Matplotlib configuration for publication quality
plt.rcParams.update({
    "font.sans-serif": "DejaVu Sans",
    "font.family": "sans-serif",
    "figure.titlesize": 13,
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
    """Loads dataset strictly filtered up to September 30, 2026."""
    cols = ["operator", "review_date", "predicted_sentiment", "predicted_category", "rating"]
    cls_dir = GLOBAL_DIR / "classified"
    print("Loading operator classified CSVs (cutoff: September 30, 2026)...")
    dfs = [
        pd.read_csv(cls_dir / f, usecols=cols)
        for f in [
            "mygp_classified_global_2020_2026.csv",
            "myrobi_classified_global_2020_2026.csv",
            "mybl_classified_global_2020_2026.csv",
        ]
    ]
    df = pd.concat(dfs, ignore_index=True)
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    
    # Strict cutoff: September 30, 2026 23:59:59
    df_sep = df[df["review_date"] <= "2026-09-30 23:59:59"].copy()
    start_common = max(df_sep[df_sep["operator"] == op]["review_date"].min() for op in OPERATOR_SERIAL)
    end_common = min(df_sep[df_sep["operator"] == op]["review_date"].max() for op in OPERATOR_SERIAL)
    
    common = df_sep[(df_sep["review_date"] >= start_common) & (df_sep["review_date"] <= end_common)].copy()
    common["year"] = common["review_date"].dt.year
    common["ym"] = common["review_date"].dt.strftime("%Y-%m")

    days = (end_common - start_common).days
    common.attrs["days"] = days
    common.attrs["start_str"] = start_common.strftime("%b %Y")
    common.attrs["end_str"] = end_common.strftime("%b %Y")
    common.attrs["start_year"] = start_common.year
    common.attrs["end_year"] = end_common.year
    print(f"Common Window (up to Sep 2026): {start_common} to {end_common} ({days:,d} days)")
    print(f"Loaded {len(common):,d} records across {common['operator'].nunique()} operators.\n")
    return common


def save_plot(fig, filename: str):
    p1 = PLOTS_DIR / filename
    p2 = ASSETS_PLOTS_DIR / filename
    fig.savefig(p1, dpi=300, bbox_inches="tight")
    fig.savefig(p2, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ Saved: {filename} (in {PLOTS_DIR.name}/ and {ASSETS_PLOTS_DIR.parent.name}/{ASSETS_PLOTS_DIR.name}/)")


def plot_operator_sentiment_distribution(df):
    """Plot 1: Grouped bar chart of Sentiment Distribution per Operator (Serial: GP, Robi, BL)"""
    print("Generating Plot 1: Operator Sentiment Distribution (Sep 2026 Cutoff)...")
    
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

    fig, ax = plt.subplots(figsize=(9, 5.6), dpi=300)
    
    pos_vals = [data[op]["Positive"] for op in OPERATOR_SERIAL]
    neu_vals = [data[op]["Neutral"] for op in OPERATOR_SERIAL]
    neg_vals = [data[op]["Negative"] for op in OPERATOR_SERIAL]

    r1 = ax.bar(x - w, pos_vals, w, label="Positive", color=SENTIMENT_COLORS["Positive"], edgecolor="black", alpha=0.9)
    r2 = ax.bar(x, neu_vals, w, label="Neutral", color=SENTIMENT_COLORS["Neutral"], edgecolor="black", alpha=0.9)
    r3 = ax.bar(x + w, neg_vals, w, label="Negative", color=SENTIMENT_COLORS["Negative"], edgecolor="black", alpha=0.9)

    days = df.attrs.get("days", 1072)
    start_str = df.attrs.get("start_str", "Oct 2023")
    end_str = df.attrs.get("end_str", "Sep 2026")
    ax.set_title(f"Customer Sentiment Distribution by Operator\n(Continuous {days:,d}-Day Common Period: {start_str} – {end_str}, N={len(df):,d})", fontsize=13, fontweight="bold", pad=54)
    ax.set_xticks(x)
    ax.set_xticklabels(OPERATOR_LABELS, fontweight="bold", fontsize=11)
    
    for tick_label, op in zip(ax.get_xticklabels(), OPERATOR_SERIAL):
        tick_label.set_color(BRAND_COLORS[op])

    ax.set_ylabel("Share of Reviews (%)", fontweight="bold")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    ax.legend(
        frameon=True,
        facecolor="white",
        edgecolor="#BDC3C7",
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=3,
        fontsize=10.5
    )

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
    print("Generating Plot 2: Net Sentiment Score Comparison (Sep 2026 Cutoff)...")
    
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
    labels.append(f"Industry Benchmark\n({len(df)/1000:.1f}k Reviews)")
    colors.append("#5D6D7E")

    fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)
    bars = ax.bar(labels, nss_vals, color=colors, edgecolor="black", width=0.55, alpha=0.9)

    start_str = df.attrs.get("start_str", "Oct 2023")
    end_str = df.attrs.get("end_str", "Sep 2026")
    ax.set_title(f"Lifetime Net Sentiment Score (NSS = % Positive − % Negative)\nAcross {len(df):,d} Verified Reviews ({start_str} – {end_str} Common Period)", fontsize=13, fontweight="bold", pad=16)
    ax.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax.set_ylim(40, 92)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for bar, val in zip(bars, nss_vals):
        h = bar.get_height()
        ax.annotate(f"+{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                    textcoords="offset points", ha="center", va="bottom", fontsize=11, fontweight="bold")

    plt.tight_layout()
    save_plot(fig, "net_sentiment_score_comparison_bars.png")


def plot_yearly_sentiment_trajectory(df):
    """Plot 3: Multi-Year Longitudinal NSS Trajectory:
    1. Complete Master Plot (2016 – 2026) covering all points from bottom to top (Y: -35% to +95%).
    2. Completely separate Pre-2020 Early Era Plot (2016 – 2019).
    3. Completely separate Modern Era Plot (2020 – 2026).
    """
    print("Generating Plot 3: Yearly Sentiment Trajectories (Complete All-Years, Pre-2020, 2020-Onwards)...")
    
    yearly_data = {}
    years = sorted([int(y) for y in df["year"].dropna().unique()])

    for op in OPERATOR_SERIAL:
        yearly_data[op] = {}
        for y in years:
            sub = df[(df["operator"] == op) & (df["year"] == y)]
            if len(sub) >= 500:
                pos = (sub["predicted_sentiment"] == "Positive").sum()
                neg = (sub["predicted_sentiment"] == "Negative").sum()
                nss = ((pos - neg) / len(sub)) * 100
                yearly_data[op][y] = nss

    markers = {"Grameenphone": "^", "Robi": "s", "Banglalink": "o"}
    styles = {"Grameenphone": "-", "Robi": "-", "Banglalink": "-"}

    years_pre = [y for y in years if y <= 2019]
    years_post = [y for y in years if y >= 2020]

    offset_all = {
        ("Banglalink", 2016): (0, 8),
        ("Banglalink", 2017): (0, 8),
        ("Grameenphone", 2017): (0, 8),
        ("Banglalink", 2018): (0, 8),
        ("Grameenphone", 2018): (0, 8),
        ("Robi", 2018): (0, -15),
        ("Grameenphone", 2019): (0, 8),
        ("Banglalink", 2019): (18, -10),
        ("Robi", 2019): (-16, -14),
        ("Robi", 2020): (0, 8),
        ("Grameenphone", 2020): (0, 8),
        ("Banglalink", 2020): (0, -15),
        ("Robi", 2021): (0, 8),
        ("Grameenphone", 2021): (0, -15),
        ("Banglalink", 2021): (0, -15),
        ("Robi", 2022): (0, 8),
        ("Grameenphone", 2022): (0, -15),
        ("Banglalink", 2022): (0, 8),
        ("Grameenphone", 2023): (0, 8),
        ("Banglalink", 2023): (0, -15),
        ("Robi", 2023): (0, 8),
        ("Grameenphone", 2024): (0, 8),
        ("Robi", 2024): (0, 8),
        ("Banglalink", 2024): (0, -15),
        ("Robi", 2025): (0, 8),
        ("Grameenphone", 2025): (0, 8),
        ("Banglalink", 2025): (0, -15),
        ("Banglalink", 2026): (0, 8),
        ("Robi", 2026): (0, -15),
        ("Grameenphone", 2026): (0, -15),
    }

    # 1. Complete Plot containing all years (2016 - 2026), full range covering all points from bottom to top
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
    for op in OPERATOR_SERIAL:
        op_years = sorted(yearly_data[op].keys())
        op_nss = [yearly_data[op][y] for y in op_years]
        ax.plot(
            op_years, op_nss,
            marker=markers[op], linestyle=styles[op], linewidth=2.6, markersize=8,
            color=BRAND_COLORS[op], label=f"{op} ({'MyGP' if op=='Grameenphone' else 'MyRobi' if op=='Robi' else 'MyBL'})"
        )
        for y, val in zip(op_years, op_nss):
            xytext = offset_all.get((op, y), (0, 8))
            ax.annotate(
                f"{val:+.1f}%", xy=(y, val), xytext=xytext,
                textcoords="offset points", ha="center", fontsize=9.0, fontweight="bold",
                color=BRAND_COLORS[op]
            )

    # 0% Neutral Baseline
    ax.axhline(0, color="#34495E", linestyle="--", linewidth=1.2, alpha=0.75)
    ax.text(min(years) - 0.2, 1.5, "0% Neutral Baseline", fontsize=8.5, color="#34495E", fontweight="bold")

    # Milestone inflection spans with clean bottom text annotations
    ax.axvspan(2023.7, 2024.3, color="#E74C3C", alpha=0.07)
    ax.text(2024.0, -30, "2023–24 VAS Hurdles", ha="center", fontsize=8.0, color="#C0392B", style="italic", fontweight="bold")
    ax.axvspan(2025.7, 2026.25, color="#2ECC71", alpha=0.07)
    ax.text(2025.98, -30, "2026 BL Surge / GP Dip", ha="center", fontsize=8.0, color="#27AE60", style="italic", fontweight="bold")

    days = df.attrs.get("days", 3716)
    start_str = df.attrs.get("start_str", "Jul 2016")
    end_str = df.attrs.get("end_str", "Sep 2026")
    ax.set_title(
        f"Longitudinal Net Sentiment Score (NSS) Trajectory ({min(years)} – {max(years)})\n"
        f"Continuous Multi-Operator Benchmark Across {days:,d} Shared Days ({start_str} – {end_str}, N = {len(df):,d})",
        fontsize=12.5, fontweight="bold", pad=52
    )
    ax.set_xlabel("Year", fontweight="bold")
    ax.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax.set_xlim(min(years) - 0.25, max(years) + 0.25)
    ax.set_ylim(-35, 95)
    ax.set_yticks(range(-30, 100, 10))
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.5)

    ax.legend(
        frameon=True, facecolor="white", edgecolor="#BDC3C7",
        loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, fontsize=10.0
    )
    plt.tight_layout()
    save_plot(fig, "multi_year_sentiment_trend_line.png")
    save_plot(fig, "monthly_sentiment_trend_line.png")
    save_plot(fig, "yearly_sentiment_trend_all_years.png")

    # 2. Completely separate Pre-2020 Yearly Plot (2016 - 2019)
    fig_pre, ax_pre = plt.subplots(figsize=(8.5, 5.4), dpi=300)
    for op in OPERATOR_SERIAL:
        op_years = [y for y in sorted(yearly_data[op].keys()) if y in years_pre]
        op_nss = [yearly_data[op][y] for y in op_years]
        if op_years:
            ax_pre.plot(
                op_years, op_nss,
                marker=markers[op], linestyle=styles[op], linewidth=2.6, markersize=8,
                color=BRAND_COLORS[op], label=f"{op} ({'MyGP' if op=='Grameenphone' else 'MyRobi' if op=='Robi' else 'MyBL'})"
            )
            for y, val in zip(op_years, op_nss):
                xytext = offset_all.get((op, y), (0, 8))
                ax_pre.annotate(f"{val:+.1f}%", (y, val), xytext=xytext, textcoords="offset points", ha="center", fontsize=9.0, fontweight="bold", color=BRAND_COLORS[op])

    ax_pre.axhline(0, color="#34495E", linestyle="--", linewidth=1.1, alpha=0.7)
    ax_pre.text(min(years_pre) - 0.2, 1.5, "0% Neutral Baseline", fontsize=8.5, color="#34495E", fontweight="bold")
    ax_pre.set_title("Early Era: Multi-Year NSS Trajectory (2016 – 2019)\n4G Rollout Backlash & Early Mobile App Ecosystem (N = 20,678)", fontsize=12, fontweight="bold", pad=48)
    ax_pre.set_xlabel("Year", fontweight="bold")
    ax_pre.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax_pre.set_xlim(min(years_pre) - 0.25, max(years_pre) + 0.25)
    ax_pre.set_ylim(-35, 55)
    ax_pre.set_yticks(range(-30, 60, 10))
    ax_pre.set_xticks(years_pre)
    ax_pre.set_xticklabels([str(y) for y in years_pre], fontweight="bold")
    ax_pre.grid(True, linestyle="--", alpha=0.5)
    ax_pre.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, frameon=True, facecolor="white", edgecolor="#BDC3C7", fontsize=9.5)
    plt.tight_layout()
    save_plot(fig_pre, "yearly_sentiment_trend_pre2020.png")

    # 3. Completely separate Modern Era Plot (2020 - 2026)
    fig_post, ax_post = plt.subplots(figsize=(9.5, 5.5), dpi=300)
    for op in OPERATOR_SERIAL:
        op_years = [y for y in sorted(yearly_data[op].keys()) if y in years_post]
        op_nss = [yearly_data[op][y] for y in op_years]
        if op_years:
            ax_post.plot(
                op_years, op_nss,
                marker=markers[op], linestyle=styles[op], linewidth=2.6, markersize=8,
                color=BRAND_COLORS[op], label=f"{op} ({'MyGP' if op=='Grameenphone' else 'MyRobi' if op=='Robi' else 'MyBL'})"
            )
            for y, val in zip(op_years, op_nss):
                xytext = offset_all.get((op, y), (0, 8))
                ax_post.annotate(f"{val:+.1f}%", (y, val), xytext=xytext, textcoords="offset points", ha="center", fontsize=9.0, fontweight="bold", color=BRAND_COLORS[op])

    ax_post.axvspan(2023.7, 2024.3, color="#E74C3C", alpha=0.07)
    ax_post.text(2024.0, 34, "2023–24 VAS Hurdles", ha="center", fontsize=8.0, color="#C0392B", style="italic", fontweight="bold")
    ax_post.axvspan(2025.7, 2026.25, color="#2ECC71", alpha=0.07)
    ax_post.text(2025.98, 34, "2026 BL Surge / GP Dip", ha="center", fontsize=8.0, color="#27AE60", style="italic", fontweight="bold")
    ax_post.set_title("Modern Era: Multi-Year NSS Trajectory (2020 – 2026)\nScale Maturation & Super-App Market Competition (N = 634,992)", fontsize=12, fontweight="bold", pad=48)
    ax_post.set_xlabel("Year", fontweight="bold")
    ax_post.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax_post.set_xlim(min(years_post) - 0.25, max(years_post) + 0.25)
    ax_post.set_ylim(30, 92)
    ax_post.set_yticks(range(30, 100, 10))
    ax_post.set_xticks(years_post)
    ax_post.set_xticklabels([str(y) for y in years_post], fontweight="bold")
    ax_post.grid(True, linestyle="--", alpha=0.5)
    ax_post.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, frameon=True, facecolor="white", edgecolor="#BDC3C7", fontsize=9.5)
    plt.tight_layout()
    save_plot(fig_post, "yearly_sentiment_trend_2020_2026.png")


def plot_operator_category_complaints(df):
    """Plot 4: Grouped Bar Chart of Actionable Complaint Categories (Serial: GP, Robi, BL)"""
    print("Generating Plot 4: Operator Complaint Category Distribution (Sep 2026 Cutoff)...")

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

    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)

    gp_vals = [cat_data[c][0] for c in complaint_cats]
    robi_vals = [cat_data[c][1] for c in complaint_cats]
    bl_vals = [cat_data[c][2] for c in complaint_cats]

    r1 = ax.bar(x - w, gp_vals, w, label="Grameenphone (MyGP)", color=BRAND_COLORS["Grameenphone"], edgecolor="black", alpha=0.9)
    r2 = ax.bar(x, robi_vals, w, label="Robi (MyRobi)", color=BRAND_COLORS["Robi"], edgecolor="black", alpha=0.9)
    r3 = ax.bar(x + w, bl_vals, w, label="Banglalink (MyBL)", color=BRAND_COLORS["Banglalink"], edgecolor="black", alpha=0.9)

    days = df.attrs.get("days", 1072)
    start_str = df.attrs.get("start_str", "Oct 2023")
    end_str = df.attrs.get("end_str", "Sep 2026")
    ax.set_title(f"Operational Complaint Rate Across Bangladesh Telecom Operators\n(Relative Prevalence in {days:,d}-Day Common Period: {start_str} – {end_str}, N={len(df):,d})", fontsize=13, fontweight="bold", pad=54)
    ax.set_xticks(x)
    ax.set_xticklabels([c.replace(" & ", "\n& ") for c in complaint_cats], fontweight="bold", fontsize=10.5)
    ax.set_ylabel("Share of Total Reviews (%)", fontweight="bold")
    ax.set_ylim(0, 7.5)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    ax.legend(
        frameon=True,
        facecolor="white",
        edgecolor="#BDC3C7",
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=3,
        fontsize=10.5
    )

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
    print("Generating Plot 5: Category Sentiment Composition (Sep 2026 Cutoff)...")

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

    fig, ax = plt.subplots(figsize=(10.5, 5.8), dpi=300)
    y = np.arange(len(categories))
    h = 0.55

    ax.barh(y, b_df["Positive"], h, label="Positive", color=SENTIMENT_COLORS["Positive"], edgecolor="black", alpha=0.9)
    ax.barh(y, b_df["Neutral"], h, left=b_df["Positive"], label="Neutral", color=SENTIMENT_COLORS["Neutral"], edgecolor="black", alpha=0.9)
    ax.barh(y, b_df["Negative"], h, left=b_df["Positive"] + b_df["Neutral"], label="Negative", color=SENTIMENT_COLORS["Negative"], edgecolor="black", alpha=0.9)

    ax.set_title(f"Sentiment Breakdown by Operational Category (Common Period N={len(df):,d})", fontsize=13, fontweight="bold", pad=48)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{c} (N={n:,d})" for c, n in zip(categories, b_df["Total"])], fontweight="bold")
    ax.set_xlabel("Proportion of Category (%)", fontweight="bold")
    ax.set_xlim(0, 100)
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    ax.legend(
        frameon=True,
        facecolor="white",
        edgecolor="#BDC3C7",
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=3,
        fontsize=10.5
    )

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
    """Plot 6: Monthly-Granularity Net Sentiment Score Trajectories:
    1. Complete Master Plot (Jul 2016 – Sep 2026) covering all points from bottom to top (Y: -80% to +95%).
    2. Completely separate Pre-2020 Early Era Plot (Jul 2016 – Dec 2019 · 42 Months · N=20,678).
    3. Completely separate Modern Era Plot (Jan 2020 – Sep 2026 · 81 Months · N=634,992).
    """
    print("Generating Plot 6: Monthly NSS Trajectories (Complete All-Months, Pre-2020, 2020-Onwards)...")

    markers = {"Grameenphone": "^", "Robi": "s", "Banglalink": "o"}

    sub_pre = df[df["review_date"] < "2020-01-01"]
    sub_post = df[df["review_date"] >= "2020-01-01"]

    all_ym_pre = sorted(sub_pre["ym"].dropna().unique())
    all_ym_post = sorted(sub_post["ym"].dropna().unique())
    all_ym = sorted(df["ym"].dropna().unique())

    ticks1 = [ym for ym in all_ym_pre if ym.endswith(("-01", "-04", "-07", "-10"))]
    ticks2 = [ym for ym in all_ym_post if ym.endswith(("-01", "-04", "-07", "-10"))]

    # 1. Complete Monthly Plot (Jul 2016 - Sep 2026) covering all points from bottom to top
    fig_all, ax_all = plt.subplots(figsize=(16, 6.4), dpi=300)
    ym_to_x_all = {ym: i for i, ym in enumerate(all_ym)}
    for op in OPERATOR_SERIAL:
        op_df = df[df["operator"] == op]
        xs, ys = [], []
        for ym in all_ym:
            m_sub = op_df[op_df["ym"] == ym]
            if len(m_sub) >= 30:
                pos = (m_sub["predicted_sentiment"] == "Positive").sum()
                neg = (m_sub["predicted_sentiment"] == "Negative").sum()
                nss = ((pos - neg) / len(m_sub)) * 100
                xs.append(ym_to_x_all[ym])
                ys.append(nss)
        ax_all.plot(
            xs, ys, marker=markers[op], color=BRAND_COLORS[op],
            linewidth=1.8, markersize=5.0, alpha=0.9,
            label=f"{op} ({'MyGP' if op == 'Grameenphone' else 'MyRobi' if op == 'Robi' else 'MyBL'})"
        )

    ax_all.axhline(0, color="#34495E", linestyle="--", linewidth=1.1, alpha=0.75)
    ax_all.text(0.5, 2.5, "0% Neutral Baseline", fontsize=8.5, color="#34495E", fontweight="bold")
    
    days = df.attrs.get("days", 3716)
    start_str = df.attrs.get("start_str", "Jul 2016")
    end_str = df.attrs.get("end_str", "Sep 2026")
    ax_all.set_title(
        f"Continuous Monthly Net Sentiment Score (NSS) Trajectory (2016 – 2026)\n"
        f"Continuous {days:,d}-Day Benchmark Across All Months ({start_str} – {end_str}, N = {len(df):,d})",
        fontsize=13, fontweight="bold", pad=52
    )
    ax_all.set_xlabel("Month (Year-Month)", fontweight="bold")
    ax_all.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax_all.set_ylim(-80, 95)
    ticks_all = [ym for ym in all_ym if ym.endswith(("-01", "-07"))]
    ax_all.set_xticks([ym_to_x_all[ym] for ym in ticks_all])
    ax_all.set_xticklabels(ticks_all, rotation=35, ha="right", fontsize=8.5, fontweight="bold")
    ax_all.set_xlim(-0.5, len(all_ym) - 0.5)
    ax_all.grid(True, linestyle="--", alpha=0.5)
    ax_all.legend(
        frameon=True, facecolor="white", edgecolor="#BDC3C7",
        loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, fontsize=10.0
    )
    plt.tight_layout()
    save_plot(fig_all, "monthly_nss_trend_line.png")
    save_plot(fig_all, "monthly_nss_trend_all_months.png")

    # 2. Standalone Pre-2020 Monthly Plot
    fig_m_pre, ax_m_pre = plt.subplots(figsize=(13, 5.2), dpi=300)
    ym_to_x_pre = {ym: i for i, ym in enumerate(all_ym_pre)}
    for op in OPERATOR_SERIAL:
        op_df = sub_pre[sub_pre["operator"] == op]
        xs, ys = [], []
        for ym in all_ym_pre:
            m_sub = op_df[op_df["ym"] == ym]
            if len(m_sub) >= 30:
                pos = (m_sub["predicted_sentiment"] == "Positive").sum()
                neg = (m_sub["predicted_sentiment"] == "Negative").sum()
                nss = ((pos - neg) / len(m_sub)) * 100
                xs.append(ym_to_x_pre[ym])
                ys.append(nss)
        ax_m_pre.plot(xs, ys, marker=markers[op], color=BRAND_COLORS[op], linewidth=2.2, markersize=6, alpha=0.9, label=f"{op} ({'MyGP' if op == 'Grameenphone' else 'MyRobi' if op == 'Robi' else 'MyBL'})")
    ax_m_pre.axhline(0, color="#34495E", linestyle="--", linewidth=1.1, alpha=0.7)
    ax_m_pre.text(0.5, 2.5, "0% Neutral Baseline", fontsize=8.5, color="#34495E", fontweight="bold")
    ax_m_pre.set_title("Early Era: Monthly Net Sentiment Score (Jul 2016 – Dec 2019 · 42 Months · 20,678 Reviews)", fontsize=12, fontweight="bold", pad=48)
    ax_m_pre.set_xlabel("Month (Year-Month)", fontweight="bold")
    ax_m_pre.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax_m_pre.set_ylim(-80, 70)
    ax_m_pre.set_xticks([ym_to_x_pre[ym] for ym in ticks1])
    ax_m_pre.set_xticklabels(ticks1, rotation=30, ha="right", fontsize=9, fontweight="bold")
    ax_m_pre.set_xlim(-0.5, len(all_ym_pre) - 0.5)
    ax_m_pre.grid(True, linestyle="--", alpha=0.5)
    ax_m_pre.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, frameon=True, facecolor="white", edgecolor="#BDC3C7", fontsize=9.5)
    plt.tight_layout()
    save_plot(fig_m_pre, "monthly_nss_trend_pre2020.png")

    # 3. Standalone 2020 Onwards Monthly Plot
    fig_m_post, ax_m_post = plt.subplots(figsize=(15, 5.6), dpi=300)
    ym_to_x_post = {ym: i for i, ym in enumerate(all_ym_post)}
    for op in OPERATOR_SERIAL:
        op_df = sub_post[sub_post["operator"] == op]
        xs, ys = [], []
        for ym in all_ym_post:
            m_sub = op_df[op_df["ym"] == ym]
            if len(m_sub) >= 30:
                pos = (m_sub["predicted_sentiment"] == "Positive").sum()
                neg = (m_sub["predicted_sentiment"] == "Negative").sum()
                nss = ((pos - neg) / len(m_sub)) * 100
                xs.append(ym_to_x_post[ym])
                ys.append(nss)
        ax_m_post.plot(xs, ys, marker=markers[op], color=BRAND_COLORS[op], linewidth=2.2, markersize=6, alpha=0.9, label=f"{op} ({'MyGP' if op == 'Grameenphone' else 'MyRobi' if op == 'Robi' else 'MyBL'})")
    ax_m_post.set_title("Modern Era: Monthly Net Sentiment Score (Jan 2020 – Sep 2026 · 81 Months · 634,992 Reviews)", fontsize=12, fontweight="bold", pad=48)
    ax_m_post.set_xlabel("Month (Year-Month)", fontweight="bold")
    ax_m_post.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax_m_post.set_ylim(15, 95)
    ax_m_post.set_xticks([ym_to_x_post[ym] for ym in ticks2])
    ax_m_post.set_xticklabels(ticks2, rotation=35, ha="right", fontsize=9, fontweight="bold")
    ax_m_post.set_xlim(-0.5, len(all_ym_post) - 0.5)
    ax_m_post.grid(True, linestyle="--", alpha=0.5)
    ax_m_post.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, frameon=True, facecolor="white", edgecolor="#BDC3C7", fontsize=9.5)
    plt.tight_layout()
    save_plot(fig_m_post, "monthly_nss_trend_2020_2026.png")


def plot_sentiment_model_benchmark():
    """Plot 7: 3-Class Sentiment Analysis Model Benchmark (Acc & Macro-F1)."""
    print("Generating Plot 7: Sentiment Model Benchmark Bars...")
    models = [
        "BUET BanglaBERT (Fine-Tuned)",
        "Hero Soft-Voting ML Ensemble",
        "Multilingual MiniLM Head",
        "Hybrid BiLSTM + Attention",
    ]
    labels = [
        "[SOTA] BUET BanglaBERT (Fine-Tuned)\n(Full 12-Layer Transformer · GPU)",
        "[Production Hero] Soft-Voting ML Ensemble\n(Dual-Gram TF-IDF · ~17.5k rev/s CPU)",
        "Multilingual MiniLM Head\n(384-dim Dense Embeddings · ~2.1k rev/s)",
        "Hybrid BiLSTM + Attention (GPU)\n(Recurrent Context Modeling · PyTorch)",
    ]
    acc = [91.60, 87.47, 82.33, 81.50]
    f1_raw = [0.8598, 0.7684, 0.7475, 0.7180]
    f1_pct = [v * 100 for v in f1_raw]

    fig, ax = plt.subplots(figsize=(11.0, 5.5), dpi=300)
    y = np.arange(len(models))
    y_rev = y[::-1]
    h = 0.35

    bars_acc = ax.barh(y_rev + h / 2, acc, h, label="CV Accuracy (%)", color="#1F77B4", edgecolor="black", alpha=0.92)
    bars_f1 = ax.barh(y_rev - h / 2, f1_pct, h, label="Macro-F1 (×100)", color="#2CA02C", edgecolor="black", alpha=0.92)

    ax.set_title(
        "Sentiment Analysis Model Benchmark (3-Class Polarity)\n"
        "5-Fold Stratified Cross-Validation on Multi-Operator Ground Truth (N = 4,500)",
        fontsize=13, fontweight="bold", pad=48
    )
    ax.set_yticks(y_rev)
    ax.set_yticklabels(labels, fontweight="bold", fontsize=9.5)
    ax.set_xlabel("Metric Score (%)", fontweight="bold")
    ax.set_xlim(0, 106)
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    ax.legend(
        frameon=True,
        facecolor="white",
        edgecolor="#BDC3C7",
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=2,
        fontsize=10.5
    )

    for bar, val in zip(bars_acc, acc):
        ax.annotate(
            f"{val:.2f}%",
            xy=(val + 1.0, bar.get_y() + bar.get_height() / 2),
            va="center", fontsize=9, fontweight="bold", color="#0E4B75"
        )

    for bar, r, scaled in zip(bars_f1, f1_raw, f1_pct):
        ax.annotate(
            f"{r:.4f} ({scaled:.1f}%)",
            xy=(scaled + 1.0, bar.get_y() + bar.get_height() / 2),
            va="center", fontsize=9, fontweight="bold", color="#145A14"
        )

    plt.tight_layout()
    save_plot(fig, "sentiment_model_benchmark_bars.png")


def plot_category_model_benchmark():
    """Plot 8: 5-Class Operational Category Model Benchmark (Acc & Macro-F1)."""
    print("Generating Plot 8: Operational Category Model Benchmark Bars...")
    models = [
        "Hero Soft-Voting ML Ensemble",
        "BUET BanglaBERT (Fine-Tuned)",
        "Multilingual MiniLM Head",
        "Hybrid BiLSTM + Attention",
    ]
    labels = [
        "[Champion] Hero Soft-Voting ML Ensemble\n(Dual-Gram TF-IDF · ~18.2k rev/s CPU)",
        "BUET BanglaBERT (Fine-Tuned)\n(End-to-End Contextual Transformer · GPU)",
        "Multilingual MiniLM Head\n(384-dim Dense Vector Embeddings)",
        "Hybrid BiLSTM + Attention (GPU)\n(Recurrent Context + Class Weighting)",
    ]
    acc = [87.44, 85.27, 81.15, 80.84]
    f1_raw = [0.7845, 0.7624, 0.7247, 0.7106]
    f1_pct = [v * 100 for v in f1_raw]

    fig, ax = plt.subplots(figsize=(11.0, 5.5), dpi=300)
    y = np.arange(len(models))
    y_rev = y[::-1]
    h = 0.35

    bars_acc = ax.barh(y_rev + h / 2, acc, h, label="CV Accuracy (%)", color="#E67E22", edgecolor="black", alpha=0.92)
    bars_f1 = ax.barh(y_rev - h / 2, f1_pct, h, label="Macro-F1 (×100)", color="#9B59B6", edgecolor="black", alpha=0.92)

    ax.set_title(
        "Operational Category Model Benchmark (5-Class Taxonomy)\n"
        "5-Fold Stratified Cross-Validation on Multi-Operator Ground Truth (N = 4,500)",
        fontsize=13, fontweight="bold", pad=48
    )
    ax.set_yticks(y_rev)
    ax.set_yticklabels(labels, fontweight="bold", fontsize=9.5)
    ax.set_xlabel("Metric Score (%)", fontweight="bold")
    ax.set_xlim(0, 106)
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    ax.legend(
        frameon=True,
        facecolor="white",
        edgecolor="#BDC3C7",
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=2,
        fontsize=10.5
    )

    for bar, val in zip(bars_acc, acc):
        ax.annotate(
            f"{val:.2f}%",
            xy=(val + 1.0, bar.get_y() + bar.get_height() / 2),
            va="center", fontsize=9, fontweight="bold", color="#7E3B06"
        )

    for bar, r, scaled in zip(bars_f1, f1_raw, f1_pct):
        ax.annotate(
            f"{r:.4f} ({scaled:.1f}%)",
            xy=(scaled + 1.0, bar.get_y() + bar.get_height() / 2),
            va="center", fontsize=9, fontweight="bold", color="#4A154B"
        )

    plt.tight_layout()
    save_plot(fig, "category_model_benchmark_bars.png")


def main():
    df = load_dataset()
    days = df.attrs.get("days", 1072)
    start_str = df.attrs.get("start_str", "Oct 2023")
    end_str = df.attrs.get("end_str", "Sep 2026")
    print("=" * 75)
    print(f"GENERATING GLOBAL COMMON PERIOD PUBLICATION PLOTS (N={len(df):,d})")
    print(f"Strict Cutoff: September 30, 2026 ({days:,d} Shared Days: {start_str} to {end_str})")
    print("Strict Operator Serial: Grameenphone, Robi, Banglalink")
    print("=" * 75)
    plot_operator_sentiment_distribution(df)
    plot_net_sentiment_score(df)
    plot_yearly_sentiment_trajectory(df)
    plot_operator_category_complaints(df)
    plot_category_sentiment_stacked(df)
    plot_monthly_nss_trend(df)
    plot_sentiment_model_benchmark()
    plot_category_model_benchmark()
    print("\n✓ ALL 8 MASTER VISUALIZATIONS GENERATED AT 300 DPI SUCCESSFULLY (SEP 2026 CUTOFF)!")


if __name__ == "__main__":
    main()
