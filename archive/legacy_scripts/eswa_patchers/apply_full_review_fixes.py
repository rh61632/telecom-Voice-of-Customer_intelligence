import os
import re

def update_manuscript(filepath):
    print(f"Applying comprehensive peer-review fixes to {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Abstract
    old_abstract_pattern = re.compile(r'\\begin\{abstract\}.*?\\end\{abstract\}', re.DOTALL)
    new_abstract = r"""\begin{abstract}
Monitoring service delivery and diagnosing customer dissatisfaction in telecommunications is severely hindered by the semantic complexity of unstructured digital feedback. Traditional retrospective surveys fail to capture real-time application degradation, while low-resource and code-mixed vernacular languages—such as Bengali and Banglish—challenge conventional natural language processing pipelines. This paper presents an intelligent decision support system designed to decouple customer-facing software application defects from underlying telecommunications network and commercial operations. The system integrates an end-to-end multi-lingual text mining architecture combining sub-word n-gram representations with a calibrated soft-voting ensemble comprising Support Vector Classifiers, Balanced Logistic Regression, and Complement Naive Bayes. Benchmarked across eight architectures on 655,649 longitudinal customer reviews from Bangladesh's three leading mobile network operators over a ten-year horizon (2016--2026), the proposed ensemble achieves 87.47\% sentiment and 87.44\% category cross-validation accuracy, aligning closely with independent double-blind human consensus ratings (94.12\% category, 87.91\% sentiment) while delivering an operational throughput of 450 reviews/second on CPU hardware. We formalize an executive priority matrix and an adaptive canary release gating protocol. Empirical findings indicate that within self-care application feedback, software defects exhibit an odds ratio of $\text{OR} = 4.23$ ($95\%$ CI: $[1.78, 10.51]$; Yates-corrected $\chi^2(1) = 11.55, p = 0.0007$; relative risk $\text{RR} = 1.74$) of heading acute sentiment shocks compared to non-software categories. This enterprise framework bridges linguistic mining with operational triage, enabling data-driven telecommunications service management.
\end{abstract}"""
    content = old_abstract_pattern.sub(lambda m: new_abstract, content)

    # 2. Fix Introduction Claims & Buzzwords
    content = content.replace("directly invalidates the prevailing assumption", "empirically challenges the common operational assumption")
    content = content.replace("proves that client-side software defects are 4.23 times more likely to trigger acute sentiment crises than core physical network outages", "indicates that within digital self-care telemetry, client-side software defects exhibit an odds ratio of $\\text{OR} = 4.23$ (relative risk $\\text{RR} = 1.74$, $p = 0.0007$) of heading acute sentiment shocks compared to non-software categories")
    content = content.replace("represents the largest longitudinal telecom text dataset compiled in South Asia", "represents a substantial longitudinal telecom text dataset spanning a decade of consumer feedback")
    content = content.replace("This research establishes a paradigm shift", "This research introduces a systematic diagnostic framework")
    content = content.replace("registered an astonishing 136.5-point turnaround", "demonstrated a substantial turnaround")

    # 3. Fix Section 4.1: Seed Dataset Annotation (Qwen-2.5-32B via Groq) & Checkpoint
    old_seed_text = r"Labels were generated via structured domain-expert prompt chains on high-throughput cloud inference engines and manually verified for code-mixed semantic integrity."
    new_seed_text = r"Initial bootstrap labels for the seed corpus were generated using Qwen-2.5-32B \citep{qwen2024} via the Groq high-throughput LPU inference API under a zero-shot structured JSON schema enforcing mutually exclusive category assignment, sentiment polarity, and English translation. To eliminate model bias and guarantee zero data leakage, all downstream evaluations were benchmarked against an independent double-blind human gold standard ($N = 300$)."
    content = content.replace(old_seed_text, new_seed_text)

    # Fix BUET BanglaBERT checkpoint: csebuetnlp/banglabert
    content = content.replace("sagorsarker/banglabert", "csebuetnlp/banglabert")

    # 4. Fix Section 4.2: Consensus subset numbers and exact fractions
    old_consensus_text = r"On the consensus subset where both judges reached full agreement ($N = 261$), the production ensemble achieved $94.12\%$ category agreement and $87.91\%$ sentiment agreement, confirming robust alignment with human cognitive truth."
    new_consensus_text = r"Inter-annotator agreement between the two independent human judges across the verification cohort yielded a raw observed agreement of 95.41\% ($\kappa = 0.7694$) for Operational Categories across $N = 196$ overlapping pairs, and 91.00\% ($\kappa = 0.5762$) for Sentiment Polarity across $N = 200$ overlapping pairs. On the consensus subsets where both human judges reached unanimous agreement ($N = 187$ for Category, $N = 182$ for Sentiment), the production Soft-Voting Ensemble achieved 94.12\% category agreement ($176/187$) and 87.91\% sentiment agreement ($160/182$), confirming robust empirical alignment with human ground truth."
    content = content.replace(old_consensus_text, new_consensus_text)

    # Fix Table 3 table note on consensus
    old_tab3_note = r"On consensus reviews where both human judges agreed ($N = 261$), the Production Soft-Voting Ensemble achieved 94.12\% agreement on Category and 87.91\% on Sentiment."
    new_tab3_note = r"On consensus reviews where both human judges agreed ($N = 187$ for Category, $N = 182$ for Sentiment), the Production Soft-Voting Ensemble achieved 94.12\% agreement ($176/187$) on Category and 87.91\% on Sentiment ($160/182$)."
    content = content.replace(old_tab3_note, new_tab3_note)

    # Fix Section 4.4 error analysis N = 261
    content = content.replace("the double-blind human consensus benchmark ($N = 261$)", "the double-blind human consensus benchmark ($N = 187$ category, $N = 182$ sentiment)")

    # 5. Fix Table 5: Decade-Long Annual Net Sentiment Score (NSS) Trajectories
    old_tab5_pattern = re.compile(r'\\begin\{table\*?\}.*?\\label\{tab:eras\}.*?\\end\{table\*?\}', re.DOTALL)
    new_tab5 = r"""\begin{table*}[t]
\centering
\caption{Decade-Long Annual Net Sentiment Score (NSS) Trajectories by Era and Operator}
\label{tab:eras}
\footnotesize
\setlength{\tabcolsep}{8pt}
\begin{tabularx}{\textwidth}{@{}lccccX@{}}
\toprule
Operational Era & Calendar Window & Grameenphone & Robi Axiata & Banglalink & Dominant Operational Dynamic \\
\midrule
\textbf{Era 1: Early Adoption} & 2016--2017 & $+8.0$ & $-54.3$ & $+45.9$ & Early digital self-care rollout; high Robi friction vs.\ stable BL launch \\
\textbf{Era 2: 4G Transition} & 2018--2020 & $+16.4$ & $+17.1$ & $+26.1$ & Tariff restructuring dip in 2018; massive lockdown volume surge in 2020 \\
\textbf{Era 3: Post-Pandemic} & 2021--2022 & $+62.6$ & $+66.1$ & $+51.1$ & Sustained high digital engagement; mature 4G data adoption \\
\textbf{Era 4: SuperApp Divergence} & 2023--2026 & $+66.9$ & $+67.8$ & $+61.4$ & SuperApp pivots, gamified rewards, and regulatory tariff realignments \\
\midrule
\textit{Yearly Breakdown:} & & & & & \\
2016 (Jul--Dec) & 6 Months & $+2.5$ & $-57.9$ & $+46.3$ & Early launch; initial Robi login/stability challenges \\
2017 & Full Year & $+13.5$ & $-50.7$ & $+45.5$ & Stable BL satisfaction; gradual GP improvement \\
2018 & Full Year & $-16.0$ & $-28.8$ & $+22.3$ & Industry-wide 4G tariff restructuring friction \\
2019 & Full Year & $+19.6$ & $+16.4$ & $+17.8$ & Rebound across all operators; Robi turns positive \\
2020 & Full Year & $+45.7$ & $+63.6$ & $+38.3$ & Lockdown volume expansion (+616\% YoY review surge) \\
2021 & Full Year & $+61.0$ & $+63.8$ & $+46.6$ & Upward trajectory; mature 4G network adoption \\
2022 & Full Year & $+64.2$ & $+68.4$ & $+55.5$ & High stability across GP and Robi; BL expansion \\
2023 & Full Year & $+69.8$ & $+48.7$ & $+40.1$ & Robi auth glitch; BL splash crash \\
2024 & Full Year & $+70.6$ & $+66.0$ & $+57.2$ & GP peak volume (>75k reviews); BL hotfix recovery \\
2025 & Full Year & $+70.3$ & $+78.6$ & $+66.4$ & Robi historic peak; BL SuperApp expansion \\
2026 (through Sep 30) & 9 Months & $+56.8$ & $+76.2$ & \textbf{+81.9} & BL gamified turnaround; GP tariff pushback \\
\bottomrule
\end{tabularx}
\vspace{0.4em}
\parbox{\textwidth}{\footnotesize \textit{Notes:} Yearly scores reflect exact annual aggregations from the common duration corpus ($N = 655{,}649$). Era averages represent the volume-weighted mean Net Sentiment Scores across the designated calendar windows.}
\end{table*}"""
    content = old_tab5_pattern.sub(lambda m: new_tab5, content)

    # Fix narrative in Section 5.1 around Era 1
    content = content.replace("Era 1: Early Parity (2016--2017): Characterized by widespread consumer frustration with first-generation self-care applications across all three operators (GP $-53.2$, Robi $-57.9$, Banglalink $-55.8$)",
                            "Era 1: Early Adoption (2016--2017): Characterized by diverging early self-care experiences across operators; while Robi experienced severe initial stability challenges ($-54.3$ average), Banglalink launched with a positive initial reception ($+45.9$ average) and Grameenphone demonstrated gradual baseline growth ($+8.0$)")

    # 6. Fix Section 5.2: Statistical Formalization of Chi-Square, Odds Ratio, and Relative Risk
    sec52_old = r"""Across the 240 operator-month transitions in the modern era (2020--2026), exactly 35 transitions satisfied the acute shock criterion ($|\Delta\text{NSS}| \ge 10.0$ points): 6 for Grameenphone, 7 for Robi, and 22 for Banglalink. Table~\ref{tab:shocks} decomposes ten prominent modern sentiment shocks across operators."""
    sec52_new = r"""Across the 240 operator-month transitions in the modern era (2020--2026), exactly 35 transitions satisfied the acute shock criterion ($|\Delta\text{NSS}| \ge 10.0$ points): 6 for Grameenphone, 7 for Robi, and 22 for Banglalink. We examine whether acute shocks are disproportionately associated with client-side application engineering failures (App Login \& Technical Bugs) compared to non-software categories (Offers, Network, Billing, and General).

Among the 35 acute shock transitions, 27 ($77.1\%$) were primarily led by App Login defects, whereas among the 205 non-shock monthly transitions, App Login was the primary driver in only 91 transitions ($44.4\%$). Constructing a $2 \times 2$ contingency matrix yields an Odds Ratio of:
\begin{equation}
\text{OR} = \frac{27 \times 114}{8 \times 91} = \mathbf{4.23} \quad (95\% \text{ CI: } [1.78, 10.51], \ p = 0.0003)
\end{equation}
The corresponding Relative Risk is $\text{RR} = (27/35) / (91/205) = \mathbf{1.74}$ ($95\%$ CI: $[1.34, 2.25]$), indicating that acute sentiment shocks in self-care feedback are 1.74 times more likely to be led by application software defects than non-software issues. A Pearson contingency test confirms strong statistical association ($\chi^2(1) = 12.83, p = 0.0003$), remaining highly significant under Yates' continuity correction ($\chi^2(1) = 11.55, p = 0.0007$). 

This empirical finding indicates that acute customer sentiment crises in digital self-care channels are predominantly led by frontend client-side application build defects rather than core physical network latency or commercial pricing shifts. Table~\ref{tab:shocks} decomposes ten prominent modern sentiment shocks across operators."""
    
    if sec52_old in content:
        content = content.replace(sec52_old, sec52_new)
        print("Updated Section 5.2 contingency text.")

    # Fix Section 5.4 Case Study 1 Banglalink 2024 shock numbers
    old_cs1_text = r"In March 2024, Banglalink deployed application build version v11.8.0 of \textit{MyBL}. Immediately following release, login failure complaints escalated from a baseline of 1.2% to 14.8%, triggering a -32.8 point drop in NSS in May 2024. The deployment of an emergency hotfix (v11.9.1) in June 2024 immediately reversed the crisis (+32.8 points)."
    new_cs1_text = r"In March 2024, Banglalink deployed application build version v11.8.0 of \textit{MyBL}. Following release, login failure complaints escalated from a historical baseline below 2\% to 14.8\%, triggering an acute sentiment shock of $\Delta\text{NSS} = -11.18$ points (dropping from $+42.82$ in March to $+31.63$ in April 2024), with App Login contributing $-8.74$ percentage points of the net decline. Following the deployment of an emergency hotfix (v11.9.1), customer sentiment experienced a major rebound in May 2024 ($\Delta\text{NSS} = +32.78$ points, jumping to $+64.42$), with App Login defect resolution driving $+13.73$ percentage points of the recovery."
    content = content.replace(old_cs1_text, new_cs1_text)

    # 7. Fix Table 6 Banglalink numbers
    content = content.replace(r"Banglalink & 2024-05 & $-32.8$ & \textbf{-18.7} & $-1.8$ & $-1.4$ & $-0.5$ & $-10.4$ & App Login & \textit{MyBL} v11.8.0 splash screen crash loop \\",
                            r"Banglalink & 2024-04 & $-11.2$ & \textbf{-8.7} & $+1.6$ & $+0.8$ & $+1.1$ & $-5.9$ & App Login & \textit{MyBL} v11.8.0 splash crash and auth failure \\")
    content = content.replace(r"Banglalink & 2024-06 & $+32.8$ & \textbf{+17.8} & $+1.6$ & $+1.2$ & $+0.4$ & $+11.8$ & App Login & Hotfix v11.9.1 rapid rollback and patch \\",
                            r"Banglalink & 2024-05 & $+32.8$ & \textbf{+13.7} & $+1.0$ & $+0.4$ & $+0.3$ & $+17.4$ & App Login & Emergency hotfix v11.9.1 recovery \\")

    # 8. Fix Section 6.1: Realistic Canary Gating Window & Role
    old_canary_intro = r"To operationalize Decision Rule 3 within modern continuous integration and continuous deployment (CI/CD) pipelines, we formalize the diagnostic workflow in Table~\ref{tab:canary_algorithm} as \textbf{Algorithm 1}. By continuously evaluating incoming customer reviews during the critical initial phased rollout window (e.g., first 5\% of active subscribers), the expert system establishes an automated early-warning circuit breaker that isolates client-side build crashes before widespread customer churn can manifest."
    new_canary_intro = r"To operationalize Decision Rule 3 within modern continuous integration and continuous deployment (CI/CD) pipelines, we formalize the diagnostic workflow in Table~\ref{tab:canary_algorithm} as \textbf{Algorithm 1}. Rather than replacing real-time Application Performance Monitoring (APM) tools such as Firebase Crashlytics, the expert system operates as a complementary semantic diagnostic layer that uncovers qualitative root causes directly from user language. For high-velocity release rollouts (or scaled over an adaptive observation window of $W \in [30, 100]$ reviews), the system monitors incoming review streams to detect statistically significant defect surges ($p < 0.01$) before market-wide customer dissatisfaction solidifies."
    content = content.replace(old_canary_intro, new_canary_intro)
    content = content.replace("Canary observation window $W = 500$ reviews;", "Canary observation window $W \\in [30, 100]$ reviews;")

    # 9. Fix Section 7.2 Threats to Validity: Yates correction & selection bias
    old_concl_val = r"The statistical significance of software defect dominance ($\chi^2(1) = 12.83, p = 0.0003$) was verified under Yates' continuity correction. Model benchmarking was executed across 5-fold stratified cross-validation alongside independent out-of-sample holdout test sets, confirming high statistical power."
    new_concl_val = r"The statistical association between App Login defects and acute sentiment shocks was evaluated using both uncorrected Pearson $\chi^2(1) = 12.83$ ($p = 0.0003$, $\text{OR} = 4.23$) and Yates' continuity-corrected $\chi^2(1) = 11.55$ ($p = 0.0007$, $\text{RR} = 1.74$). We explicitly emphasize that these statistics reflect associations within self-care app store telemetry; they do not imply physical causal dominance over nationwide telecommunications infrastructure."
    content = content.replace(old_concl_val, new_concl_val)

    # 10. Fix Section 8 Conclusion wording
    content = content.replace(r"Empirical findings provide rigorous statistical proof ($\chi^2(1) = 12.83, p = 0.0003; \text{OR} = 4.23$) that mobile software build crashes are over four times more likely to induce severe sentiment crises than physical network outages.",
                            r"Empirical findings indicate that within customer self-care feedback channels, mobile software build defects exhibit an odds ratio of $\text{OR} = 4.23$ ($p = 0.0003$; Yates-corrected $\chi^2(1) = 11.55, p = 0.0007$; relative risk $\text{RR} = 1.74$) of heading acute sentiment shocks compared to non-software categories.")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully updated {filepath}.")

if __name__ == '__main__':
    update_manuscript('paper/eswa_latex/manuscript.tex')
    update_manuscript('paper/eswa_latex/manuscript_twocolumn.tex')
