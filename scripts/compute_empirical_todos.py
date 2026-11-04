import pandas as pd
import numpy as np

# Load classified dataset
df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['review_date'] = pd.to_datetime(df['review_date'])
df['year_month'] = df['review_date'].dt.to_period('M')

# Modern Era: 2020-01 to 2026-09
modern = df[(df['review_date'] >= '2020-01-01') & (df['review_date'] <= '2026-09-30')].copy()

# Function to compute monthly NSS
def get_monthly_nss(sub_df, sent_col='predicted_sentiment'):
    monthly = sub_df.groupby(['operator', 'year_month'])[sent_col].value_counts().unstack(fill_value=0)
    for col in ['Positive', 'Negative', 'Neutral']:
        if col not in monthly.columns:
            monthly[col] = 0
    monthly['total'] = monthly['Positive'] + monthly['Negative'] + monthly['Neutral']
    monthly['nss'] = ((monthly['Positive'] - monthly['Negative']) / monthly['total']) * 100.0
    return monthly.reset_index()

m_nss = get_monthly_nss(modern, 'predicted_sentiment')

# 1. RMSSD and Moving Block Bootstrap
operators = ['Grameenphone', 'Robi', 'Banglalink']
rmssd_results = {}

for op in operators:
    s = m_nss[m_nss['operator'] == op].sort_values('year_month')['nss'].values
    diffs = np.diff(s)
    rmssd = np.sqrt(np.mean(diffs**2))
    rmssd_results[op] = (rmssd, diffs, s)
    print(f"{op} RMSSD: {rmssd:.2f}")

# Moving block bootstrap for RMSSD and Ratio (block length = 4 months)
np.random.seed(42)
B = 2000
block_len = 4
n_months = 81
n_blocks = int(np.ceil(n_months / block_len))

boot_rmssd = {op: [] for op in operators}
boot_ratios = []

for _ in range(B):
    for op in operators:
        s = rmssd_results[op][2]
        starts = np.random.randint(0, n_months - block_len + 1, size=n_blocks)
        sampled = []
        for st in starts:
            sampled.extend(s[st:st+block_len])
        sampled = np.array(sampled[:n_months])
        diffs = np.diff(sampled)
        b_rmssd = np.sqrt(np.mean(diffs**2))
        boot_rmssd[op].append(b_rmssd)
    
    boot_ratios.append(boot_rmssd['Banglalink'][-1] / boot_rmssd['Robi'][-1])

print("\n--- 95% Bootstrap CIs for RMSSD ---")
for op in operators:
    ci_low = np.percentile(boot_rmssd[op], 2.5)
    ci_high = np.percentile(boot_rmssd[op], 97.5)
    print(f"{op}: {rmssd_results[op][0]:.2f} (95% CI: [{ci_low:.2f}, {ci_high:.2f}])")

ratio_low = np.percentile(boot_ratios, 2.5)
ratio_high = np.percentile(boot_ratios, 97.5)
orig_ratio = rmssd_results['Banglalink'][0] / rmssd_results['Robi'][0]
print(f"BL/Robi RMSSD Ratio: {orig_ratio:.2f} (95% CI: [{ratio_low:.2f}, {ratio_high:.2f}])")

# Sensitivity analysis with LinearSVC
svm_nss = get_monthly_nss(modern, 'sentiment_linearsvc')
print("\n--- Sensitivity: LinearSVC RMSSD ---")
for op in operators:
    s_svm = svm_nss[svm_nss['operator'] == op].sort_values('year_month')['nss'].values
    d_svm = np.diff(s_svm)
    rmssd_svm = np.sqrt(np.mean(d_svm**2))
    print(f"{op} SVM RMSSD: {rmssd_svm:.2f} (Ensemble: {rmssd_results[op][0]:.2f})")

