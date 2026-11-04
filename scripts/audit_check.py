with open('paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex', 'r', encoding='utf-8') as f:
    text = f.read()

ref_idx = text.find(r'\jbasection{REFERENCES}')
body = text[:ref_idx]

refs = [
    ("Anderson & Sullivan", "1993"),
    ("Anderson, Fornell", "2004"),
    ("Bhattacharjee", "2022"),
    ("Boulding", "1993"),
    ("BTRC", "2025"),
    ("Cohen", "1960"),
    ("Cooil", "2007"),
    ("Fornell", "1996"),
    ("Gerpott", "2001"),
    ("Kahneman", "1979"),
    ("Khalid", "2015"),
    ("Kim", "2004"),
    ("Landis & Koch", "1977"),
    ("Mittal", "1998"),
    ("Netzer", "2012"),
    ("Oliver", "1980"),
    ("Parasuraman", "1988"),
    ("Politis & Romano", "1994"),
    ("Reichheld", "2003"),
    ("Rust & Zahorik", "1993"),
    ("Siddiqi", "2011"),
    ("Tirunillai & Tellis", "2014"),
    ("The Business Standard", "2025"),
    ("von Neumann", "1941"),
    ("Zeithaml", "2002")
]

print("=== CHECKING ALL 25 REFERENCES IN BODY ===")
for author, year in refs:
    # search in body
    in_body = (year in body) and any(w.lower() in body.lower() for w in author.split() if len(w) > 3)
    if in_body:
        print(f"CITED: {author} ({year})")
    else:
        print(f"NOT CITED: {author} ({year})")
