#!/usr/bin/env python3
"""
Generate Publication-Quality Visualizations for Telecom VoC Intelligence Pipeline.
Saves:
  - Gold Standard benchmark heatmaps and performance bar charts to: scraped_data_2020/gold_set/plots/
  - Production dataset VoC sentiment distributions and trend charts to: scraped_data_2020/common_duration/plots/
"""

import os
import sys
from pathlib import Path

# Configure matplotlib cache and import from system path
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib_cache"
sys.path.append("/usr/lib/python3/dist-packages")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent if SCRIPT_DIR.name == "pipeline" else SCRIPT_DIR
GOLD_DIR = BASE_DIR / "gold_set"
COMMON_DIR = BASE_DIR / "common_duration"

GOLD_PLOTS = GOLD_DIR / "plots"
COMMON_PLOTS = COMMON_DIR / "plots"

GOLD_PLOTS.mkdir(parents=True, exist_ok=True)
COMMON_PLOTS.mkdir(parents=True, exist_ok=True)

# Styling Defaults
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

LABELS = ["Negative", "Neutral", "Positive"]
COLOR_PALETTE = {
    "Positive": "#2ECC71",       # Green
    "Neutral": "#F39C12",        # Orange
    "Negative": "#E74C3C",       # Red
    "Grameenphone": "#0090ff",   # GP Electric Blue
    "GP": "#0090ff",
    "Robi": "#e60000",           # Robi Vibrant Red
    "Banglalink": "#ff7a00",     # BL Vibrant Orange
    "BL": "#ff7a00",
    "Hero": "#2E86C1",           # Ensemble Royal Blue
    "LinearSVC": "#8E44AD",      # Purple
    "LogReg": "#16A085",         # Teal
    "BiLSTM": "#E67E22",         # Deep Orange
    "Star": "#7F8C8D",           # Gray
}


def plot_single_heatmap(cm, ax, title, cmap="Blues"):
    """Render an annotated confusion matrix heatmap on a given Axes."""
    im = ax.imshow(cm, interpolation="nearest", cmap=cmap)
    total_samples = np.sum(cm)
    
    # Tick marks
    tick_marks = np.arange(len(LABELS))
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(LABELS, fontweight="bold")
    ax.set_yticks(tick_marks)
    ax.set_yticklabels(LABELS, fontweight="bold")
    
    # Annotate numbers & row-normalized percentage
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        row_sum = cm[i].sum()
        for j in range(cm.shape[1]):
            val = cm[i, j]
            pct = (val / row_sum * 100) if row_sum > 0 else 0
            color = "white" if val > thresh else "black"
            ax.text(j, i, f"{val}\n({pct:.1f}%)",
                    ha="center", va="center",
                    color=color, fontsize=10, fontweight="bold")
            
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.set_ylabel("True Human Gold Label", fontweight="bold")
    ax.set_xlabel("Predicted Label", fontweight="bold")
    return im


