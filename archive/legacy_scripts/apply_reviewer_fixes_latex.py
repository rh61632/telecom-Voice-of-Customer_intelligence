import re
from pathlib import Path

tex_path = Path("paper/journal_manuscript/Telecom_VoC_Intelligence_JBA_Manuscript.tex")
with open(tex_path, "r", encoding="utf-8") as f:
    text = f.read()

# -------------------------------------------------------------
# 1. ABSTRACT UPDATE
# -------------------------------------------------------------
old_abstract = r"""\noindent\textit{This study analyzes 655,670 Google Play reviews of the three largest Bangladeshi mobile operators' self-care apps (2016--2026) to measure customer-experience level and volatility. We combine the Net Sentiment Score (NSS), a successive-difference volatility measure, and an additive decomposition of monthly NSS shifts across five operational domains. Billing and app-login discussions are overwhelmingly negative, while offers are mixed. Banglalink is about 2.4 times more volatile month to month than Robi. App-login and technical-bug problems are the leading single operational driver in 27 of 35 modern sentiment shocks (77.1\%), though typically explaining a minority of the shift (median operational share: 23.6\%). The findings indicate that release instability matters for app-visible sentiment, but they cannot be read as evidence of churn. We outline monitoring, staged-release and reporting implications.}"""

new_abstract = r"""\noindent\textit{This study analyzes 655,670 Google Play reviews of the three largest Bangladeshi mobile operators' self-care apps (2016--2026) to measure customer-experience level and volatility. We combine the Net Sentiment Score (NSS), a successive-difference volatility measure, and an additive decomposition of monthly NSS shifts across five operational domains. Billing and app-login discussions are overwhelmingly negative, while offers are mixed. Banglalink exhibits higher unadjusted month-to-month volatility (RMSSD = 13.61) than Robi (5.61) and Grameenphone (6.28), but this gap narrows substantially (RMSSD = 7.56 vs.\ 4.53 and 5.15) when excluding volume-surge transitions, indicating that sentiment volatility reflects reviewer-mix fluctuations alongside operational shocks. Across 35 large monthly shocks, General / Other absorbs a median of 62.9\% of raw movement and tracks volume growth ($R^2 = 0.56$), while App Login leads among functional domains in 27 shocks (median operational share: 23.6\%). The findings indicate that release instability matters for app-visible sentiment, but they cannot be read as evidence of churn. We outline monitoring, staged-release and reporting implications.}"""

assert old_abstract in text, "old_abstract not found!"
text = text.replace(old_abstract, new_abstract)

# -------------------------------------------------------------
# 2. SECTION 3.1: Minimum volume sentence
# -------------------------------------------------------------
old_s31 = r"and the smallest monthly count per operator across this period is 294 reviews (Banglalink, August 2025; Robi minimum is 327; Grameenphone minimum is 734), ensuring that all monthly estimates rest on substantial sample sizes."

new_s31 = r"and the smallest monthly count per operator across this period is 294 reviews (Banglalink, August 2025; standard error $\approx 4.2$ points; Robi minimum is 327; Grameenphone minimum is 734), establishing an adequate empirical sample size while acknowledging that low-volume months carry wider confidence bands."

assert old_s31 in text, "old_s31 not found!"
text = text.replace(old_s31, new_s31)

# -------------------------------------------------------------
# 3. SECTION 3.2: Escape %, BanglaBERT evaluation sets, NSS bias
# -------------------------------------------------------------
old_s32_bert = r"A fine-tuned BanglaBERT model (Bhattacharjee et al., 2022) reached 91.60\% cross-validated sentiment accuracy and 85.27\% category accuracy; fine-tuning added 10.39 points of category accuracy over a frozen-encoder baseline (74.88\%)."

new_s32_bert = r"A fine-tuned BanglaBERT model (Bhattacharjee et al., 2022) reached 91.60\% cross-validated sentiment accuracy and 85.27\% category accuracy on the 4,500-review weakly supervised seed corpus (adding 10.39 points of category accuracy over a frozen-encoder baseline of 74.88\%)."

assert old_s32_bert in text, "old_s32_bert not found!"
text = text.replace(old_s32_bert, new_s32_bert)

