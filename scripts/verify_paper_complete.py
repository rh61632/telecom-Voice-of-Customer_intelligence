import pandas as pd
import numpy as np
from scipy import stats

print("==================================================")
print("COMPREHENSIVE VERIFICATION OF THE JBA MANUSCRIPT")
print("==================================================")

# 1. Load data
df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['review_date'] = pd.to_datetime(df['review_date'])
df['ym'] = df['review_date'].dt.to_period('M')

# Verify date range and days
min_date = df['review_date'].min()
max_date = df['review_date'].max()
days = (max_date - min_date).days + 1
print(f"Date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
print(f"Total days: {days} (Paper says: 3,716 days)")

# Modern era
modern = df[(df['review_date'] >= '2020-01-01') & (df['review_date'] <= '2026-09-30')].copy()
print(f"Modern era reviews: {len(modern):,} (Paper says: 634,992)")
early = df[df['review_date'] < '2020-01-01'].copy()
print(f"Early era reviews: {len(early):,} (Paper says: 20,678)")

# Smallest monthly count
monthly_counts = modern.groupby(['operator', 'ym']).size().unstack(level='operator')
print("\nSmallest monthly count per operator (2020-2026):")
for op in ['Banglalink', 'Robi', 'Grameenphone']:
    min_m = monthly_counts[op].idxmin()
    min_val = monthly_counts[op].min()
    print(f"  {op}: {min_val} in {min_m}")

# 2. Section 4.2 Chi-Square & Odds Ratios
cats = [
    'App Login & Technical Bugs',
    'Offers & Data Packs',
    'Network Speed & 4G Latency',
    'Billing & Airtime Deductions'
]
df_4 = df[df['predicted_category'].isin(cats)].copy()
print(f"\nTotal in 4 domains: {len(df_4):,} (Paper says: 88,184)")

# Within-domain negativity across 4 domains
cont_tab = pd.crosstab(df_4['predicted_category'], df_4['predicted_sentiment'] == 'Negative')
chi2, p, dof, _ = stats.chi2_contingency(cont_tab)
n_tot = len(df_4)
cramers_v = np.sqrt(chi2 / (n_tot * (min(cont_tab.shape) - 1)))
print(f"Chi2(3) = {chi2:.2f}, p = {p}, Cramers V = {cramers_v:.2f}")

neg_rates = df_4.groupby('predicted_category')['predicted_sentiment'].apply(lambda x: (x == 'Negative').mean() * 100)
print("\nPooled negativity rates:")
for c in ['Billing & Airtime Deductions', 'App Login & Technical Bugs', 'Network Speed & 4G Latency', 'Offers & Data Packs']:
    print(f"  {c}: {neg_rates.loc[c]:.1f}%")

# Odds ratios relative to Offers
def get_odds(cat_name):
    sub = df_4[df_4['predicted_category'] == cat_name]
    neg = (sub['predicted_sentiment'] == 'Negative').sum()
    non_neg = len(sub) - neg
    return neg, non_neg

o_neg, o_pos = get_odds('Offers & Data Packs')
odds_offers = o_neg / o_pos

for c in ['Billing & Airtime Deductions', 'App Login & Technical Bugs', 'Network Speed & 4G Latency']:
    c_neg, c_pos = get_odds(c)
    odds_c = c_neg / c_pos
    or_val = odds_c / odds_offers
    se_log_or = np.sqrt(1/c_neg + 1/c_pos + 1/o_neg + 1/o_pos)
    ci_low = np.exp(np.log(or_val) - 1.96 * se_log_or)
    ci_high = np.exp(np.log(or_val) + 1.96 * se_log_or)
    print(f"Odds Ratio {c} vs Offers: {or_val:.1f} (95% CI: [{ci_low:.1f}, {ci_high:.1f}])")

# App Login vs Network
l_neg, l_pos = get_odds('App Login & Technical Bugs')
n_neg, n_pos = get_odds('Network Speed & 4G Latency')
or_ln = (l_neg / l_pos) / (n_neg / n_pos)
se_ln = np.sqrt(1/l_neg + 1/l_pos + 1/n_neg + 1/n_pos)
ci_low_ln = np.exp(np.log(or_ln) - 1.96 * se_ln)
ci_high_ln = np.exp(np.log(or_ln) + 1.96 * se_ln)
print(f"Odds Ratio App Login vs Network: {or_ln:.1f} (95% CI: [{ci_low_ln:.1f}, {ci_high_ln:.1f}])")

# Section 5.2 Complaint rate comparisons:
print("\nSection 5.2 complaint rate comparisons:")
bl_tot = len(df[df['operator'] == 'Banglalink'])
bl_bug = len(df[(df['operator'] == 'Banglalink') & (df['predicted_category'] == 'App Login & Technical Bugs') & (df['predicted_sentiment'] == 'Negative')])
bl_bug_rate = bl_bug / bl_tot * 100.0

market_tot = len(df)
market_bug = len(df[(df['predicted_category'] == 'App Login & Technical Bugs') & (df['predicted_sentiment'] == 'Negative')])
market_bug_rate = market_bug / market_tot * 100.0

other_tot = len(df[df['operator'].isin(['Grameenphone', 'Robi'])])
other_bug = len(df[df['operator'].isin(['Grameenphone', 'Robi']) & (df['predicted_category'] == 'App Login & Technical Bugs') & (df['predicted_sentiment'] == 'Negative')])
other_bug_rate = other_bug / other_tot * 100.0

print(f"Banglalink app-bug rate: {bl_bug_rate:.2f}% (Paper: 7.25%)")
print(f"Market-wide app-bug rate: {market_bug_rate:.2f}% (Paper: 4.4%)")
print(f"Other two combined app-bug rate: {other_bug_rate:.2f}% (Paper: 3.7%)")
print(f"Ratio BL / Market: {bl_bug_rate / market_bug_rate:.2f} (Paper: ~1.6x)")
print(f"Ratio BL / Others: {bl_bug_rate / other_bug_rate:.2f} (Paper: ~twice)")


