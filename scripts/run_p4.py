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
gen_cat = 'General Appreciation / Other'

operators = ['Grameenphone', 'Robi', 'Banglalink']
shocks = []

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
        d_ln_vol = np.log(monthly_totals.loc[m_curr]) - np.log(monthly_totals.loc[m_prev])
        pct_vol = (monthly_totals.loc[m_curr] - monthly_totals.loc[m_prev]) / monthly_totals.loc[m_prev]
        
        if abs(d_nss) >= 10.0:
            diffs = contrib.loc[m_curr] - contrib.loc[m_prev]
            gen_diff = diffs[gen_cat]
            four_domain_diff = diffs[cats].sum()
            
            gen_share = (gen_diff / d_nss) * 100.0
            four_domain_share = (four_domain_diff / d_nss) * 100.0
            
            all_diffs = diffs * np.sign(d_nss)
            lead_all = all_diffs.idxmax()
            
            op_diffs = diffs[cats] * np.sign(d_nss)
            lead_op = op_diffs.idxmax()
            lead_op_val = diffs[lead_op]
            lead_op_share = (lead_op_val / d_nss) * 100.0
            
            shocks.append({
                'operator': op,
                'period': f'{m_prev} to {m_curr}',
                'delta_nss': d_nss,
                'd_ln_vol': d_ln_vol,
                'pct_vol': pct_vol,
                'is_surge': abs(pct_vol) >= 0.50,
                'gen_diff': gen_diff,
                'gen_share': gen_share,
                'four_domain_diff': four_domain_diff,
                'four_domain_share': four_domain_share,
                'lead_all': lead_all,
                'lead_op': lead_op,
                'lead_op_share': lead_op_share
            })

sdf = pd.DataFrame(shocks)
print(f'Total shocks: {len(sdf)}')
med_gen = sdf['gen_share'].median()
print(f'Median Gen/Other share across 35 shocks: {med_gen:.1f}%')
mean_gen = sdf['gen_share'].mean()
print(f'Mean Gen/Other share across 35 shocks: {mean_gen:.1f}%')
med_4dom = sdf['four_domain_share'].median()
print(f'Median 4-Domain share across 35 shocks: {med_4dom:.1f}%')
lead_gen_count = (sdf['lead_all'] == gen_cat).sum()
print(f'How many shocks does Gen/Other lead (across all 5): {lead_gen_count} of {len(sdf)}')

# Regression of gen_diff on d_ln_vol
slope, intercept, r_val, p_val, std_err = stats.linregress(sdf['d_ln_vol'], sdf['gen_diff'])
print(f'Regression of Gen/Other contribution on d_ln_vol: R^2 = {r_val**2:.4f}, slope = {slope:.2f}, p = {p_val:.4e}')

# Correlation of d_nss with d_ln_vol across shocks
corr, p_corr = stats.pearsonr(sdf['d_ln_vol'], sdf['delta_nss'])
print(f'Correlation of Delta NSS with d_ln_vol across shocks: r = {corr:.4f}, p = {p_corr:.4e}')

# Fisher exact test / Chi-square for Proposition 2
# H2: App Login is primary operational driver in >= 50% of shocks
# Tally of operational drivers by operator:
print('\nTally of operational drivers by operator:')
print(pd.crosstab(sdf['operator'], sdf['lead_op'], margins=True))

print('\nTally of operational drivers excluding volume surges (pct_vol < 50%):')
nosurge_sdf = sdf[~sdf['is_surge']]
print(f'Non-surge shocks count: {len(nosurge_sdf)}')
print(pd.crosstab(nosurge_sdf['operator'], nosurge_sdf['lead_op'], margins=True))

# Chi-square / Fisher exact tests
# Testing whether App Login is significantly more frequent than expected by chance (1/4 = 25% or equal across 4 domains)
# Or comparing operators:
for op in operators:
    op_s = sdf[sdf['operator'] == op]
    app_c = (op_s['lead_op'] == 'App Login & Technical Bugs').sum()
    tot_c = len(op_s)
    print(f'{op}: App Login leads in {app_c}/{tot_c} ({app_c/tot_c*100:.1f}%)')
    # Binomial test against 0.25 (null that each of 4 domains is equally likely)
    binom_res = stats.binomtest(app_c, tot_c, p=0.25, alternative='greater')
    print(f'   Binomial test vs 0.25: p = {binom_res.pvalue:.4f}')

# Overall Chi-square test goodness of fit against uniform across 4 domains
obs = sdf['lead_op'].value_counts().reindex(cats, fill_value=0).values
exp = [len(sdf)/4.0] * 4
chisq_res = stats.chisquare(obs, f_exp=exp)
print(f'\nGoodness of fit Chi-square across 4 domains (all 35 shocks): Chi2 = {chisq_res.statistic:.2f}, p = {chisq_res.pvalue:.4e}')

# Non-surge Chi-square
obs_ns = nosurge_sdf['lead_op'].value_counts().reindex(cats, fill_value=0).values
exp_ns = [len(nosurge_sdf)/4.0] * 4
chisq_ns = stats.chisquare(obs_ns, f_exp=exp_ns)
print(f'Goodness of fit Chi-square across 4 domains (non-surge {len(nosurge_sdf)} shocks): Chi2 = {chisq_ns.statistic:.2f}, p = {chisq_ns.pvalue:.4e}')

