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
        pct_vol = (monthly_totals.loc[m_curr] - monthly_totals.loc[m_prev]) / monthly_totals.loc[m_prev]
        
        diffs = contrib.loc[m_curr] - contrib.loc[m_prev]
        op_diffs = diffs[cats] * np.sign(d_nss)
        lead_op = op_diffs.idxmax()
        
        is_shock = abs(d_nss) >= 10.0
        is_surge = abs(pct_vol) >= 0.50
        
        transitions.append({
            'operator': op,
            'period': f'{m_prev} to {m_curr}',
            'delta_nss': d_nss,
            'pct_vol': pct_vol,
            'is_shock': is_shock,
            'is_surge': is_surge,
            'lead_op': lead_op,
            'lead_op_is_login': (lead_op == 'App Login & Technical Bugs')
        })

tdf = pd.DataFrame(transitions)
print('Total transitions:', len(tdf))
print('Surges:', tdf['is_surge'].sum(), 'Non-surges:', (~tdf['is_surge']).sum())
print(f"Shocks in surges: {tdf[tdf['is_surge']]['is_shock'].sum()} of {tdf['is_shock'].sum()} ({tdf[tdf['is_surge']]['is_shock'].sum()/tdf['is_shock'].sum()*100:.1f}%)")
print(f"Surges as % of all transitions: {tdf['is_surge'].sum()}/{len(tdf)} ({tdf['is_surge'].sum()/len(tdf)*100:.1f}%)")

ns = tdf[~tdf['is_surge']]
shocks_ns = ns[ns['is_shock']]
non_shocks_ns = ns[~ns['is_shock']]

print('\nNon-surge shocks login leads:', shocks_ns['lead_op_is_login'].sum(), 'of', len(shocks_ns))
print('\nNon-surge non-shocks by operator:')
for op in operators:
    sub = non_shocks_ns[non_shocks_ns['operator'] == op]
    print(f"  {op}: {sub['lead_op_is_login'].sum()} of {len(sub)} ({sub['lead_op_is_login'].sum()/len(sub)*100:.1f}%)")
print('Total non-surge non-shocks login leads:', non_shocks_ns['lead_op_is_login'].sum(), 'of', len(non_shocks_ns))

# 2x2 table for non-surge:
tbl_ns = np.array([
    [shocks_ns['lead_op_is_login'].sum(), len(shocks_ns) - shocks_ns['lead_op_is_login'].sum()],
    [non_shocks_ns['lead_op_is_login'].sum(), len(non_shocks_ns) - non_shocks_ns['lead_op_is_login'].sum()]
])
print('\nNon-surge 2x2 table:\n', tbl_ns)
chi2_ns, p_chi2_ns, _, _ = stats.chi2_contingency(tbl_ns, correction=False)
res_fisher_ns = stats.fisher_exact(tbl_ns)
print(f'Non-surge Chi2: {chi2_ns:.2f}, p = {p_chi2_ns:.4f}')
print(f'Non-surge Fisher: OR = {res_fisher_ns.statistic:.2f}, p = {res_fisher_ns.pvalue:.4f}')

