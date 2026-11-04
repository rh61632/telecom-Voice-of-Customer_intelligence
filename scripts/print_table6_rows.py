from run_p4 import sdf
import pandas as pd

top10_idx = [
    ('Grameenphone', '2020-03 to 2020-04'),
    ('Grameenphone', '2021-04 to 2021-05'),
    ('Grameenphone', '2021-08 to 2021-09'),
    ('Grameenphone', '2025-08 to 2025-09'),
    ('Robi', '2022-12 to 2023-01'),
    ('Robi', '2023-01 to 2023-02'),
    ('Robi', '2023-11 to 2023-12'),
    ('Banglalink', '2021-04 to 2021-05'),
    ('Banglalink', '2024-03 to 2024-04'),
    ('Banglalink', '2024-04 to 2024-05'),
]

for op, p in top10_idx:
    r = sdf[(sdf['operator'] == op) & (sdf['period'] == p)].iloc[0]
    p_fmt = p.replace(' to ', r' $\to$ ')
    lead_name = r['lead_op'].replace(' & Technical Bugs', ' & Bugs').replace('Speed & 4G Latency', 'Speed & Latency').replace('&', r'\&')
    lead_val = r['delta_nss'] * (r['lead_op_share'] / 100.0)
    print(f"{r['operator']} & {p_fmt} & {r['delta_nss']:+.1f} & {lead_name} & {lead_val:+.2f} ({r['lead_op_share']:.0f}\\%) & {r['four_domain_diff']:+.2f} ({r['four_domain_share']:.0f}\\%) & {r['gen_diff']:+.2f} ({r['gen_share']:.0f}\\%) \\\\")
