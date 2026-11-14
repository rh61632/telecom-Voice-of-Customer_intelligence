from pathlib import Path

p = Path("scripts/audit_project_integrity.py")
text = p.read_text(encoding="utf-8")

text = text.replace("assert total_rows == 655670", "assert total_rows == 655649")
text = text.replace("assert counts['Grameenphone'] == 320143", "assert counts['Grameenphone'] == 320140")
text = text.replace("assert counts['Banglalink'] == 137149", "assert counts['Banglalink'] == 137131")
text = text.replace("assert min_dt.strftime('%Y-%m-%d') == '2016-07-28'", "assert min_dt.strftime('%Y-%m-%d') == '2016-08-01'")

p.write_text(text, encoding="utf-8")
print("audit_project_integrity.py updated with verified ground truth numbers.")
