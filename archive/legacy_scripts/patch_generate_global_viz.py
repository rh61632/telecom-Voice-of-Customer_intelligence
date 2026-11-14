from pathlib import Path

path = Path("scraped_data_global/pipeline/generate_global_visualizations.py")
text = path.read_text(encoding="utf-8")

text = text.replace("3,716 Days, N = 655,670 Verified Reviews", "3,713 Days, N = 655,649 Verified Reviews")
text = text.replace("Common Duration VoC Dataset (Jul 2016 - Sep 2026)", "Common Duration VoC Dataset (Aug 2016 - Sep 2026)")
text = text.replace("Complete Master Plot (Jul 2016 – Sep 2026)", "Complete Master Plot (Aug 2016 – Sep 2026)")
text = text.replace("Pre-2020 Early Era Plot (Jul 2016 – Dec 2019 · 42 Months · N=20,678)", "Pre-2020 Early Era Plot (Aug 2016 – Dec 2019 · 41 Months · N=20,657)")
text = text.replace("# 1. Complete Monthly Plot (Jul 2016 - Sep 2026)", "# 1. Complete Monthly Plot (Aug 2016 - Sep 2026)")
text = text.replace("Early Period: Monthly Net Sentiment Score (Jul 2016 – Dec 2019 · 42 Months · 20,678 Reviews)", "Early Period: Monthly Net Sentiment Score (Aug 2016 – Dec 2019 · 41 Months · 20,657 Reviews)")

text = text.replace('df.attrs.get("days", 3716)', 'df.attrs.get("days", 3713)')
text = text.replace('df.attrs.get("start_str", "Jul 2016")', 'df.attrs.get("start_str", "Aug 2016")')

old_load = """def load_dataset():
    \"\"\"Loads dataset strictly filtered up to September 30, 2026.\"\"\"
    cols = ["operator", "review_date", "predicted_sentiment", "predicted_category", "rating"]
    cls_dir = GLOBAL_DIR / "classified"
    print("Loading operator classified CSVs (cutoff: September 30, 2026)...")
    dfs = [
        pd.read_csv(cls_dir / f, usecols=cols)
        for f in [
            "mygp_classified_global.csv",
            "myrobi_classified_global.csv",
            "mybl_classified_global.csv",
        ]
    ]
    df = pd.concat(dfs, ignore_index=True)
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    
    # Strict cutoff: September 30, 2026 23:59:59
    df_sep = df[df["review_date"] <= "2026-09-30 23:59:59"].copy()
    start_common = max(df_sep[df_sep["operator"] == op]["review_date"].min() for op in OPERATOR_SERIAL)
    end_common = min(df_sep[df_sep["operator"] == op]["review_date"].max() for op in OPERATOR_SERIAL)
    
    common = df_sep[(df_sep["review_date"] >= start_common) & (df_sep["review_date"] <= end_common)].copy()"""

new_load = """def load_dataset():
    \"\"\"Loads dataset strictly filtered up to September 30, 2026.\"\"\"
    cols = ["operator", "review_date", "predicted_sentiment", "predicted_category", "rating"]
    cls_dir = GLOBAL_DIR / "classified"
    common_csv = cls_dir / "all_operators_common_duration_classified.csv"
    if common_csv.exists():
        print(f"Loading verified common duration dataset ({common_csv.name})...")
        common = pd.read_csv(common_csv, usecols=cols)
        common["review_date"] = pd.to_datetime(common["review_date"], errors="coerce")
        start_common = common["review_date"].min()
        end_common = common["review_date"].max()
    else:
        print("Loading operator classified CSVs (cutoff: September 30, 2026)...")
        dfs = [
            pd.read_csv(cls_dir / f, usecols=cols)
            for f in [
                "mygp_classified_global.csv",
                "myrobi_classified_global.csv",
                "mybl_classified_global.csv",
            ]
        ]
        df = pd.concat(dfs, ignore_index=True)
        df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
        
        # Strict cutoff: September 30, 2026 23:59:59
        df_sep = df[df["review_date"] <= "2026-09-30 23:59:59"].copy()
        start_common = pd.Timestamp("2016-08-01 00:00:00")
        end_common = min(df_sep[df_sep["operator"] == op]["review_date"].max() for op in OPERATOR_SERIAL)
        common = df_sep[(df_sep["review_date"] >= start_common) & (df_sep["review_date"] <= end_common)].copy()"""

assert old_load in text, "old_load block not found"
text = text.replace(old_load, new_load)

path.write_text(text, encoding="utf-8")
print("Successfully patched generate_global_visualizations.py!")
