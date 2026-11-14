import re

with open('scripts/fix_table_formatting.py', 'r', encoding='utf-8') as f:
    text = f.read()

var_names = ['TABLE1_NEW', 'TABLE2_NEW', 'TABLE3_NEW', 'TABLE4_NEW', 'TABLE5_NEW', 'TABLE6_NEW', 'TABLE7_NEW', 'TABLE8_NEW']
for v in var_names:
    pattern = v + r'\s*=\s*r?"""(.*?)"""'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        content = m.group(1).strip()
        labels = re.findall(r'\\label\{([^}]+)\}', content)
        print(f'{v}: {len(content)} chars, labels: {labels}')
    else:
        print(f'{v}: NOT FOUND')
