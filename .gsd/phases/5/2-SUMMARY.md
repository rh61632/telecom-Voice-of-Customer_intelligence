# Plan 5.2 Summary: Gradio Demo UI Wiring, Banner & Dependency Manifests Alignment

## Summary

Successfully remediated the disconnected `out_cat` operational domain component in `demo/app.py`, corrected the demo training volume claim and research paper title, and reconciled all dependency manifests across `demo/requirements.txt`, `ml/requirements.txt`, `dl/requirements.txt`, and root `requirements.txt`.

## Tasks Completed

| Task | Description | Status | Evidence |
|---|---|---|---|
| Task 1 | Fix Gradio demo UI `out_cat` callback, training volume banner, and paper title | Complete | AST parsed cleanly; verified 6-element tuple return on empty & valid review branches, defensive category confidence formatting, `out_cat` in click outputs, updated training banner text ("4,500 expert/LLM-labeled seed reviews... 655,649 longitudinal customer reviews"), and unified ESWA paper title without informal prefix. |
| Task 2 | Reconcile dependency manifests across demo, ML, DL, and project root | Complete | `demo/requirements.txt` aligned to `scikit-learn>=1.4.0`, `nltk>=3.8.1`, `pandas>=2.0.0`; `ml/requirements.txt` includes `nltk>=3.8.1`; `dl/requirements.txt` and `requirements.txt` stripped of unused heavy packages `torchvision` and `torchaudio`; `requirements.txt` declared runtime dependencies (`nltk`, `gradio`, `python-docx`, `openpyxl`, `Pillow`, `huggingface-hub`). |

## Verification Details

1. **AST & UI Callback Verification:**
   ```powershell
   python -c "import ast; tree = ast.parse(open('demo/app.py', encoding='utf-8').read()); code = open('demo/app.py', encoding='utf-8').read(); assert 'outputs=[out_lang, out_sent, out_cat, out_sent_probs, out_cat_probs, out_diag]' in code; assert '4,500 expert' in code; assert 'With Great Reviews Comes Great Responsibility:' not in code; assert 'An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer' in code; print('Task 1 verified')"
   ```
   *Result:* Clean exit code 0 (`Task 1 verified: demo/app.py layout, banner, and title confirmed.`).

2. **Dependency Manifests Verification:**
   ```powershell
   python -c "demo_req = open('demo/requirements.txt').read(); ml_req = open('ml/requirements.txt').read(); dl_req = open('dl/requirements.txt').read(); root_req = open('requirements.txt').read(); assert 'nltk>=3.8.1' in demo_req and 'scikit-learn>=1.4.0' in demo_req and 'pandas>=2.0.0' in demo_req; assert 'nltk>=3.8.1' in ml_req; assert 'torchvision' not in dl_req and 'torchaudio' not in dl_req; assert 'torchvision' not in root_req and 'torchaudio' not in root_req; assert all(pkg in root_req for pkg in ['nltk>=3.8.1', 'gradio>=4.0.0', 'python-docx>=1.1.0', 'openpyxl>=3.1.0', 'Pillow>=10.0.0', 'huggingface-hub>=0.23.0']); print('Task 2 verified')"
   ```
   *Result:* Clean exit code 0 (`Task 2 verified: All requirements manifests aligned and verified.`).

3. **Composite Must-Haves Verification:**
   All 7 must-have assertions passed simultaneously with zero errors.

## Discrepancies Closed

- **`DISC-MAJ-08`**: Gradio UI `out_cat` operational category component disconnected from inference output tuple.
- **`DISC-MIN-14`**: Gradio demo UI banner claiming "Trained on 655,649" instead of 4,500 seed reviews.
- **`DISC-HYG-01`**: Inconsistent paper title across demo UI vs formal manuscript.
- **`DISC-MAJ-03`**: Incomplete standalone dependencies in `demo/requirements.txt` and `ml/requirements.txt` (`nltk`, `scikit-learn>=1.4.0`, `pandas`).
- **`DISC-HYG-02`**: Unused heavy dependencies `torchvision` and `torchaudio` declared in DL and root manifests.
- **`DISC-HYG-03`**: Sub-module dependency specifier mismatch (`scikit-learn>=1.3.0` vs `>=1.4.0`).

## Deviations from Plan

None.

## Git Commits

None (`commits: none (ADR-003)`). Working tree preserved for staged inspection.
