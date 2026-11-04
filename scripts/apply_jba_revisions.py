"""
apply_jba_revisions.py
Applies all 10 peer-review revisions directly to
Telecom_VoC_Intelligence_JBA_Manuscript.tex using lambda replacements.
"""

from pathlib import Path
import re

TEX_PATH = Path("paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex")
with open(TEX_PATH, "r", encoding="utf-8") as f:
    text = f.read()

def safe_replace_regex(pattern, replacement, content):
    m = re.search(pattern, content)
    if not m:
        raise ValueError(f"Pattern not found: {pattern[:40]}")
    return content[:m.start()] + replacement + content[m.end():]

# 1. Abstract
t_old_abs = "App-login and technical-bug problems are the leading single driver in seven of ten major sentiment shocks, though usually explaining a minority of the shift."
t_new_abs = "App-login and technical-bug problems are the leading single operational driver in 27 of 35 modern sentiment shocks (77.1%), though typically explaining a minority of the shift (median operational share: 23.6%)."
assert t_old_abs in text, "old_abs not found"
text = text.replace(t_old_abs, t_new_abs)

# 2. Section 3.2: Gold set level bias and BanglaBERT
p_sec32 = r"We therefore treat classifier error as a material limitation and conducted an extensive sensitivity analysis.*?\n"
t_new_sec32 = (
    "On the 300-review gold standard, evaluating level bias reveals that the production ensemble exhibits a modest negative "
    "bias of -2.92 percentage points relative to human consensus (Model NSS 82.50% vs.\\ Human 85.42%), compared to -4.17 points "
    "for the linear SVM and -3.33 points for logistic regression. Fine-tuning BUET BanglaBERT (Bhattacharjee et al., 2022) "
    "achieved 89.78% sentiment accuracy (Macro $F_1 = 0.832$) and 87.11% category accuracy (Macro $F_1 = 0.802$). We treat classifier "
    "error as a material limitation and conducted sensitivity analyses recomputing longitudinal metrics with the challenger linear SVM. "
    "Across the modern era, resulting RMSSD values (Grameenphone: 6.24 vs.\\ 6.28 ensemble; Robi: 5.43 vs.\\ 5.61 ensemble; "
    "Banglalink: 13.76 vs.\\ 13.61 ensemble) and modern shock counts (34 under linear SVM vs.\\ 35 under ensemble) remain essentially "
    "identical, confirming that operator volatility rankings and shock attributions are robust to classifier specification.\n"
)
text = safe_replace_regex(p_sec32, t_new_sec32, text)

# 3. Section 3.5: Operational movement definition and shock count reconciliation
p_sec35 = r"A shift with \$\|\\Delta\\text\{NSS\}\| \\ge 10\.0\$ points defines a Significant Shock.*?\n"
t_new_sec35 = (
    "We define operational movement as the shift attributable to the four actionable, functional domains "
    "($\\mathcal{C}_{\\text{actionable}} = \\{\\text{App Login}, \\text{Billing}, \\text{Network}, \\text{Offers}\\}$), "
    "separating functional departmental complaints from unspecific baseline sentiment drift captured by General / Other. "
    "Because General / Other accounts for 83.1\\%--87.9\\% of all reviews, its contribution shift absorbs a median of 76.4\\% "
    "of raw monthly NSS movement (leading the unconstrained 5-class decomposition in 33 of 35 shocks). We focus on actionable "
    "operational domains because management cannot intervene on non-specific commentary. A shift with $|\\Delta\\text{NSS}| \\ge 10.0$ "
    "points defines a Significant Shock. Across the 80 monthly transitions per operator in the modern era ($3 \\times 80 = 240$ transitions), "
    "exactly 35 meet this criterion: 6 for Grameenphone, 7 for Robi, and 22 for Banglalink. (A 37-shock variant arose in earlier drafts "
    "by including the boundary transition from December 2019 into January 2020). Across the full 10-year window, 98 transitions meet "
    "this threshold; however, early-era months near the $n \\ge 30$ CLT floor carry standard errors of approximately 13 percentage "
    "points, so early shocks reflect substantial sampling noise. The modern 35 shocks provide our basis for inference.\n"
)
text = safe_replace_regex(p_sec35, t_new_sec35, text)

