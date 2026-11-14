import pandas as pd
import numpy as np

df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['ym'] = df['review_date'].str[:7]
m = df.groupby(['operator', 'ym'])['predicted_sentiment'].apply(
    lambda x: ((x == 'Positive').sum() - (x == 'Negative').sum()) / len(x) * 100.0 if len(x) >= 30 else np.nan
).unstack(level='operator')
all_months = sorted(df['ym'].unique())

for ev, name in [('2018-02', '4G Commercial Launch'), 
                 ('2020-03', 'COVID-19 Onset'), 
                 ('2024-04', 'BL v11.8 Crash & Hotfix'), 
                 ('2025-09', '5G Commercial Launch')]:
    idx = all_months.index(ev)
    print(f"\n=== {ev}: {name} (index {idx}) ===")
    window = all_months[max(0, idx-5):min(len(all_months), idx+6)]
    sub = m.reindex(window)
    print("Min NSS in window:", sub.min().to_dict())
    print("Max NSS in window:", sub.max().to_dict())