old_s32_valid = r"""On the 300-review gold standard, evaluating level bias reveals that the production ensemble exhibits a modest negative bias of -2.92 percentage points relative to human consensus (Model NSS 82.50\% vs.\ Human 85.42\%), compared to -4.17 points for the linear SVM and -3.33 points for logistic regression. Fine-tuning BUET BanglaBERT (Bhattacharjee et al., 2022) achieved 89.78% sentiment accuracy (Macro $F_1 = 0.832$) and 87.11% category accuracy (Macro $F_1 = 0.802$). We treat classifier error as a material limitation and conducted sensitivity analyses recomputing longitudinal metrics with the challenger linear SVM. Across the modern era, resulting RMSSD values (Grameenphone: 6.24 vs.\ 6.28 ensemble; Robi: 5.43 vs.\ 5.61 ensemble; Banglalink: 13.76 vs.\ 13.61 ensemble) and modern shock counts (34 under linear SVM vs.\ 35 under ensemble) remain essentially identical, confirming that operator volatility rankings and shock attributions are robust to classifier specification."""

new_s32_valid = r"""On the gold standard ($n = 300$; and $n = 182$ on the human-consensus subset), evaluating level bias reveals that the production ensemble exhibits a negative bias of $-2.92$ percentage points relative to human annotations in the unweighted sample (Model NSS 82.50\% vs.\ Human 85.42\%, compared to $-4.17$ points for the linear SVM and $-3.33$ points for logistic regression). Because the gold set is stratified rather than representative of the corpus (sample NSS is $\approx 85\%$, versus $\approx 63\%$ in the 655,670-review corpus), this unweighted difference does not directly transfer to corpus-level NSS without post-stratification reweighting. When evaluated against the held-out human gold standard ($n = 300$), fine-tuned BanglaBERT achieved 89.78\% sentiment accuracy (Macro $F_1 = 0.832$) and 87.11\% category accuracy (Macro $F_1 = 0.802$). We treat classifier error as a material limitation and conducted sensitivity analyses recomputing longitudinal metrics with the challenger linear SVM. Across the modern era, resulting RMSSD values (Grameenphone: 6.24 vs.\ 6.28 ensemble; Robi: 5.43 vs.\ 5.61 ensemble; Banglalink: 13.76 vs.\ 13.61 ensemble) and modern shock counts (34 under linear SVM vs.\ 35 under ensemble) remain essentially identical, confirming that operator volatility rankings and shock attributions are robust to classifier specification."""

assert old_s32_valid in text, "old_s32_valid not found!"
text = text.replace(old_s32_valid, new_s32_valid)

# -------------------------------------------------------------
# 4. SECTION 3.5: Remove draft traces & flag 98 shocks
# -------------------------------------------------------------
old_s35 = r"""A shift with $|\Delta\text{NSS}| \ge 10.0$ points defines a Significant Shock. Across the 80 monthly transitions per operator in the modern era ($3 \times 80 = 240$ transitions), exactly 35 meet this criterion: 6 for Grameenphone, 7 for Robi, and 22 for Banglalink. (A 37-shock variant arose in earlier drafts by including the boundary transition from December 2019 into January 2020). Across the full 10-year window, 98 transitions meet this threshold; however, early-era months near the $n \ge 30$ CLT floor carry standard errors of approximately 13 percentage points, so early shocks reflect substantial sampling noise. The modern 35 shocks provide our basis for inference."""

new_s35 = r"""A shift with $|\Delta\text{NSS}| \ge 10.0$ points defines a Significant Shock. Across the 80 monthly transitions per operator in the modern era ($3 \times 80 = 240$ transitions), exactly 35 meet this criterion: 6 for Grameenphone, 7 for Robi, and 22 for Banglalink. Across the full 10-year common window, 98 transitions nominally meet this threshold; however, early-era months near the $n \ge 30$ CLT floor carry standard errors of approximately 13 percentage points, rendering early shocks noise-dominated. The 35 modern shocks provide our sole basis for empirical inference."""

assert old_s35 in text, "old_s35 not found!"
text = text.replace(old_s35, new_s35)

# -------------------------------------------------------------
# 5. SECTION 4.1: Restore 2026 results, Fig 1 reference, volume caution
# -------------------------------------------------------------
old_s41 = r"""Commercial 5G launched on September 1, 2025 (Grameenphone in all divisional headquarters; Robi in parts of Dhaka, Chattogram and Sylhet) (The Business Standard, 2025; BTRC, 2025)."""