# 4. Section 4.1: 5G commercial launch citation
p_5g = r"Commercial 5G launched on September 1, 2025.*?\n"
t_new_5g = "Commercial 5G launched on September 1, 2025 (Grameenphone in all divisional headquarters; Robi in parts of Dhaka, Chattogram and Sylhet) (The Business Standard, 2025; BTRC, 2025).\n"
text = safe_replace_regex(p_5g, t_new_5g, text)

# 5. Section 4.3: Volatility, Bootstrap & Volume Diagnostic
p_sec43 = r"Stationary block bootstrap 95\\% confidence intervals confirm.*?\n"
t_new_sec43 = (
    "Stationary block bootstrap confidence intervals ($B = 10{,}000$, average block length $b = 4$ transitions; "
    "Politis \\& Romano, 1994) confirm: Grameenphone RMSSD = 6.28 [95\\% CI 4.33, 7.93], Robi RMSSD = 5.61 [3.88, 7.16], "
    "and Banglalink RMSSD = 13.61 [8.53, 18.77]. The Banglalink/Robi ratio is 2.43 [1.45, 4.01] (bootstrap $p = 0.0008$) "
    "and the Banglalink/Grameenphone ratio is 2.17 [1.33, 3.59] ($p = 0.0013$), both strictly excluding unity. Because "
    "Grameenphone and Robi intervals overlap substantially (ratio 1.12 [0.72, 1.71], $p = 0.3416$), we do not assert a "
    "meaningful volatility ranking between those two operators. Monte Carlo downsampling downsamples Grameenphone and Robi "
    "monthly reviews to Banglalink's exact monthly review counts across 1,000 runs, yielding downsampled mean RMSSD values "
    "of 6.71 [6.22, 7.32] for Grameenphone and 5.91 [5.48, 6.40] for Robi, demonstrating that Banglalink's higher volatility "
    "is not an artifact of review count differences.\n\n"
    "To diagnose potential confounding from review volume surges, we regressed $\\Delta\\text{NSS}$ on $\\Delta\\ln(\\text{Volume})$ "
    "across all 80 transitions for each operator. Review volume changes strongly couple with sentiment for Banglalink "
    "($\\beta = 17.46, \\text{SE} = 1.90, t = 9.21, p < 0.0001, R^2 = 0.521$) and Grameenphone ($\\beta = 8.55, \\text{SE} = 1.71, "
    "t = 5.01, p < 0.0001, R^2 = 0.243$), whereas Robi's sentiment shifts are uncoupled from volume fluctuations "
    "($\\beta = 2.34, \\text{SE} = 1.73, t = 1.35, p = 0.181, R^2 = 0.023$). Without the two Spring 2024 transitions "
    "(April--May 2024), Banglalink's RMSSD decreases only from 13.61 to 13.21 points (78 transitions), preserving its $>2\\times$ "
    "divergence. Excluding all transitions with $>50\\%$ volume changes yields an RMSSD of 7.55 points. We therefore interpret "
    "Banglalink's volatility not as purely an operational divergence, but as an interplay between release instability and "
    "review-volume sensitivity.\n"
)
text = safe_replace_regex(p_sec43, t_new_sec43, text)

# 6. Section 4.4 Shocks intro
p_sec44_intro = r"Across all 35 modern shocks, when isolating operational complaints.*?\n"
t_new_sec44_intro = (
    "Across all 35 modern shocks, App Login \\& Technical Bugs accounts for the primary operational movement in 77.1\\% "
    "of shocks (27 of 35), 86.7\\% of drops (13 of 15), and 70.0\\% of rises (14 of 20), with a median operational "
    "contribution share of 23.6\\% (and 34\\% among the ten major shocks). As a null comparison for Proposition 2, in the "
    "205 non-shock modern transitions, App Login leads in only 46.8\\% (96 of 205), followed by Offers (31.2\\%, $n=64$), "
    "Network (17.1\\%, $n=35$), and Billing (4.9\\%, $n=10$). A chi-square test confirms that App Login is significantly "
    "more dominant during shocks than during non-shock months ($\\chi^2(1) = 10.95, p = 0.0009$), providing strong empirical "
    "support for Proposition 2. Large shocks remain multi-domain events where technical issues trigger secondary complaints "
    "in offers and billing.\n"
)
text = safe_replace_regex(p_sec44_intro, t_new_sec44_intro, text)

# 7. Table 6 footnote and row
t_old_row = "Banglalink & 2024-04 $\\to$ 05 & +32.8 & App Login \\& Bugs & +13.73 & 42\\% \\\\"
t_new_row = "Banglalink & 2024-04 $\\to$ 05\\textsuperscript{b} & +32.8 & App Login \\& Bugs & +13.73 & 42\\% \\\\"
assert t_old_row in text, "old_row not found"
text = text.replace(t_old_row, t_new_row)

