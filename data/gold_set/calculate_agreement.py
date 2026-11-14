"""
Script: calculate_agreement.py
Purpose: Compute Cohen's Kappa and inter-annotator agreement between Annotator 1 and Annotator 2.
"""

from pathlib import Path
import csv
from collections import Counter

GOLD_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = GOLD_DIR.parent.parent


def count_annotations(filepath):
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            return sum(1 for r in reader if r.get("sentiment_label", "").strip())
    except Exception:
        return -1


def resolve_best_file(candidates):
    existing = [c for c in candidates if c.exists()]
    if not existing:
        return None
    # Pick the candidate file with the most completed annotations
    existing.sort(key=lambda p: count_annotations(p), reverse=True)
    return existing[0]


def resolve_files():
    annotator1_candidates = [
        GOLD_DIR / "blind_annotation_300_annotator1.csv",
        GOLD_DIR.parent / "pipeline" / "blind_annotation_300_annotator1.csv",
        Path.cwd() / "blind_annotation_300_annotator1.csv",
        PROJECT_ROOT / "blind_annotation_300_annotator1.csv",
    ]
    annotator2_candidates = [
        GOLD_DIR / "blind_annotation_200_annotator2.csv",
        GOLD_DIR.parent / "pipeline" / "blind_annotation_200_annotator2.csv",
        Path.cwd() / "blind_annotation_200_annotator2.csv",
        PROJECT_ROOT / "blind_annotation_200_annotator2.csv",
    ]
    return resolve_best_file(annotator1_candidates), resolve_best_file(annotator2_candidates)


def compute_kappa(y1, y2, categories):
    n = len(y1)
    if n == 0:
        return 0.0, 0.0
    po = sum(1 for a, b in zip(y1, y2) if a == b) / n
    pe = sum((y1.count(c) / n) * (y2.count(c) / n) for c in categories)
    if pe >= 1.0:
        kappa = 1.0
    else:
        kappa = (po - pe) / (1.0 - pe)
    return po * 100, kappa


