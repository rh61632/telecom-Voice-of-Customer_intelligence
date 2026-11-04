import re

tex_path = 'paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex'

with open(tex_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Section 3.2: SVM shock counts
target_sec32 = "and modern shock counts (34 under linear SVM vs.\\ 35 under ensemble) remain essentially identical"
repl_sec32 = "and modern shock counts (32 under linear SVM strictly $\\ge 10.0$, or 34 when rounding to one decimal place, vs.\\ 35 under ensemble) remain essentially identical"
assert target_sec32 in text, "Target sec 3.2 not found!"
text = text.replace(target_sec32, repl_sec32)

# 2. Section 3.5: General / Other median share 76.4% -> 62.9%
target_sec35 = "its contribution shift absorbs a median of 76.4\\% of raw monthly NSS movement (leading the unconstrained 5-class decomposition in 33 of 35 shocks)."
repl_sec35 = "its contribution shift absorbs a median of 62.9\\% of raw monthly NSS movement (leading the unconstrained 5-class decomposition in 33 of 35 shocks, while the four functional domains together account for a median of 37.1\\%)."
assert target_sec35 in text, "Target sec 3.5 not found!"
text = text.replace(target_sec35, repl_sec35)

# 3. Section 4.4: text for Table 7
target_sec44 = "In March 2024 ($N = 1{,}093$, NSS = $+42.8$), build v11.7.1 recorded $+40.8$ NSS. In April 2024 ($N = 1{,}315$, NSS = $+31.6$, $\\Delta\\text{NSS} = -11.2$), the newly deployed build v11.8.0 recorded a negative NSS of $-7.6$ [95\\% CI $-22.7$, $+7.5$] across $n = 158$ reviews, characterized by app launch freezing and authentication crashes. Counterfactually replacing the v11.8.0 cohort with the balance of April's reviews (NSS $\\approx +37.0$) raises monthly NSS by 5.36 points, indicating that roughly half of April's 11.2-point decline is traceable to the identifiable v11.8.0 cohort, while the remainder sits in the unversioned majority (which fell to $+35.3$). In May 2024 ($N = 2{,}265$, NSS = $+64.4$, $\\Delta\\text{NSS} = +32.8$), public Google Play release notes for hotfix build v11.9.1 explicitly documented fixes for launch freezing and OTP authentication. However, the telemetry contradicts attributing the entire 32.8-point May surge to the hotfix: the identical build v11.9.1 scored only $+40.5$ [29.5, 51.5] during its initial rollout in late April, non-overlapping with its May score (+77.0 [72.8, 81.2]). Furthermore, control cohorts unexposed to the hotfix moved in parallel: legacy versions rose from $+42.7$ to $+60.2$, and unversioned reviews jumped from $+35.3$ to $+62.3$, accompanied by a 72.2\\% review volume surge ($1{,}315 \\to 2{,}265$)."

repl_sec44 = "In March 2024 ($N = 1{,}093$, NSS = $+42.8$), build v11.7.1 recorded $+42.9$ NSS. In April 2024 ($N = 1{,}315$, NSS = $+31.6$, $\\Delta\\text{NSS} = -11.2$), the newly deployed build v11.8.0 recorded a negative NSS of $-7.6$ [95\\% CI $-22.3$, $+7.1$] across $n = 158$ reviews, characterized by app launch freezing and authentication crashes. Counterfactually replacing the v11.8.0 cohort with the balance of April's reviews (NSS $\\approx +37.0$) raises monthly NSS by 5.36 points, indicating that roughly half of April's 11.2-point decline is traceable to the identifiable v11.8.0 cohort, while the remainder sits in the unversioned majority (which fell to $+35.3$). In May 2024 ($N = 2{,}265$, NSS = $+64.4$, $\\Delta\\text{NSS} = +32.8$), public Google Play release notes for hotfix build v11.9.1 explicitly documented fixes for launch freezing and OTP authentication. However, the telemetry contradicts attributing the entire 32.8-point May surge to the hotfix: the identical build v11.9.1 scored only $+40.5$ [25.5, 55.5] during its initial rollout in late April, non-overlapping with its May score (+77.0 [72.9, 81.0]). Furthermore, control cohorts unexposed to the hotfix moved in parallel: legacy versions rose from $+42.7$ to $+56.8$, and unversioned reviews jumped from $+35.3$ to $+62.3$, accompanied by a 72.2\\% review volume surge ($1{,}315 \\to 2{,}265$)."

assert target_sec44 in text, "Target sec 4.4 not found!"
text = text.replace(target_sec44, repl_sec44)

# 4. Table 7 contents
target_tab7 = r"""\begin{tabular}{llrrrr}
\toprule
\textbf{Month} & \textbf{Build Version} & \textbf{$n$} & \textbf{Share} & \textbf{NSS [95\% CI]} & \textbf{Operational Context} \\
\midrule
2024-03 & v11.7.1 & 170 & 15.6\% & +40.8 [33.4, 48.2] & Pre-crisis stable baseline \\
& Other versions & 205 & 18.7\% & +47.3 [40.5, 54.1] & Legacy active versions \\
& Unversioned & 718 & 65.7\% & +42.6 [39.0, 46.2] & Unrecorded version string \\
\midrule
2024-04 & v11.8.0 & 158 & 12.0\% & $-$7.6 [$-$22.7, +7.5] & Crashing update (login freeze) \\
& v11.9.1 & 121 & 9.2\% & +40.5 [29.5, 51.5] & Early hotfix cohort (late April) \\
& Other versions & 185 & 14.1\% & +42.7 [35.6, 49.8] & Legacy versions \\
& Unversioned & 851 & 64.7\% & +35.3 [32.0, 38.6] & Unrecorded version string \\
\midrule
2024-05 & v11.9.1 & 708 & 31.3\% & +77.0 [72.8, 81.2] & Main hotfix; crash resolved \\
& v11.10.x & 122 & 5.4\% & +22.1 [12.9, 31.3] & Subsequent minor releases \\
& Other versions & 118 & 5.2\% & +60.2 [51.3, 69.1] & Legacy versions \\
& Unversioned & 1,317 & 58.1\% & +62.3 [59.6, 65.0] & Volume surge cohort \\
\bottomrule
\end{tabular}"""

repl_tab7 = r"""\begin{tabular}{llrrrr}
\toprule
\textbf{Month} & \textbf{Build Version} & \textbf{$n$} & \textbf{Share} & \textbf{NSS [95\% CI]} & \textbf{Operational Context} \\
\midrule
2024-03 & v11.7.1 & 170 & 15.6\% & +42.9 [30.5, 55.4] & Pre-crisis stable baseline \\
& Other versions & 205 & 18.8\% & +42.0 [31.2, 52.7] & Legacy active versions \\
& Unversioned & 718 & 65.7\% & +43.0 [37.0, 49.0] & Unrecorded version string \\
\midrule
2024-04 & v11.8.0 & 158 & 12.0\% & $-$7.6 [$-$22.3, +7.1] & Crashing update (login freeze) \\
& v11.9.1 & 121 & 9.2\% & +40.5 [25.5, 55.5] & Early hotfix cohort (late April) \\
& Other versions & 185 & 14.1\% & +42.7 [31.2, 54.2] & Legacy versions \\
& Unversioned & 851 & 64.7\% & +35.3 [29.4, 41.1] & Unrecorded version string \\
\midrule
2024-05 & v11.9.1 & 708 & 31.3\% & +77.0 [72.9, 81.0] & Main hotfix; crash resolved \\
& v11.10.x & 122 & 5.4\% & +22.1 [6.1, 38.2] & Subsequent minor releases \\
& Other versions & 118 & 5.2\% & +56.8 [42.7, 70.8] & Legacy versions \\
& Unversioned & 1,317 & 58.1\% & +62.3 [58.4, 66.1] & Volume surge cohort \\
\bottomrule
\end{tabular}"""

assert target_tab7 in text, "Target Tab 7 not found!"
text = text.replace(target_tab7, repl_tab7)

# 5. References order: swap Tirunillai and The Business Standard
target_refs = r"""\vspace{0.6em}\noindent Tirunillai, S., \& Tellis, G. J. (2014). Mining marketing meaning from online chatter: Strategic brand analysis of big data using latent Dirichlet allocation. \textit{Journal of Marketing Research}, \textit{51}(4), 463--479. \url{https://doi.org/10.1509/jmr.12.0106}

\vspace{0.6em}\noindent The Business Standard. (2025, September 1). Grameenphone, Robi launch commercial 5G services in Bangladesh. \textit{The Business Standard}. \url{https://www.tbsnews.net/bangladesh/telecom/gp-robi-launch-commercial-5g-services-bangladesh}"""

repl_refs = r"""\vspace{0.6em}\noindent The Business Standard. (2025, September 1). Grameenphone, Robi launch commercial 5G services in Bangladesh. \textit{The Business Standard}. \url{https://www.tbsnews.net/bangladesh/telecom/gp-robi-launch-commercial-5g-services-bangladesh}

\vspace{0.6em}\noindent Tirunillai, S., \& Tellis, G. J. (2014). Mining marketing meaning from online chatter: Strategic brand analysis of big data using latent Dirichlet allocation. \textit{Journal of Marketing Research}, \textit{51}(4), 463--479. \url{https://doi.org/10.1509/jmr.12.0106}"""

assert target_refs in text, "Target refs not found!"
text = text.replace(target_refs, repl_refs)

with open(tex_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("All fixes applied successfully to LaTeX source!")

