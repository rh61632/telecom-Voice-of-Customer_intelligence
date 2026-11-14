---
phase: 5
plan: 2
wave: 1
depends_on: []
files_modified:
  - demo/app.py
  - demo/requirements.txt
  - ml/requirements.txt
  - dl/requirements.txt
  - requirements.txt
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "demo/app.py wires out_cat in callback outputs and returns 6-tuples matching layout"
    - "demo/app.py banner cites models trained on 4,500 seed reviews and evaluated on 655,649 reviews"
    - "demo/app.py paper reference uses the unified formal ESWA title without 'With Great Reviews...' prefix"
    - "demo/requirements.txt includes scikit-learn>=1.4.0, nltk>=3.8.1, and pandas>=2.0.0"
    - "ml/requirements.txt includes nltk>=3.8.1"
    - "dl/requirements.txt and root requirements.txt exclude torchvision and torchaudio"
    - "root requirements.txt includes all active runtime libraries (nltk, gradio, python-docx, openpyxl, Pillow, huggingface-hub)"
  artifacts:
    - "demo/app.py with complete 6-element return signature and verified AST"
    - "demo/requirements.txt with aligned dependencies"
    - "ml/requirements.txt with nltk declared"
    - "dl/requirements.txt free of unused heavy dependencies"
    - "requirements.txt canonical full-stack manifest"
---

# Plan 5.2: Gradio Demo UI Wiring, Banner & Dependency Manifests Alignment

