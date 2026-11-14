from pathlib import Path
import re

TABLE1_NEW = r"""\begin{table*}[t]
\singlespacing
\centering
\caption{Operational Domain Taxonomy for Telecommunications Voice-of-the-Customer Feedback}
\label{tab:taxonomy}
\footnotesize
\setlength{\tabcolsep}{5pt}
\begin{tabularx}{\textwidth}{@{}c p{3.2cm} X ccc@{}}
\toprule
\textbf{ID} & \textbf{Category Name} & \textbf{Diagnostic Semantic Scope and Exemplar User Grievances} & \textbf{Seed $N$} & \textbf{Seed \%} & \textbf{Deployed \%} \\
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
\parbox{\textwidth}{\footnotesize \textit{Notes:} Diagnostic scope synthesized from expert operator taxonomy rulebooks. Seed $N = 4{,}499$ verified multi-operator reviews across Grameenphone, Robi, and Banglalink ($1{,}500$ per operator). Deployed \% reflects empirical distribution across the full longitudinal common duration corpus ($N = 655{,}649$).}
\end{table*}"""

TABLE2_NEW = r"""\begin{table*}[t]
\singlespacing
\centering
\caption{Multi-Paradigm Model Leaderboard across 5-Fold Stratified Cross-Validation ($N = 4{,}499$)}
\label{tab:leaderboard}
\footnotesize
\setlength{\tabcolsep}{4pt}
\begin{tabularx}{\textwidth}{@{}p{2.8cm} p{3.2cm} X ccc c r@{}}
\toprule
\textbf{Model Paradigm} & \textbf{Architecture} & \textbf{Feature Representation} & \textbf{Macro-F1 (Mean$\pm$Std)} & \textbf{Weighted-F1} & \textbf{Accuracy} & \textbf{Hardware} & \textbf{Latency} \\
\midrule
\textit{Heuristic Floor} & Dummy Classifier & Most Frequent Class & $0.1511 \pm 0.000$ & $0.4583$ & $60.68\% \pm 0.03\%$ & CPU & $<0.01$ ms \\
\addlinespace
\textit{Classical Generative} & Complement Naive Bayes & Char (2-5) + Word (1-3) & $0.7418 \pm 0.018$ & $0.8412$ & $84.21\% \pm 0.95\%$ & CPU & $0.45$ ms \\
\textit{Classical Discriminative} & Balanced Logistic Regression & Char (2-5) + Word (1-3) & $0.7781 \pm 0.018$ & $0.8682$ & $86.44\% \pm 1.13\%$ & CPU & $0.82$ ms \\
\textit{Margin-Based Classical} & Calibrated LinearSVC & Platt Scaled Sigmoid & $0.7687 \pm 0.020$ & $0.8676$ & $87.09\% \pm 1.01\%$ & CPU & $0.95$ ms \\
\addlinespace
\textbf{\textit{Hero Classical Ensemble}} & \textbf{Soft-Voting Classifier} & \textbf{Word (1-2) + Char (3-5)} & $\mathbf{0.7845 \pm 0.019}$ & $\mathbf{0.8738}$ & $\mathbf{87.44\% \pm 0.88\%}$ & \textbf{CPU} & $\mathbf{1.42\text{ ms}}$ \\
\midrule
\textit{Recurrent Deep Learning} & Hybrid BiLSTM + Attn & GloVe (300d) + Char-CNN & $0.7106 \pm 0.022$ & $0.8015$ & $80.84\% \pm 1.12\%$ & GPU & $18.4$ ms \\
\textit{Native Bengali Transformer} & BUET BanglaBERT & 110M Params (BERT-Base) & $0.6253 \pm 0.031$ & $0.7389$ & $74.88\% \pm 1.64\%$ & GPU & $32.6$ ms \\
\textit{Multilingual Transformer} & Multilingual MiniLM & 384d Dense Embeddings & $0.7247 \pm 0.024$ & $0.8104$ & $81.15\% \pm 1.25\%$ & GPU & $14.1$ ms \\
\bottomrule
\end{tabularx}
\vspace{0.4em}
\parbox{\textwidth}{\footnotesize \textit{Notes:} Evaluated on seed dataset ($N = 4{,}499$) with identical 5-fold stratified cross-validation splits. Hero Ensemble combines Balanced Logistic Regression ($w=2$), Calibrated LinearSVC ($w=2$), and Complement Naive Bayes ($w=1$). Latency measures single-review inference time on an Intel Xeon CPU vs.\ NVIDIA T4 GPU.}
\end{table*}"""

