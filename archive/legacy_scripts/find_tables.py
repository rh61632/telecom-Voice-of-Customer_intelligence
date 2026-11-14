import docx

doc = docx.Document('paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx')

for i, p in enumerate(doc.paragraphs):
    if 'Table ' in p.text:
        print(f'P{i}: {p.text}')