new_s41 = r"""Commercial 5G launched on September 1, 2025 (Grameenphone in all divisional headquarters; Robi in parts of Dhaka, Chattogram and Sylhet) (The Business Standard, 2025; BTRC, 2025). By 2026 (January--September), Banglalink leads annual sentiment (+81.9), followed by Robi (+76.2) and Grameenphone (+56.8). Figure~\ref{fig:monthly} plots the monthly trajectories across all 81 modern-era months ($n \ge 30$). However, because review volume fluctuates sharply across years and operators (for example, Grameenphone peaks at 75,059 reviews in 2024 before receding, while Banglalink doubles its 2025 pace in early 2026), these aggregate level shifts must be read cautiously: shifts in review volume reflect changes in reviewer composition and in-app prompt intensity as well as underlying service quality."""

assert old_s41 in text, "old_s41 not found!"
text = text.replace(old_s41, new_s41)

# -------------------------------------------------------------
# 6. SECTION 4.3 & TABLE 5: Reframe headline, volume filter, CIs
# -------------------------------------------------------------
old_s43 = r"""Over the 81 months of the modern era (January 2020 to September 2026; $N = 634{,}992$), Banglalink has the highest month-to-month volatility (RMSSD = 13.61 points), compared with 5.61 for Robi and 6.28 for Grameenphone (Table~\ref{tab:stability}). Banglalink is therefore 2.4 times as volatile as Robi and 2.2 times as volatile as Grameenphone. Banglalink also has the lowest mean NSS (50.06), and it records 22 shocks in 80 transitions (27.5\%), against 7 (8.8\%) for Robi and 6 (7.5\%) for Grameenphone, with a median absolute monthly shift of 5.82 points (compared to 2.57 for Robi and 2.84 for Grameenphone). The interquartile range, however, does not follow RMSSD: Grameenphone has the tightest range (14.07), while Robi (18.08) and Banglalink (18.25) are almost identical, so the operators differ mainly in how quickly NSS moves from month to month, not in how widely it ranges. Volatility also coexists with strong outcomes: Banglalink's 2026 NSS ($+81.9$) is the highest of the three, so we do not interpret volatility as a marker of weak brand health. Stationary block bootstrap confidence intervals ($B = 10{,}000$, average block length $b = 4$ transitions; Politis \& Romano, 1994) confirm: Grameenphone RMSSD = 6.28 [95\% CI 4.33, 7.93], Robi RMSSD = 5.61 [3.88, 7.16], and Banglalink RMSSD = 13.61 [8.53, 18.77]. The Banglalink/Robi ratio is 2.43 [1.45, 4.01] (bootstrap $p = 0.0008$) and the Banglalink/Grameenphone ratio is 2.17 [1.33, 3.59] ($p = 0.0013$), both strictly excluding unity. Because Grameenphone and Robi intervals overlap substantially (ratio 1.12 [0.72, 1.71], $p = 0.3416$), we do not assert a meaningful volatility ranking between those two operators. Monte Carlo downsampling downsamples Grameenphone and Robi monthly reviews to Banglalink's exact monthly review counts across 1,000 runs, yielding downsampled mean RMSSD values of 6.71 [6.22, 7.32] for Grameenphone and 5.91 [5.48, 6.40] for Robi, demonstrating that Banglalink's higher volatility is not an artifact of review count differences.

To diagnose potential confounding from review volume surges, we regressed $\Delta\text{NSS}$ on $\Delta\ln(\text{Volume})$ across all 80 transitions for each operator. Review volume changes strongly couple with sentiment for Banglalink ($\beta = 17.46, \text{SE} = 1.90, t = 9.21, p < 0.0001, R^2 = 0.521$) and Grameenphone ($\beta = 8.55, \text{SE} = 1.71, t = 5.01, p < 0.0001, R^2 = 0.243$), whereas Robi's sentiment shifts are uncoupled from volume fluctuations ($\beta = 2.34, \text{SE} = 1.73, t = 1.35, p = 0.181, R^2 = 0.023$). Without the two Spring 2024 transitions (April--May 2024), Banglalink's RMSSD decreases only from 13.61 to 13.21 points (78 transitions), preserving its $>2\times$ divergence. Excluding all transitions with $>50\%$ volume changes yields an RMSSD of 7.55 points. We therefore interpret Banglalink's volatility not as purely an operational divergence, but as an interplay between release instability and review-volume sensitivity."""

