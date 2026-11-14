with open('paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(r'\begin{table}[htbp]', r'\begin{table}[!ht]', 1) # Table 4
# And figure:
text = text.replace(r'\begin{figure}[htbp]', r'\begin{figure}[!ht]', 1)

with open('paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated float specifiers for Table 4 and Figure 1")

