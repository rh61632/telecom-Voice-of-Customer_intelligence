import os
import re

pattern = re.compile(r'(Grameenphone|Robi|Banglalink|operator_colors|brand_colors|COLORS).*?(#[0-9a-fA-F]{6})', re.IGNORECASE)
found = set()

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or 'brain' in root:
        continue
    for f in files:
        if f.endswith(('.py', '.md', '.json', '.txt')):
            p = os.path.join(root, f)
            try:
                content = open(p, encoding='utf-8', errors='ignore').read()
                for line in content.splitlines():
                    if any(k in line for k in ['Grameenphone', 'Robi', 'Banglalink', 'palette', 'color', 'BRAND']):
                        for m in re.finditer(r'[\'"](#[0-9a-fA-F]{6})[\'"]', line):
                            found.add((p, line.strip()))
            except Exception as e:
                pass

for path, line in sorted(found):
    print(f"{path}: {line}")
