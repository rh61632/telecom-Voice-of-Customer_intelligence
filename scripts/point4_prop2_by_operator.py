import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['review_date'] = pd.to_datetime(df['review_date'])
df['year_month'] = df['review_date'].dt.to_period('M')

modern = df[(df['review_date'] >= '2020-01-01') & (df['review_date'] <= '2026-09-30')].copy()

cats = [
    'App Login & Technical Bugs',
    'Offers & Data Packs',
    'Network Speed & 4G Latency',
    'Billing & Airtime Deductions'
]

operators = ['Grameenphone', 'Robi', 'Banglalink']
all_trans = []

for op in operators:
    op_m = modern[modern['operator'] == op]
    monthly_totals = op_m.groupby('year_month').size()
    
    cat_sent = op_m.groupby(['year_month', 'predicted_category', 'predicted_sentiment']).size().unstack(fill_value=0)
    for col in ['Positive', 'Negative', 'Neutral']:
        if col not in cat_sent.columns: cat_sent[col] = 0
    
    net = (cat_sent['Positive'] - cat_sent['Negative']).unstack(level='predicted_category', fill_value=0)
    contrib = net.div(monthly_totals, axis=0) * 100.0
    
    nss = ((op_m.groupby('year_month')['predicted_sentiment'].apply(lambda x: (x=='Positive').sum() - (x=='Negative').sum())) / monthly_totals) * 100.0
    
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
        
        all_trans.append({
            'operator': op,
            'transition': f'{m_prev} -> {m_curr}',
            'delta_nss': d_nss,
            'is_shock': is_shock,
            'is_surge': is_surge,
            'lead_op': lead_op,
            'is_login': (lead_op == 'App Login & Technical Bugs')
        })

tdf = pd.DataFrame(all_trans)

print("=== PROPOSITION 2: OPERATOR-BY-OPERATOR BREAKDOWN ===")
for op in operators:
    sub = tdf[tdf['operator'] == op]
    shk = sub[sub['is_shock']]
    non = sub[~sub['is_shock']]
    
    shk_login = shk['is_login'].sum()
    shk_other = len(shk) - shk_login
    non_login = non['is_login'].sum()
    non_other = len(non) - non_login
    
    tbl = [[shk_login, shk_other], [non_login, non_other]]
    f_res = stats.fisher_exact(tbl)
    print(f"\n{op}:")
    print(f"  Shocks: {shk_login}/{len(shk)} ({shk_login/len(shk)*100:.1f}% login)")
    print(f"  Non-shocks: {non_login}/{len(non)} ({non_login/len(non)*100:.1f}% login)")
    print(f"  Fisher exact test: OR = {f_res.statistic:.2f}, p = {f_res.pvalue:.4f}")

print("\n=== PROPOSITION 2: EXCLUDING VOLUME SURGES (NON-SURGE ONLY) ===")
nosurge = tdf[~tdf['is_surge']]
shk_ns = nosurge[nosurge['is_shock']]
non_ns = nosurge[~nosurge['is_shock']]

shk_ns_login = shk_ns['is_login'].sum()
shk_ns_other = len(shk_ns) - shk_ns_login
non_ns_login = non_ns['is_login'].sum()
non_ns_other = len(non_ns) - non_ns_login

tbl_ns = [[shk_ns_login, shk_ns_other], [non_ns_login, non_ns_other]]
f_res_ns = stats.fisher_exact(tbl_ns)
chi2_ns = stats.chi2_contingency(tbl_ns, correction=False)
print(f"Pooled Non-surge:")
print(f"  Shocks: {shk_ns_login}/{len(shk_ns)} ({shk_ns_login/len(shk_ns)*100:.1f}% login)")
print(f"  Non-shocks: {non_ns_login}/{len(non_ns)} ({non_ns_login/len(non_ns)*100:.1f}% login)")
print(f"  Chi2 = {chi2_ns.statistic:.2f}, p = {chi2_ns.pvalue:.4f}; Fisher exact OR = {f_res_ns.statistic:.2f}, p = {f_res_ns.pvalue:.4f}")

for op in operators:
    sub = nosurge[nosurge['operator'] == op]
    shk = sub[sub['is_shock']]
    non = sub[~sub['is_shock']]
    
    shk_login = shk['is_login'].sum()
    shk_other = len(shk) - shk_login
    non_login = non['is_login'].sum()
    non_other = len(non) - non_login
    
    tbl = [[shk_login, shk_other], [non_login, non_other]]
    f_res = stats.fisher_exact(tbl)
    print(f"\n{op} (Non-surge):")
    print(f"  Shocks: {shk_login}/{len(shk)} ({shk_login/len(shk)*100 if len(shk) else 0:.1f}% login)")
    print(f"  Non-shocks: {non_login}/{len(non)} ({non_login/len(non)*100:.1f}% login)")
    print(f"  Fisher exact test: OR = {f_res.statistic:.2f}, p = {f_res.pvalue:.4f}")

