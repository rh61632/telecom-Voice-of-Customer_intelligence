from pathlib import Path
import re

html_path = Path('paper/index.html')
text = html_path.read_text(encoding='utf-8')

sections = re.findall(r'<section id="([^"]+)">(.*?)</section>', text, re.DOTALL)
print('--- TRUE PROSE WORD COUNTS (EXCLUDING TABLES, FIGURES, EQUATIONS) ---')
total_words = 0
for sid, scontent in sections:
    # Remove tables, figures, equations, callouts, metadata
    clean = re.sub(r'<table\b.*?</table>', '', scontent, flags=re.DOTALL)
    clean = re.sub(r'<div class="(?:callout-box|metadata-box|equation-row|figure-img-wrap|figure-note|figure-caption|table-note|table-caption)">.*?</div>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<button[^>]*>.*?</button>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<h[1-3][^>]*>.*?</h[1-3]>', '', clean, flags=re.DOTALL)
    
    plain = re.sub(r'<[^>]+>', ' ', clean)
    plain = re.sub(r'\s+', ' ', plain).strip()
    words = plain.split()
    w_count = len(words)
    if sid not in ['page1-title', 'sec8-references', 'sec9-annexure']:
        total_words += w_count
    print(f'  {sid:20s}: {w_count:5d} words')

print(f'\nTotal Manuscript Prose: {total_words:,} words (Guideline Target: ~3,200 words)')