new_s43 = r"""Over the 81 months of the modern era (January 2020 to September 2026; $N = 634{,}992$), Banglalink exhibits the highest unadjusted month-to-month volatility (RMSSD = 13.61 points), compared with 5.61 for Robi and 6.28 for Grameenphone (Table~\ref{tab:stability}). Banglalink also records 22 shocks in 80 transitions (27.5\%), against 7 (8.8\%) for Robi and 6 (7.5\%) for Grameenphone, with a median absolute monthly shift of 5.82 points (versus 2.57 for Robi and 2.84 for Grameenphone). The interquartile range, however, does not follow RMSSD: Grameenphone has the tightest range (14.07), while Robi (18.08) and Banglalink (18.25) are almost identical, indicating that the operators differ in month-to-month shift velocity rather than overall sentiment bounds. Furthermore, volatility coexists with strong outcomes: Banglalink's 2026 NSS ($+81.9$) is the highest of the three, so volatility cannot be interpreted as a marker of weak brand health. Stationary block bootstrap confidence intervals ($B = 10{,}000$, average block length $b = 4$ transitions; Politis \& Romano, 1994) confirm: Grameenphone RMSSD = 6.28 [95\% CI 4.33, 7.93], Robi RMSSD = 5.61 [3.88, 7.16], and Banglalink RMSSD = 13.61 [8.53, 18.77]. Because Grameenphone and Robi intervals overlap substantially (ratio 1.12 [0.72, 1.71], $p = 0.3416$), we do not assert a meaningful volatility difference between those two operators. Monte Carlo downsampling downsamples Grameenphone and Robi monthly reviews to Banglalink's exact monthly review counts across 1,000 runs, yielding downsampled mean RMSSD values of 6.71 (run-to-run 2.5th--97.5th percentile range across simulations [6.22, 7.32], reflecting simulation variability rather than confidence intervals) for Grameenphone and 5.91 (range [5.48, 6.40]) for Robi.

Crucially, diagnostic regressions reveal that monthly sentiment swings are heavily coupled with review volume growth: regressing $\Delta\text{NSS}$ on $\Delta\ln(\text{Volume})$ across all 80 transitions yields $R^2 = 0.5217$ for Banglalink ($\beta = 17.47, p < 0.0001$) and $R^2 = 0.2442$ for Grameenphone ($\beta = 8.57, p < 0.0001$), whereas Robi's sentiment shifts are uncoupled from volume ($R^2 = 0.0236, \beta = 2.38, p = 0.1738$). When we apply an objective volume-surge filter excluding transitions with $\ge 50\%$ month-over-month volume changes, 13 of 80 transitions are removed for Banglalink (retaining 67), 11 for Grameenphone (retaining 69), and 8 for Robi (retaining 72). Under this volume-filtered benchmark, Banglalink's RMSSD drops sharply from 13.61 to 7.56 points [95\% bootstrap CI 6.15, 8.93], Grameenphone's RMSSD falls to 5.15 [3.86, 6.29], and Robi's RMSSD falls to 4.53 [3.44, 5.67]. Comparing filtered Banglalink (7.56) to unfiltered Robi (5.61) yields a ratio of 1.35; comparing filtered series directly yields a ratio of 1.69 [1.23, 2.32] against Robi and 1.50 [1.10, 2.02] against Grameenphone. Similarly, evaluating RMSSD on volume-adjusted regression residuals yields 9.41 for Banglalink, 5.54 for Robi, and 5.44 for Grameenphone (ratio: 1.70). These tests demonstrate that most of the apparent ``2.4$\times$'' volatility gap is driven by changes in reviewer volume and mix rather than pure operational failure. We therefore reframe the finding: volatility in app-visible sentiment is partly driven by changes in who reviews, and only partly by operational divergence."""

assert old_s43 in text, "old_s43 not found!"
text = text.replace(old_s43, new_s43)

old_tab5_note = r"""\raggedright\footnotesize\textit{Note:} RMSSD, SSI (Equations~\ref{eq:rmssd}--\ref{eq:ssi}) and IQR in NSS points. Shocks are monthly transitions with $|\Delta\text{NSS}| \ge 10.0$ across the 80 modern transitions (35 total; 37 if including the December 2019 $\to$ January 2020 transition)."""

new_tab5_note = r"""\raggedright\footnotesize\textit{Note:} RMSSD, SSI (Equations~\ref{eq:rmssd}--\ref{eq:ssi}) and IQR in NSS points. Shocks are monthly transitions with $|\Delta\text{NSS}| \ge 10.0$ across the 80 modern transitions (35 total)."""

