import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['ym'] = df['review_date'].str[:7]
modern = df[df['ym'].between('2020-01', '2026-09')].copy()

cats = [
    'App Login & Technical Bugs',
    'Offers & Data Packs',
    'Network Speed & 4G Latency',
    'Billing & Airtime Deductions'
]
gen_cat = 'General Appreciation / Other'

operators = ['Grameenphone', 'Robi', 'Banglalink']
transitions = []

for op in operators:
    op_m = modern[modern['operator'] == op]
    monthly_totals = op_m.groupby('ym').size()
    
    cat_sent = op_m.groupby(['ym', 'predicted_category', 'predicted_sentiment']).size().unstack(fill_value=0)
    for col in ['Positive', 'Negative', 'Neutral']:
        if col not in cat_sent.columns: cat_sent[col] = 0
    
    net = (cat_sent['Positive'] - cat_sent['Negative']).unstack(level='predicted_category', fill_value=0)
    contrib = net.div(monthly_totals, axis=0) * 100.0
    
    nss = ((op_m.groupby('ym')['predicted_sentiment'].apply(lambda x: (x=='Positive').sum() - (x=='Negative').sum())) / monthly_totals) * 100.0
    
    months = sorted(monthly_totals.index)
    for i in range(1, len(months)):
        m_prev = months[i-1]
        m_curr = months[i]
        d_nss = nss.loc[m_curr] - nss.loc[m_prev]
        d_ln_vol = np.log(monthly_totals.loc[m_curr]) - np.log(monthly_totals.loc[m_prev])
        pct_vol = (monthly_totals.loc[m_curr] - monthly_totals.loc[m_prev]) / monthly_totals.loc[m_prev]
        
        diffs = contrib.loc[m_curr] - contrib.loc[m_prev]
        gen_diff = diffs[gen_cat]
        four_diff = diffs[cats].sum()
        
        # Absolute volume change
        added_vol = monthly_totals.loc[m_curr] - monthly_totals.loc[m_prev]
        
        is_shock = abs(d_nss) >= 10.0
        is_surge = abs(pct_vol) >= 0.50
        
        transitions.append({
            'operator': op,
            'period': f'{m_prev} to {m_curr}',
            'delta_nss': d_nss,
            'd_ln_vol': d_ln_vol,
            'pct_vol': pct_vol,
            'added_vol': added_vol,
            'is_shock': is_shock,
            'is_surge': is_surge,
            'gen_diff': gen_diff,
            'four_diff': four_diff
        })

tdf = pd.DataFrame(transitions)

print("=== 1. REGRESSION OF CONTRIBUTIONS ON D_LN_VOL ===")
# A. Across all 35 shocks:
shocks_tdf = tdf[tdf['is_shock']].copy()
r_gen_shocks = stats.linregress(shocks_tdf['d_ln_vol'], shocks_tdf['gen_diff'])
r_four_shocks = stats.linregress(shocks_tdf['d_ln_vol'], shocks_tdf['four_diff'])
r_tot_shocks = stats.linregress(shocks_tdf['d_ln_vol'], shocks_tdf['delta_nss'])
print("Across 35 shocks:")
print(f"  General / Other diff vs d_ln_vol: R2 = {r_gen_shocks.rvalue**2:.4f}, slope = {r_gen_shocks.slope:.2f}, p = {r_gen_shocks.pvalue:.4e}")
print(f"  4-Domain Total diff vs d_ln_vol:  R2 = {r_four_shocks.rvalue**2:.4f}, slope = {r_four_shocks.slope:.2f}, p = {r_four_shocks.pvalue:.4e}")
print(f"  Delta NSS vs d_ln_vol:            R2 = {r_tot_shocks.rvalue**2:.4f}, slope = {r_tot_shocks.slope:.2f}, p = {r_tot_shocks.pvalue:.4e}")

# B. Across all 240 transitions:
r_gen_all = stats.linregress(tdf['d_ln_vol'], tdf['gen_diff'])
r_four_all = stats.linregress(tdf['d_ln_vol'], tdf['four_diff'])
r_tot_all = stats.linregress(tdf['d_ln_vol'], tdf['delta_nss'])
print("\nAcross all 240 transitions:")
print(f"  General / Other diff vs d_ln_vol: R2 = {r_gen_all.rvalue**2:.4f}, slope = {r_gen_all.slope:.2f}, p = {r_gen_all.pvalue:.4e}")
print(f"  4-Domain Total diff vs d_ln_vol:  R2 = {r_four_all.rvalue**2:.4f}, slope = {r_four_all.slope:.2f}, p = {r_four_all.pvalue:.4e}")
print(f"  Delta NSS vs d_ln_vol:            R2 = {r_tot_all.rvalue**2:.4f}, slope = {r_tot_all.slope:.2f}, p = {r_tot_all.pvalue:.4e}")

# 2. Decompose Volume Surges: positive surges vs negative surges
print("\n=== 2. DECOMPOSITION OF VOLUME SURGES (|pct_vol| >= 50%) ===")
surges = tdf[tdf['is_surge']].copy()
print(f"Total surges: {len(surges)} ({len(surges)/240*100:.1f}% of all transitions)")
pos_surges = surges[surges['pct_vol'] > 0]
neg_surges = surges[surges['pct_vol'] < 0]
print(f"  Positive surges (expansion): {len(pos_surges)}")
print(f"  Negative surges (contraction): {len(neg_surges)}")

print(f"Mean Gen/Other impact during positive surges: {pos_surges['gen_diff'].mean():+.2f}")
print(f"Mean 4-Domain impact during positive surges:  {pos_surges['four_diff'].mean():+.2f}")
print(f"Mean Delta NSS during positive surges:        {pos_surges['delta_nss'].mean():+.2f}")

