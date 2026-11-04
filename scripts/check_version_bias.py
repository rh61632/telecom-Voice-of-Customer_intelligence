import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['has_version'] = df['app_version'].notna()

print("=== VERSIONED VS UNVERSIONED REVIEW COMPARISON ===")
print(f"Total reviews: {len(df):,}")
print(f"Versioned: {df['has_version'].sum():,} ({df['has_version'].mean()*100:.1f}%)")
print(f"Unversioned: {(~df['has_version']).sum():,} ({(~df['has_version']).mean()*100:.1f}%)")

# Compare Rating
mean_r_v = df[df['has_version']]['rating'].mean()
mean_r_u = df[~df['has_version']]['rating'].mean()
print(f"\nMean Star Rating: Versioned = {mean_r_v:.2f}, Unversioned = {mean_r_u:.2f}")

# Compare NSS
def get_nss(sub):
    p = (sub['predicted_sentiment'] == 'Positive').sum()
    n = (sub['predicted_sentiment'] == 'Negative').sum()
    return (p - n) / len(sub) * 100.0

nss_v = get_nss(df[df['has_version']])
nss_u = get_nss(df[~df['has_version']])
print(f"Overall NSS: Versioned = {nss_v:+.2f}%, Unversioned = {nss_u:+.2f}% (difference = {nss_v - nss_u:+.2f} pp)")

# Compare Category Distribution
print("\nCategory Distribution:")
cats = df['predicted_category'].value_counts(normalize=True).index
cat_v = df[df['has_version']]['predicted_category'].value_counts(normalize=True) * 100
cat_u = df[~df['has_version']]['predicted_category'].value_counts(normalize=True) * 100
for c in cats:
    print(f"  {c[:30]:30}: Versioned = {cat_v.get(c, 0):4.1f}%, Unversioned = {cat_u.get(c, 0):4.1f}%")

# Compare Banglalink Spring 2024 specifically
bl_spring = df[(df['operator'] == 'Banglalink') & df['review_date'].str.contains('^2024-0[345]')].copy()
bl_v = bl_spring[bl_spring['has_version']]
bl_u = bl_spring[~bl_spring['has_version']]
print(f"\nBanglalink Spring 2024: Versioned N={len(bl_v)} (NSS={get_nss(bl_v):+.1f}%), Unversioned N={len(bl_u)} (NSS={get_nss(bl_u):+.1f}%)")

