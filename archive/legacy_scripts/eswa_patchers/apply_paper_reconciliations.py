from pathlib import Path

# 1. Table 1 target and replacement
TAB1_TARGET = r"""\begin{tabularx}{\textwidth}{@{}llXcc@{}}
\toprule
Domain Identifier & Category Name & Diagnostic Semantic Scope and Exemplar User Grievances & Seed $N$ & Corpus \% \\
\midrule
$\mathcal{C}_1$ & \textbf{App Login \& Technical Bugs} & Authentication errors, OTP delivery failures, biometric login timeouts, application splash crashes, session expiration loops. \textit{Exemplar: ``App khule na, bar bar update chay kintu login hoy na''} [App doesn't open, keeps asking for updates but cannot log in]. & 400 & 8.9\% \\
\addlinespace
$\mathcal{C}_2$ & \textbf{Network Speed \& 4G Latency} & Slow data throughput, 4G-to-3G drops, packet loss, video buffering, voice call drops, indoor coverage degradation. \textit{Exemplar: ``Net speed ekdom baje, 4G thakleo kono kisu load hoy na''} [Net speed is totally useless, nothing loads even on 4G]. & 364 & 8.1\% \\
\addlinespace
$\mathcal{C}_3$ & \textbf{Billing \& Airtime Deductions} & Unrecognized balance deductions, recharge failures, value-added service (VAS) auto-renewals, emergency balance penalties. \textit{Exemplar: ``Taka kete niyeche kintu MB dey nai, faltu service''} [Deducted money but did not credit MB, useless service]. & 217 & 4.8\% \\
\addlinespace
$\mathcal{C}_4$ & \textbf{Offers \& Data Packs} & Tariff pricing dissatisfaction, bundle validity duration, package affordability, megabyte quota complaints. \textit{Exemplar: ``Dam onek beshi, kom dam e bhalo internet offer chai''} [Price is too high, want better internet offers at lower price]. & 788 & 17.5\% \\
\addlinespace
$\mathcal{C}_5$ & \textbf{General Appreciation / Other} & Non-operational feedback, generic 5-star praise, customer service appreciation, UI praise. \textit{Exemplar: ``Khub bhalo app, shob shundor bhabe kaj kore''} [Very good app, everything works nicely]. & 2,730 & 60.7\% \\
\bottomrule
\end{tabularx}
\vspace{0.4em}
\parbox{\textwidth}{\footnotesize \textit{Notes:} Diagnostic scope synthesized from expert operator taxonomy rulebooks. Seed $N = 4{,}499$ verified multi-operator reviews across Grameenphone, Robi, and Banglalink.}"""

TAB1_REPLACEMENT = r"""\begin{tabularx}{\textwidth}{@{}llXccc@{}}
\toprule
Domain Identifier & Category Name & Diagnostic Semantic Scope and Exemplar User Grievances & Seed $N$ & Seed \% & Deployed \% \\
\midrule
$\mathcal{C}_1$ & \textbf{App Login \& Technical Bugs} & Authentication errors, OTP delivery failures, biometric login timeouts, application splash crashes, session expiration loops. \textit{Exemplar: ``App khule na, bar bar update chay kintu login hoy na''} [App doesn't open, keeps asking for updates but cannot log in]. & 400 & 8.9\% & 5.0\% \\
\addlinespace
$\mathcal{C}_2$ & \textbf{Network Speed \& 4G Latency} & Slow data throughput, 4G-to-3G drops, packet loss, video buffering, voice call drops, indoor coverage degradation. \textit{Exemplar: ``Net speed ekdom baje, 4G thakleo kono kisu load hoy na''} [Net speed is totally useless, nothing loads even on 4G]. & 364 & 8.1\% & 2.5\% \\
\addlinespace
$\mathcal{C}_3$ & \textbf{Billing \& Airtime Deductions} & Unrecognized balance deductions, recharge failures, value-added service (VAS) auto-renewals, emergency balance penalties. \textit{Exemplar: ``Taka kete niyeche kintu MB dey nai, faltu service''} [Deducted money but did not credit MB, useless service]. & 217 & 4.8\% & 1.0\% \\
\addlinespace
$\mathcal{C}_4$ & \textbf{Offers \& Data Packs} & Tariff pricing dissatisfaction, bundle validity duration, package affordability, megabyte quota complaints. \textit{Exemplar: ``Dam onek beshi, kom dam e bhalo internet offer chai''} [Price is too high, want better internet offers at lower price]. & 788 & 17.5\% & 5.0\% \\
\addlinespace
$\mathcal{C}_5$ & \textbf{General Appreciation / Other} & Non-operational feedback, generic 5-star praise, customer service appreciation, UI praise. \textit{Exemplar: ``Khub bhalo app, shob shundor bhabe kaj kore''} [Very good app, everything works nicely]. & 2,730 & 60.7\% & 86.6\% \\
\bottomrule
\end{tabularx}
\vspace{0.4em}
\parbox{\textwidth}{\footnotesize \textit{Notes:} Diagnostic scope synthesized from expert operator taxonomy rulebooks. Seed $N = 4{,}499$ verified multi-operator reviews across Grameenphone, Robi, and Banglalink ($1{,}500$ per operator). Deployed \% reflects empirical distribution across the full longitudinal common duration corpus ($N = 655{,}649$).}"""


# 2. Section 4.4 Linguistic section target and replacement
SEC44_TARGET = r"""Across our verified multi-operator corpus ($N = 4,499$), standard English comprises $66.8\%$ ($N = 3,005$), native script Bangla accounts for $24.2\%$ ($N = 1,091$), and Romanized Banglish represents $8.7\%$ ($N = 390$) (with $0.3\%$ consisting of non-verbal symbolic/emoticon feedback)."""