# 2. All 37 Shocks Analysis
all_transitions = []
for op in operators:
    op_m = modern[modern['operator'] == op]
    # monthly counts per category and sentiment
    cat_sent = op_m.groupby(['year_month', 'predicted_category', 'predicted_sentiment']).size().unstack(fill_value=0)
    for col in ['Positive', 'Negative', 'Neutral']:
        if col not in cat_sent.columns:
            cat_sent[col] = 0
    cat_sent['total_cat'] = cat_sent.sum(axis=1)
    
    # monthly total reviews
    monthly_totals = op_m.groupby('year_month').size()
    
    # contribution c_{k,t} = (Pos_{k,t} - Neg_{k,t}) / Total_t
    cat_net = (cat_sent['Positive'] - cat_sent['Negative']).unstack(level='predicted_category', fill_value=0)
    cat_contrib = cat_net.div(monthly_totals, axis=0) * 100.0
    
    months = sorted(monthly_totals.index)
    for i in range(1, len(months)):
        m_prev = months[i-1]
        m_curr = months[i]
        
        nss_prev = cat_contrib.loc[m_prev].sum()
        nss_curr = cat_contrib.loc[m_curr].sum()
        delta_nss = nss_curr - nss_prev
        
        contrib_diff = cat_contrib.loc[m_curr] - cat_contrib.loc[m_prev]
        
        if abs(delta_nss) >= 10.0:
            aligned_contrib = contrib_diff * np.sign(delta_nss)
            leading_cat = aligned_contrib.idxmax()
            leading_val = contrib_diff[leading_cat]
            leading_share = (leading_val / delta_nss) * 100.0
            
            all_transitions.append({
                'operator': op,
                'period': f"{m_prev} to {m_curr}",
                'delta_nss': delta_nss,
                'direction': 'Rise' if delta_nss > 0 else 'Drop',
                'leading_cat': leading_cat,
                'leading_share': leading_share
            })

shocks_df = pd.DataFrame(all_transitions)
print(f"\nTotal Modern Shocks (|Delta NSS| >= 10): {len(shocks_df)}")
print(shocks_df['direction'].value_counts())
print("\nLeading Category Tally for All 37 Shocks:")
print(pd.crosstab(shocks_df['leading_cat'], shocks_df['direction'], margins=True))

print(f"\nMedian Leading Domain Share: {shocks_df['leading_share'].median():.1f}%")
print(f"Leading Share IQR: [{shocks_df['leading_share'].quantile(0.25):.1f}%, {shocks_df['leading_share'].quantile(0.75):.1f}%]")

# 3. Banglalink Spring 2024 App Version Breakdown
bl_spring = df[(df['operator'] == 'Banglalink') & 
               (df['review_date'] >= '2024-03-01') & 
               (df['review_date'] <= '2024-05-31')].copy()
bl_spring['month'] = bl_spring['review_date'].dt.strftime('%Y-%m')

print("\n--- Banglalink Spring 2024 by Month and Top Versions ---")
for m in ['2024-03', '2024-04', '2024-05']:
    sub = bl_spring[bl_spring['month'] == m]
    n_tot = len(sub)
    pos = (sub['predicted_sentiment'] == 'Positive').sum()
    neg = (sub['predicted_sentiment'] == 'Negative').sum()
    nss = ((pos - neg) / n_tot) * 100.0
    print(f"\nMonth {m}: Total N = {n_tot}, NSS = {nss:.2f}")
    
    # App version distribution
    v_counts = sub['app_version'].value_counts(dropna=False).head(5)
    for v, c in v_counts.items():
        v_sub = sub[sub['app_version'] == v]
        v_pos = (v_sub['predicted_sentiment'] == 'Positive').sum()
        v_neg = (v_sub['predicted_sentiment'] == 'Negative').sum()
        v_nss = ((v_pos - v_neg) / len(v_sub)) * 100.0
        print(f"   Version {v}: N={c} ({c/n_tot*100:.1f}%), NSS={v_nss:.2f}")