def evaluate_agreement():
    print("=" * 70)
    print("      INTER-ANNOTATOR AGREEMENT & COHEN'S KAPPA EVALUATION")
    print("=" * 70)

    ann1_csv, ann2_csv = resolve_files()
    if not ann1_csv or not ann2_csv:
        print("Missing annotation CSV files.")
        print(f"Annotator 1 file found: {ann1_csv}")
        print(f"Annotator 2 file found: {ann2_csv}")
        return

    print(f"Annotator 1 CSV: {ann1_csv}")
    print(f"Annotator 2 CSV: {ann2_csv}")

    with open(ann1_csv, "r", encoding="utf-8-sig") as f:
        ann1_rows = list(csv.DictReader(f))
    with open(ann2_csv, "r", encoding="utf-8-sig") as f:
        ann2_rows = list(csv.DictReader(f))

    ann1_dict = {r["sample_id"]: r for r in ann1_rows if "sample_id" in r}
    ann2_dict = {r["sample_id"]: r for r in ann2_rows if "sample_id" in r}

    ann1_annotated_count = sum(1 for r in ann1_rows if r.get("sentiment_label", "").strip())
    ann2_annotated_count = sum(1 for r in ann2_rows if r.get("sentiment_label", "").strip())

    common_ids = [sid for sid in ann1_dict if sid in ann2_dict]
    paired = []
    for sid in common_ids:
        s_1 = ann1_dict[sid].get("sentiment_label", "").strip()
        s_2 = ann2_dict[sid].get("sentiment_label", "").strip()
        if s_1 and s_2:
            paired.append({
                "sample_id": sid,
                "operator": ann1_dict[sid].get("operator", ""),
                "rating": ann1_dict[sid].get("rating", ""),
                "review_text": ann1_dict[sid].get("review_text", ""),
                "sentiment_ann1": s_1,
                "sentiment_ann2": s_2,
                "category_ann1": ann1_dict[sid].get("category_label", "").strip(),
                "category_ann2": ann2_dict[sid].get("category_label", "").strip(),
            })

    total_paired = len(paired)
    if total_paired == 0:
        print("No overlapping reviews have been annotated by both annotators yet.")
        print(f"Annotator 1 completed: {ann1_annotated_count} / {len(ann1_rows)}")
        print(f"Annotator 2 completed: {ann2_annotated_count} / {len(ann2_rows)}")
        return

    print(f"\nTotal overlapping reviews evaluated: {total_paired} / {len(common_ids)}")

    # 1. Sentiment Agreement
    y_1 = [p["sentiment_ann1"] for p in paired]
    y_2 = [p["sentiment_ann2"] for p in paired]
    labels = ["Positive", "Neutral", "Negative"]

    raw_agreement, kappa = compute_kappa(y_1, y_2, labels)

    print(f"\n📊 SENTIMENT RESULTS:")
    print(f"  • Raw Percentage Agreement : {raw_agreement:.2f}%")
    print(f"  • Cohen's Kappa (κ)         : {kappa:.4f}")

    if kappa > 0.80:
        interp = "Near Perfect Agreement"
    elif kappa > 0.60:
        interp = "Substantial Agreement"
    elif kappa > 0.40:
        interp = "Moderate Agreement"
    else:
        interp = "Fair / Slight Agreement"
    print(f"  • Interpretation            : {interp}")

    # Per-Operator Sentiment Breakdown
    print("\n📊 PER-OPERATOR SENTIMENT BREAKDOWN:")
    for op in ["Grameenphone", "Banglalink", "Robi"]:
        op_paired = [p for p in paired if p["operator"] == op]
        if op_paired:
            op_y1 = [p["sentiment_ann1"] for p in op_paired]
            op_y2 = [p["sentiment_ann2"] for p in op_paired]
            op_raw, op_k = compute_kappa(op_y1, op_y2, labels)
            print(f"  • {op:13s} (N={len(op_paired)}): agreement {op_raw:.2f}%, κ = {op_k:.4f}")

    # Confusion matrix
    print("\nConfusion Matrix (Rows: Annotator 1, Columns: Annotator 2):")
    header = f"{'':15s}" + "".join([f"{l:>12s}" for l in labels])
    print(header)
    for l_1 in labels:
        row_str = f"{'Ann1_' + l_1:15s}"
        for l_2 in labels:
            c = sum(1 for a, b in zip(y_1, y_2) if a == l_1 and b == l_2)
            row_str += f"{c:>12d}"
        print(row_str)

    # Disagreements
    disagreements = [p for p in paired if p["sentiment_ann1"] != p["sentiment_ann2"]]
    if disagreements:
        print(f"\nSentiment Disagreements ({len(disagreements)} cases):")
        for p in disagreements[:10]:
            print(f"  [{p['sample_id']}] Annotator 1: {p['sentiment_ann1']} vs Annotator 2: {p['sentiment_ann2']}")
            print(f"    Rating: {p['rating']}★ | \"{p['review_text']}\"\n")

    # 2. Category Agreement
    paired_cat = [p for p in paired if p["category_ann1"] and p["category_ann2"]]
    if paired_cat:
        y_1_c = [p["category_ann1"] for p in paired_cat]
        y_2_c = [p["category_ann2"] for p in paired_cat]
        cat_labels = [
            "Billing & Airtime Deductions",
            "App Login & Technical Bugs",
            "Network Speed & 4G Latency",
            "Offers & Data Packs",
            "General Appreciation / Other",
        ]
        raw_c, kappa_c = compute_kappa(y_1_c, y_2_c, cat_labels)
        print(f"\n📊 OPERATIONAL CATEGORY RESULTS (N={len(paired_cat)}):")
        print(f"  • Raw Percentage Agreement : {raw_c:.2f}%")
        print(f"  • Cohen's Kappa (κ)         : {kappa_c:.4f}")

        if kappa_c > 0.80:
            interp_c = "Near Perfect Agreement"
        elif kappa_c > 0.60:
            interp_c = "Substantial Agreement"
        elif kappa_c > 0.40:
            interp_c = "Moderate Agreement"
        else:
            interp_c = "Fair / Slight Agreement"
        print(f"  • Interpretation            : {interp_c}")

        disagreements_c = [p for p in paired_cat if p["category_ann1"] != p["category_ann2"]]
        if disagreements_c:
            print(f"\nCategory Disagreements ({len(disagreements_c)} cases):")
            for p in disagreements_c[:10]:
                print(f"  [{p['sample_id']}] Annotator 1: {p['category_ann1']} vs Annotator 2: {p['category_ann2']}")
                print(f"    Rating: {p['rating']}★ | \"{p['review_text']}\"\n")


if __name__ == "__main__":
    evaluate_agreement()
