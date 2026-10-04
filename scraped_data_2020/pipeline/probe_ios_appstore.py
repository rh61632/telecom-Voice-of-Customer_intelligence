"""
Pipeline Utility: probe_ios_appstore.py
Purpose: Empirical evaluation and scraping of Apple App Store (iOS) customer reviews
         for Grameenphone (MyGP), Banglalink (MyBL), and Robi (MyRobi).
Quantifies why iOS is methodologically excluded from the primary Voice-of-Customer dataset.
"""

import sys
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
import csv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUT_DIR = PROJECT_ROOT / "scraped_data_2020" / "ios_probe"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = OUT_DIR / "ios_scraped_reviews_empirical_probe.csv"
OUT_SUMMARY = OUT_DIR / "ios_probe_summary.json"

APPS = {
    "Grameenphone": "MyGP",
    "Banglalink": "My Banglalink",
    "Robi": "My Robi",
}

COUNTRIES = ["bd", "us"]


def search_app(term, country="bd"):
    url = f"https://itunes.apple.com/search?term={urllib.parse.quote(term)}&country={country}&entity=software&limit=5"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("results", [])
            if results:
                for r in results:
                    return {
                        "name": r.get("trackName", ""),
                        "id": r.get("trackId"),
                        "rating_count": r.get("userRatingCount", 0),
                        "avg_rating": r.get("averageUserRating", 0.0),
                    }
    except Exception as e:
        print(f"Error searching {term} in {country}: {e}")
    return None


def fetch_reviews(app_id, country="bd", max_pages=10):
    all_reviews = []
    for page in range(1, max_pages + 1):
        url = f"https://itunes.apple.com/{country}/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                entries = data.get("feed", {}).get("entry", [])
                if not entries:
                    break
                for entry in entries:
                    if "im:rating" in entry and "content" in entry:
                        r_id = entry.get("id", {}).get("label")
                        rating = entry.get("im:rating", {}).get("label")
                        title = entry.get("title", {}).get("label", "")
                        content = entry.get("content", {}).get("label", "")
                        date_str = entry.get("updated", {}).get("label", "")
                        
                        all_reviews.append({
                            "review_id": r_id,
                            "rating": rating,
                            "title": title,
                            "content": content,
                            "review_date": date_str,
                            "storefront": country.upper(),
                        })
            time.sleep(0.3)
        except urllib.error.HTTPError as e:
            if e.code in (404, 400):
                break
        except Exception:
            break
            
    # Deduplicate
    seen = set()
    unique = []
    for r in all_reviews:
        if r["review_id"] not in seen:
            seen.add(r["review_id"])
            unique.append(r)
    return unique


def run_ios_probe():
    print("=" * 75)
    print("   EMPIRICAL iOS APP STORE SCRAPING PROBE — BANGLADESH TELCOS")
    print("=" * 75)

    app_meta = {}
    for op, term in APPS.items():
        meta = search_app(term, "bd") or search_app(term, "us")
        if meta:
            print(f"✓ Found {op}: '{meta['name']}' (ID: {meta['id']}) | {meta['avg_rating']:.2f}★ ({meta['rating_count']:,d} ratings)")
            app_meta[op] = meta

    all_scraped_rows = []
    summary_data = {}

    for op, meta in app_meta.items():
        op_revs = []
        for country in COUNTRIES:
            revs = fetch_reviews(meta["id"], country=country)
            op_revs.extend(revs)

        # Deduplicate
        seen = set()
        deduped = []
        for r in op_revs:
            if r["review_id"] not in seen:
                seen.add(r["review_id"])
                r["operator"] = op
                deduped.append(r)
                all_scraped_rows.append(r)

        dates = sorted([r["review_date"][:10] for r in deduped if r.get("review_date")])
        date_span = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

        summary_data[op] = {
            "app_name": meta["name"],
            "app_id": meta["id"],
            "total_app_store_ratings": meta["rating_count"],
            "avg_star_rating": meta["avg_rating"],
            "scraped_text_reviews": len(deduped),
            "date_span": date_span,
            "earliest_date": dates[0] if dates else None,
            "latest_date": dates[-1] if dates else None,
        }
        print(f"  • {op}: Scraped {len(deduped):,d} text reviews (Span: {date_span})")

    # Save to CSV
    if all_scraped_rows:
        fieldnames = ["operator", "review_id", "rating", "review_date", "storefront", "title", "content"]
        with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in all_scraped_rows:
                writer.writerow({k: r.get(k, "") for k in fieldnames})
        print(f"\n✓ Saved {len(all_scraped_rows):,d} raw iOS reviews to: {OUT_CSV}")

    # Save summary JSON
    with open(OUT_SUMMARY, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)
    print(f"✓ Saved probe summary metadata to: {OUT_SUMMARY}")
    print("=" * 75)


if __name__ == "__main__":
    run_ios_probe()