p_tab6_note = r"These ten are a selection of major shocks, not the full set of 37\..*?\n"
t_new_tab6_note = (
    "These ten are a selection of major modern shocks, not the full set of 35. "
    "\\textsuperscript{b}Confounded: hotfix build v11.9.1 co-occurred with a 72.2\\% review volume surge "
    "($N = 1{,}315 \\to 2{,}265$), lifting baseline sentiment beyond pre-crisis levels.\n"
)
text = safe_replace_regex(p_tab6_note, t_new_tab6_note, text)

# 8. Section 4.4 text cases & Table 7
p_cases = r"Three cases illustrate what the decomposition can and cannot show.*?\n"
t_new_cases = (
    "Three cases illustrate what the decomposition can and cannot show. Banglalink's March--April 2024 fall is the cleanest: "
    "about 78\\% of the 11.2-point drop sits in app-login and bug sentiment, directly matching release telemetry. "
    "In March 2024 ($N = 1{,}093$, NSS = $+42.8$), build v11.7.1 recorded $+40.8$ NSS (Table~\\ref{tab:versions}). "
    "In April 2024 ($N = 1{,}315$, NSS = $+31.6$), build v11.8.0 accounted for 34.1\\% of version-identified reviews ($n = 158$) "
    "and generated a deeply negative NSS of $-7.59$, driving the decline; however, only 35.3\\% of April reviews reported a version string. "
    "In May 2024 ($N = 2{,}265$, NSS = $+64.4$, $\\Delta\\text{NSS} = +32.8$), hotfix build v11.9.1 dominated versioned reviews "
    "(74.7\\%, $n = 708$) with an NSS of $+77.0$, about 34 points above the pre-crisis build v11.7.1. However, review volume also "
    "surged by 72.2\\% ($1{,}315 \\to 2{,}265$). While release notes confirm the launch crash fix, attributing volume growth to "
    "in-app review prompts is an inference, as prompt logging is internal; we therefore treat the May rebound as confounded by "
    "volume acceleration co-occurring with the hotfix. Grameenphone's September 2025 fall of 18.5 points is led by Offers ($-2.68$ pp, "
    "14\\% share) while General / Other absorbed $-13.1$ pp; this coincided with the commercial 5G rollout and consumer dissatisfaction "
    "with data pack tariffs. Finally, Banglalink's April--May 2021 fall is led by network sentiment, showing that Proposition 2 is not universal.\n\n"
    "\\begin{table}[htbp]\n"
    "\\centering\n"
    "\\begin{spacing}{1.0}\n"
    "\\caption{Banglalink App Build Version Telemetry, Spring 2024}\n"
    "\\label{tab:versions}\n"
    "\\small\n"
    "\\begin{tabular}{llrrrr}\n"
    "\\toprule\n"
    "\\textbf{Month} & \\textbf{Build Version} & \\textbf{$n$} & \\textbf{Share} & \\textbf{NSS [95\\% CI]} & \\textbf{Operational Context} \\\\\n"
    "\\midrule\n"
    "2024-03 & v11.7.1 & 170 & 15.6\\% & +40.8 [33.4, 48.2] & Pre-crisis stable baseline \\\\\n"
    "& Other versions & 205 & 18.7\\% & +47.3 [40.5, 54.1] & Legacy active versions \\\\\n"
    "& Unversioned & 718 & 65.7\\% & +42.6 [39.0, 46.2] & Unrecorded version string \\\\\n"
    "\\midrule\n"
    "2024-04 & v11.8.0 & 158 & 12.0\\% & $-$7.6 [$-$22.7, +7.5] & Crashing update (login freeze) \\\\\n"
    "& v11.9.1 & 121 & 9.2\\% & +40.5 [29.5, 51.5] & Early hotfix cohort (late April) \\\\\n"
    "& Other versions & 185 & 14.1\\% & +42.7 [35.6, 49.8] & Legacy versions \\\\\n"
    "& Unversioned & 851 & 64.7\\% & +35.3 [32.0, 38.6] & Unrecorded version string \\\\\n"
    "\\midrule\n"
    "2024-05 & v11.9.1 & 708 & 31.3\\% & +77.0 [72.8, 81.2] & Main hotfix; crash resolved \\\\\n"
    "& v11.10.x & 122 & 5.4\\% & +22.1 [12.9, 31.3] & Subsequent minor releases \\\\\n"
    "& Other versions & 118 & 5.2\\% & +60.2 [51.3, 69.1] & Legacy versions \\\\\n"
    "& Unversioned & 1,317 & 58.1\\% & +62.3 [59.6, 65.0] & Volume surge cohort \\\\\n"
    "\\bottomrule\n"
    "\\end{tabular}\n\n"
    "\\vspace{0.3em}\n"
    "\\raggedright\\footnotesize\\textit{Note:} Share of reviews within the month. Confidence intervals use normal approximation for NSS. Version strings are absent in 58--66\\% of reviews due to Play Store scraper recording constraints.\n"
    "\\end{spacing}\n"
    "\\end{table}\n"
)
text = safe_replace_regex(p_cases, t_new_cases, text)

