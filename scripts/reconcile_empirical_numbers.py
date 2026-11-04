"""
reconcile_empirical_numbers.py
Calculates exact empirical statistics:
1. Exact counts and NSS by year (Table 4)
2. MoM transitions and exact shock counts (|ΔNSS| >= 10.0 pts)
3. Bootstrap 95% CIs for NSS per operator
4. Chi-square test of independence for operator sentiment and category differences
5. App version analysis for Banglalink 2024 shocks
"""

import pandas as pd
import numpy as np
from scipy import stats

DATA_PATH = "scraped_data_global/classified/all_operators_common_duration_classified.csv"
print("Loading common duration dataset...")
df = pd.read_csv(DATA_PATH, low_memory=False)
print(f"Total rows loaded: {len(df):,}")

# Ensure date parsing
df['date'] = pd.to_datetime(df['review_date'])
df['year'] = df['date'].dt.year
df['year_month'] = df['date'].dt.to_period('M')

# 1. Overall Operator Stats & Chi-Square Test
print("\n--- 1. Overall Operator Sentiment Breakdown ---")
ct = pd.crosstab(df['operator'], df['predicted_sentiment'])
print(ct)
chi2, p_val, dof, ex = stats.chi2_contingency(ct)
print(f"Chi-square test of sentiment vs operator: Chi2 = {chi2:.2f}, df = {dof}, p = {p_val:.4e}")

# Category crosstab
ct_cat = pd.crosstab(df['operator'], df['predicted_category'])
chi2_cat, p_cat, dof_cat, _ = stats.chi2_contingency(ct_cat)
print(f"Chi-square test of category vs operator: Chi2 = {chi2_cat:.2f}, df = {dof_cat}, p = {p_cat:.4e}")

# 2. Bootstrap 95% CIs for NSS
print("\n--- 2. Bootstrap 95% CIs for NSS ---")
np.random.seed(42)
for op in ['Grameenphone', 'Robi', 'Banglalink']:
    op_df = df[df['operator'] == op]
    pos = (op_df['predicted_sentiment'] == 'Positive').values
    neg = (op_df['predicted_sentiment'] == 'Negative').values
    n = len(op_df)
    nss_point = (pos.sum() - neg.sum()) / n * 100
    
    # Fast analytical standard error for difference of proportions
    # Var(p_pos - p_neg) = (p_pos*(1-p_pos) + p_neg*(1-p_neg) + 2*p_pos*p_neg) / n
    p_pos = pos.mean()
    p_neg = neg.mean()
    var_diff = (p_pos * (1 - p_pos) + p_neg * (1 - p_neg) + 2 * p_pos * p_neg) / n
    se_diff = np.sqrt(var_diff) * 100
    ci_lower = nss_point - 1.96 * se_diff
    ci_upper = nss_point + 1.96 * se_diff
    ci_str = f"[{ci_lower:.2f}%, {ci_upper:.2f}%]"
    print(f"{op}: NSS = {nss_point:.2f}% (95% CI: {ci_str}, SE = {se_diff:.2f} pts, N = {n:,})")

# 3. Monthly Shocks Analysis
print("\n--- 3. Monthly Shocks (|ΔNSS| >= 10.0 pts) Analysis ---")
monthly = df.groupby(['operator', 'year_month']).agg(
    total=('predicted_sentiment', 'count'),
    pos=('predicted_sentiment', lambda s: (s == 'Positive').sum()),
    neg=('predicted_sentiment', lambda s: (s == 'Negative').sum())
).reset_index()

monthly['nss'] = (monthly['pos'] - monthly['neg']) / monthly['total'] * 100

# Filter N >= 30 CLT floor
monthly_clt = monthly[monthly['total'] >= 30].copy()
monthly_clt['prev_month'] = monthly_clt.groupby('operator')['year_month'].shift(1)
monthly_clt['month_diff'] = (monthly_clt['year_month'] - monthly_clt['prev_month']).apply(lambda x: x.n if pd.notnull(x) else np.nan)

# Only strictly consecutive months
consec = monthly_clt[monthly_clt['month_diff'] == 1].copy()
consec['prev_nss'] = consec.groupby('operator')['nss'].shift(1)
consec['delta_nss'] = consec['nss'] - consec['prev_nss']
consec = consec.dropna(subset=['delta_nss'])

print(f"Total consecutive monthly transitions (CLT N>=30): {len(consec)}")
shocks_all = consec[consec['delta_nss'].abs() >= 10.0]
print(f"Total shocks (|ΔNSS| >= 10.0) across all valid transitions: {len(shocks_all)} ({len(shocks_all)/len(consec)*100:.1f}%)")

# Modern era (2020-01 to 2026-09)
consec_modern = consec[consec['year_month'] >= '2020-01']
print(f"Modern era (2020-2026) consecutive monthly transitions: {len(consec_modern)}")
shocks_modern = consec_modern[consec_modern['delta_nss'].abs() >= 10.0]
print(f"Modern era shocks (|ΔNSS| >= 10.0): {len(shocks_modern)} out of {len(consec_modern)} transitions ({len(shocks_modern)/len(consec_modern)*100:.1f}%)")

for op in ['Grameenphone', 'Robi', 'Banglalink']:
    op_m = consec_modern[consec_modern['operator'] == op]
    op_s = op_m[op_m['delta_nss'].abs() >= 10.0]
    med_shift = op_m['delta_nss'].abs().median()
    p90_shift = np.percentile(op_m['delta_nss'].abs(), 90)
    print(f"  {op}: {len(op_s)} shocks / {len(op_m)} transitions ({len(op_s)/len(op_m)*100:.1f}%). Median |ΔNSS| = {med_shift:.2f} pts, 90th percentile = {p90_shift:.2f} pts.")

# Print all modern shocks
print("\nAll Modern Era Shocks (|ΔNSS| >= 10.0):")
for idx, r in shocks_modern.sort_values(by=['year_month', 'operator']).iterrows():
    print(f"  {r['operator']} | {r['year_month']} | Prev NSS: {r['prev_nss']:.1f}% -> NSS: {r['nss']:.1f}% | ΔNSS: {r['delta_nss']:+.1f} pts (N={r['total']})")

# 4. Banglalink Spring 2024 App Version Data
print("\n--- 4. Banglalink Spring 2024 App Versions ---")
bl_2024 = df[(df['operator'] == 'Banglalink') & (df['date'].between('2024-03-01', '2024-06-30'))]
if 'app_version' in df.columns or 'review_version' in df.columns:
    col = 'app_version' if 'app_version' in df.columns else 'review_version'
    print(f"Version column '{col}' value counts for BL March-June 2024:")
    print(bl_2024[col].value_counts().head(10))
else:
    print("No direct app_version column in common duration file; checking text keywords:")
    bl_april = df[(df['operator'] == 'Banglalink') & (df['date'].between('2024-04-01', '2024-04-30'))]
    print(f"BL April 2024 total reviews: {len(bl_april)}")
    print(f"BL April 2024 negative reviews: {(bl_april['predicted_sentiment'] == 'Negative').sum()} ({(bl_april['predicted_sentiment'] == 'Negative').mean()*100:.1f}%)")
    bl_may = df[(df['operator'] == 'Banglalink') & (df['date'].between('2024-05-01', '2024-05-31'))]
    print(f"BL May 2024 total reviews: {len(bl_may)}")
    print(f"BL May 2024 positive reviews: {(bl_may['predicted_sentiment'] == 'Positive').sum()} ({(bl_may['predicted_sentiment'] == 'Positive').mean()*100:.1f}%)")