TABLE3_NEW = r"""\begin{table*}[t]
\singlespacing
\centering
\caption{Per-Class Classification Metrics and Confusion Matrix for the Deployed Hero Ensemble}
\label{tab:perclass}
\footnotesize
\setlength{\tabcolsep}{6pt}
\resizebox{\textwidth}{!}{%
\begin{tabular}{@{}lccccccccc@{}}
\toprule
& & & & \multicolumn{5}{c}{\textbf{Confusion Matrix (Predicted Class Counts)}} \\
\cmidrule(lr){5-9}
\textbf{Operational Category} & \textbf{Precision} & \textbf{Recall} & \textbf{F1-Score} & $\mathcal{C}_1$ & $\mathcal{C}_2$ & $\mathcal{C}_3$ & $\mathcal{C}_4$ & $\mathcal{C}_5$ & \textbf{Support ($N$)} \\
\midrule
$\mathcal{C}_1$: App Login \& Technical Bugs & $0.9828$ & $1.0000$ & $0.9913$ & \textbf{400} & 0 & 0 & 0 & 0 & 400 \\
$\mathcal{C}_2$: Network Speed \& 4G Latency & $0.9453$ & $0.9973$ & $0.9706$ & 0 & \textbf{363} & 1 & 0 & 0 & 364 \\
$\mathcal{C}_3$: Billing \& Airtime Deductions & $0.9775$ & $1.0000$ & $0.9886$ & 0 & 0 & \textbf{217} & 0 & 0 & 217 \\
$\mathcal{C}_4$: Offers \& Data Packs & $0.9837$ & $0.9975$ & $0.9905$ & 0 & 0 & 2 & \textbf{786} & 0 & 788 \\
$\mathcal{C}_5$: General Appreciation / Other & $1.0000$ & $0.9842$ & $0.9921$ & 7 & 21 & 2 & 13 & \textbf{2687} & 2,730 \\
\midrule
\textbf{Macro Average} & $\mathbf{0.9779}$ & $\mathbf{0.9958}$ & $\mathbf{0.9866}$ & -- & -- & -- & -- & -- & 4,499 \\
\textbf{Weighted Average} & $\mathbf{0.9901}$ & $\mathbf{0.9898}$ & $\mathbf{0.9898}$ & -- & -- & -- & -- & -- & 4,499 \\
\bottomrule
\end{tabular}%
}
\vspace{0.4em}
\parbox{\textwidth}{\footnotesize \textit{Notes:} Metrics reflect full seed corpus evaluation ($N = 4{,}499$). Five-fold cross-validation out-of-fold average: Accuracy $= 87.44\% \pm 0.88\%$, Macro-F1 $= 0.7845 \pm 0.019$. Confusion matrix columns: $\mathcal{C}_1$: App Login, $\mathcal{C}_2$: Network, $\mathcal{C}_3$: Billing, $\mathcal{C}_4$: Offers, $\mathcal{C}_5$: General.}
\end{table*}"""

TABLE4_NEW = r"""\begin{table*}[t]
\singlespacing
\centering
\caption{Empirical Classification Benchmark across Linguistic Sub-Cohorts (5-Fold Stratified Cross-Validation vs. Production Model)}
\label{tab:linguistic_benchmark}
\footnotesize
\setlength{\tabcolsep}{5pt}
\resizebox{\textwidth}{!}{%
\begin{tabular}{@{}lcccccccc@{}}
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
\end{tabular}%
}
\vspace{0.4em}
\parbox{\textwidth}{\footnotesize \textit{Notes:} Evaluated under identical 5-fold stratified splits (random seed 42) across $N = 4{,}499$ verified multi-operator reviews. Sub-cohort classification follows \citet{barman2014code} Unicode script filtering and \citet{gamback2016comparing} CMI threshold ($\text{CMI} \le 30$).}
\end{table*}"""

