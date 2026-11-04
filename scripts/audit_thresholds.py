import pandas as pd
import numpy as np

df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['ym'] = df['review_date'].str[:7]
modern = df[df['ym'].between('2020-01', '2026-09')].copy()

operators = ['Grameenphone', 'Robi', 'Banglalink']

for thresh in [8.0, 10.0, 12.0]:
    print(f"\n--- THRESHOLD |Delta NSS| >= {thresh} ---")
    tot_ens = 0
    tot_svm = 0
    for op in operators:
        op_m = modern[modern['operator'] == op]
        
        # Ensemble
        m_ens = op_m.groupby('ym')['predicted_sentiment'].apply(lambda x: ((x=='Positive').sum() - (x=='Negative').sum()) / len(x) * 100)
        d_ens = np.diff(m_ens.values)
        c_ens = np.sum(np.abs(d_ens) >= thresh)
        tot_ens += c_ens
        
        # Linear SVM
        m_svm = op_m.groupby('ym')['sentiment_linearsvc'].apply(lambda x: ((x=='Positive').sum() - (x=='Negative').sum()) / len(x) * 100)
        d_svm = np.diff(m_svm.values)
        c_svm = np.sum(np.abs(d_svm) >= thresh)
        tot_svm += c_svm
        
        print(f"  {op:12}: Ensemble = {c_ens:2d}, SVM = {c_svm:2d}")
    print(f"  Total across all 3: Ensemble = {tot_ens:2d}, SVM = {tot_svm:2d}")

