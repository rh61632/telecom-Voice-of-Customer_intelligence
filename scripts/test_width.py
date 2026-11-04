with open('paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace \includegraphics[width=\textwidth] with \includegraphics[width=0.90\textwidth]
text = text.replace(r'\includegraphics[width=\textwidth]{figures/monthly_nss_trend_2020_2026.png}',
                    r'\includegraphics[width=0.92\textwidth]{figures/monthly_nss_trend_2020_2026.png}')

with open('paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated LaTeX figure width to 0.92\\textwidth")

