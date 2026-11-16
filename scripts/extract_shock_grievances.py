"""
scripts/extract_shock_grievances.py
=============================================================================
Statistical Grievance Term Extraction and Root-Cause Attribution Engine
Uses Weighted Log-Odds Ratio with an Informative Dirichlet Prior (Monroe et al., 2008)
to prove why specific operational categories plunged during telecom sentiment shocks.
=============================================================================
"""

import os
import re
import json
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

STOPWORDS = {
    # English standard stopwords
    'the', 'is', 'and', 'to', 'for', 'in', 'of', 'this', 'that', 'it', 'on', 'are', 'was',
    'my', 'at', 'by', 'from', 'with', 'as', 'be', 'an', 'have', 'has', 'had', 'do', 'does',
    'did', 'can', 'will', 'very', 'too', 'so', 'me', 'you', 'your', 'we', 'our', 'they',
    'app', 'apps', 'gp', 'mygp', 'robi', 'myrobi', 'banglalink', 'mybl', 'please', 'pls',
    'good', 'bad', 'bhalo', 'valo', 'service', 'operator', 'sim', 'customer', 'care',
    # Bengali common functional stopwords
    'এই', 'একটি', 'এবং', 'করা', 'করে', 'হয়', 'না', 'কি', 'বা', 'জন্য', 'থেকে', 'হবে',
    'আর', 'যে', 'এর', 'সব', 'কে', 'কিন্তু', 'যদি', 'আমি', 'আমার', 'তুমি', 'তোমার',
    'তারা', 'তাদের', 'দিয়ে', 'নিয়ে', 'আছে', 'ছিল', 'হলে', 'বলে', 'হচ্ছে', 'করছে',
    'করতে', 'যায়', 'দিতে', 'নেয়', 'হতে', 'পারে', 'পর', 'এখন', 'অনেক', 'একটু', 'খুব'
}

def compute_log_odds_z_scores(target_texts, background_texts, min_count=3, ngram_range=(1, 2)):
    """
    Computes Dirichlet-prior Log-Odds Z-scores comparing target shock corpus against background corpus.
    Formula: Monroe, Colaresi, & Quinn (2008), Political Analysis.
    """
    vec = CountVectorizer(
        ngram_range=ngram_range,
        min_df=min_count,
        token_pattern=r'(?u)\b[\w\u0980-\u09FF]{2,}\b',
        stop_words=list(STOPWORDS)
    )
    
    # Fit on combined corpus
    all_texts = list(target_texts) + list(background_texts)
    if len(target_texts) == 0 or len(background_texts) == 0:
        return []
    
    vec.fit(all_texts)
    vocab = vec.get_feature_names_out()
    
    # Counts
    y1 = np.array(vec.transform(target_texts).sum(axis=0)).flatten()
    y2 = np.array(vec.transform(background_texts).sum(axis=0)).flatten()
    
    n1 = y1.sum()
    n2 = y2.sum()
    
    if n1 == 0 or n2 == 0:
        return []
        
    # Dirichlet prior parameter alpha_w proportional to background frequencies
    alpha = y2 + 0.1
    alpha_0 = alpha.sum()
    
    # Log-odds calculation
    log_odds_1 = np.log((y1 + alpha) / (n1 + alpha_0 - y1 - alpha))
    log_odds_2 = np.log((y2 + alpha) / (n2 + alpha_0 - y2 - alpha))
    delta = log_odds_1 - log_odds_2
    
    # Variance & Z-score
    variance = (1.0 / (y1 + alpha)) + (1.0 / (y2 + alpha))
    z_scores = delta / np.sqrt(variance)
    
    results = []
    for word, count_target, count_bg, z in zip(vocab, y1, y2, z_scores):
        if count_target >= min_count:
            results.append({
                "term": word,
                "target_count": int(count_target),
                "background_count": int(count_bg),
                "z_score": round(float(z), 3)
            })
            
    results = sorted(results, key=lambda x: x["z_score"], reverse=True)
    return results