SEC44_REPLACEMENT = r"""We evaluate linguistic distributions across two rigorous scopes: the balanced ground truth seed corpus ($N = 4{,}499$) utilized for supervised model validation, and the full decade-long ingested repository ($N = 661{,}160$; $655{,}649$ in the common duration window). In the balanced seed corpus, standard English comprises $66.8\%$ ($N = 3{,}005$), native script Bangla accounts for $24.2\%$ ($N = 1{,}091$), Romanized Banglish represents $8.7\%$ ($N = 390$), and symbolic/emoticon reviews constitute $0.3\%$ ($N = 14$).

When evaluating the full $N = 661{,}160$ market repository across 2016--2026, the real-world macro distribution reflects: standard English at $77.12\%$ ($N = 509{,}887$), Romanized Banglish at $11.27\%$ ($N = 74{,}515$), native script Bangla at $9.42\%$ ($N = 62{,}296$), and symbolic feedback at $2.19\%$ ($N = 14{,}462$), with $2.51\%$ ($N = 16{,}615$) exhibiting heavy intra-sentential code-mixing. Across network operators, Grameenphone ($N = 321{,}374$) comprises $78.46\%$ English, $10.86\%$ Banglish, and $8.43\%$ Bangla; Robi ($N = 200{,}652$) comprises $77.44\%$ English, $10.50\%$ Banglish, and $9.95\%$ Bangla; and Banglalink ($N = 139{,}134$) comprises $73.56\%$ English, $13.32\%$ Banglish, and $10.95\%$ Bangla. Longitudinally, native Bangla script usage grew more than fourfold from $2.8\%$ in 2016 to $13.4\%$ in 2026, driven by nationwide smartphone keyboard adoption (e.g., Gboard, Ridmik)."""


# 3. Section 5.3 Case Study 2 target and replacement
SEC53_TARGET = r"""Applying Rule 2, the expert system executed the dual-track decomposition illustrated in Figure~\ref{fig:banglalink_reversal}:
\begin{itemize}
    \item \textbf{Branch A (Genuine Engineering Optimization):} Login complaints dropped from $8.1\%$ to $4.8\%$, contributing $+2.80$ points of genuine operational recovery. Network improvements contributed $+1.07$ points, and Offers $+0.98$ points, validating authentic infrastructure upgrades.
    \item \textbf{Branch B (Promotional Surface Distortion):} Concurrently, Banglalink implemented aggressive in-app review prompts tied to its \textit{Toffee} digital entertainment ecosystem. Generic 5-star \textit{General Appreciation} reviews expanded by $3.9$ percentage points, absorbing $+6.95$ points (57.4\%) of the measured NSS gain.
\end{itemize}
The expert system successfully prevented executive leadership from attributing the entire 2026 surge to core engineering, quantifying the exact split between authentic technical optimization ($42.6\%$) and promotional eWOM inflation ($57.4\%$)."""

SEC53_REPLACEMENT = r"""Applying Rule 2, the expert system executed the dual-track decomposition illustrated in Figure~\ref{fig:banglalink_reversal}:
\begin{itemize}
    \item \textbf{Branch A (Genuine Engineering Optimization):} App Login complaints dropped from $4.62\%$ ($473$ reviews in 2025) to $1.38\%$ ($301$ reviews in 2026), representing a $3.24$ percentage-point reduction in defect rate and contributing $+2.80$ points ($18.0\%$) to the net $+15.54$ point NSS rebound. Concurrently, Network improvements contributed $+1.07$ points ($6.9\%$), Offers added $+0.98$ points ($6.3\%$), and Billing deductions contributed $+0.36$ points ($2.3\%$), validating authentic cross-subsystem engineering enhancements totaling $+5.21$ points ($33.5\%$).
    \item \textbf{Branch B (Promotional Surface Distortion):} Concurrently, Banglalink implemented aggressive in-app review prompts tied to its \textit{Toffee} digital entertainment ecosystem. Generic 5-star \textit{General Appreciation} reviews expanded from $87.36\%$ to $92.71\%$ ($+5.35$ percentage points), absorbing $+10.33$ points ($66.5\%$) of the measured $+15.54$ point NSS gain.
\end{itemize}
The expert system successfully prevented executive leadership from attributing the entire 2026 surge to core engineering, quantifying the exact split between authentic technical optimization ($33.5\%$, $+5.21$ points) and promotional eWOM inflation ($66.5\%$, $+10.33$ points)."""


for filename in ["paper/eswa_latex/manuscript.tex", "paper/eswa_latex/manuscript_twocolumn.tex"]:
    p = Path(filename)
    content = p.read_text(encoding="utf-8")
    
    # Apply Tab 1
    if TAB1_TARGET in content:
        content = content.replace(TAB1_TARGET, TAB1_REPLACEMENT, 1)
        print(f"Applied Table 1 update to {filename}")
    else:
        print(f"Table 1 target not found in {filename}")

    # Apply Sec 4.4
    if SEC44_TARGET in content:
        content = content.replace(SEC44_TARGET, SEC44_REPLACEMENT, 1)
        print(f"Applied Sec 4.4 update to {filename}")
    else:
        print(f"Sec 4.4 target not found in {filename}")

    # Apply Sec 5.3
    if SEC53_TARGET in content:
        content = content.replace(SEC53_TARGET, SEC53_REPLACEMENT, 1)
        print(f"Applied Sec 5.3 update to {filename}")
    else:
        print(f"Sec 5.3 target not found in {filename}")

    p.write_text(content, encoding="utf-8")

print("\nReconciliation script completed!")
