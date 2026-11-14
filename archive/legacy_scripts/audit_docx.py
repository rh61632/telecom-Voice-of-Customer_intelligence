import docx

doc = docx.Document('paper/Telecom_VoC_Intelligence_JBA_Manuscript.docx')

print('=== SECTION MARGINS ===')
for i, s in enumerate(doc.sections):
    print(f'Section {i}: Top={s.top_margin.inches}", Bottom={s.bottom_margin.inches}", Left={s.left_margin.inches}", Right={s.right_margin.inches}"')

print('\n=== WORD COUNT ===')
total_words = sum(len(p.text.split()) for p in doc.paragraphs)
print(f'Total prose words across paragraphs: {total_words}')

print('\n=== HEADING AUDIT ===')
for p in doc.paragraphs:
    txt = p.text.strip()
    if any(txt.startswith(prefix) for prefix in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', 'Table ', 'Figure ']):
        print(f'{txt[:75]}')