TABLE5_NEW = r"""\begin{table*}[t]
\singlespacing
\centering
\caption{Decade-Long Annual Net Sentiment Score (NSS) Trajectories by Era and Operator}
\label{tab:eras}
\footnotesize
\setlength{\tabcolsep}{5pt}
\begin{tabularx}{\textwidth}{@{}p{3.0cm} p{2.2cm} ccc X@{}}
\toprule
\textbf{Operational Era} & \textbf{Calendar Window} & \textbf{Grameenphone} & \textbf{Robi Axiata} & \textbf{Banglalink} & \textbf{Dominant Operational Dynamic} \\
\midrule
\textbf{Era 1: Early Adoption} & 2016--2017 & $+8.0$ & $-54.3$ & $+45.9$ & Early digital self-care rollout; high Robi friction vs.\ stable BL launch \\
\textbf{Era 2: 4G Transition} & 2018--2020 & $+16.4$ & $+17.1$ & $+26.1$ & Tariff restructuring dip in 2018; massive lockdown volume surge in 2020 \\
\textbf{Era 3: Post-Pandemic} & 2021--2022 & $+62.6$ & $+66.1$ & $+51.1$ & Sustained high digital engagement; mature 4G data adoption \\
\textbf{Era 4: SuperApp Divergence} & 2023--2026 & $+66.9$ & $+67.8$ & $+61.4$ & SuperApp pivots, gamified rewards, and regulatory tariff realignments \\
\midrule
\multicolumn{6}{@{}l}{\textit{Annual Progression:}} \\
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

TABLE6_NEW = r"""\begin{table*}[t]
\singlespacing
\centering
\caption{Cross-Layer Operational Decomposition of Ten Prominent Modern Sentiment Shocks}
\label{tab:shocks}
\footnotesize
\setlength{\tabcolsep}{4pt}
\resizebox{\textwidth}{!}{%
\begin{tabular}{@{}llccccccc l p{6.0cm}@{}}
\toprule
\textbf{Operator} & \textbf{Month} & $\Delta\text{\textbf{NSS}}$ & $\Delta\text{\textbf{App}}$ & $\Delta\text{\textbf{Net}}$ & $\Delta\text{\textbf{Off}}$ & $\Delta\text{\textbf{Bil}}$ & $\Delta\text{\textbf{Gen}}$ & \textbf{Shock Driver} & \textbf{Operational Root Cause Context} \\
\midrule
Grameenphone & 2020-04 & $-18.6$ & \textbf{-5.8} & $-3.2$ & $-1.4$ & $-0.8$ & $-7.4$ & App Login & Initial lockdown surge; frequent app updates and login friction \\
Grameenphone & 2021-09 & $+15.2$ & $+2.1$ & $+1.4$ & \textbf{+4.8} & $+0.3$ & $+6.6$ & Offers & BTRC unified bundle launch \\
Grameenphone & 2024-03 & $+11.4$ & \textbf{+4.2} & $+1.1$ & $+1.8$ & $+0.2$ & $+4.1$ & App Login & \textit{MyGP} biometric v10.4 update \\
Grameenphone & 2026-06 & $-12.8$ & $-1.6$ & $-1.2$ & \textbf{-4.9} & $-0.6$ & $-4.5$ & Offers & Regulatory 5G test pack price backlash \\
\addlinespace
Robi Axiata & 2020-03 & $+33.9$ & $+4.2$ & $+3.1$ & $+3.8$ & $+0.9$ & \textbf{+21.9} & General Praise & COVID emergency data relief campaign \\
Robi Axiata & 2023-01 & $-22.6$ & \textbf{-7.6} & $-3.4$ & $-2.1$ & $-1.1$ & $-8.4$ & App Login & Core billing migration and OTP authentication timeout \\
Robi Axiata & 2024-11 & $-12.9$ & $-2.1$ & \textbf{-4.8} & $-1.9$ & $-0.7$ & $-3.4$ & Network & Cyclone Midhili coastal tower outages \\
\addlinespace
Banglalink & 2024-04 & $-11.2$ & \textbf{-8.7} & $-1.1$ & $-0.4$ & $-0.2$ & $-0.8$ & App Login & Splash screen crash in build v11.8.0 \\
Banglalink & 2024-05 & $+32.8$ & \textbf{+13.7} & $+2.4$ & $+1.8$ & $+0.6$ & $+14.3$ & App Login & Emergency hotfix release v11.9.1 resolving crash bug \\
Banglalink & 2026-01 & $+15.5$ & $+2.8$ & $+1.1$ & $+1.0$ & $+0.4$ & \textbf{+10.3} & General Praise & Gamified daily login rewards program \\
\bottomrule
\end{tabular}%
}
\vspace{0.4em}
\parbox{\textwidth}{\footnotesize \textit{Notes:} Decompositions extracted via Equation~(13). $\Delta\text{App}, \Delta\text{Net}, \Delta\text{Off}, \Delta\text{Bil}, \Delta\text{Gen}$ represent net contributions from App Login, Network, Offers, Billing, and General categories, where $\Delta\text{NSS} = \sum \Delta \mathcal{C}_k$.}
\end{table*}"""

TABLE7_NEW = r"""\begin{table*}[t]
\singlespacing
\centering
\caption{Algorithm 1: Real-Time Canary Release Gating and Automated Subsystem Triage Protocol}
\label{alg:canary}
\footnotesize
\setlength{\tabcolsep}{6pt}
\begin{tabularx}{\textwidth}{@{}p{2.5cm} X@{}}
\toprule
\textbf{Step} & \textbf{Operational Action and Algorithmic Logic} \\
\midrule
\textbf{Input:} & Streaming review stream $\mathcal{R}_{\text{canary}} = \{r_1, r_2, \dots\}$ for canary build $V_{\text{canary}}$ (e.g., $5\%$ phased rollout); baseline login negative rate $p_{\text{base}}$. \\
\textbf{Parameter:} & Window size $W = 50$ reviews; significance threshold $\alpha = 0.01$; emergency abort threshold $\tau_{\text{abort}} = 0.25$. \\
\textbf{Output:} & Deployment status $\mathcal{D} \in \{\text{PROCEED}, \text{HOLD}, \text{ROLLBACK}\}$. \\
\addlinespace
\textbf{1: Initialization} & Set canary review counter $N_{\text{canary}} \leftarrow 0$, login negative counter $N_{\text{login\_neg}} \leftarrow 0$; \\
\textbf{2: Ingestion Loop} & \textbf{for each} incoming review $r_i \in \mathcal{R}_{\text{canary}}$ \textbf{do} \\
\textbf{3: Classification} & Run ensemble inference: $\hat{c}_i \leftarrow \text{PredictCategory}(r_i)$, $\hat{s}_i \leftarrow \text{PredictSentiment}(r_i)$; \\
\textbf{4: Filtering} & \textbf{if} $\hat{c}_i = \text{App Login \& Technical Bugs}$ \textbf{and} $\hat{s}_i = \text{Negative}$ \textbf{then} \\
\textbf{5:} & \quad $N_{\text{login\_neg}} \leftarrow N_{\text{login\_neg}} + 1$; \\
\textbf{6:} & \textbf{end if} \\
\textbf{7:} & $N_{\text{canary}} \leftarrow N_{\text{canary}} + 1$; \\
\textbf{8: Evaluation} & \textbf{if} $N_{\text{canary}} \ge W$ \textbf{then} \\
\textbf{9: Test Statistic} & Compute exact binomial test: $p_{\text{val}} \leftarrow \text{BinomialTest}(k = N_{\text{login\_neg}}, n = N_{\text{canary}}, p = p_{\text{base}})$; \\
\textbf{10: Decision Gate} & \textbf{if} $p_{\text{val}} < \alpha$ \textbf{and} $(N_{\text{login\_neg}} / N_{\text{canary}}) \ge \tau_{\text{abort}}$ \textbf{then} \\
\textbf{11:} & \quad \textbf{return} $\mathcal{D} \leftarrow \text{ROLLBACK}$ (Trigger CI/CD automated deployment halt); \\
\textbf{12:} & \textbf{else if} $p_{\text{val}} < \alpha$ \textbf{then} \\
\textbf{13:} & \quad \textbf{return} $\mathcal{D} \leftarrow \text{HOLD}$ (Alert Level 2: flag engineering triage team); \\
\textbf{14:} & \textbf{else} \\
\textbf{15:} & \quad \textbf{return} $\mathcal{D} \leftarrow \text{PROCEED}$ (Advance canary rollout tier); \\
\textbf{16:} & \textbf{end if} \\
\textbf{17:} & \textbf{end if} \\
\textbf{18:} & \textbf{end for} \\
\bottomrule
\end{tabularx}
\vspace{0.4em}
\parbox{\textwidth}{\footnotesize \textit{Notes:} Formalized algorithmic specification for Decision Rule 3, validated via trace-driven simulation across historical version rollouts. The binomial test evaluates whether the observed concentration of client-side failures deviates significantly from the historical baseline.}
\end{table*}"""

TABLE8_NEW = r"""\begin{table*}[t]
\singlespacing
\centering
\caption{Executive Operational Decision Matrix: Mapping Real-Time VoC Telemetry to Industrial Triage Workflows}
\label{tab:decision_matrix}
\footnotesize
\setlength{\tabcolsep}{4pt}
\begin{tabularx}{\textwidth}{@{}p{1.8cm} p{2.2cm} p{2.0cm} X X X@{}}
\toprule
\textbf{Alert Level} & \textbf{Statistical Threshold} & \textbf{Primary Subsystem} & \textbf{Diagnostic Symptom Profile} & \textbf{Prescriptive Operational Triage Action} & \textbf{Strategic Business Objective} \\
\midrule
\textbf{Level 1 (Routine)} & $p \ge 0.05, |\Delta\text{NSS}| < 5.0$ & Balanced across categories & Normal background feedback; non-systemic friction & Standard customer service queue processing; routine sprint backlog logging & Maintenance of baseline customer satisfaction \\
\addlinespace
\textbf{Level 2 (Warning)} & $p < 0.05, 5.0 \le |\Delta\text{NSS}| < 10.0$ & Offers \& Data Packs & Price sensitivity backlash; promo validity dissatisfaction & Alert Commercial Division; re-evaluate data bundle validity and tariff pricing & Commercial churn mitigation; competitive pricing retention \\
\addlinespace
\textbf{Level 3 (Critical Circuit)} & $p < 0.01, \Delta\text{NSS} \le -10.0$ & Client App Software & Fatal build crash; authentication gateway timeout & Immediate CI/CD canary freeze; rollback to previous stable APK; zero RF field dispatch & Protection of digital subscriber experience in self-care channels \\
\addlinespace
\textbf{Level 4 (Promotional Distortion)} & $\Delta V \ge 50\%, \Delta\text{Gen} \ge 5.0$ & General Appreciation & Sudden rate surge; cluster of generic 5-star praise & Dual-Track Surge-Adjust Filter (Rule 2); isolate Track A for engineering evaluation & Prevention of executive complacency from promotional noise \\
\bottomrule
\end{tabularx}
\vspace{0.4em}
\parbox{\textwidth}{\footnotesize \textit{Notes:} Synthesized from decade-long empirical shock profiles across Grameenphone, Robi, and Banglalink.}
\end{table*}"""

NEW_TABLES = [
    ("tab:taxonomy", TABLE1_NEW),
    ("tab:leaderboard", TABLE2_NEW),
    ("tab:perclass", TABLE3_NEW),
    ("tab:linguistic_benchmark", TABLE4_NEW),
    ("tab:eras", TABLE5_NEW),
    ("tab:shocks", TABLE6_NEW),
    ("alg:canary", TABLE7_NEW),
    ("tab:decision_matrix", TABLE8_NEW),
]

for filename in ["paper/eswa_latex/manuscript.tex", "paper/eswa_latex/manuscript_twocolumn.tex"]:
    p = Path(filename)
    content = p.read_text(encoding="utf-8")
    
    for label, new_tab in NEW_TABLES:
        # Match table by label
        pattern = r"\\begin\{table\*?\}.*?\\label\{" + re.escape(label) + r"\}.*?\\end\{table\*?\}"
        m = re.search(pattern, content, re.DOTALL)
        if m:
            content = content[:m.start()] + new_tab + content[m.end():]
            print(f"Replaced {label} in {filename}")
        else:
            print(f"Could not find {label} in {filename}")
            
    p.write_text(content, encoding="utf-8")

print("\nAll 8 tables updated with clean formatting and singlespacing!")
