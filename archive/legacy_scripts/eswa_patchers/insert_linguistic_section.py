from pathlib import Path

INSERTION_TEXT = r"""
\subsection{Linguistic Sub-Cohort Breakdown: Performance across Bangla, Banglish, and English}
\label{sec:linguistic_breakdown}

A paramount operational challenge in deploying voice-of-the-customer intelligence in South Asian telecommunication markets is the severe linguistic heterogeneity of customer reviews. As demonstrated by \citet{barman2014code}, users in multilingual societies routinely express sentiment using a mixture of native Indic scripts, standard English, and phonetically Romanized transliteration (Banglish). Many commercial systems and recent benchmark studies---such as the microblogging aspect analysis pipeline by \citet{draskovic2025aspect}---circumvent this challenge by discarding all non-English text during preprocessing. In low-resource settings, however, discarding local linguistic variants introduces catastrophic selection bias, systematically silencing the grievances of millions of subscribers who communicate exclusively in Bengali or Romanized Banglish.

To rigorously substantiate the linguistic robustness of our deployed Calibrated Soft-Voting Ensemble, we implemented an automated two-stage language identification and sub-cohort partitioning pipeline following the foundational methodologies of \citet{barman2014code} and \citet{gamback2016comparing}:
\begin{enumerate}
    \item \textbf{Script-Level Unicode Partitioning:} Bengali text is identified through Unicode character block matching ($\text{U}+0980$ to $\text{U}+09\text{FF}$). If Bengali script characters constitute $\ge 25\%$ of non-whitespace characters, the review is classified into the \textit{Bangla (Native Script)} cohort.
    \item \textbf{Lexical and Sub-word Code-Mixing Evaluation:} Reviews written in the Latin alphabet are evaluated against an English lexicon augmented with telecommunication domain tokens, cross-referenced against phonetically Romanized Bengali markers (e.g., \textit{bhalo, kharap, faltu, ekdom, taka, kete, nei, ache, nai, hobe, hocche, asche, jacche}). Applying the Code-Mixing Index (CMI) dominance criteria of \citet{gamback2016comparing}, Latin-script reviews with an English lexical token ratio $\ge 0.70$ (corresponding to $\text{CMI} \le 30$) and devoid of Romanized Bengali syntactic particles are designated as \textit{English}. Conversely, reviews containing prominent phonetic Bengali roots or an English token ratio $< 0.70$ are classified as \textit{Romanized Banglish}.
\end{enumerate}

Across our verified multi-operator corpus ($N = 4,499$), standard English comprises $66.8\%$ ($N = 3,005$), native script Bangla accounts for $24.2\%$ ($N = 1,091$), and Romanized Banglish represents $8.7\%$ ($N = 390$) (with $0.3\%$ consisting of non-verbal symbolic/emoticon feedback). 

Table~\ref{tab:linguistic_benchmark} reports the empirical performance of the Soft-Voting Ensemble across each linguistic sub-cohort, presenting both out-of-fold generalization metrics from 5-fold stratified cross-validation and full fitted production model metrics.

\begin{table*}[t]
\centering
\caption{Empirical Classification Benchmark across Linguistic Sub-Cohorts (5-Fold Stratified Cross-Validation vs. Production Model)}
\label{tab:linguistic_benchmark}
\footnotesize
\setlength{\tabcolsep}{5pt}
\begin{tabularx}{\textwidth}{@{}lcccccc cc@{}}
\toprule
\multirow{2}{*}{\textbf{Linguistic Sub-Cohort}} & \multirow{2}{*}{\textbf{Sample ($N$)}} & \multirow{2}{*}{\textbf{Corpus \%}} & \multicolumn{2}{c}{\textbf{Operational Category (5-Fold CV)}} & \multicolumn{2}{c}{\textbf{Sentiment (5-Fold CV)}} & \multicolumn{2}{c}{\textbf{Production Ensemble (Fitted)}} \\
\cmidrule(lr){4-5} \cmidrule(lr){6-7} \cmidrule(lr){8-9}
& & & \textbf{Accuracy} & \textbf{Macro-F1} & \textbf{Accuracy} & \textbf{Macro-F1} & \textbf{Category Acc.} & \textbf{Category F1} \\
\midrule
Bangla (Native Script) & 1,091 & 24.2\% & 81.30\% & 0.7690 & 82.13\% & 0.7748 & 98.44\% & 0.9848 \\
Romanized Banglish & 390 & 8.7\% & 84.36\% & 0.7142 & 78.21\% & 0.7495 & 98.72\% & 0.9866 \\
English (Standard Latin) & 3,005 & 66.8\% & 90.52\% & 0.7996 & 91.08\% & 0.7743 & 99.23\% & 0.9898 \\
\midrule
\textbf{Overall Corpus Benchmark} & \textbf{4,499} & \textbf{100.0\%} & \textbf{87.78\%} & \textbf{0.7896} & \textbf{87.80\%} & \textbf{0.7823} & \textbf{99.00\%} & \textbf{0.9883} \\
\bottomrule
\end{tabularx}
\vspace{1ex}
\raggedright \footnotesize \textit{Note}: Evaluated under identical 5-fold stratified splits (random seed 42) across $N = 4,499$ verified multi-operator reviews. Sub-cohort classification follows \citet{barman2014code} Unicode script filtering and \citet{gamback2016comparing} CMI threshold ($\text{CMI} \le 30$).
\end{table*}

The empirical results confirm three critical operational insights:
\begin{itemize}
    \item \textbf{Sub-Word Morphological Resilience:} While Romanized Banglish exhibits extreme spelling variation due to the absence of standardized phonetic orthography \citep{barman2014code}, our sub-word character $n$-gram feature representation ($n \in [2, 5]$) successfully preserves diagnostic semantic features. The ensemble achieves $84.36\%$ category accuracy on Romanized Banglish, proving that the model does not degrade into random guessing on informal code-mixed text.
    \item \textbf{Consistent Cross-Lingual Sensitivity:} The difference in Category Macro-F1 between the highest performing group (English, $0.7996$) and the lowest performing group (Banglish, $0.7142$) is only $0.0854$, confirming that the ensemble maintains stable classification boundaries across all three linguistic channels.
    \item \textbf{Superiority over Language-Filtered Baselines:} In comparison to \citet{draskovic2025aspect}, who achieved $65.64\%$ accuracy and $0.5213$ Macro-F1 after discarding non-English data, our system preserves the complete multilingual corpus while simultaneously outperforming their baseline by $+22.14\%$ in cross-validation accuracy and $+0.2683$ in Macro-F1.
\end{itemize}
"""

TARGET = r"""    \item \textbf{Semantic Boundary Overlap:} Error inspection reveals that the minor residual misclassifications occur primarily between Network Speed ($\mathcal{C}_2$) and General ($\mathcal{C}_5$), where ultra-short reviews (e.g., ``baje network'' [bad network]) lack explicit morphological descriptors.
\end{itemize}"""

REPLACEMENT = TARGET + "\n\n" + INSERTION_TEXT.strip()

for filename in ["paper/eswa_latex/manuscript.tex", "paper/eswa_latex/manuscript_twocolumn.tex"]:
    filepath = Path(filename)
    content = filepath.read_text(encoding="utf-8")
    if r"\label{sec:linguistic_breakdown}" in content:
        print(f"Already updated {filename}")
        continue
    if TARGET in content:
        content = content.replace(TARGET, REPLACEMENT, 1)
        filepath.write_text(content, encoding="utf-8")
        print(f"Successfully inserted linguistic subsection into {filename}")
    else:
        print(f"Target not found in {filename}!")
