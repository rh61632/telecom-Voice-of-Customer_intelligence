"""
Script: create_common_duration_datasets.py
Purpose: Filter scraped operator datasets to the exact shared common time window
         across Grameenphone, Banglalink, and Robi for fair multi-brand benchmarking.
"""

from pathlib import Path
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent if SCRIPT_DIR.name == "pipeline" else SCRIPT_DIR
RAW_DIR = BASE_DIR / "raw"
COMMON_DIR = BASE_DIR / "common_duration"
COMMON_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "Grameenphone": RAW_DIR / "mygp_scraped_2020_to_sep2026.csv",
    "Banglalink": RAW_DIR / "mybl_scraped_2020_to_sep2026.csv",
    "Robi": RAW_DIR / "myrobi_scraped_2020_to_sep2026.csv",
}

def main():
    print("=" * 70)
    print("EXTRACTING COMMON DURATION DATASETS FOR TELECOM VOC INTELLIGENCE")
    print("=" * 70)

    loaded_dfs = {}
    date_ranges = {}

    for op, fpath in FILES.items():
        if not fpath.exists():
            raise FileNotFoundError(f"Source file not found: {fpath}")
        df = pd.read_csv(fpath)
        df["review_date_parsed"] = pd.to_datetime(df["review_date"])
        min_date = df["review_date_parsed"].min()
        max_date = df["review_date_parsed"].max()
        date_ranges[op] = (min_date, max_date)
        loaded_dfs[op] = df
        print(f"[{op:13s}] Source reviews: {len(df):7,d} | Range: {min_date} to {max_date}")

    # Determine exact common overlap
    common_start = max(r[0] for r in date_ranges.values())
    common_end = min(r[1] for r in date_ranges.values())

    print("\n" + "-" * 70)
    print(f"Computed Common Time Window across all 3 operators:")
    print(f"  Start Timestamp : {common_start}")
    print(f"  End Timestamp   : {common_end}")
    print(f"  Duration Span   : {(common_end - common_start).days} days (~13.2 months)")
    print("-" * 70 + "\n")

    filtered_dfs = []
    file_map = {
        "Grameenphone": COMMON_DIR / "mygp_common_duration.csv",
        "Banglalink": COMMON_DIR / "mybl_common_duration.csv",
        "Robi": COMMON_DIR / "myrobi_common_duration.csv",
    }

    report_lines = [
        "# Common Duration Dataset Summary",
        "",
        f"- **Shared Time Window**: `{common_start}` to `{common_end}`",
        f"- **Total Duration**: {(common_end - common_start).days} days",
        "",
        "| Operator | App ID | Common Reviews | % of Dataset | Mean Rating |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]

    for op, df in loaded_dfs.items():
        sub_df = df[
            (df["review_date_parsed"] >= common_start)
            & (df["review_date_parsed"] <= common_end)
        ].copy()

        # Sort chronologically descending (newest first)
        sub_df.sort_values(by="review_date_parsed", ascending=False, inplace=True)
        sub_df.drop(columns=["review_date_parsed"], inplace=True)

        out_path = file_map[op]
        sub_df.to_csv(out_path, index=False)
        filtered_dfs.append(sub_df)

        mean_rating = sub_df["rating"].mean()
        print(f"Saved: {out_path.name:32s} | Rows: {len(sub_df):6,d} | Avg Rating: {mean_rating:.2f}")

    # Combined master dataset
    combined_common_df = pd.concat(filtered_dfs, ignore_index=True)
    # Sort combined by review_date descending
    combined_common_df["review_date_parsed"] = pd.to_datetime(combined_common_df["review_date"])
    combined_common_df.sort_values(by="review_date_parsed", ascending=False, inplace=True)
    combined_common_df.drop(columns=["review_date_parsed"], inplace=True)

    combined_file = COMMON_DIR / "all_operators_common_duration.csv"
    combined_common_df.to_csv(combined_file, index=False)
    print(f"Saved: {combined_file.name:32s} | Rows: {len(combined_common_df):6,d} (Master Combined)")

    # Build report table
    for op in ["Grameenphone", "Banglalink", "Robi"]:
        op_df = combined_common_df[combined_common_df["operator"] == op]
        pct = (len(op_df) / len(combined_common_df)) * 100
        mean_r = op_df["rating"].mean()
        report_lines.append(f"| **{op}** | `{FILES[op].name.split('_')[0]}` | {len(op_df):,d} | {pct:.1f}% | {mean_r:.2f} ★ |")

    report_lines.extend([
        f"| **Total** | *All 3 Operators* | **{len(combined_common_df):,d}** | **100.0%** | **{combined_common_df['rating'].mean():.2f} ★** |",
        "",
        "## Generated Files",
        f"- Individual Grameenphone: `{file_map['Grameenphone'].name}`",
        f"- Individual Banglalink: `{file_map['Banglalink'].name}`",
        f"- Individual Robi: `{file_map['Robi'].name}`",
        f"- Master Combined Dataset: `{combined_file.name}`",
        "",
        "## Rating Distribution Across Operators in Common Window",
        "```",
    ])

    crosstab = pd.crosstab(combined_common_df["operator"], combined_common_df["rating"], margins=True)
    report_lines.append(crosstab.to_string())
    report_lines.append("```\n")

    summary_file = COMMON_DIR / "README.md"
    summary_file.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Saved: {summary_file.name:32s} | Summary Report Generated")
    print("\n" + "=" * 70)
    print("ALL COMMON DURATION FILES SUCCESSFULLY CREATED!")
    print("=" * 70)

if __name__ == "__main__":
    main()
