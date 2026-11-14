#!/usr/bin/env python3
"""
Sync ESWA Two-Column Manuscript (manuscript_twocolumn.tex) from Single-Column (manuscript.tex).

Maintains byte-identical body parity between single-column and two-column
manuscripts while swapping only the preamble to elsarticle final,5p twocolumn.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
ESWA_DIR = REPO_ROOT / "paper" / "eswa_latex"
MANUSCRIPT_SC = ESWA_DIR / "manuscript.tex"
MANUSCRIPT_TC = ESWA_DIR / "manuscript_twocolumn.tex"

TWOCOLUMN_PREAMBLE = """\\documentclass[final,5p,times,twocolumn,authoryear]{elsarticle}

%% =========================================================================
%% PACKAGES & PREAMBLE
%% =========================================================================
\\usepackage[T1]{fontenc}
\\usepackage{amsmath,amssymb}
\\usepackage{booktabs}
\\usepackage{array}
\\usepackage{tabularx}
\\usepackage{multirow}
\\usepackage{float}
\\usepackage{caption}
\\usepackage{graphicx}
\\usepackage{microtype}
\\usepackage{hyperref,url,xcolor}
\\usepackage{setspace}
\\setlength{\\bibsep}{0.5pt plus 0.2ex}
\\setlength{\\dbltextfloatsep}{6pt plus 1pt minus 1pt}
\\setlength{\\textfloatsep}{6pt plus 1pt minus 1pt}
\\setlength{\\floatsep}{6pt plus 1pt minus 1pt}
\\setlength{\\dblfloatsep}{6pt plus 1pt minus 1pt}
\\captionsetup{skip=4pt}"""


def sync_twocolumn() -> None:
    if not MANUSCRIPT_SC.exists():
        print(f"ERROR: {MANUSCRIPT_SC} not found", file=sys.stderr)
        sys.exit(1)

    sc_text = MANUSCRIPT_SC.read_text(encoding="utf-8")
    sc_lines = sc_text.splitlines()

    # Locate body beginning at \\journal{Expert Systems with Applications}
    journal_idx = None
    for i, line in enumerate(sc_lines):
        if line.strip().startswith(r"\journal{Expert Systems with Applications}"):
            journal_idx = i
            break

    if journal_idx is None:
        print("ERROR: Could not locate '\\journal{Expert Systems with Applications}' in manuscript.tex", file=sys.stderr)
        sys.exit(1)

    assert journal_idx == 24, f"Expected \\journal at index 24 (line 25), got index {journal_idx}"

    body_lines = sc_lines[journal_idx:]
    preamble_lines = TWOCOLUMN_PREAMBLE.splitlines()
    assert len(preamble_lines) == len(TWOCOLUMN_PREAMBLE.splitlines()), f"Expected {len(TWOCOLUMN_PREAMBLE.splitlines())}-line twocolumn preamble, got {len(preamble_lines)}"

    tc_lines = preamble_lines + body_lines
    tc_text = "\n".join(tc_lines) + "\n"

    MANUSCRIPT_TC.write_text(tc_text, encoding="utf-8")
    print(f"✓ Synchronized {MANUSCRIPT_TC} ({len(tc_lines)} lines)")

    # Validate byte-identical body parity
    s_lines = sc_lines[24:]
    t_lines = tc_lines[len(preamble_lines):]
    assert s_lines == t_lines, "Body lines diverged between single-column and two-column"
    print(f"✓ Validated exact byte-identical body parity (single-column line 25-end == twocolumn line {len(preamble_lines)+1}-end)")


if __name__ == "__main__":
    sync_twocolumn()
