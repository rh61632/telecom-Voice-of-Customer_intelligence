import os
import re
import subprocess
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DIR = Path("paper/journal_manuscript").resolve()
TEX_PATH = DIR / "Telecom_VoC_Intelligence_JBA_Manuscript.tex"
BIB_PATH = DIR / "references.bib"
TEMP_TEX = DIR / "temp_for_pandoc.tex"
DOCX_PATH = DIR / "Telecom_VoC_Intelligence_JBA_Manuscript.docx"
TITLE_PAGE_DOCX = DIR / "Title_Page_JBA.docx"
PANDOC_EXE = r"C:\Users\user\AppData\Local\Pandoc\pandoc.exe"

# ==============================================================================
# 1. CREATE SEPARATE TITLE PAGE FOR DOUBLE-BLIND SUBMISSION
# ==============================================================================
def make_title_page():
    doc_tp = Document()
    for sec in doc_tp.sections:
        sec.top_margin = Inches(1.5)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
    
    p_title = doc_tp.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(24)
    r = p_title.add_run("Customer Experience Volatility and Operational Shock Attribution:\nMulti-Year Telecom Evidence from Bangladesh")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True

    p_author = doc_tp.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.space_before = Pt(24)
    p_author.paragraph_format.space_after = Pt(12)
    r = p_author.add_run("Md. Ratul Hasan")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True

    p_affil = doc_tp.add_paragraph()
    p_affil.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_affil.paragraph_format.line_spacing = 1.3
    p_affil.paragraph_format.space_after = Pt(36)
    r = p_affil.add_run(
        "Undergraduate Student\n"
        "Department of Electrical and Electronic Engineering\n"
        "Jashore University of Science and Technology\n"
        "Jashore - 7408, Bangladesh\n"
        "Email: rh61632@gmail.com | Phone: +880 1916-277722"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    p_note = doc_tp.add_paragraph()
    p_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_note.paragraph_format.space_before = Pt(48)
    r = p_note.add_run("Manuscript Type: Original Empirical Research Paper\nTarget Journal: Journal of Business Administration (JBA)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True

    doc_tp.save(TITLE_PAGE_DOCX)
    print("Saved Title Page document to:", TITLE_PAGE_DOCX)

make_title_page()

# ==============================================================================
# 2. PRE-PROCESS LATEX FOR BLINDED MAIN MANUSCRIPT
# ==============================================================================
with open(TEX_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Strip titlepage environment for double-blind manuscript
text = re.sub(r'\\begin\{titlepage\}[\s\S]*?\\end\{titlepage\}', '', text)

# Map custom JBA headings to standard LaTeX sections
text = re.sub(r'\\jbasection\{([^}]*)\}', r'\\section{\1}', text)
text = re.sub(r'\\jbasubsection\{([^}]*)\}', r'\\subsection{\1}', text)

# Clean \resizebox{\textwidth}{!}{% ... }%
text = re.sub(r'\\resizebox\{\\textwidth\}\{!\}[\s%]*', '', text)
text = re.sub(r'(\\end\{tabular\})\s*\}%', r'\1', text)
text = re.sub(r'(\\end\{tabular\})\s*\}', r'\1', text)

# Clean \shortstack
def clean_shortstack(m):
    inner = m.group(1)
    cleaned = inner.replace('\\\\', ' ').replace('\n', ' ')
    cleaned = ' '.join(cleaned.split())
    return cleaned
text = re.sub(r'\\shortstack\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', clean_shortstack, text)

# Clean \texorpdfstring
text = re.sub(r'\\texorpdfstring\{([^}]*)\}\{([^}]*)\}', r'\1', text)

# Clean spacing & font sizing macros
text = re.sub(r'\\begin\{spacing\}\{[^}]*\}', '', text)
text = re.sub(r'\\end\{spacing\}', '', text)
text = re.sub(r'\\begin\{hangparas\}\{[^}]*\}\{[^}]*\}', '', text)
text = re.sub(r'\\end\{hangparas\}', '', text)
text = text.replace(r'\singlespacing', '')
text = re.sub(r'\\fontsize\{[^}]*\}\{[^}]*\}\s*\\selectfont', '', text)
text = re.sub(r'\\setlength\{\\tabcolsep\}\{[^}]*\}', '', text)
text = re.sub(r'\\setstretch\{[^}]*\}', '', text)

# Clean \IfFileExists block
text = re.sub(r'\\IfFileExists\{[^{}]*\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{[\s\S]*?\\vspace\{3cm\}\}\}?%?\s*\}', r'\1', text)

with open(TEMP_TEX, "w", encoding="utf-8") as f:
    f.write(text)

print("Pre-processed Blinded LaTeX saved to temp_for_pandoc.tex")

# ==============================================================================
# 3. CONVERT VIA PANDOC
# ==============================================================================
cmd = [
    PANDOC_EXE,
    str(TEMP_TEX),
    f"--bibliography={BIB_PATH}",
    "--citeproc",
    "-o", str(DOCX_PATH)
]
res = subprocess.run(cmd, cwd=str(DIR), capture_output=True, text=True)
if res.returncode != 0:
    print("Pandoc Error:", res.stderr)
else:
    print("Pandoc successfully converted to docx.")

if TEMP_TEX.exists():
    TEMP_TEX.unlink()

# ==============================================================================
# 4. POST-PROCESS AND STYLE DOCX VIA PYTHON-DOCX
# ==============================================================================
doc = Document(DOCX_PATH)

# Strip document properties metadata
core_props = doc.core_properties
core_props.author = ""
core_props.last_modified_by = ""
core_props.title = "Customer Experience Volatility and Operational Shock Attribution: Multi-Year Telecom Evidence from Bangladesh"
core_props.subject = "Empirical Study of Mobile Telecommunications Service Quality"
core_props.keywords = "Net Sentiment Score; Service Quality; Mobile Network Operators; Sequential Stability; Digital Self-Care"
core_props.comments = ""

# Set margins to 1 inch all around
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)

    # Add bottom page number
    footer = section.footer
    p_ft = footer.paragraphs[0]
    p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ft.paragraph_format.line_spacing = 1.0
    p_ft.paragraph_format.space_before = Pt(0)
    p_ft.paragraph_format.space_after = Pt(0)
    r_ft = p_ft.add_run()
    r_ft.font.name = "Times New Roman"
    r_ft.font.size = Pt(10)
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    p_ft._p.append(fldSimple)

# Track when we are inside REFERENCES
in_references = False

for p in doc.paragraphs:
    t = p.text.strip()
    
    if t == "REFERENCES":
        in_references = True
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(12)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(14)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        continue

    if in_references:
        # APA References: single spaced, hanging indent 0.5 in, space after 4 pt
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(0, 0, 0)
        continue

    # Title paragraph
    if t.startswith("Customer Experience Volatility and Operational Shock Attribution:"):
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(12)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(15)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        continue

    # ABSTRACT Heading
    if t == "ABSTRACT":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        continue

    # Abstract body
    if t.startswith("This study analyzes 655,670 Google Play reviews"):
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.right_indent = Inches(0.25)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
            r.font.italic = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        continue

    # JEL & Keywords
    if t.startswith("JEL Classification Codes:") or t.startswith("Keywords:"):
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.right_indent = Inches(0.25)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)
            r.font.italic = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        continue

    # Main Section Headings (e.g. 1. INTRODUCTION, 2. THEORETICAL...)
    if re.match(r'^[1-7]\.\s+[A-Z\s,]+$', t):
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        continue

    # Subsection Headings (e.g. 2.1 Service Quality...)
    if re.match(r'^[1-7]\.[1-9]\s+', t):
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        continue

    # Table Captions
    if t.startswith("Table") or t.startswith("Descriptive Statistics") or t.startswith("Human Inter-Annotator") or t.startswith("Complaint Prevalence") or t.startswith("Level and Month-to-Month") or t.startswith("Additive Decomposition"):
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        continue

    # Table Notes
    if t.startswith("Note:") or t.startswith("aNote:"):
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(8)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        continue

    # Figure Captions
    if t.startswith("Figure"):
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(10)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        continue

    # Normal Body Paragraphs
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.9  # clean double spacing in academic docx
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.first_line_indent = Inches(0.5)
    for r in p.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)

