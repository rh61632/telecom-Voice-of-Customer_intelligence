import pandas as pd
import numpy as np

df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['review_date'] = pd.to_datetime(df['review_date'])
df['year_month'] = df['review_date'].dt.to_period('M')

monthly = df.groupby(['operator', 'year_month'])['predicted_sentiment'].value_counts().unstack(fill_value=0)
for col in ['Positive', 'Negative', 'Neutral']:
    if col not in monthly.columns: monthly[col] = 0
monthly['total'] = monthly['Positive'] + monthly['Negative'] + monthly['Neutral']
monthly['nss'] = ((monthly['Positive'] - monthly['Negative']) / monthly['total']) * 100.0

print("--- FULL COMMON DURATION SHOCK COUNTS ---")
for min_n in [0, 30]:
    total_shocks = 0
    total_transitions = 0
    print(f"\nMinimum monthly N = {min_n}:")
    for op in ['Grameenphone', 'Robi', 'Banglalink']:
        op_m = monthly.loc[op].copy()
        if min_n > 0:
            op_m = op_m[op_m['total'] >= min_n]
        diffs = np.diff(op_m['nss'].values)
        shocks = np.sum(np.abs(diffs) >= 10.0)
        total_shocks += shocks
        total_transitions += len(diffs)
        print(f"  {op}: {shocks} shocks out of {len(diffs)} transitions")
    print(f"Total: {total_shocks} shocks out of {total_transitions} transitions")

