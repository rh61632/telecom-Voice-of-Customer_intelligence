import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import time
import json
import pandas as pd
from collections import Counter, defaultdict
from ml.language_detector import detector

INPUT_CSV = PROJECT_ROOT / "scraped_data_global" / "classified" / "all_operators_classified_global.csv"
OUTPUT_JSON = PROJECT_ROOT / "ml" / "reports" / "global_language_distribution.json"
OUTPUT_MD = PROJECT_ROOT / "ml" / "reports" / "global_language_distribution.md"


def main():
    print("=" * 75)
    print("ANALYZING LINGUISTIC DISTRIBUTION ACROSS FULL 661k CORPUS")
    print("=" * 75)
    print(f"Reading: {INPUT_CSV}")

    t0 = time.time()
    total_processed = 0
    overall_counter = Counter()
    operator_counters = defaultdict(Counter)
    year_counters = defaultdict(Counter)
    code_mixed_count = 0

    chunksize = 50000
    for chunk_idx, chunk in enumerate(pd.read_csv(
        INPUT_CSV,
        usecols=["review_text", "operator", "year"],
        chunksize=chunksize,
        dtype={"operator": "str", "year": "str"}
    )):
        chunk_t0 = time.time()
        reviews = chunk["review_text"].fillna("").astype(str).tolist()
        operators = chunk["operator"].fillna("Unknown").tolist()
        years = chunk["year"].fillna("Unknown").tolist()

        for text, op, yr in zip(reviews, operators, years):
            res = detector.analyze(text)
            lang = res["language"]
            if res["is_code_mixed"]:
                code_mixed_count += 1
            overall_counter[lang] += 1
            operator_counters[op][lang] += 1
            year_counters[yr][lang] += 1

        total_processed += len(chunk)
        elapsed = time.time() - chunk_t0
        print(f"Chunk {chunk_idx + 1:2d}: {len(chunk):6d} reviews processed in {elapsed:.2f}s (Total: {total_processed:,d})")

    total_time = time.time() - t0
    print("\n" + "=" * 75)
    print(f"COMPLETED IN {total_time:.2f} SECONDS ({total_processed / total_time:.1f} reviews/sec)")
    print("=" * 75)

    # Compile distribution stats
    overall_dist = {}
    for lang, count in overall_counter.most_common():
        pct = (count / total_processed) * 100
        overall_dist[lang] = {"count": count, "percentage": round(pct, 2)}
        print(f"  - {lang:26s}: {count:7,d} ({pct:5.2f}%)")

    print(f"\nCode-Mixed Reviews Identified: {code_mixed_count:,d} ({code_mixed_count / total_processed * 100:.2f}%)")

    # Operator breakdown
    op_breakdown = {}
    print("\nOperator Breakdown:")
    for op, counts in sorted(operator_counters.items()):
        op_total = sum(counts.values())
        op_breakdown[op] = {
            "total": op_total,
            "distribution": {
                lang: {"count": c, "percentage": round((c / op_total) * 100, 2)}
                for lang, c in counts.most_common()
            }
        }
        print(f"\n--- {op} (Total: {op_total:,d}) ---")
        for lang, c in counts.most_common():
            pct = (c / op_total) * 100
            print(f"  - {lang:26s}: {c:7,d} ({pct:5.2f}%)")

    # Year breakdown
    year_breakdown = {}
    for yr, counts in sorted(year_counters.items()):
        yr_total = sum(counts.values())
        year_breakdown[yr] = {
            "total": yr_total,
            "distribution": {
                lang: {"count": c, "percentage": round((c / yr_total) * 100, 2)}
                for lang, c in counts.most_common()
            }
        }

    # Save to JSON
    summary_data = {
        "total_reviews": total_processed,
        "runtime_seconds": round(total_time, 2),
        "overall_distribution": overall_dist,
        "code_mixed_total": code_mixed_count,
        "code_mixed_percentage": round((code_mixed_count / total_processed) * 100, 2),
        "operator_breakdown": op_breakdown,
        "year_breakdown": year_breakdown,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    # Save to Markdown
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("# Full Corpus Linguistic Distribution Analysis (N = 661,160)\n\n")
        f.write(f"Analyzed {total_processed:,d} multi-operator reviews covering a full decade (2014–2026).\n\n")
        f.write("## Overall Distribution\n\n")
        f.write("| Linguistic Cohort | Total Reviews | Percentage (%) |\n")
        f.write("| :--- | :---: | :---: |\n")
        for lang, stats in overall_dist.items():
            f.write(f"| **{lang}** | {stats['count']:,d} | {stats['percentage']:.2f}% |\n")
        f.write(f"| *Code-Mixed (Sub-segment)* | *{code_mixed_count:,d}* | *{code_mixed_count / total_processed * 100:.2f}%* |\n")
        f.write("\n## Breakdown by Mobile Network Operator\n\n")
        f.write("| Operator | Total Reviews | English (%) | Bangla Script (%) | Romanized Banglish (%) | Symbolic (%) |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")
        for op, data in op_breakdown.items():
            d = data["distribution"]
            en_pct = d.get("English", {}).get("percentage", 0.0)
            bn_pct = d.get("Bangla (Native Script)", {}).get("percentage", 0.0)
            bg_pct = d.get("Romanized Banglish", {}).get("percentage", 0.0)
            sy_pct = d.get("Symbolic / Emoticons", {}).get("percentage", 0.0)
            f.write(f"| **{op}** | {data['total']:,d} | {en_pct:.2f}% | {bn_pct:.2f}% | {bg_pct:.2f}% | {sy_pct:.2f}% |\n")

    print(f"\nSaved analysis JSON to: {OUTPUT_JSON}")
    print(f"Saved analysis Markdown to: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