def analyze_operator_shock(df, operator, shock_months, target_category, shock_name):
    print(f"\n==================================================================")
    print(f"SHOCK CASE: {shock_name} ({operator})")
    print(f"Target Months: {shock_months} | Focus Category: {target_category}")
    print(f"==================================================================")
    
    op_df = df[df['operator'].str.lower() == operator.lower()].copy()
    op_df['review_date'] = pd.to_datetime(op_df['review_date'], errors='coerce')
    op_df['ym'] = op_df['review_date'].dt.strftime('%Y-%m')
    
    # Filter target reviews: Negative reviews in the target category during shock months
    shock_reviews = op_df[
        (op_df['ym'].isin(shock_months)) &
        (op_df['predicted_sentiment'] == 'Negative') &
        (op_df['predicted_category'] == target_category)
    ]['review_text'].dropna().tolist()
    
    # Background reviews: Negative reviews in the same category during all other months
    bg_reviews = op_df[
        (~op_df['ym'].isin(shock_months)) &
        (op_df['predicted_sentiment'] == 'Negative') &
        (op_df['predicted_category'] == target_category)
    ]['review_text'].dropna().tolist()
    
    print(f"Target Negative Reviews in Shock Window: {len(shock_reviews):,}")
    print(f"Baseline Negative Reviews in Comparison Window: {len(bg_reviews):,}")
    
    if len(shock_reviews) < 5:
        print("Insufficient reviews to compute statistically robust z-scores.")
        return None
        
    z_results = compute_log_odds_z_scores(shock_reviews, bg_reviews, min_count=3, ngram_range=(1, 2))
    
    print(f"\nTop Over-Represented Grievance Terms (Dirichlet Log-Odds Z-Score):")
    print(f"{'Term / N-Gram':<25} | {'Shock Count':<12} | {'Baseline Count':<14} | {'Z-Score':<8}")
    print("-" * 65)
    for res in z_results[:12]:
        print(f"{res['term']:<25} | {res['target_count']:<12} | {res['background_count']:<14} | {res['z_score']:<8.2f}")
        
    # Extract representative quotes that contain the top z-score terms
    top_terms = [r['term'] for r in z_results[:5]]
    exemplars = []
    # Pass 1: High-density matches (>=2 terms)
    for r in shock_reviews:
        score = sum(1 for t in top_terms if t in r.lower())
        if score >= 2 and len(r.split()) >= 4:
            exemplars.append(r.strip().replace('\n', ' '))
            if len(exemplars) >= 3:
                break
                
    # Pass 2: Fallback for concise single-term complaints if fewer than 3 found
    if len(exemplars) < 3:
        for r in shock_reviews:
            clean_r = r.strip().replace('\n', ' ')
            if clean_r in exemplars:
                continue
            score = sum(1 for t in top_terms if t in r.lower())
            if score >= 1 and len(r.split()) >= 4:
                exemplars.append(clean_r)
                if len(exemplars) >= 3:
                    break
                
    print(f"\nCanonical Representative Review Exemplars:")
    for idx, ex in enumerate(exemplars, 1):
        print(f"  {idx}. \"{ex}\"")
        
    return {
        "operator": operator,
        "shock_name": shock_name,
        "shock_months": shock_months,
        "category": target_category,
        "target_count": len(shock_reviews),
        "baseline_count": len(bg_reviews),
        "top_grievance_terms": z_results[:15],
        "representative_exemplars": exemplars
    }

def main():
    data_path = 'scraped_data_global/classified/all_operators_classified_global.csv'
    print(f"Loading full classified dataset from {data_path}...")
    df = pd.read_csv(data_path, usecols=['operator', 'review_date', 'review_text', 'predicted_sentiment', 'predicted_category'])
    
    shocks_to_analyze = [
        {
            "operator": "Grameenphone",
            "months": ["2025-08", "2025-09", "2026-06"],
            "category": "Offers & Data Packs",
            "name": "BTRC Package Restructuring & 5G Tariff Backlash"
        },
        {
            "operator": "Banglalink",
            "months": ["2024-03", "2024-04", "2024-05"],
            "category": "App Login & Technical Bugs",
            "name": "MyBL v11.8.0 Splash Crash & Authentication Loop"
        },
        {
            "operator": "Banglalink",
            "months": ["2021-04", "2021-05", "2021-07"],
            "category": "Network Speed & 4G Latency",
            "name": "Monsoon Fiber Cut & Base Station Backhaul Outage"
        },
        {
            "operator": "Robi",
            "months": ["2018-01", "2018-02", "2018-03"],
            "category": "Offers & Data Packs",
            "name": "4G Commercial Tariff Realignment Backlash"
        }
    ]
    
    all_evidence = []
    for s in shocks_to_analyze:
        res = analyze_operator_shock(df, s["operator"], s["months"], s["category"], s["name"])
        if res:
            all_evidence.append(res)
            
    out_file = 'scraped_data_global/classified/shock_grievance_statistical_evidence.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(all_evidence, f, indent=2, ensure_ascii=False)
    print(f"\n[SUCCESS] Statistical grievance evidence exported to {out_file}")

if __name__ == '__main__':
    main()