## Objective
Wire the disconnected `out_cat` UI component in `demo/app.py`, update its training volume banner and unify its research paper title to the formal ESWA manuscript title, and reconcile dependency manifests across `demo/requirements.txt`, `ml/requirements.txt`, `dl/requirements.txt`, and root `requirements.txt` to eliminate unused heavy packages and ensure turnkey environment reproduction.

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/DECISIONS.md` (`ADR-002`, `ADR-003`)
- `.gsd/phases/5/RESEARCH.md`
- `demo/app.py`
- `demo/requirements.txt`
- `ml/requirements.txt`
- `dl/requirements.txt`
- `requirements.txt`

## Tasks

<task type="auto">
  <name>Fix Gradio demo UI out_cat callback, training volume banner, and paper title</name>
  <files>
    demo/app.py
  </files>
  <action>
    In `demo/app.py`:
    1. Fix the `out_cat` wiring bug (`DISC-MAJ-08`):
       - Line 31 (empty input branch): Update return tuple from 5 elements to 6 elements:
         ```python
         return "N/A", "N/A", "N/A", {}, {}, "Please enter a customer review."
         ```
       - Line 38: Add defensive guard against missing category model or confidence:
         ```python
         category_label = (
             f"{res['category']} ({res['category_confidence'] * 100:.1f}%)"
             if res.get("category") and res.get("category_confidence") is not None
             else "N/A"
         )
         ```
       - Line 54 (successful prediction branch): Update return tuple from 5 elements to 6 elements by inserting `category_label` at index 2:
         ```python
         return lang_badge, sentiment_label, category_label, res["probabilities"], cat_probs, diagnostic_summary
         ```
       - Line 108: Update click listener `outputs` list to include `out_cat` matching the return tuple:
         ```python
         outputs=[out_lang, out_sent, out_cat, out_sent_probs, out_cat_probs, out_diag]
         ```
    2. Fix the training volume banner claim at line 67 (`DISC-MIN-14`):
       Replace:
       ```markdown
       *Trained on 655,649 longitudinal customer reviews across Grameenphone, Robi Axiata, and Banglalink (2016–2026).*
       ```
       with:
       ```markdown
       *Demonstrating models trained on 4,500 expert/LLM-labeled seed reviews and evaluated across 655,649 longitudinal customer reviews from Grameenphone, Robi Axiata, and Banglalink (2016–2026).*
       ```
    3. Unify research paper title reference at line 114:
       Remove the informal `"With Great Reviews Comes Great Responsibility: "` prefix to align with formal ESWA title:
       ```markdown
       **Research Paper:** *“An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling”*
       ```
    
    AVOID: Modifying model loading paths or changing the theme/styling CSS.
    USE: Exact 6-tuple returns matching `[out_lang, out_sent, out_cat, out_sent_probs, out_cat_probs, out_diag]`.
  </action>
  <verify>
    python -c "import ast; tree = ast.parse(open('demo/app.py', encoding='utf-8').read()); code = open('demo/app.py', encoding='utf-8').read(); assert 'outputs=[out_lang, out_sent, out_cat, out_sent_probs, out_cat_probs, out_diag]' in code, 'out_cat missing from outputs'; assert '4,500 expert' in code, 'Banner text not updated'; assert 'With Great Reviews Comes Great Responsibility:' not in code, 'Title prefix not removed'; assert 'An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer' in code, 'Title text missing'; print('Task 1 verified: demo/app.py layout, banner, and title confirmed.')"
  </verify>
  <done>
    `demo/app.py` has `out_cat` wired in both returns and outputs, accurate training volume in banner, and formal ESWA paper title without informal prefix.
  </done>
</task>

<task type="auto">
  <name>Reconcile dependency manifests across demo, ML, DL, and project root</name>
  <files>
    demo/requirements.txt
    ml/requirements.txt
    dl/requirements.txt
    requirements.txt
  </files>
  <action>
    1. In `demo/requirements.txt` (`DISC-MAJ-03`, `DISC-HYG-03`):
       - Update line 2: change `scikit-learn>=1.3.0` to `scikit-learn>=1.4.0` (models were pickled under scikit-learn 1.6.1; aligns with root and ML manifests).
       - Add `nltk>=3.8.1` (imported at runtime by `ml/language_detector.py` via `ml/predict.py`).
       - Add `pandas>=2.0.0` (aligning with ML manifest).
    2. In `ml/requirements.txt` (`DISC-MAJ-03`):
       - Add `nltk>=3.8.1` (required by `ml.language_detector` when executing `python ml/predict.py` in standalone ML virtualenvs).
    3. In `dl/requirements.txt` (`DISC-HYG-02`):
       - Remove `torchvision>=0.17.0` (line 6) and `torchaudio>=2.2.0` (line 7). Codebase AST scan proves 0 imports of either package.
    4. In root `requirements.txt` (`DISC-MAJ-03`, `DISC-HYG-02`):
       - Remove `torchvision>=0.17.0` (line 36) and `torchaudio>=2.2.0` (line 37).
       - Add missing runtime dependencies proven by codebase imports across tools and pipelines:
         ```text
         # ── NLP & Demo UI ─────────────────────────────────────────────────────────────
         nltk>=3.8.1
         gradio>=4.0.0

         # ── Office & Paper Tooling ────────────────────────────────────────────────────
         python-docx>=1.1.0
         openpyxl>=3.1.0
         Pillow>=10.0.0

         # ── Hugging Face Hub ──────────────────────────────────────────────────────────
         huggingface-hub>=0.23.0
         ```
    
    AVOID: Exact version pinning (`==`) which causes dependency conflicts across Python versions.
    USE: `>=` minimum floor specifiers matching established repository conventions.
  </action>
  <verify>
    python -c "demo_req = open('demo/requirements.txt').read(); ml_req = open('ml/requirements.txt').read(); dl_req = open('dl/requirements.txt').read(); root_req = open('requirements.txt').read(); assert 'nltk>=3.8.1' in demo_req and 'scikit-learn>=1.4.0' in demo_req and 'pandas>=2.0.0' in demo_req, 'demo/requirements.txt incomplete'; assert 'nltk>=3.8.1' in ml_req, 'ml/requirements.txt missing nltk'; assert 'torchvision' not in dl_req and 'torchaudio' not in dl_req, 'dl/requirements.txt contains unused heavy libs'; assert 'torchvision' not in root_req and 'torchaudio' not in root_req, 'requirements.txt contains unused heavy libs'; assert all(pkg in root_req for pkg in ['nltk>=3.8.1', 'gradio>=4.0.0', 'python-docx>=1.1.0', 'openpyxl>=3.1.0', 'Pillow>=10.0.0', 'huggingface-hub>=0.23.0']), 'requirements.txt missing runtime packages'; print('Task 2 verified: All requirements manifests aligned and verified.')"
  </verify>
  <done>
    `demo/requirements.txt`, `ml/requirements.txt`, `dl/requirements.txt`, and root `requirements.txt` are free of unused dependencies and declare all required runtime packages.
  </done>
</task>

</tasks>

## Must-Haves
After all tasks complete, verify:
- [ ] `demo/app.py` parses cleanly via `ast.parse` and registers `out_cat` in click outputs
- [ ] `demo/app.py` banner reflects 4,500 seed reviews and 655,649 evaluation reviews
- [ ] `demo/app.py` uses the formal ESWA paper title without `"With Great Reviews..."` prefix
- [ ] `demo/requirements.txt` declares `scikit-learn>=1.4.0`, `nltk>=3.8.1`, and `pandas>=2.0.0`
- [ ] `ml/requirements.txt` declares `nltk>=3.8.1`
- [ ] `torchvision` and `torchaudio` are completely removed from `dl/requirements.txt` and `requirements.txt`
- [ ] `requirements.txt` declares `nltk`, `gradio`, `python-docx`, `openpyxl`, `Pillow`, and `huggingface-hub`

## Success Criteria
- [ ] Both tasks verified passing with single-command PowerShell checks
- [ ] Must-haves confirmed
- [ ] Zero unsolicited git commits generated (`ADR-003`)
