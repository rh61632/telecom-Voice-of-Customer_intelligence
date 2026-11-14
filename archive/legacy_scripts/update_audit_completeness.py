from pathlib import Path

path = Path("scripts/audit_project_integrity.py")
text = path.read_text(encoding="utf-8")

old_sec8 = """# MODULE 8: ANONYMITY AND PAGE BUDGET AUDIT
# ---------------------------------------------------------
print("\\n[MODULE 8] Verifying Double-Blind Anonymity & Document Length...")
blinded_tex = 'paper/eswa_latex/manuscript.tex'
with open(blinded_tex, 'r', encoding='utf-8') as f:
    tex_content = f.read()

for term in ['Ratul', 'rh61632', 'Leading University', 'github.com']:
    matches = len(re.findall(re.escape(term), tex_content, re.IGNORECASE))
    assert matches == 0, f"Found {matches} occurrences of prohibited identifier '{term}' in blinded manuscript!"
print("  [PASS] Anonymity check: 0 occurrences of author name, email, institution, or GitHub repo URL.")"""

new_sec8 = """# MODULE 8: ANONYMITY, MANUSCRIPT COMPLETENESS & PAGE BUDGET AUDIT
# ---------------------------------------------------------
print("\\n[MODULE 8] Verifying Double-Blind Anonymity, Section Completeness & Deliverables...")
blinded_tex = 'paper/eswa_latex/manuscript.tex'
with open(blinded_tex, 'r', encoding='utf-8') as f:
    tex_content = f.read()

for term in ['Ratul', 'rh61632', 'Leading University', 'github.com']:
    matches = len(re.findall(re.escape(term), tex_content, re.IGNORECASE))
    assert matches == 0, f"Found {matches} occurrences of prohibited identifier '{term}' in blinded manuscript!"
print("  [PASS] Anonymity check: 0 occurrences of author name, email, institution, or GitHub repo URL.")

# Verify all 8 core sections exist in the manuscript
expected_sections = [
    "Introduction",
    "Related Work",
    "VoC-Intelligence: System Architecture and Methodology",
    "Experimental Setup and Empirical Validation",
    "Real-World Deployment and Diagnostic Case Studies",
    "Managerial Decision Support and Industrial Implementation Guidelines",
    "Discussion, Threats to Validity, and Limitations",
    "Conclusion and Future Work"
]
for sec in expected_sections:
    assert f"\\\\section{{{sec}}}" in tex_content, f"Missing core section: '{sec}' in {blinded_tex}!"
print(f"  [PASS] Manuscript completeness: All {len(expected_sections)} core academic sections verified present.")

# Verify all key tables and algorithms exist
expected_labels = [
    "tab:taxonomy",
    "tab:model_leaderboard",
    "tab:perclass",
    "tab:linguistic_benchmark",
    "tab:eras",
    "tab:shocks",
    "alg:canary",
    "tab:decision_matrix"
]
for lbl in expected_labels:
    assert f"\\\\label{{{lbl}}}" in tex_content, f"Missing table/algorithm label: '{lbl}' in {blinded_tex}!"
print(f"  [PASS] Structural artifacts: All {len(expected_labels)} key tables, algorithms, and matrices verified present.")"""

assert old_sec8 in text, "old_sec8 not found"
text = text.replace(old_sec8, new_sec8)

path.write_text(text, encoding="utf-8")
print("Successfully updated audit_project_integrity.py with completeness checks!")
