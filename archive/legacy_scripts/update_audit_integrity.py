from pathlib import Path

p = Path("scripts/audit_project_integrity.py")
text = p.read_text(encoding="utf-8")

old_marker = "blinded_tex = 'paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript_Blinded.tex'"
idx = text.find(old_marker)
if idx != -1:
    end_marker = "print(\"  [PASS] Final deliverables generated:"
    end_idx = text.find(end_marker, idx)
    if end_idx != -1:
        # Find newline after that line
        nl_idx = text.find("\n", end_idx)
        replacement = """blinded_tex = 'paper/eswa_latex/manuscript.tex'
with open(blinded_tex, 'r', encoding='utf-8') as f:
    tex_content = f.read()

for term in ['Ratul', 'rh61632', 'Leading University', 'github.com']:
    matches = len(re.findall(re.escape(term), tex_content, re.IGNORECASE))
    assert matches == 0, f"Found {matches} occurrences of prohibited identifier '{term}' in blinded manuscript!"
print("  [PASS] Anonymity check: 0 occurrences of author name, email, institution, or GitHub repo URL.")

pdf_path = 'paper/manuscript.pdf'
pdf_twocol_path = 'paper/manuscript_twocolumn.pdf'
assert os.path.exists(pdf_path), "Single-column PDF not found!"
assert os.path.exists(pdf_twocol_path), "Two-column PDF not found!"
print("  [PASS] Final deliverables generated: manuscript.pdf and manuscript_twocolumn.pdf both verified.")"""
        text = text[:idx] + replacement + text[nl_idx+1:]
        p.write_text(text, encoding="utf-8")
        print("audit_project_integrity.py updated successfully.")
    else:
        print("End marker not found!")
else:
    print("Start marker not found!")
