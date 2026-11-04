import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
df['ym'] = df['review_date'].str[:7]
modern = df[df['ym'].between('2020-01', '2026-09')].copy()

# Compute monthly NSS
monthly = modern.groupby(['operator', 'ym'])['predicted_sentiment'].value_counts().unstack(fill_value=0)
for col in ['Positive', 'Negative', 'Neutral']:
    if col not in monthly.columns: monthly[col] = 0
monthly['total'] = monthly['Positive'] + monthly['Negative'] + monthly['Neutral']
monthly['nss'] = ((monthly['Positive'] - monthly['Negative']) / monthly['total']) * 100.0

gp_nss = monthly.loc['Grameenphone']['nss']
robi_nss = monthly.loc['Robi']['nss']
bl_nss = monthly.loc['Banglalink']['nss']

print("Months count:", len(gp_nss))
print("GP min/max:", gp_nss.min(), gp_nss.max())
print("Robi min/max:", robi_nss.min(), robi_nss.max())
print("BL min/max:", bl_nss.min(), bl_nss.max())