assert old_tab5_note in text, "old_tab5_note not found!"
text = text.replace(old_tab5_note, new_tab5_note)

# -------------------------------------------------------------
# 7. SECTION 4.4 & TABLE 6: Shock Decomposition, General/Other, Prop 2, Table 7
# -------------------------------------------------------------
old_s44_p1 = r"""Across the full common window ($n \ge 30$), 98 monthly transitions meet the shock criterion ($|\Delta\text{NSS}| \ge 10.0$); 35 of the 240 modern-era transitions do (6 Grameenphone, 7 Robi, 22 Banglalink; 37 across 243 transitions if including the baseline December 2019 $\to$ January 2020 transition). Table~\ref{tab:shocks} decomposes ten major modern-era shocks. App-login and technical-bug sentiment is the leading contributor in seven of the ten, offers in two and network speed in one. Across all 35 modern shocks, App Login \& Technical Bugs accounts for the primary operational movement in 77.1\% of shocks (27 of 35), 86.7\% of drops (13 of 15), and 70.0\% of rises (14 of 20), with a median operational contribution share of 23.6\% (and 34\% among the ten major shocks). As a null comparison for Proposition 2, in the 205 non-shock modern transitions, App Login leads in only 46.8\% (96 of 205), followed by Offers (31.2\%, $n=64$), Network (17.1\%, $n=35$), and Billing (4.9\%, $n=10$). A chi-square test confirms that App Login is significantly more dominant during shocks than during non-shock months ($\chi^2(1) = 10.95, p = 0.0009$), providing strong empirical support for Proposition 2. Large shocks remain multi-domain events where technical issues trigger secondary complaints in offers and billing."""

new_s44_p1 = r"""Across the modern era, 35 of the 240 transitions meet the shock criterion ($|\Delta\text{NSS}| \ge 10.0$): 6 for Grameenphone, 7 for Robi, and 22 for Banglalink. Table~\ref{tab:shocks} decomposes ten major modern shocks. Because General / Other absorbs a median of 62.9\% of raw monthly NSS movement across all 35 shocks (leading in 33 of 35 shocks) and tracks volume fluctuations ($R^2 = 0.5616, p < 0.0001$), sentiment shifts are predominantly diffuse. Among the four specific operational domains, however, App Login \& Technical Bugs is the primary operational driver in 77.1\% of shocks (27 of 35; 13 of 15 drops and 14 of 20 rises), with a median operational share of 23.6\% across all 35 shocks (and 33.6\% among the ten major shocks in Table~\ref{tab:shocks}). As a null comparison for Proposition 2, in the 205 non-shock modern transitions, App Login leads among operational domains in only 46.8\% (96 of 205). A pooled test confirms that App Login is significantly more dominant during shocks than during non-shock months ($\chi^2(1) = 11.00, p = 0.0009$; Fisher's exact test odds ratio $\text{OR} = 3.83, p = 0.0009$). However, this pooled result is heavily driven by Banglalink, where App Login leads in 20 of 22 shocks (90.9\%) versus 29 of 58 non-shocks (50.0\%; Fisher's exact $p = 0.0007, \text{OR} = 10.00$). For Grameenphone, App Login leads in 3 of 6 shocks (50.0\%) versus 30 of 74 non-shocks (40.5\%; Fisher's exact $p = 0.6866, \text{OR} = 1.47$). For Robi, App Login leads in 4 of 7 shocks (57.1\%) versus 32 of 73 non-shocks (43.8\%; Fisher's exact $p = 0.6949, \text{OR} = 1.71$). Excluding volume-surge transitions ($\ge 50\%$ volume shift) retains 19 non-surge shocks, where App Login still leads in 14 (73.7\%) versus 82 of 189 non-surge non-shocks (43.4\%; $\chi^2(1) = 6.38, p = 0.0116$; Fisher's exact $p = 0.0150, \text{OR} = 3.65$). Because app login is mechanically the highest-variance operational domain, Proposition 2 receives authentic support, but its magnitude is strongly amplified by Banglalink's specific release volatility."""

assert old_s44_p1 in text, "old_s44_p1 not found!"
text = text.replace(old_s44_p1, new_s44_p1)