# Format Tables
def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", sz="4", color="auto"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for b_name, b_val in [('top', top), ('left', left), ('bottom', bottom), ('right', right)]:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), b_val)
        if b_val != "none":
            b.set(qn('w:sz'), sz)
            b.set(qn('w:space'), '0')
            b.set(qn('w:color'), color)
        tcBorders.append(b)
    tcPr.append(tcBorders)

tables_to_remove = []
for table in doc.tables:
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    if len(table.rows) == 1 and len(table.columns) == 1 and table.rows[0].cells[0].text.strip() in ['1.0', '']:
        tables_to_remove.append(table)
        continue

    for r_idx, row in enumerate(table.rows):
        is_header = (r_idx == 0)
        is_last = (r_idx == len(table.rows) - 1)
        for cell in row.cells:
            top_b = "single" if is_header else "none"
            bot_b = "single" if (is_header or is_last) else "none"
            set_cell_borders(cell, top=top_b, bottom=bot_b, sz="6" if (is_header and top_b=="single" or is_last) else "4", color="333333")
            set_cell_margins(cell, top=50, bottom=50, left=90, right=90)
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.05
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(9.5)
                    if is_header:
                        run.font.bold = True

for t in tables_to_remove:
    p = t._tbl.getparent()
    p.remove(t._tbl)

doc.save(DOCX_PATH)
print("Successfully generated and styled Blinded Word manuscript at:", DOCX_PATH)