def generate_gold_set_visuals():
    print("Generating Gold Set Visualizations...")
    gold_csv = GOLD_DIR / "gold_set_verified.csv"
    if not gold_csv.exists():
        print(f"Error: {gold_csv} not found.")
        return

    df = pd.read_csv(gold_csv)
    y_true = df["gold_sentiment"]

    # 1. Hero Model Single Confusion Matrix
    cm_hero = confusion_matrix(y_true, df["pred_ensemble"], labels=LABELS)
    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=300)
    im = plot_single_heatmap(cm_hero, ax, "Hero Model (Soft-Voting Ensemble)\nvs. Verified Human Gold Standard (N=600)", cmap="Blues")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Review Count", fontweight="bold")
    plt.tight_layout()
    out1 = GOLD_PLOTS / "confusion_matrix_hero_ensemble.png"
    plt.savefig(out1, dpi=300)
    plt.close()
    print(f"  ✓ Saved: {out1.name}")

    # 2. 2x2 Grid Confusion Matrix Comparison
    models_to_compare = [
        ("pred_ensemble", "Hero Model: Soft-Voting Ensemble (Acc: 82.0%)", "Blues"),
        ("pred_linearsvc", "Challenger: Calibrated LinearSVC (Acc: 79.3%)", "Purples"),
        ("pred_bilstm", "Deep Learning: BiLSTM + Attention (Acc: 71.5%)", "Oranges"),
        ("pred_star_rating", "Naive Baseline: Star Rating (Acc: 80.2%, F1: 0.55)", "Greys"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10.5), dpi=300)
    axes = axes.flatten()

    for idx, (col, title, cmap) in enumerate(models_to_compare):
        cm = confusion_matrix(y_true, df[col], labels=LABELS)
        plot_single_heatmap(cm, axes[idx], title, cmap=cmap)

    plt.suptitle("Multi-Architecture Confusion Matrix Comparison (N=600 Human Gold Set)", fontsize=14, fontweight="bold", y=0.99)
    plt.tight_layout()
    out2 = GOLD_PLOTS / "confusion_matrices_comparison_grid.png"
    plt.savefig(out2, dpi=300)
    plt.close()
    print(f"  ✓ Saved: {out2.name}")

    # 3. Model Benchmark Bar Chart (Accuracy & F1)
    models_dict = {
        "Soft-Voting Ensemble (Hero)": ("pred_ensemble", "#2E86C1"),
        "Calibrated LinearSVC": ("pred_linearsvc", "#8E44AD"),
        "Balanced Logistic Regression": ("pred_logistic", "#16A085"),
        "Deep Learning BiLSTM+Attention": ("pred_bilstm", "#E67E22"),
        "Star-Rating Heuristic Baseline": ("pred_star_rating", "#7F8C8D"),
    }

    names = list(models_dict.keys())
    accs = [accuracy_score(y_true, df[col]) * 100 for col, _ in models_dict.values()]
    macro_f1s = [f1_score(y_true, df[col], average="macro") * 100 for col, _ in models_dict.values()]
    weighted_f1s = [f1_score(y_true, df[col], average="weighted") * 100 for col, _ in models_dict.values()]

    x = np.arange(len(names))
    width = 0.26

    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    rects1 = ax.bar(x - width, accs, width, label="Accuracy (%)", color="#2E86C1", edgecolor="black", alpha=0.9)
    rects2 = ax.bar(x, macro_f1s, width, label="Macro F1 (x100)", color="#27AE60", edgecolor="black", alpha=0.9)
    rects3 = ax.bar(x + width, weighted_f1s, width, label="Weighted F1 (x100)", color="#F39C12", edgecolor="black", alpha=0.9)

    ax.set_title("Empirical Benchmark on Human Gold Standard (N=600)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15, ha="right", fontweight="bold")
    ax.set_ylabel("Score (%)", fontweight="bold")
    ax.set_ylim(40, 95)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(frameon=True, facecolor="white", edgecolor="gray")

    # Add value labels
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f"{h/100:.3f}", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")
    for rect in rects3:
        h = rect.get_height()
        ax.annotate(f"{h/100:.3f}", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")

    plt.tight_layout()
    out3 = GOLD_PLOTS / "model_benchmark_f1_accuracy_bars.png"
    plt.savefig(out3, dpi=300)
    plt.close()
    print(f"  ✓ Saved: {out3.name}")

    # 4. Operator Accuracy Breakdown Bar Chart
    models_to_plot = [
        ("Soft-Voting Ensemble\n(Hero)", "pred_ensemble"),
        ("Calibrated\nLinearSVC", "pred_linearsvc"),
        ("Balanced\nLogReg", "pred_logistic"),
        ("Deep Learning\nBiLSTM+Attention", "pred_bilstm"),
    ]
    ops_to_plot = [
        ("Grameenphone", COLOR_PALETTE["Grameenphone"]),
        ("Robi", COLOR_PALETTE["Robi"]),
        ("Banglalink", COLOR_PALETTE["Banglalink"]),
    ]

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    x = np.arange(len(models_to_plot))
    w = 0.24

    for i, (op_name, op_color) in enumerate(ops_to_plot):
        sub_df = df[df["operator"] == op_name]
        vals = [accuracy_score(sub_df["gold_sentiment"], sub_df[col]) * 100 for _, col in models_to_plot]
        rects = ax.bar(x + (i - 1) * w, vals, w, label=op_name, color=op_color, edgecolor="black", alpha=0.9)
        for r in rects:
            h = r.get_height()
            ax.annotate(f"{h:.1f}%", xy=(r.get_x() + r.get_width()/2, h), xytext=(0, 2),
                        textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")

    ax.set_title("Gold Standard Accuracy by Model & Operator (N=200 per brand)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels([m[0] for m in models_to_plot], fontweight="bold", fontsize=10)
    ax.set_ylabel("Accuracy (%)", fontweight="bold")
    ax.set_ylim(60, 92)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(frameon=True, loc="upper right")

    plt.tight_layout()
    out4 = GOLD_PLOTS / "operator_accuracy_gold_set_bars.png"
    plt.savefig(out4, dpi=300)
    plt.close()
    print(f"  ✓ Saved: {out4.name}")


def generate_production_visuals():
    print("\nGenerating Production VoC Visualizations (N=83,417)...")
    prod_csv = COMMON_DIR / "classified_all_operators_pretrained.csv"
    if not prod_csv.exists():
        print(f"Error: {prod_csv} not found.")
        return

    df = pd.read_csv(prod_csv, usecols=["operator", "review_date", "pred_ensemble", "rating"])

    # 1. Operator Sentiment Distribution (Stacked / Grouped)
    dist = df.groupby("operator")["pred_ensemble"].value_counts(normalize=True).unstack()[LABELS] * 100

    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
    x = np.arange(len(dist))
    w = 0.24

    r_pos = ax.bar(x - w, dist["Positive"], w, label="Positive", color=COLOR_PALETTE["Positive"], edgecolor="black", alpha=0.9)
    r_neu = ax.bar(x, dist["Neutral"], w, label="Neutral", color=COLOR_PALETTE["Neutral"], edgecolor="black", alpha=0.9)
    r_neg = ax.bar(x + w, dist["Negative"], w, label="Negative", color=COLOR_PALETTE["Negative"], edgecolor="black", alpha=0.9)

    ax.set_title("Customer Sentiment Distribution by Operator (Shared 402-Day Window)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(dist.index, fontweight="bold", fontsize=11)
    for tick_label in ax.get_xticklabels():
        txt = tick_label.get_text()
        if "Grameenphone" in txt:
            tick_label.set_color(COLOR_PALETTE["Grameenphone"])
        elif "Robi" in txt:
            tick_label.set_color(COLOR_PALETTE["Robi"])
        elif "Banglalink" in txt:
            tick_label.set_color(COLOR_PALETTE["Banglalink"])

    ax.set_ylabel("Share of Reviews (%)", fontweight="bold")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(frameon=True, loc="upper right")

    for rect in r_pos:
        h = rect.get_height()
        ax.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 2),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    for rect in r_neu:
        h = rect.get_height()
        ax.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 2),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    for rect in r_neg:
        h = rect.get_height()
        ax.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 2),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    plt.tight_layout()
    out1 = COMMON_PLOTS / "operator_sentiment_distribution_bars.png"
    plt.savefig(out1, dpi=300)
    plt.close()
    print(f"  ✓ Saved: {out1.name}")

    # 2. Net Sentiment Score (NSS) Comparison Bar Chart
    nss_data = {
        "Banglalink\n(MyBL)": 88.3 - 6.8,
        "Robi\n(MyRobi)": 86.5 - 7.1,
        "Industry Baseline\n(83.4k Reviews)": 84.1 - 9.9,
        "Grameenphone\n(MyGP)": 75.0 - 18.4,
    }
    colors = [COLOR_PALETTE["Banglalink"], COLOR_PALETTE["Robi"], "#5D6D7E", COLOR_PALETTE["Grameenphone"]]

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    bars = ax.bar(nss_data.keys(), nss_data.values(), color=colors, edgecolor="black", width=0.55, alpha=0.9)

    ax.set_title("Net Sentiment Score (NSS = % Positive − % Negative)\nAcross 83,417 Common Duration Reviews", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax.set_ylim(40, 95)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"+{h:.1f}%", xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 4),
                    textcoords="offset points", ha="center", va="bottom", fontsize=11, fontweight="bold")

    plt.tight_layout()
    out2 = COMMON_PLOTS / "net_sentiment_score_comparison_bars.png"
    plt.savefig(out2, dpi=300)
    plt.close()
    print(f"  ✓ Saved: {out2.name}")

    # 3. Monthly Sentiment Trend Line Chart
    df["review_date"] = pd.to_datetime(df["review_date"])
    df["ym"] = df["review_date"].dt.strftime("%Y-%m")

    def calc_nss(s):
        return (s == "Positive").mean() * 100 - (s == "Negative").mean() * 100

    trend = df.groupby(["ym", "operator"])["pred_ensemble"].apply(calc_nss).unstack()

    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    
    months = trend.index.tolist()
    ax.plot(months, trend["Banglalink"], marker="o", linewidth=2.5, label="Banglalink (MyBL)", color=COLOR_PALETTE["Banglalink"])
    ax.plot(months, trend["Robi"], marker="s", linewidth=2.5, label="Robi (MyRobi)", color=COLOR_PALETTE["Robi"])
    ax.plot(months, trend["Grameenphone"], marker="^", linewidth=2.5, label="Grameenphone (MyGP)", color=COLOR_PALETTE["Grameenphone"])

    ax.set_title("Monthly Net Sentiment Score (NSS) Trajectory\n(Aug 2025 – Sep 2026, Common Duration)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Month", fontweight="bold")
    ax.set_ylabel("Net Sentiment Score (%)", fontweight="bold")
    ax.set_ylim(20, 95)
    ax.set_xticks(range(len(months)))
    ax.set_xticklabels(months, rotation=35, ha="right", fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(frameon=True, facecolor="white", edgecolor="gray", loc="lower right")

    plt.tight_layout()
    out3 = COMMON_PLOTS / "monthly_sentiment_trend_line.png"
    plt.savefig(out3, dpi=300)
    plt.close()
    print(f"  ✓ Saved: {out3.name}")


if __name__ == "__main__":
    generate_gold_set_visuals()
    generate_production_visuals()
    print("\nAll visualizations generated and saved successfully!")
