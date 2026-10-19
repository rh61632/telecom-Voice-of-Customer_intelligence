"""
Script: calculate_agreement.py
Purpose: Compute Cohen's Kappa and inter-annotator agreement between Ratul and second annotator (Friend).
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
    ratul_candidates = [
        GOLD_DIR / "blind_annotation_300_ratul.csv",
        GOLD_DIR.parent / "pipeline" / "blind_annotation_300_ratul.csv",
        Path.cwd() / "blind_annotation_300_ratul.csv",
        PROJECT_ROOT / "blind_annotation_300_ratul.csv",
        GOLD_DIR / "blind_annotation_600_ratul.csv",
        Path.cwd() / "blind_annotation_600_ratul.csv",
        PROJECT_ROOT / "blind_annotation_600_ratul.csv",
    ]
    friend_candidates = [
        GOLD_DIR / "blind_annotation_200_friend.csv",
        GOLD_DIR.parent / "pipeline" / "blind_annotation_200_friend.csv",
        Path.cwd() / "blind_annotation_200_friend.csv",
        PROJECT_ROOT / "blind_annotation_200_friend.csv",
    ]
    return resolve_best_file(ratul_candidates), resolve_best_file(friend_candidates)


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

    ratul_csv, friend_csv = resolve_files()
    if not ratul_csv or not friend_csv:
        print("Missing annotation CSV files.")
        print(f"Ratul file found : {ratul_csv}")
        print(f"Friend file found: {friend_csv}")
        return

    print(f"Ratul CSV : {ratul_csv}")
    print(f"Friend CSV: {friend_csv}")

    with open(ratul_csv, "r", encoding="utf-8-sig") as f:
        r_rows = list(csv.DictReader(f))
    with open(friend_csv, "r", encoding="utf-8-sig") as f:
        f_rows = list(csv.DictReader(f))

    r_dict = {r["sample_id"]: r for r in r_rows if "sample_id" in r}
    f_dict = {r["sample_id"]: r for r in f_rows if "sample_id" in r}

    r_annotated_count = sum(1 for r in r_rows if r.get("sentiment_label", "").strip())
    f_annotated_count = sum(1 for r in f_rows if r.get("sentiment_label", "").strip())

    common_ids = [sid for sid in r_dict if sid in f_dict]
    paired = []
    for sid in common_ids:
        s_r = r_dict[sid].get("sentiment_label", "").strip()
        s_f = f_dict[sid].get("sentiment_label", "").strip()
        if s_r and s_f:
            paired.append({
                "sample_id": sid,
                "operator": r_dict[sid].get("operator", ""),
                "rating": r_dict[sid].get("rating", ""),
                "review_text": r_dict[sid].get("review_text", ""),
                "sentiment_ratul": s_r,
                "sentiment_friend": s_f,
                "category_ratul": r_dict[sid].get("category_label", "").strip(),
                "category_friend": f_dict[sid].get("category_label", "").strip(),
            })

    total_paired = len(paired)
    if total_paired == 0:
        print("No overlapping reviews have been annotated by both annotators yet.")
        print(f"Ratul completed : {r_annotated_count} / {len(r_rows)}")
        print(f"Friend completed: {f_annotated_count} / {len(f_rows)}")
        return

    print(f"\nTotal overlapping reviews evaluated: {total_paired} / {len(common_ids)}")

    # 1. Sentiment Agreement
    y_r = [p["sentiment_ratul"] for p in paired]
    y_f = [p["sentiment_friend"] for p in paired]
    labels = ["Positive", "Neutral", "Negative"]

    raw_agreement, kappa = compute_kappa(y_r, y_f, labels)

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

    # Confusion matrix
    print("\nConfusion Matrix (Rows: Ratul, Columns: Friend):")
    header = f"{'':15s}" + "".join([f"{l:>12s}" for l in labels])
    print(header)
    for l_r in labels:
        row_str = f"{'Ratul_' + l_r:15s}"
        for l_f in labels:
            c = sum(1 for a, b in zip(y_r, y_f) if a == l_r and b == l_f)
            row_str += f"{c:>12d}"
        print(row_str)

    # Disagreements
    disagreements = [p for p in paired if p["sentiment_ratul"] != p["sentiment_friend"]]
    if disagreements:
        print(f"\nSentiment Disagreements ({len(disagreements)} cases):")
        for p in disagreements[:10]:
            print(f"  [{p['sample_id']}] Ratul: {p['sentiment_ratul']} vs Friend: {p['sentiment_friend']}")
            print(f"    Rating: {p['rating']}★ | \"{p['review_text']}\"\n")

    # 2. Category Agreement
    paired_cat = [p for p in paired if p["category_ratul"] and p["category_friend"]]
    if paired_cat:
        y_r_c = [p["category_ratul"] for p in paired_cat]
        y_f_c = [p["category_friend"] for p in paired_cat]
        cat_labels = [
            "Billing & Airtime Deductions",
            "App Login & Technical Bugs",
            "Network Speed & 4G Latency",
            "Offers & Data Packs",
            "General Appreciation / Other",
        ]
        raw_c, kappa_c = compute_kappa(y_r_c, y_f_c, cat_labels)
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

        disagreements_c = [p for p in paired_cat if p["category_ratul"] != p["category_friend"]]
        if disagreements_c:
            print(f"\nCategory Disagreements ({len(disagreements_c)} cases):")
            for p in disagreements_c[:10]:
                print(f"  [{p['sample_id']}] Ratul: {p['category_ratul']} vs Friend: {p['category_friend']}")
                print(f"    Rating: {p['rating']}★ | \"{p['review_text']}\"\n")


if __name__ == "__main__":
    evaluate_agreement()

