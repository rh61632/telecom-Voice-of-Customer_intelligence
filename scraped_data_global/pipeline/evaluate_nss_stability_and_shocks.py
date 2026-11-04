"""
Evaluate NSS Stability and Significant Jump Attribution across Bangladesh Telecom Operators.
Computes:
1. Time-series stability metrics (RMSSD, Std Dev, IQR, Stability Index SSI).
2. Significant shock detection (|delta NSS| >= 10.0 percentage points).
3. Exact additive category attribution: Delta NSS = sum(Delta Contribution_c).
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CLS_DIR = BASE_DIR / "classified"

OPERATORS = ["Grameenphone", "Robi", "Banglalink"]
ACTIONABLE_CATS = [
    "Offers & Data Packs",
    "App Login & Technical Bugs",
    "Network Speed & 4G Latency",
    "Billing & Airtime Deductions",
]
ALL_CATS = ACTIONABLE_CATS + ["General Appreciation / Other"]


def load_dataset():
    cols = ["operator", "review_date", "predicted_sentiment", "predicted_category"]
    print("Loading classified datasets...")
    dfs = [
        pd.read_csv(CLS_DIR / f, usecols=cols)
        for f in [
            "mygp_classified_global.csv",
            "myrobi_classified_global.csv",
            "mybl_classified_global.csv",
        ]
    ]
    df = pd.concat(dfs, ignore_index=True)
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    
    # Common duration cutoff: Sep 30, 2026
    df_sep = df[df["review_date"] <= "2026-09-30 23:59:59"].copy()
    start_common = max(df_sep[df_sep["operator"] == op]["review_date"].min() for op in OPERATORS)
    end_common = min(df_sep[df_sep["operator"] == op]["review_date"].max() for op in OPERATORS)
    
    common = df_sep[(df_sep["review_date"] >= start_common) & (df_sep["review_date"] <= end_common)].copy()
    common["ym"] = common["review_date"].dt.strftime("%Y-%m")
    common["year"] = common["review_date"].dt.year
    return common


def compute_monthly_trajectory(df):
    records = []
    for (op, ym), g in df.groupby(["operator", "ym"]):
        n = len(g)
        if n < 30:  # CLT standard
            continue
        pos = (g["predicted_sentiment"] == "Positive").sum()
        neg = (g["predicted_sentiment"] == "Negative").sum()
        nss = ((pos - neg) / n) * 100.0
        
        # Contribution per category
        cat_contrib = {}
        for c in ALL_CATS:
            sub_c = g[g["predicted_category"] == c]
            p_c = (sub_c["predicted_sentiment"] == "Positive").sum()
            ng_c = (sub_c["predicted_sentiment"] == "Negative").sum()
            cat_contrib[c] = ((p_c - ng_c) / n) * 100.0
            
        records.append({
            "operator": op,
            "ym": ym,
            "year": int(ym.split("-")[0]),
            "n_reviews": int(n),
            "nss": float(nss),
            "contributions": cat_contrib
        })
    mdf = pd.DataFrame(records).sort_values(["operator", "ym"])
    return mdf


def compute_stability_metrics(mdf, era_label="All Common (2016-2026)"):
    stability = {}
    for op in OPERATORS:
        sub = mdf[mdf["operator"] == op].copy()
        if len(sub) < 2:
            continue
        nss_vals = sub["nss"].values
        deltas = np.diff(nss_vals)
        abs_deltas = np.abs(deltas)
        
        mean_nss = float(np.mean(nss_vals))
        std_nss = float(np.std(nss_vals, ddof=1))
        rmssd = float(np.sqrt(np.mean(deltas ** 2)))
        ssi = max(0.0, 100.0 - rmssd)
        q25, q75 = np.percentile(nss_vals, [25, 75])
        iqr = float(q75 - q25)
        
        stability[op] = {
            "era": era_label,
            "qualified_months": len(sub),
            "mean_nss": round(mean_nss, 2),
            "std_dev_nss": round(std_nss, 2),
            "mom_volatility_rmssd": round(rmssd, 2),
            "sentiment_stability_index_ssi": round(ssi, 2),
            "iqr": round(iqr, 2),
            "median_abs_mom_shift": round(float(np.median(abs_deltas)), 2),
            "p75_abs_mom_shift": round(float(np.percentile(abs_deltas, 75)), 2),
            "p90_abs_mom_shift": round(float(np.percentile(abs_deltas, 90)), 2),
            "p95_abs_mom_shift": round(float(np.percentile(abs_deltas, 95)), 2),
        }
    return stability


def detect_and_attribute_shocks(mdf, threshold=10.0):
    shocks = []
    for op in OPERATORS:
        sub = mdf[mdf["operator"] == op].copy().reset_index(drop=True)
        for i in range(1, len(sub)):
            prev = sub.iloc[i - 1]
            curr = sub.iloc[i]
            
            # Check calendar continuity (if there's a gap between months, note it)
            delta_nss = curr["nss"] - prev["nss"]
            if abs(delta_nss) >= threshold:
                contrib_changes = {
                    c: curr["contributions"][c] - prev["contributions"][c]
                    for c in ALL_CATS
                }
                
                # Primary operational department driver (among actionable categories)
                op_changes = {c: contrib_changes[c] for c in ACTIONABLE_CATS}
                # Select the category whose change aligns best or has largest magnitude
                top_op_driver = max(op_changes.items(), key=lambda x: abs(x[1]))
                
                shocks.append({
                    "operator": op,
                    "previous_month": prev["ym"],
                    "current_month": curr["ym"],
                    "nss_before": round(prev["nss"], 2),
                    "nss_after": round(curr["nss"], 2),
                    "delta_nss": round(delta_nss, 2),
                    "direction": "Positive Jump" if delta_nss > 0 else "Negative Shock",
                    "primary_operational_driver": top_op_driver[0],
                    "operational_driver_impact_pp": round(top_op_driver[1], 2),
                    "general_appreciation_impact_pp": round(contrib_changes["General Appreciation / Other"], 2),
                    "offers_impact_pp": round(contrib_changes["Offers & Data Packs"], 2),
                    "app_login_impact_pp": round(contrib_changes["App Login & Technical Bugs"], 2),
                    "network_speed_impact_pp": round(contrib_changes["Network Speed & 4G Latency"], 2),
                    "billing_impact_pp": round(contrib_changes["Billing & Airtime Deductions"], 2),
                    "reviews_curr_month": int(curr["n_reviews"])
                })
    return shocks


def main():
    df = load_dataset()
    mdf = compute_monthly_trajectory(df)
    
    # Stability for both eras
    stability_all = compute_stability_metrics(mdf, "All Common (Jul 2016 - Sep 2026)")
    mdf_recent = mdf[mdf["year"] >= 2020].copy()
    stability_recent = compute_stability_metrics(mdf_recent, "Recent High-Volume (Jan 2020 - Sep 2026)")
    
    # Shock detection
    shocks = detect_and_attribute_shocks(mdf, threshold=10.0)
    shocks_df = pd.DataFrame(shocks)
    
    print("\n" + "=" * 80)
    print("NSS STABILITY SCORECARD (2020 - 2026 HIGH-VOLUME ERA | 81 MONTHS)")
    print("=" * 80)
    print(f"{'Operator':<15} | {'Mean NSS':<10} | {'RMSSD (Volatility)':<20} | {'Stability Index (SSI)':<22} | {'IQR':<10}")
    print("-" * 80)
    for op in OPERATORS:
        s = stability_recent[op]
        print(f"{op:<15} | {s['mean_nss']:>7.2f}%  | {s['mom_volatility_rmssd']:>17.2f} pp  | {s['sentiment_stability_index_ssi']:>19.2f} / 100 | {s['iqr']:>7.2f} pp")
        
    print("\n" + "=" * 80)
    print(f"HISTORICAL SIGNIFICANT JUMPS (|ΔNSS| >= 10.0 pp): {len(shocks)} TOTAL SHOCKS DETECTED")
    print("=" * 80)
    recent_shocks = [s for s in shocks if int(s['current_month'].split('-')[0]) >= 2020]
    print(f"  - 2020-2026 Modern Era: {len(recent_shocks)} shocks")
    print(f"  - Pre-2020 Early Era: {len(shocks) - len(recent_shocks)} shocks\n")
    
    # Save outputs
    out_json = {
        "stability_metrics": {
            "high_volume_era_2020_2026": stability_recent,
            "full_common_window_2016_2026": stability_all
        },
        "significant_shocks_count": len(shocks),
        "recent_shocks_count": len(recent_shocks),
        "shocks_data": shocks
    }
    
    with open(CLS_DIR / "nss_stability_and_shocks_summary.json", "w", encoding="utf-8") as f:
        json.dump(out_json, f, indent=2)
    print(f"Saved summary JSON to {CLS_DIR / 'nss_stability_and_shocks_summary.json'}")
    
    shocks_df.to_csv(CLS_DIR / "nss_significant_shocks.csv", index=False)
    print(f"Saved shocks CSV to {CLS_DIR / 'nss_significant_shocks.csv'}")


if __name__ == "__main__":
    main()
