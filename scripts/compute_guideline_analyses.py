import pandas as pd
import numpy as np
from scipy import stats

print("Loading dataset...")
df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['review_date'] = pd.to_datetime(df['review_date'])
df['ym'] = df['review_date'].dt.strftime('%Y-%m')

# C1: September 2026 NSS by operator with N, bootstrap interval, rolling 3-month NSS (Jul-Sep 2026)
print("\n=== C1: September 2026 & Q3 2026 (Jul-Sep) NSS ===")
for op in ['Grameenphone', 'Robi', 'Banglalink']:
    # September 2026
    sub_sep = df[(df['operator'] == op) & (df['ym'] == '2026-09')]
    n_sep = len(sub_sep)
    pos_sep = (sub_sep['predicted_sentiment'] == 'Positive').sum()
    neg_sep = (sub_sep['predicted_sentiment'] == 'Negative').sum()
    nss_sep = (pos_sep - neg_sep) / n_sep * 100.0 if n_sep > 0 else 0
    
    # Bootstrap CI for Sep 2026
    np.random.seed(42)
    boot_nss = []
    vals = (sub_sep['predicted_sentiment'] == 'Positive').astype(int) - (sub_sep['predicted_sentiment'] == 'Negative').astype(int)
    val_arr = vals.values
    if len(val_arr) > 0:
        for _ in range(2000):
            sample = np.random.choice(val_arr, size=len(val_arr), replace=True)
            boot_nss.append(sample.mean() * 100.0)
        ci_low, ci_high = np.percentile(boot_nss, [2.5, 97.5])
    else:
        ci_low, ci_high = 0, 0

    # Rolling 3-month (Jul-Sep 2026)
    sub_q3 = df[(df['operator'] == op) & (df['ym'].isin(['2026-07', '2026-08', '2026-09']))]
    n_q3 = len(sub_q3)
    pos_q3 = (sub_q3['predicted_sentiment'] == 'Positive').sum()
    neg_q3 = (sub_q3['predicted_sentiment'] == 'Negative').sum()
    nss_q3 = (pos_q3 - neg_q3) / n_q3 * 100.0 if n_q3 > 0 else 0

    print(f"{op} Sep 2026: N={n_sep}, NSS={nss_sep:.2f} (95% CI: [{ci_low:.2f}, {ci_high:.2f}]), Q3 2026 (Jul-Sep): N={n_q3}, NSS={nss_q3:.2f}")

# C2: Surge test for Banglalink 2026 and Robi 2025
print("\n=== C2: Surge tests for BL 2025->2026 and Robi 2024->2025 ===")
for op, y1, y2 in [('Banglalink', 2025, 2026), ('Robi', 2024, 2025)]:
    df_y1 = df[(df['operator'] == op) & (df['review_date'].dt.year == y1)]
    df_y2 = df[(df['operator'] == op) & (df['review_date'].dt.year == y2)]
    
    n1, n2 = len(df_y1), len(df_y2)
    nss1 = ((df_y1['predicted_sentiment'] == 'Positive').sum() - (df_y1['predicted_sentiment'] == 'Negative').sum()) / n1 * 100.0
    nss2 = ((df_y2['predicted_sentiment'] == 'Positive').sum() - (df_y2['predicted_sentiment'] == 'Negative').sum()) / n2 * 100.0
    vol_ratio = n2 / n1
    
    gen_share1 = (df_y1['predicted_category'] == 'General Appreciation / Other').mean() * 100.0
    gen_share2 = (df_y2['predicted_category'] == 'General Appreciation / Other').mean() * 100.0
    
    # Additive decomposition
    cats = ['General Appreciation / Other', 'App Login & Technical Bugs', 'Offers & Data Packs', 'Network Speed & 4G Latency', 'Billing & Airtime Deductions']
    print(f"\n{op} {y1} -> {y2}: Vol {n1} -> {n2} ({vol_ratio:.2f}x), NSS {nss1:.2f} -> {nss2:.2f} (Delta: {nss2 - nss1:+.2f})")
    print(f"General share: {gen_share1:.2f}% -> {gen_share2:.2f}%")
    print("Additive decomposition of Delta NSS:")
    tot_check = 0
    for c in cats:
        pos1 = ((df_y1['predicted_category'] == c) & (df_y1['predicted_sentiment'] == 'Positive')).sum()
        neg1 = ((df_y1['predicted_category'] == c) & (df_y1['predicted_sentiment'] == 'Negative')).sum()
        c1 = (pos1 - neg1) / n1 * 100.0
        
        pos2 = ((df_y2['predicted_category'] == c) & (df_y2['predicted_sentiment'] == 'Positive')).sum()
        neg2 = ((df_y2['predicted_category'] == c) & (df_y2['predicted_sentiment'] == 'Negative')).sum()
        c2 = (pos2 - neg2) / n2 * 100.0
        
        diff_c = c2 - c1
        tot_check += diff_c
        print(f"  {c:30s}: {c1:+.2f} -> {c2:+.2f} (Delta: {diff_c:+.2f})")
    print(f"Total delta check: {tot_check:+.2f}")