# 9. Section 5.1
p_sec51 = r"Back-testing across the 37 modern shocks shows that a 1\.5-point rolling seven-day threshold.*?\n"
t_new_sec51 = (
    "While rolling contribution alerts provide timely operational signals, thresholds must be calibrated against review volume: "
    "at low daily volumes, sampling noise can trigger spurious warnings, whereas high-volume surges can mask localized operational friction.\n"
)
text = safe_replace_regex(p_sec51, t_new_sec51, text)

# 10. References DOIs and additions
p_gerpott = r"Gerpott, T\. J\..*?\n"
t_new_gerpott = "Gerpott, T. J., Rams, W., \\& Schindler, A. (2001). Customer retention, loyalty, and satisfaction in the German mobile cellular telecommunications market. \\textit{Telecommunications Policy}, \\textit{25}(4), 249--269. \\url{https://doi.org/10.1016/S0308-5961(00)00097-5}\n"
text = safe_replace_regex(p_gerpott, t_new_gerpott, text)

p_kim = r"Kim, M\.-K\..*?\n"
t_new_kim = "Kim, M.-K., Park, M.-C., \\& Jeong, D.-H. (2004). The effects of customer satisfaction and switching barrier on customer loyalty in Korean mobile telecommunication services. \\textit{Telecommunications Policy}, \\textit{28}(2), 145--159. \\url{https://doi.org/10.1016/j.telpol.2003.12.003}\n"
text = safe_replace_regex(p_kim, t_new_kim, text)

p_mittal = r"Mittal, V\..*?\n"
t_new_mittal = "Mittal, V., Ross, W. T., Jr., \\& Baldasare, P. M. (1998). The asymmetric impact of negative and positive attribute-level performance on overall satisfaction and repurchase intentions. \\textit{Journal of Marketing}, \\textit{62}(1), 33--47. \\url{https://doi.org/10.1177/002224299806200104}\n"
text = safe_replace_regex(p_mittal, t_new_mittal, text)

p_neumann = r"von Neumann, J\..*?\n"
t_new_neumann = (
    "Politis, D. N., \\& Romano, J. P. (1994). The stationary bootstrap. \\textit{Journal of the American Statistical Association}, \\textit{89}(428), 1303--1313. \\url{https://doi.org/10.1080/01621459.1994.10476870}\n\n"
    "\\vspace{0.6em}\\noindent The Business Standard. (2025, September 1). Grameenphone, Robi launch commercial 5G services in Bangladesh. \\textit{The Business Standard}. \\url{https://www.tbsnews.net/bangladesh/telecom/gp-robi-launch-commercial-5g-services-bangladesh}\n\n"
    "\\vspace{0.6em}\\noindent von Neumann, J., Kent, R. H., Bellinson, H. R., \\& Hart, B. I. (1941). The mean square successive difference. \\textit{The Annals of Mathematical Statistics}, \\textit{12}(2), 153--162. \\url{https://doi.org/10.1214/aoms/1177731746}\n"
)
text = safe_replace_regex(p_neumann, t_new_neumann, text)

p_btrc = r"BTRC\. \(2025\)\..*?\n"
t_new_btrc = "BTRC. (2025). \\textit{Mobile phone subscribers in Bangladesh (August 2025)}. Bangladesh Telecommunication Regulatory Commission. \\url{http://www.btrc.gov.bd/content/mobile-phone-subscribers-bangladesh-august-2025}\n"
text = safe_replace_regex(p_btrc, t_new_btrc, text)

with open(TEX_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("All 10 revisions successfully written to Telecom_VoC_Intelligence_JBA_Manuscript.tex!")