old_table6 = r"""\begin{table}[htbp]
\centering
\begin{spacing}{1.0}
\caption{Additive Decomposition of Ten Major Operational Shocks, 2020--2026}
\label{tab:shocks}
\small
\begin{tabular}{llrlrr}
\toprule
\textbf{Operator} & \textbf{Transition} & \textbf{$\Delta$NSS} & \textbf{Leading domain} & \textbf{Impact} & \textbf{Share} \\
\midrule
Grameenphone & 2020-03 $\to$ 04 & +31.2 & App Login \& Bugs & +5.49 & 18\% \\
Grameenphone & 2021-04 $\to$ 05 & $-$13.8 & App Login \& Bugs & $-$2.29 & 17\% \\
Grameenphone & 2021-08 $\to$ 09 & +13.6 & App Login \& Bugs & +5.08 & 37\% \\
Grameenphone & 2025-08 $\to$ 09 & $-$18.5 & Offers \& Data Packs & $-$2.68 & 14\% \\
Robi & 2022-12 $\to$ 2023-01 & $-$16.6 & App Login \& Bugs & $-$7.40 & 45\% \\
Robi & 2023-01 $\to$ 02 & +10.7 & App Login \& Bugs & +4.64 & 43\% \\
Robi & 2023-11 $\to$ 12 & +10.0 & Offers \& Data Packs & +2.67 & 27\% \\
Banglalink & 2021-04 $\to$ 05 & $-$16.4 & Network Speed \& Latency & $-$4.90 & 30\% \\
Banglalink & 2024-03 $\to$ 04 & $-$11.2 & App Login \& Bugs & $-$8.74 & 78\% \\
Banglalink & 2024-04 $\to$ 05\textsuperscript{b} & +32.8 & App Login \& Bugs & +13.73 & 42\% \\
\bottomrule
\end{tabular}

\vspace{0.3em}
\raggedright\footnotesize\textit{Note:} $\Delta$NSS and Impact (the leading domain's contribution, Equation~\ref{eq:decomp}) in NSS points. Share = Impact / $\Delta$NSS. These ten are a selection of major modern shocks, not the full set of 35. \textsuperscript{b}Confounded: hotfix build v11.9.1 co-occurred with a 72.2\% review volume surge ($N = 1{,}315 \to 2{,}265$), lifting baseline sentiment beyond pre-crisis levels.
\end{spacing}
\end{table}"""

new_table6 = r"""\begin{table}[htbp]
\centering
\begin{spacing}{1.0}
\caption{Additive Decomposition of Ten Major Operational Shocks, 2020--2026}
\label{tab:shocks}
\small
\begin{tabular}{llrlrrr}
\toprule
\textbf{Operator} & \textbf{Transition} & \textbf{$\Delta$NSS} & \textbf{Leading Op.\ Domain} & \textbf{Op.\ Impact (Share)\textsuperscript{a}} & \textbf{4-Domain Total} & \textbf{General / Other} \\
\midrule
Grameenphone & 2020-03 $\to$ 04 & +31.2 & App Login \& Bugs & +5.49 (18\%) & +10.54 (34\%) & +20.70 (66\%) \\
Grameenphone & 2021-04 $\to$ 05 & $-$13.8 & App Login \& Bugs & $-$2.29 (17\%) & $-$5.28 (38\%) & $-$8.47 (62\%) \\
Grameenphone & 2021-08 $\to$ 09 & +13.6 & App Login \& Bugs & +5.08 (37\%) & +6.59 (49\%) & +6.98 (51\%) \\
Grameenphone & 2025-08 $\to$ 09 & $-$18.5 & Offers \& Data Packs & $-$2.68 (14\%) & $-$5.47 (30\%) & $-$13.06 (70\%) \\
Robi & 2022-12 $\to$ 2023-01 & $-$16.6 & App Login \& Bugs & $-$7.40 (45\%) & $-$7.15 (43\%) & $-$9.45 (57\%) \\
Robi & 2023-01 $\to$ 02 & +10.7 & App Login \& Bugs & +4.64 (44\%) & +4.74 (44\%) & +5.93 (56\%) \\
Robi & 2023-11 $\to$ 12 & +10.0 & Offers \& Data Packs & +2.67 (27\%) & +2.82 (28\%) & +7.19 (72\%) \\
Banglalink & 2021-04 $\to$ 05 & $-$16.4 & Network Speed \& Latency & $-$4.90 (30\%) & $-$9.33 (57\%) & $-$7.10 (43\%) \\
Banglalink & 2024-03 $\to$ 04 & $-$11.2 & App Login \& Bugs & $-$8.74 (78\%) & $-$5.32 (48\%) & $-$5.87 (52\%) \\
Banglalink & 2024-04 $\to$ 05 & +32.8 & App Login \& Bugs & +13.73 (42\%) & +15.40 (47\%) & +17.38 (53\%) \\
\bottomrule
\end{tabular}

\vspace{0.3em}
\raggedright\footnotesize\textsuperscript{a}\textit{Note:} $\Delta$NSS and impacts in NSS points. Leading operational domain share is the share of $\Delta$NSS explained by that domain (median 33.6\% across these ten major shocks, vs.\ 23.6\% across all 35 modern shocks). The 4-Domain Total and General / Other columns sum exactly to $\Delta$NSS per Equation~\ref{eq:decomp}.
\end{spacing}
\end{table}"""

