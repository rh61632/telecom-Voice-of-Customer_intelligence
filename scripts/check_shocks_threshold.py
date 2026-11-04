import pandas as pd
import numpy as np

df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['review_date'] = pd.to_datetime(df['review_date'])
df['year_month'] = df['review_date'].dt.to_period('M')

m_sub = df[(df['review_date'] >= '2020-01-01') & (df['review_date'] <= '2026-09-30')]
monthly = m_sub.groupby(['operator', 'year_month'])['predicted_sentiment'].value_counts().unstack(fill_value=0)
for col in ['Positive', 'Negative', 'Neutral']:
    if col not in monthly.columns: monthly[col] = 0
monthly['total'] = monthly['Positive'] + monthly['Negative'] + monthly['Neutral']
monthly['nss'] = ((monthly['Positive'] - monthly['Negative']) / monthly['total']) * 100.0

for op in ['Grameenphone', 'Robi', 'Banglalink']:
    op_m = monthly.loc[op].copy()
    diffs = np.diff(op_m['nss'].values)
    months = op_m.index
    print(f"\n{op} transitions with |Delta NSS| >= 9.8:")
    for i in range(len(diffs)):
        d = diffs[i]
        if abs(d) >= 9.8:
            print(f"  {months[i]} -> {months[i+1]}: Delta NSS = {d:+.4f}")

