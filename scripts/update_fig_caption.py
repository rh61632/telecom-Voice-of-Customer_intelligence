import re

tex_path = 'paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex'
with open(tex_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update text reference in Section 4.1
old_ref = r"Figure~\ref{fig:monthly} plots the monthly trajectories across all 81 modern-era months ($n \ge 30$)."
new_ref = r"Figure~\ref{fig:monthly}a plots monthly trajectories across all 81 modern-era months ($n \ge 30$), while Figure~\ref{fig:monthly}b--c deconstructs the Spring 2024 volatility episode into build telemetry and review volume surges."

assert old_ref in text, "old_ref not found!"
text = text.replace(old_ref, new_ref)

# 2. Update caption of Figure 1
old_cap = r"\caption{Monthly NSS by Operator, January 2020 to September 2026 (81 Months, $n \ge 30$ per Operator-Month)}"
new_cap = r"\caption{Longitudinal Sentiment Trajectories and Micro-Level Shock Telemetry: (a) Monthly NSS by Operator, 2020--2026 (81 Months, $N = 634{,}992$); (b) Banglalink Build-Level NSS and 95\% CIs during Spring 2024; (c) Contemporaneous Monthly Review Volume Distribution showing the +72.2\% surge confound.}"

assert old_cap in text, "old_cap not found!"
text = text.replace(old_cap, new_cap)

with open(tex_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Caption and text reference updated successfully!")

