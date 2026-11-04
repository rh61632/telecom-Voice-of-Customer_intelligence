import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['review_date'] = pd.to_datetime(df['review_date'])
df['year_month'] = df['review_date'].dt.to_period('M')

print("==================================================")
print("AUDIT: EXACT CATEGORY MATCHES & TEXT RECONCILIATION")
print("==================================================")

cats = [
    'App Login & Technical Bugs',
    'Offers & Data Packs',
    'Network Speed & 4G Latency',
    'Billing & Airtime Deductions',
    'General Appreciation / Other'
]

# 1. Total across 4 domains
sub_4 = df[df['predicted_category'].isin(cats[:4])]
print(f"Total reviews in 4 domains: {len(sub_4)} (Paper says: 88,184)")

# Table 3 check
print("\n--- TABLE 3 AUDIT (Exact) ---")
for op in ['Grameenphone', 'Robi', 'Banglalink']:
    sub = df[df['operator'] == op]
    tot_op = len(sub)
    print(f"\n{op} (N={tot_op}):")
    for cat in cats[:4]:
        sub_cat = sub[sub['predicted_category'] == cat]
        neg_cat = (sub_cat['predicted_sentiment'] == 'Negative').sum()
        opt_a = neg_cat / tot_op * 100.0
        opt_b = neg_cat / len(sub_cat) * 100.0 if len(sub_cat) > 0 else 0
        print(f"  {cat}: Option A = {opt_a:.2f}%, Option B = {opt_b:.2f}% (Tot in Cat: {len(sub_cat)}, Neg: {neg_cat})")

# General / Other share
print("\nGeneral / Other Share & Negativity Share:")
for op in ['Grameenphone', 'Robi', 'Banglalink']:
    sub = df[df['operator'] == op]
    gen = sub[sub['predicted_category'] == 'General Appreciation / Other']
    gen_share = len(gen) / len(sub) * 100.0
    tot_neg = (sub['predicted_sentiment'] == 'Negative').sum()
    gen_neg = (gen['predicted_sentiment'] == 'Negative').sum()
    gen_neg_share = gen_neg / tot_neg * 100.0
    print(f"  {op}: share = {gen_share:.1f}%, share of all negatives = {gen_neg_share:.1f}%")

# Table 6 Decompositions
print("\n--- TABLE 6 TRANSITIONS AUDIT (Exact) ---")
m_sub = df[(df['review_date'] >= '2020-01-01') & (df['review_date'] <= '2026-09-30')]

transitions_to_check = [
    ('Grameenphone', '2020-03', '2020-04'),
    ('Grameenphone', '2021-04', '2021-05'),
    ('Grameenphone', '2021-08', '2021-09'),
    ('Grameenphone', '2025-08', '2025-09'),
    ('Robi', '2022-12', '2023-01'),
    ('Robi', '2023-01', '2023-02'),
    ('Robi', '2023-11', '2023-12'),
    ('Banglalink', '2021-04', '2021-05'),
    ('Banglalink', '2024-03', '2024-04'),
    ('Banglalink', '2024-04', '2024-05')
]

for op, m1_str, m2_str in transitions_to_check:
    m1 = pd.Period(m1_str, 'M')
    m2 = pd.Period(m2_str, 'M')
    
    op_data = m_sub[m_sub['operator'] == op]
    t1 = op_data[op_data['year_month'] == m1]
    t2 = op_data[op_data['year_month'] == m2]
    
    nss1 = ((t1['predicted_sentiment'] == 'Positive').sum() - (t1['predicted_sentiment'] == 'Negative').sum()) / len(t1) * 100.0
    nss2 = ((t2['predicted_sentiment'] == 'Positive').sum() - (t2['predicted_sentiment'] == 'Negative').sum()) / len(t2) * 100.0
    delta = nss2 - nss1
    
    print(f"\n{op} {m1_str} -> {m2_str}: Delta NSS = {delta:+.2f}")
    for c in cats:
        c1 = ((t1['predicted_category'] == c) & (t1['predicted_sentiment'] == 'Positive')).sum() - ((t1['predicted_category'] == c) & (t1['predicted_sentiment'] == 'Negative')).sum()
        c2 = ((t2['predicted_category'] == c) & (t2['predicted_sentiment'] == 'Positive')).sum() - ((t2['predicted_category'] == c) & (t2['predicted_sentiment'] == 'Negative')).sum()
        impact = (c2 / len(t2) * 100.0) - (c1 / len(t1) * 100.0)
        share = (impact / delta) * 100.0
        print(f"    {c}: Impact={impact:+.2f}, Share={share:.1f}%")
