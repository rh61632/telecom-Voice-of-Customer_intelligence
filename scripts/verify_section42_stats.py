import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
cats = ['Billing & Airtime Deductions', 'App Login & Technical Bugs', 'Network Speed & 4G Latency', 'Offers & Data Packs']
sub = df[df['predicted_category'].isin(cats)].copy()
sub['is_neg'] = (sub['predicted_sentiment'] == 'Negative')

print('Total 4 domains:', len(sub))
for c in cats:
    sc = sub[sub['predicted_category'] == c]
    neg_count = sc['is_neg'].sum()
    print(f"{c}: Neg={neg_count}/{len(sc)} ({sc['is_neg'].mean()*100:.1f}%)")

ct = pd.crosstab(sub['predicted_category'], sub['is_neg'])
chi2, p, dof, ex = chi2_contingency(ct)
n = len(sub)
v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
print(f"Chi2 = {chi2:.1f}, dof = {dof}, p = {p}, Cramer V = {v:.4f}")

# Odds ratios relative to Offers
p_off = sub[sub['predicted_category'] == 'Offers & Data Packs']['is_neg'].mean()
odds_off = p_off / (1 - p_off)
for c in ['Billing & Airtime Deductions', 'App Login & Technical Bugs', 'Network Speed & 4G Latency']:
    p_c = sub[sub['predicted_category'] == c]['is_neg'].mean()
    odds_c = p_c / (1 - p_c)
    or_val = odds_c / odds_off
    a = (sub[sub['predicted_category'] == c]['is_neg']).sum()
    b = len(sub[sub['predicted_category'] == c]) - a
    c_off = (sub[sub['predicted_category'] == 'Offers & Data Packs']['is_neg']).sum()
    d_off = len(sub[sub['predicted_category'] == 'Offers & Data Packs']) - c_off
    se_lor = np.sqrt(1/a + 1/b + 1/c_off + 1/d_off)
    ci_low = np.exp(np.log(or_val) - 1.96 * se_lor)
    ci_high = np.exp(np.log(or_val) + 1.96 * se_lor)
    print(f"OR {c} vs Offers: {or_val:.2f} [{ci_low:.2f}, {ci_high:.2f}]")

# App Login vs Network
p_app = sub[sub['predicted_category'] == 'App Login & Technical Bugs']['is_neg'].mean()
odds_app = p_app / (1 - p_app)
p_net = sub[sub['predicted_category'] == 'Network Speed & 4G Latency']['is_neg'].mean()
odds_net = p_net / (1 - p_net)
or_an = odds_app / odds_net
a = (sub[sub['predicted_category'] == 'App Login & Technical Bugs']['is_neg']).sum()
b = len(sub[sub['predicted_category'] == 'App Login & Technical Bugs']) - a
c_net = (sub[sub['predicted_category'] == 'Network Speed & 4G Latency']['is_neg']).sum()
d_net = len(sub[sub['predicted_category'] == 'Network Speed & 4G Latency']) - c_net
se_an = np.sqrt(1/a + 1/b + 1/c_net + 1/d_net)
print(f"OR App Login vs Network: {or_an:.2f} [{np.exp(np.log(or_an)-1.96*se_an):.2f}, {np.exp(np.log(or_an)+1.96*se_an):.2f}]")

