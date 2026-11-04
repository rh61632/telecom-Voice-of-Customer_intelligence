import pandas as pd
import numpy as np

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
shocks = []

for op in operators:
    op_m = modern[modern['operator'] == op]
    monthly_totals = op_m.groupby('year_month').size()
    
    # Category net
    cat_sent = op_m.groupby(['year_month', 'predicted_category', 'predicted_sentiment']).size().unstack(fill_value=0)
    for col in ['Positive', 'Negative', 'Neutral']:
        if col not in cat_sent.columns: cat_sent[col] = 0
    
    net = (cat_sent['Positive'] - cat_sent['Negative']).unstack(level='predicted_category', fill_value=0)
    contrib = net.div(monthly_totals, axis=0) * 100.0
    
    # overall NSS
    nss = ((op_m.groupby('year_month')['predicted_sentiment'].apply(lambda x: (x=='Positive').sum() - (x=='Negative').sum())) / monthly_totals) * 100.0
    
    months = sorted(monthly_totals.index)
    for i in range(1, len(months)):
        m_prev = months[i-1]
        m_curr = months[i]
        d_nss = nss.loc[m_curr] - nss.loc[m_prev]
        if abs(d_nss) >= 10.0:
            diffs = contrib.loc[m_curr] - contrib.loc[m_prev]
            # Operational leading domain (among the 4 specific operational domains)
            op_diffs = diffs[cats] * np.sign(d_nss)
            lead_op_cat = op_diffs.idxmax()
            lead_op_val = diffs[lead_op_cat]
            lead_op_share = (lead_op_val / d_nss) * 100.0
            
            shocks.append({
                'operator': op,
                'transition': f"{m_prev} -> {m_curr}",
                'delta_nss': d_nss,
                'direction': 'Drop' if d_nss < 0 else 'Rise',
                'lead_op_cat': lead_op_cat,
                'lead_op_share': lead_op_share
            })

sdf = pd.DataFrame(shocks)
print(f"Total shocks evaluated: {len(sdf)}")
print("\nLeading Operational Domain across all 35 shocks:")
print(pd.crosstab(sdf['lead_op_cat'], sdf['direction'], margins=True))

print(f"\nMedian operational share: {sdf['lead_op_share'].median():.1f}%")
app_shocks = (sdf['lead_op_cat'] == 'App Login & Technical Bugs').sum()
print(f"App Login & Bugs leads in: {app_shocks} / {len(sdf)} ({app_shocks/len(sdf)*100:.1f}%)")

drop_sdf = sdf[sdf['direction'] == 'Drop']
app_drops = (drop_sdf['lead_op_cat'] == 'App Login & Technical Bugs').sum()
print(f"App Login & Bugs leads in Drops: {app_drops} / {len(drop_sdf)} ({app_drops/len(drop_sdf)*100:.1f}%)")

