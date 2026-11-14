from pathlib import Path

target = r"\usepackage{amsmath,amssymb}"
replacement = "\\usepackage[T1]{fontenc}\n\\usepackage{amsmath,amssymb}"

for f in ["paper/eswa_latex/manuscript.tex", "paper/eswa_latex/manuscript_twocolumn.tex"]:
    p = Path(f)
    content = p.read_text(encoding="utf-8")
    if "fontenc" not in content:
        content = content.replace(target, replacement, 1)
        p.write_text(content, encoding="utf-8")
        print(f"Added fontenc to {f}")
    else:
        print(f"fontenc already in {f}")