# C3: Bootstrap CIs for decade NSS & GP-Robi gap test
print("\n=== C3: Decade NSS Bootstrap CIs & GP vs Robi gap ===")
nss_vals = {}
for op in ['Grameenphone', 'Robi', 'Banglalink']:
    sub = df[df['operator'] == op]
    n = len(sub)
    vals = (sub['predicted_sentiment'] == 'Positive').astype(int) - (sub['predicted_sentiment'] == 'Negative').astype(int)
    nss = vals.mean() * 100.0
    # Bootstrap
    np.random.seed(42)
    boot = np.random.choice(vals.values, size=(1000, 2000)).mean(axis=1) * 100.0
    # True SE of mean
    se = vals.std(ddof=1) / np.sqrt(n) * 100.0
    ci_low = nss - 1.96 * se
    ci_high = nss + 1.96 * se
    nss_vals[op] = (nss, se, n)
    print(f"{op}: N={n}, NSS={nss:.2f} (SE={se:.3f}, 95% CI: [{ci_low:.2f}, {ci_high:.2f}])")

# Two sample test GP vs Robi
nss_gp, se_gp, n_gp = nss_vals['Grameenphone']
nss_robi, se_robi, n_robi = nss_vals['Robi']
diff_gp_robi = nss_robi - nss_gp
se_diff = np.sqrt(se_gp**2 + se_robi**2)
z_stat = diff_gp_robi / se_diff
p_val = 2 * (1 - stats.norm.cdf(abs(z_stat)))
print(f"Robi - GP gap: {diff_gp_robi:+.2f} points (SE={se_diff:.3f}, 95% CI: [{diff_gp_robi - 1.96*se_diff:.2f}, {diff_gp_robi + 1.96*se_diff:.2f}], z={z_stat:.2f}, p={p_val:.4e})")

# C5: Event study around Feb 2018 (4G launch), Mar 2020 (COVID), Sep 2025 (5G launch)
print("\n=== C5: Event studies (6-month pre/post) ===")
events = [
    ("4G Launch (Feb 2018)", '2017-08', '2018-01', '2018-03', '2018-08'),
    ("COVID Onset (Mar 2020)", '2019-09', '2020-02', '2020-04', '2020-09'),
    ("5G Launch (Sep 2025)", '2025-03', '2025-08', '2025-10', '2026-03'),
]
for name, pre_start, pre_end, post_start, post_end in events:
    print(f"\n--- {name} ---")
    for op in ['Grameenphone', 'Robi', 'Banglalink']:
        pre = df[(df['operator'] == op) & (df['ym'].between(pre_start, pre_end))]
        post = df[(df['operator'] == op) & (df['ym'].between(post_start, post_end))]
        
        nss_pre = ((pre['predicted_sentiment'] == 'Positive').sum() - (pre['predicted_sentiment'] == 'Negative').sum()) / len(pre) * 100.0 if len(pre)>0 else 0
        nss_post = ((post['predicted_sentiment'] == 'Positive').sum() - (post['predicted_sentiment'] == 'Negative').sum()) / len(post) * 100.0 if len(post)>0 else 0
        
        print(f"  {op:13s}: Pre ({pre_start}..{pre_end}, N={len(pre)}) NSS={nss_pre:.2f} -> Post ({post_start}..{post_end}, N={len(post)}) NSS={nss_post:.2f} (Delta: {nss_post - nss_pre:+.2f})")

# C6: Recovery time & shock asymmetry
print("\n=== C6: Shock Recovery Time & Direction Asymmetry ===")
# Let's run on modern era (2020-2026)
modern = df[df['ym'].between('2020-01', '2026-09')].copy()
# Monthly NSS table
monthly = modern.groupby(['operator', 'ym'])['predicted_sentiment'].apply(lambda x: ((x=='Positive').sum() - (x=='Negative').sum()) / len(x) * 100.0).unstack(level='operator')

