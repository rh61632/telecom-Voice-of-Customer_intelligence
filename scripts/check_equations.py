from pathlib import Path
import re

text = Path('paper/index.html').read_text(encoding='utf-8')
matches = re.findall(r'<div class="equation-row">(.*?)</div>\s*</div>', text, re.DOTALL)
print(f"Total equations found: {len(matches)}")
for m in matches:
    num_match = re.search(r'<div class="equation-num">(.*?)</div>', m)
    num = num_match.group(1) if num_match else "?"
    clean = re.sub(r'<[^>]+>', ' ', m)
    clean = ' '.join(clean.split())
    print(f"Eq {num}: {clean}")