assert old_table6 in text, "old_table6 not found!"
text = text.replace(old_table6, new_table6)

old_s44_p2 = r"""Three cases illustrate what the decomposition can and cannot show. Banglalink's March--April 2024 fall is the cleanest: about 78\% of the 11.2-point drop sits in app-login and bug sentiment, directly matching release telemetry. In March 2024 ($N = 1{,}093$, NSS = $+42.8$), build v11.7.1 recorded $+40.8$ NSS (Table~\ref{tab:versions}). In April 2024 ($N = 1{,}315$, NSS = $+31.6$), build v11.8.0 accounted for 34.1\% of version-identified reviews ($n = 158$) and generated a deeply negative NSS of $-7.59$, driving the decline; however, only 35.3\% of April reviews reported a version string. In May 2024 ($N = 2{,}265$, NSS = $+64.4$, $\Delta\text{NSS} = +32.8$), hotfix build v11.9.1 dominated versioned reviews (74.7\%, $n = 708$) with an NSS of $+77.0$, about 34 points above the pre-crisis build v11.7.1. However, review volume also surged by 72.2\% ($1{,}315 \to 2{,}265$). While release notes confirm the launch crash fix, attributing volume growth to in-app review prompts is an inference, as prompt logging is internal; we therefore treat the May rebound as confounded by volume acceleration co-occurring with the hotfix. Grameenphone's September 2025 fall of 18.5 points is led by Offers ($-2.68$ pp, 14\% share) while General / Other absorbed $-13.1$ pp; this coincided with the commercial 5G rollout and consumer dissatisfaction with data pack tariffs. Finally, Banglalink's April--May 2021 fall is led by network sentiment, showing that Proposition 2 is not universal."""

new_s44_p2 = r"""Three cases illustrate what the decomposition can and cannot show. First, Banglalink's March--April 2024 shock cycle highlights both the reach and limits of app-version telemetry (Table~\ref{tab:versions}). In March 2024 ($N = 1{,}093$, NSS = $+42.8$), build v11.7.1 recorded $+40.8$ NSS. In April 2024 ($N = 1{,}315$, NSS = $+31.6$, $\Delta\text{NSS} = -11.2$), the newly deployed build v11.8.0 recorded a negative NSS of $-7.6$ [95\% CI $-22.7$, $+7.5$] across $n = 158$ reviews, characterized by app launch freezing and authentication crashes. Counterfactually replacing the v11.8.0 cohort with the balance of April's reviews (NSS $\approx +37.0$) raises monthly NSS by 5.36 points, indicating that roughly half of April's 11.2-point decline is traceable to the identifiable v11.8.0 cohort, while the remainder sits in the unversioned majority (which fell to $+35.3$). In May 2024 ($N = 2{,}265$, NSS = $+64.4$, $\Delta\text{NSS} = +32.8$), public Google Play release notes for hotfix build v11.9.1 explicitly documented fixes for launch freezing and OTP authentication. However, the telemetry contradicts attributing the entire 32.8-point May surge to the hotfix: the identical build v11.9.1 scored only $+40.5$ [29.5, 51.5] during its initial rollout in late April, non-overlapping with its May score (+77.0 [72.8, 81.2]). Furthermore, control cohorts unexposed to the hotfix moved in parallel: legacy versions rose from $+42.7$ to $+60.2$, and unversioned reviews jumped from $+35.3$ to $+62.3$, accompanied by a 72.2\% review volume surge ($1{,}315 \to 2{,}265$). This demonstrates that while the hotfix resolved the acute functional crash, the monthly recovery was heavily amplified by contemporaneous reviewer-volume and composition shifts. Second, Grameenphone's September 2025 fall of 18.5 points is led among operational domains by Offers ($-2.68$ pp, 14\% share) while General / Other absorbed $-13.1$ pp (71\% share); this coincided with commercial 5G commercialization, where data pack tariff dissatisfaction represents only a small slice of a broad sentiment drop. Finally, Banglalink's April--May 2021 fall is led by network sentiment ($-4.90$ pp, 30\% share), showing that Proposition 2 is not universal."""