shocks_all = []
for op in ['Grameenphone', 'Robi', 'Banglalink']:
    s = monthly[op]
    months = s.index.tolist()
    for i in range(1, len(months)):
        prev_m = months[i-1]
        curr_m = months[i]
        d = s.loc[curr_m] - s.loc[prev_m]
        if abs(d) >= 10.0:
            target = s.loc[prev_m]
            # recovery: months after curr_m to cross target again
            rec_months = None
            for j in range(i+1, len(months)):
                future_m = months[j]
                if d < 0 and s.loc[future_m] >= target:
                    rec_months = j - i
                    break
                elif d > 0 and s.loc[future_m] <= target:
                    rec_months = j - i
                    break
            shocks_all.append({
                'operator': op,
                'period': f"{prev_m} -> {curr_m}",
                'delta': d,
                'type': 'Positive' if d > 0 else 'Negative',
                'recovery_months': rec_months
            })

sdf = pd.DataFrame(shocks_all)
print(f"Total shocks: {len(sdf)} (Positive: {(sdf['type']=='Positive').sum()}, Negative: {(sdf['type']=='Negative').sum()})")
print(f"GP: {(sdf['operator']=='Grameenphone').sum()} (Pos: {((sdf['operator']=='Grameenphone') & (sdf['type']=='Positive')).sum()}, Neg: {((sdf['operator']=='Grameenphone') & (sdf['type']=='Negative')).sum()})")
print(f"Robi: {(sdf['operator']=='Robi').sum()} (Pos: {((sdf['operator']=='Robi') & (sdf['type']=='Positive')).sum()}, Neg: {((sdf['operator']=='Robi') & (sdf['type']=='Negative')).sum()})")
print(f"BL: {(sdf['operator']=='Banglalink').sum()} (Pos: {((sdf['operator']=='Banglalink') & (sdf['type']=='Positive')).sum()}, Neg: {((sdf['operator']=='Banglalink') & (sdf['type']=='Negative')).sum()})")
resolved = sdf[sdf['recovery_months'].notnull()]
print(f"Median recovery time for resolved shocks: {resolved['recovery_months'].median():.1f} months (IQR: [{resolved['recovery_months'].quantile(0.25):.1f}, {resolved['recovery_months'].quantile(0.75):.1f}])")
print(f"Percent resolved within 1 month: {(resolved['recovery_months'] == 1).mean() * 100:.1f}%")
print(f"Percent resolved within 3 months: {(resolved['recovery_months'] <= 3).mean() * 100:.1f}%")

# C7: Exact share of negatives mapped to the four domains & BL vs Robi gap decomposition
print("\n=== C7: Negative share mapped to 4 domains ===")
actionable = ['App Login & Technical Bugs', 'Offers & Data Packs', 'Network Speed & 4G Latency', 'Billing & Airtime Deductions']
for op in ['Grameenphone', 'Robi', 'Banglalink']:
    neg_op = df[(df['operator'] == op) & (df['predicted_sentiment'] == 'Negative')]
    tot_neg = len(neg_op)
    act_neg = neg_op['predicted_category'].isin(actionable).sum()
    pct = act_neg / tot_neg * 100.0
    print(f"{op}: {act_neg} / {tot_neg} negatives in 4 actionable domains ({pct:.2f}%)")

print("\n--- Additive decomposition of Decade BL vs Robi NSS gap (+53.07 vs +65.92: Delta = -12.85) ---")
bl_df = df[df['operator'] == 'Banglalink']
robi_df = df[df['operator'] == 'Robi']
n_bl, n_robi = len(bl_df), len(robi_df)
for c in ['General Appreciation / Other'] + actionable:
    pos_bl = ((bl_df['predicted_category'] == c) & (bl_df['predicted_sentiment'] == 'Positive')).sum()
    neg_bl = ((bl_df['predicted_category'] == c) & (bl_df['predicted_sentiment'] == 'Negative')).sum()
    c_bl = (pos_bl - neg_bl) / n_bl * 100.0

    pos_robi = ((robi_df['predicted_category'] == c) & (robi_df['predicted_sentiment'] == 'Positive')).sum()
    neg_robi = ((robi_df['predicted_category'] == c) & (robi_df['predicted_sentiment'] == 'Negative')).sum()
    c_robi = (pos_robi - neg_robi) / n_robi * 100.0
    
    diff_c = c_bl - c_robi
    print(f"  {c:30s}: BL={c_bl:+.2f}, Robi={c_robi:+.2f}, Delta Contribution = {diff_c:+.2f}")
