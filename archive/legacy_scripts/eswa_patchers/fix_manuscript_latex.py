from pathlib import Path

proper_section = r"""where weights $\boldsymbol{\omega} = [0.40, 0.40, 0.20]$ are assigned respectively to Calibrated LinearSVC ($w=2$), Balanced Logistic Regression ($w=2$), and Complement Naive Bayes ($w=1$) based on cross-validation log-loss optimization.

\subsubsection{Asymptotic Computational Complexity Analysis}
The computational complexity of the inference pipeline scales linearly with input text length and feature density. Let $L$ denote the character length of review $r_i$, $V$ represent the sub-word n-gram vocabulary size ($V \approx 50{,}000$), $d \ll V$ the non-zero feature density per tokenized sequence ($d \approx 20\text{--}45$), and $K$ the number of output classes ($K \in \{3, 5\}$). Text normalization and n-gram hash lookup require $\mathcal{O}(L)$ time. Sparse vector dot-product scoring across the linear ensemble models incurs $\mathcal{O}(d \cdot K)$ per review, followed by $\mathcal{O}(K)$ soft-voting probability aggregation. Consequently, total inference time complexity is $\mathcal{O}(L + d \cdot K)$, operating in strictly sub-millisecond execution time and completely bypassing the quadratic self-attention complexity ($\mathcal{O}(L^2 \cdot D)$) of full-scale transformer alternatives. The auxiliary memory footprint during production inference remains bounded at $\mathcal{O}(V \cdot K)$ for weight storage, enabling continuous throughput exceeding $450$ reviews/second on modest CPU hardware.

\subsection{Rogan-Gladen Misclassification Adjustment}"""

for fname in ["paper/eswa_latex/manuscript.tex", "paper/eswa_latex/manuscript_twocolumn.tex"]:
    p = Path(fname)
    content = p.read_text(encoding="utf-8")
    
    # Locate where the equation ends
    eq_end = "\\end{equation}\n"
    eq_idx = content.find(eq_end)
    rg_marker = "\\subsection{Rogan-Gladen Misclassification Adjustment}"
    rg_idx = content.find(rg_marker)
    
    if eq_idx != -1 and rg_idx != -1:
        prefix = content[:eq_idx + len(eq_end)]
        suffix = content[rg_idx + len(rg_marker):]
        # Replace the mangled region between \end{equation} and after \subsection{Rogan-Gladen...}
        content = prefix + proper_section + suffix
        p.write_text(content, encoding="utf-8")
        print(f"Fixed {fname} cleanly.")
    else:
        print(f"Failed to find markers in {fname}!")