assert old_s44_p2 in text, "old_s44_p2 not found!"
text = text.replace(old_s44_p2, new_s44_p2)

# -------------------------------------------------------------
# 8. SECTION 5.2: Reframe Banglalink 22 shocks
# -------------------------------------------------------------
old_s52 = r"""For Banglalink, app-bug complaints (7.25\% of reviews) are about 1.6 times the market-wide rate (4.4\%) and roughly twice the rate of the other two operators combined (3.7\%), and its 22 shocks point to strengthening release testing."""

new_s52 = r"""For Banglalink, app-bug complaints (7.25\% of reviews) are about 1.6 times the market-wide rate (4.4\%) and roughly twice the rate of the other two operators combined (3.7\%). However, because Banglalink's sentiment shifts are strongly coupled with volume fluctuations ($R^2 = 0.52$) and roughly half of its shock frequency and excess volatility recedes when volume surges are removed, its 22 shocks reflect an interplay between genuine release instability (such as the build v11.8.0 crash cohort) and acute sensitivity to reviewer composition. Management priorities should therefore combine pre-release automated testing and staged rollouts with active monitoring of review collection dynamics."""

assert old_s52 in text, "old_s52 not found!"
text = text.replace(old_s52, new_s52)

# -------------------------------------------------------------
# 9. REFERENCES: Alphabetical order & remove draft comments
# -------------------------------------------------------------
old_refs = r"""\vspace{0.6em}\noindent Tirunillai, S., \& Tellis, G. J. (2014). Mining marketing meaning from online chatter: Strategic brand analysis of big data using latent Dirichlet allocation. \textit{Journal of Marketing Research}, \textit{51}(4), 463--479. \url{https://doi.org/10.1509/jmr.12.0106} % CORRECTED: earlier draft had Marketing Science 33(4), 463--486

\vspace{0.6em}\noindent Politis, D. N., \& Romano, J. P. (1994). The stationary bootstrap. \textit{Journal of the American Statistical Association}, \textit{89}(428), 1303--1313. \url{https://doi.org/10.1080/01621459.1994.10476870}"""

new_refs_tir = r"""\vspace{0.6em}\noindent Tirunillai, S., \& Tellis, G. J. (2014). Mining marketing meaning from online chatter: Strategic brand analysis of big data using latent Dirichlet allocation. \textit{Journal of Marketing Research}, \textit{51}(4), 463--479. \url{https://doi.org/10.1509/jmr.12.0106}"""

# Move Politis after Parasuraman
old_paras = r"""\vspace{0.6em}\noindent Parasuraman, A., Zeithaml, V. A., \& Berry, L. L. (1988). SERVQUAL: A multiple-item scale for measuring consumer perceptions of service quality. \textit{Journal of Retailing}, \textit{64}(1), 12--40."""

new_paras = r"""\vspace{0.6em}\noindent Parasuraman, A., Zeithaml, V. A., \& Berry, L. L. (1988). SERVQUAL: A multiple-item scale for measuring consumer perceptions of service quality. \textit{Journal of Retailing}, \textit{64}(1), 12--40.

\vspace{0.6em}\noindent Politis, D. N., \& Romano, J. P. (1994). The stationary bootstrap. \textit{Journal of the American Statistical Association}, \textit{89}(428), 1303--1313. \url{https://doi.org/10.1080/01621459.1994.10476870}"""

assert old_refs in text, "old_refs not found!"
assert old_paras in text, "old_paras not found!"
text = text.replace(old_refs, new_refs_tir)
text = text.replace(old_paras, new_paras)

# Clean trailing comments in references
text = re.sub(r' % NEW', '', text)
text = re.sub(r' % CORRECTED[^\n]*', '', text)

# Write updated text
with open(tex_path, "w", encoding="utf-8") as f:
    f.write(text)

print("All reviewer fixes applied successfully to LaTeX file.")

