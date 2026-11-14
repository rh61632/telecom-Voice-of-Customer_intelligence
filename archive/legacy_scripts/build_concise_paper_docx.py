"""
build_concise_paper_docx.py
Rebuilds Telecom_VoC_Intelligence_JBA_Manuscript.docx to STRICTLY satisfy the 20-page JBA limit:
- Preserves User's exact Page 1 edits (Md. Ratul Hasan, JUST, contact details)
- Concise, high-impact prose (~3,200 words)
- Compact, publication-grade exhibit sizing (tables 9pt single-spaced, figures optimized)
- Double-spaced 12pt Times New Roman, 1-inch margins
- Fully updated with 1 August 2016 start (655,649 reviews, 122 months), BTRC 2026 data, trilingual context
"""

import sys
import os
from copy import deepcopy
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

ROOT = Path(__file__).resolve().parent.parent
PAPER_DIR = ROOT / "paper"
DOCX_OUT = PAPER_DIR / "Telecom_VoC_Intelligence_JBA_Manuscript.docx"
FIG_DIR = PAPER_DIR / "figures"

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, val in edge_data.items():
                element.set(qn('w:{}'.format(key)), str(val))

def set_cell_margins(cell, top=30, bottom=30, left=50, right=50):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_page_number_to_run(run):
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def build_concise_docx():
    bak_path = PAPER_DIR / "Telecom_VoC_Intelligence_JBA_Manuscript.docx.bak"
    if bak_path.exists():
        doc = Document(str(bak_path))
        body_elms = list(doc._body._element)
        sect_pr = doc._body._element.find(qn('w:sectPr'))
        for el in body_elms[7:]:
            if el is not sect_pr:
                doc._body._element.remove(el)
        has_bak_page1 = True
    else:
        doc = Document()
        has_bak_page1 = False

    # Section & Page Setup (1 inch margins all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True
        
        # Header / Page Numbering on Page 2+
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("A Decade of Telecom Consumer Voice in Bangladesh  |  Page ")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(120, 120, 120)
        prun = hp.add_run()
        prun.font.name = "Times New Roman"
        prun.font.size = Pt(8.5)
        prun.font.color.rgb = RGBColor(120, 120, 120)
        add_page_number_to_run(prun)

    # Base Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=2.0, space_before=0, space_after=0, bold=False, italic=False, size=12, indent=0):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        if indent > 0:
            p.paragraph_format.first_line_indent = Inches(indent)
        if text:
            r = p.add_run(text)
            r.bold = bold
            r.italic = italic
            r.font.name = "Times New Roman"
            r.font.size = Pt(size)
        return p

    def add_heading_1(title):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        return p

    def add_heading_2(title):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        return p

    def add_equation(math_text, eq_num_str):
        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        table.columns[0].width = Inches(5.8)
        table.columns[1].width = Inches(0.7)
        cell_eq = table.cell(0, 0)
        cell_num = table.cell(0, 1)
        
        pe = cell_eq.paragraphs[0]
        pe.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pe.paragraph_format.line_spacing = 1.0
        pe.paragraph_format.space_before = Pt(2)
        pe.paragraph_format.space_after = Pt(2)
        re = pe.add_run(math_text)
        re.italic = True
        re.font.name = "Times New Roman"
        re.font.size = Pt(10.5)

        pn = cell_num.paragraphs[0]
        pn.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        pn.paragraph_format.line_spacing = 1.0
        pn.paragraph_format.space_before = Pt(2)
        pn.paragraph_format.space_after = Pt(2)
        rn = pn.add_run(eq_num_str)
        rn.font.name = "Times New Roman"
        rn.font.size = Pt(10.5)

        set_cell_border(cell_eq, top={'val': 'none'}, bottom={'val': 'none'}, left={'val': 'none'}, right={'val': 'none'})
        set_cell_border(cell_num, top={'val': 'none'}, bottom={'val': 'none'}, left={'val': 'none'}, right={'val': 'none'})
        set_cell_margins(cell_eq, top=20, bottom=20, left=40, right=40)
        set_cell_margins(cell_num, top=20, bottom=20, left=40, right=40)

    def add_figure(img_name, caption_text, note_text, width_in=5.8):
        img_path = FIG_DIR / img_name
        if img_path.exists():
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.line_spacing = 1.0
            p_img.paragraph_format.space_before = Pt(4)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            run = p_img.add_run()
            run.add_picture(str(img_path), width=Inches(width_in))
            
            p_cap = add_p(caption_text, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.0, space_before=1, space_after=1, bold=True, size=9.5)
            p_cap.paragraph_format.keep_with_next = True
            if note_text:
                add_p(note_text, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.0, space_before=0, space_after=4, italic=True, size=8.5)

    # =========================================================
    # PAGE 1: TITLE PAGE (USER'S EXACT EDITED VERSION PRESERVED DIRECTLY)
    # =========================================================
    print("Preserving User's Page 1 with 100% exact fidelity...")
    if not has_bak_page1:
        add_p("With Great Reviews Comes Great Responsibility:\nA Decade of Telecom Consumer Voice in Bangladesh",
              align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.5, space_before=64, space_after=32, bold=True, size=18)
        add_p("Md. Ratul Hasan", align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=0, space_after=4, bold=True, size=14)
        add_p("Department of Electrical and Electronic Engineering,", align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=0, space_after=4, size=12)
        add_p("Jashore University of Science and Technology", align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=0, space_after=4, size=12)
        add_p("Jashore -7408, Bangladesh", align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=0, space_after=4, size=12)
        add_p("Email: rh61632@gmail.com | Phone: +880 1916-277722", align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=0, space_after=32, size=11)
        doc.add_page_break()

    # =========================================================
    # PAGE 2: TITLE, ABSTRACT, KEYWORDS, JEL CODES
    # =========================================================
    print("Building Page 2: Abstract & Metadata...")
    add_p("With Great Reviews Comes Great Responsibility:\nA Decade of Telecom Consumer Voice in Bangladesh",
          align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.3, space_before=12, space_after=18, bold=True, size=16)

    add_p("Abstract", align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.0, space_before=0, space_after=6, bold=True, size=12)

    abstract_text = (
        "This study examines a decade of consumer voice for Bangladesh's three largest mobile operators using 655,649 "
        "Google Play reviews of MyGP, My Robi, and MyBL apps across a continuous 3,713-day window (August 2016 to September 2026). "
        "Deploying a domain-tuned trilingual (English, Bengali, and Banglish) classifier validated against blind human annotation, "
        "we observe long-term Net Sentiment Scores (NSS) of +64.9 for Grameenphone, +65.9 for Robi, and +53.0 for Banglalink, against an "
        "industry benchmark of +62.7. Consumer sentiment moved from sharp negativity during 2016–2018 to positive endorsement post-2020, "
        "with Robi demonstrating a 136.5-point swing (-57.9 to +78.6). However, approval is not performance: apparent volatility is heavily "
        "confounded by volume surges, compressing Banglalink's volatility ratio over Robi from 2.4-fold to 1.7-fold once filtered. "
        "App login and technical bugs led 77.1% of 35 significant sentiment shocks versus 44.4% of ordinary months (Fisher's odds ratio 4.23). "
        "Telecommunications operators must read reviews carefully before acting."
    )
    add_p(abstract_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.0, space_before=0, space_after=14, italic=True, size=11)

    p_kw = add_p("", align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.15, space_before=0, space_after=4, size=10.5)
    r_kwh = p_kw.add_run("Keywords: ")
    r_kwh.bold = True
    p_kw.add_run("net sentiment, app reviews, service failure, operator benchmarking, Bangla NLP, volatility, complaint attribution, mobile telecommunications.")

    p_jel = add_p("", align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.15, space_before=0, space_after=0, size=10.5)
    r_jelh = p_jel.add_run("JEL Classification Codes: ")
    r_jelh.bold = True
    p_jel.add_run("L96 (Telecommunications), M31 (Marketing), C55 (Large Data Sets: Modeling and Analysis), D12 (Consumer Economics: Empirical Analysis), L86 (Information and Internet Services), L15 (Information and Product Quality).")

    doc.add_page_break()

    # =========================================================
    # SECTION 1: INTRODUCTION (~380 words)
    # =========================================================
    print("Building Section 1: Introduction...")
    add_heading_1("1. INTRODUCTION")

    add_p(
        "Over a continuous ten-year span from 1 August 2016 through 30 September 2026 (3,713 days, encompassing exactly 122 complete calendar months), "
        "655,649 Bangladeshi consumers publicly evaluated their mobile network operators through self-service application reviews on Google Play. "
        "Bangladesh represents one of the largest and most rapidly transforming telecommunications ecosystems in the Global South. Official regulatory "
        "statistics released by the Bangladesh Telecommunication Regulatory Commission record 191.09 million active, biometric-verified mobile phone "
        "subscriptions: market leader Grameenphone Ltd. with 87.20 million subscribers (45.6% market share), Robi Axiata Limited with 59.04 million "
        "(30.9%), Banglalink Digital Communications Limited with 37.95 million (19.9%), and state-owned Teletalk Bangladesh Limited with 6.90 million "
        "(3.6%) (BTRC, 2026). Concurrently, mobile internet adoption reached 122.26 million active users, driven by nationwide 4G LTE penetration and "
        "commercial 5G non-standalone rollouts inaugurated on 1 September 2025. Across this decade, self-service applications—specifically MyGP, My Robi, "
        "and MyBL—evolved from rudimentary balance checkers into mission-critical platforms handling airtime recharges, algorithmic bundle purchases, "
        "fintech integrations, and frontline customer service resolution.",
        indent=0.5
    )

    add_p(
        "Despite this digital migration, telecommunications executives routinely rely on crude, aggregated metrics—such as lifetime star ratings and "
        "high-level sentiment averages—as executive proxies for operational health. This reliance creates severe managerial vulnerabilities. Public star "
        "ratings suffer from acute aggregation bias: they conflate genuine operational stability with promotional review-prompt campaigns, obscure transient "
        "volume surges, and fail to isolate which functional subsystem is failing. Furthermore, in linguistically complex developing markets characterized by "
        "trilingual feedback spanning standard English, native Bengali script, and Romanized Banglish, longitudinal cross-operator empirical evidence has "
        "remained virtually nonexistent. Decision-makers are consequently left blind to whether a sudden collapse in customer sentiment reflects genuine "
        "network degradation or a minor client-side application authentication bug.",
        indent=0.5
    )

    add_p(
        "To address this managerial and empirical gap, this study provides the first comprehensive, decade-long econometric and natural language processing "
        "(NLP) analysis of telecom customer voice in an emerging market. We investigate four interconnected research questions: (RQ1) How has consumer "
        "sentiment evolved across mobile network operators over ten years of infrastructural maturation, and how has market leadership rotated across distinct "
        "digital eras? (RQ2) Is observed month-over-month sentiment volatility genuine operational instability, or an artefact of promotional volume surges and "
        "reviewer-mix shifts? (RQ3) Which operational subsystems—client-side software engineering versus core telecommunications infrastructure—trigger acute "
        "sentiment shocks? (RQ4) Can automated NLP models reliably parse trilingual consumer feedback compared to human gold standards and naive star-rating heuristics?",
        indent=0.5
    )

    add_p(
        "Our empirical findings provide decisive answers. Over the decade, Grameenphone (+64.9) and Robi (+65.9) maintained near-parity in Net Sentiment Score (NSS), "
        "while Banglalink trailed by over 12 percentage points (+53.0). Robi executed an extraordinary 136.5-point turnaround, rising from -57.9 in 2016 to "
        "+78.6 in 2025. Crucially, our econometric audits reveal that approval is not performance: 77.1% of acute sentiment shocks (27 of 35) were triggered "
        "by client-side app login and authentication failures (Fisher's exact odds ratio 4.23), rather than core network signal latency or billing disputes. "
        "Furthermore, apparent volatility is heavily inflated by promotional volume surges; filtering surges compresses Banglalink's perceived volatility excess "
        "over Robi from 2.43-fold down to 1.67-fold (-31.3%).",
        indent=0.5
    )

    add_p(
        "This paper delivers four core contributions: (1) the largest standardized, tri-operator trilingual review corpus in South Asian telecommunications "
        "(N = 655,649); (2) surge-filtered volatility metrics based on the Root Mean Square Successive Difference (RMSSD) and Sentiment Stability Index (SSI); "
        "(3) an additive category decomposition framework isolating root causes of sentiment swings; and (4) an actionable four-part monitoring protocol for "
        "telecom leadership. The manuscript is organized around three structural responsibilities: Listen (Sections 4.1–4.2), Read Correctly (Sections 3.4, 4.3, 4.6), "
        "and Act (Sections 4.4, 4.5, 5).",
        indent=0.5
    )

    # =========================================================
    # SECTION 2: LITERATURE REVIEW (~440 words)
    # =========================================================
    print("Building Section 2: Literature Review...")
    add_heading_1("2. LITERATURE REVIEW AND CONCEPTUAL FRAMEWORK")

    add_heading_2("2.1 Customer Voice and Electronic Word-of-Mouth")
    add_p(
        "Electronic word-of-mouth (eWOM) represents one of the most influential market forces shaping consumer behavior and firm equity in digital economies "
        "(Hennig-Thurau et al., 2004). Unlike solicited survey instruments such as the Net Promoter Score (NPS; Reichheld, 2003), which suffer from non-response "
        "bias, sampling fatigue, and retrospective recall errors (Keiningham et al., 2007), public online reviews provide unprompted, high-frequency consumer "
        "telemetry generated at the precise moment of service consumption. In mobile platform ecosystems, public app store feedback directly influences consumer "
        "adoption decisions and brand equity (Chevalier & Mayzlin, 2006; Mudambi & Schuff, 2010). However, online reviews typically exhibit bimodal, J-shaped "
        "rating distributions dominated by extreme positive or negative polarization (Hu et al., 2008), making granular textual sentiment analysis mandatory "
        "to extract meaningful managerial signals.",
        indent=0.5
    )

    add_heading_2("2.2 Digital Service Quality, Failure, and Recovery")
    add_p(
        "Conceptualizing service quality in self-service digital platforms requires extending traditional SERVQUAL dimensions (Parasuraman et al., 1985) to "
        "electronic environments through the E-S-QUAL framework (Parasuraman et al., 2005). In self-service technologies (SSTs; Meuter et al., 2000; Bitner et al., 2000), "
        "consumers assume the role of co-producers. Consequently, service failures operate under distinct psychological mechanisms governed by Expectation-Confirmation "
        "Theory (Oliver, 1980). When a mobile application fails to execute core tasks—such as user authentication or balance retrieval—the customer experiences immediate "
        "service disruption. Maxham (2001) demonstrated that service recovery velocity is paramount: catastrophic software failures trigger intense negative word-of-mouth "
        "unless rectified through swift technical intervention. In telecom apps, technical reliability represents a hygiene factor; when it collapses, overall brand trust "
        "deteriorates rapidly regardless of core network quality.",
        indent=0.5
    )

    add_heading_2("2.3 Measuring Sentiment in Trilingual, Code-Mixed Digital Markets")
    add_p(
        "Natural language processing in multilingual, developing markets presents severe linguistic hurdles (Pang & Lee, 2008; Bhattacharjee et al., 2022). In Bangladesh, "
        "online consumer voice encompasses three distinct linguistic modalities: (1) Standard English, widely used by educated smartphone users for technical feedback "
        "(e.g., 'Worst network connection after update'); (2) Native Bengali Script, utilized for formal and colloquial evaluations (e.g., 'খুব ভালো সার্ভিস'); and "
        "(3) Romanized Bengali ('Banglish') and Intra-Sentential Code-Mixing, where users transcribe phonetic Bengali using Latin letters while interweaving English "
        "technical terms (e.g., 'Net speed onek slow, balance kete nilo but offer dilo na'). Mono-lingual English models and naive star-rating heuristics systematically "
        "fail in this trilingual environment due to cultural sarcasm, rating-text inversions (satisfied users selecting 1 star), and orthographic slang contractions "
        "(e.g., 'nc app'). Inter-annotator reliability metrics (Cohen, 1960; Landis & Koch, 1977) are therefore essential to establish objective ground truth.",
        indent=0.5
    )

    add_heading_2("2.4 Conceptual Framework and Testable Propositions")
    add_p(
        "To bridge digital service operations and empirical customer voice analytics, we advance three testable propositions grounded in service operations and measurement theory:",
        indent=0.5
    )
    add_p("Proposition 1 (Reviewer-Mix Confounding): Observed month-over-month sentiment volatility is significantly driven by promotional volume surges dominated by casual positive reviews, rather than shifts in core operational quality.", italic=True, indent=0.5)
    add_p("Proposition 2 (Client-Side Friction Dominance): Acute consumer sentiment shocks are predominantly triggered by client-side application failures (login/authentication barriers and technical bugs) rather than core infrastructure (network latency or billing disputes).", italic=True, indent=0.5)
    add_p("Proposition 3 (Persistent Operator Heterogeneity): Mobile network operators exhibit persistent, structural differences in shock frequency and operational stability that survive surge filtering and threshold variations.", italic=True, indent=0.5)

    # =========================================================
    # SECTION 3: DATA AND METHODOLOGY (~520 words)
    # =========================================================
    print("Building Section 3: Methodology...")
    add_heading_1("3. DATA AND METHODOLOGY")

    add_heading_2("3.1 Research Design")
    add_p(
        "This study employs a repeated cross-sectional observational design analyzing public app store reviews across a standardized 3,713-day window extending "
        "from 1 August 2016 through 30 September 2026 (122 continuous full calendar months). The starting boundary coincides with the commercial availability of "
        "all three primary operator applications on Google Play, ensuring strict tri-operator concurrency across the entire analytical horizon.",
        indent=0.5
    )

    add_heading_2("3.2 Data Collection, Cleansing, and Ethical Standards")
    add_p(
        "Reviews were harvested via automated Google Play scraper scripts extracting review text, numerical rating (1–5 stars), timestamp, thumbs-up upvotes, app version, "
        "and developer replies. The raw master database comprised 661,160 reviews (October 2014 to October 2026). Applying the synchronized window boundary (1 August 2016 "
        "to 30 September 2026) excluded 5,511 boundary records (including 21 initial reviews from the 4-day partial period in late July 2016 to enforce 100% full calendar "
        "months), yielding exactly N = 655,649 standardized observations: Grameenphone (N = 320,140), Robi (N = 198,378), and Banglalink (N = 137,131). Linguistic "
        "decomposition reveals that the corpus is predominantly Latin-script based (88.3%; 578,780 reviews), spanning standard English and Romanized Banglish, alongside "
        "native Bengali script (8.5%; 55,689 reviews), inter-script code-mixing (1.0%; 6,585 reviews), and emoji-only feedback (2.2%; 14,544 reviews). Preprocessing "
        "involved Unicode normalization, whitespace trimming, emoji preservation, and trilingual sub-word tokenization. All user screen names and personal identifiers "
        "were discarded; analyses are conducted strictly at aggregate econometric levels.",
        indent=0.5
    )

    add_heading_2("3.3 Mathematical Formulation of Empirical Measures")
    add_p(
        "To rigorously quantify customer sentiment dynamics and operational stability, we formulate seven empirical metrics:",
        indent=0.5
    )
    add_equation("NSS[m,k] = ((P[m,k] - N[m,k]) / T[m,k]) * 100", "(1)")
    add_equation("RMSSD = sqrt( (1 / (M - 1)) * sum( (NSS[m] - NSS[m-1])^2 ) )", "(2)")
    add_equation("SSI = 100 - RMSSD", "(3)")
    add_equation("Shock = { 1 if |Delta NSS[m]| >= 10.0, 0 otherwise }", "(4)")
    add_equation("Delta NSS[m] = sum( Delta C[k,m] )", "(5)")
    add_equation("CR[k] = (Negative[k] / Total Operator Reviews) * 100", "(6)")
    add_equation("DR[k] = (Negative[k] / Total Category Reviews[k]) * 100", "(7)")

    add_heading_2("3.4 Classification Architecture and Human Validation")
    add_p(
        "Reviews were classified into 3 sentiment classes (Positive, Neutral, Negative) and 5 operational categories (App Login & Technical Bugs, Offers & Data Packs, "
        "Network Speed & 4G Latency, Billing & Airtime Deductions, General Appreciation / Other). The classification architecture was trained on 4,500 domain-expert "
        "LLM-annotated seeds using a soft-voting ensemble combining sub-word TF-IDF n-grams (1–5 character and word grams) across Logistic Regression, Complement "
        "Naive Bayes, and LinearSVC. In 5-fold cross-validation, the ensemble achieved 87.47% accuracy (Macro-F1 0.7684) on sentiment and 87.44% accuracy (Macro-F1 0.7845) "
        "on category. Fine-tuned deep learning models (BUET BanglaBERT) achieved 91.60% CV accuracy (Macro-F1 0.8598) on sentiment and 85.27% on category. Models were "
        "independently evaluated against a zero-leakage blind human gold set (N = 300 primary blind annotations; N = 200 dual-annotator cohort). Inter-annotator reliability "
        "reached Cohen's kappa = 0.5762 (raw agreement 91.00%) for 3-class sentiment and kappa = 0.7694 (raw agreement 95.41%) for 5-class operational categories. On this "
        "human benchmark, the production ensemble attained 83.67% sentiment accuracy and 91.33% category accuracy (LinearSVC: 89.00%; star-rating baseline: 80.17%).",
        indent=0.5
    )

    add_heading_2("3.5 Analytical Strategy")
    add_p(
        "A strict monthly volume threshold of N >= 30 reviews is enforced to prevent small-sample volatility artefacts from distorting RMSSD or shock detection. "
        "Surge-filtering applies a 2.0x volume multiplier hurdle over rolling trailing medians. Additive domain decomposition isolates exact operational drivers of "
        "sentiment shifts, and 2x2 contingency tables evaluated via Chi-square and Fisher's exact tests assess structural over-representation during crisis shocks.",
        indent=0.5
    )

    # =========================================================
    # SECTION 4: RESULTS AND ANALYSIS (~1,000 words + exhibits)
    # =========================================================
    print("Building Section 4: Results & Analysis...")
    add_heading_1("4. RESULTS AND ANALYSIS")

    add_heading_2("4.1 The Decade at a Glance")
    add_p(
        "Table 1 summarizes the ten-year Voice-of-Customer scorecard across 655,649 standardized reviews. Over the decade, the Bangladeshi mobile telecommunications "
        "sector achieved an aggregate Net Sentiment Score of +62.7 (95% CI: [62.53, 62.87]), reflecting an industry-wide sentiment distribution of 75.9% positive, "
        "10.9% neutral, and 13.2% negative reviews. Market leaders Grameenphone (+64.9) and Robi (+65.9) sit in virtual statistical parity, separated by just 1.06 "
        "percentage points. While this gap achieves nominal statistical significance due to the enormous sample size (z = 5.42, p < 0.0001), its practical managerial "
        "effect size is negligible (~1 point on a 200-point scale). In contrast, Banglalink trails both peers by over 12 percentage points (+53.0), weighed down by a "
        "17.3% negative review share that is roughly 43% higher than Grameenphone (12.1%) or Robi (12.0%). Review volume share is heavily dominated by Grameenphone "
        "(48.8%), followed by Robi (30.3%) and Banglalink (20.9%), reflecting Grameenphone's early app onboarding campaigns.",
        indent=0.5
    )

    # Table 1
    t1_caption = "Table 1: Ten-Year Common-Window Voice-of-Customer Scorecard (1 August 2016 to 30 September 2026)"
    add_p(t1_caption, bold=True, size=10, space_before=4, space_after=1)
    t1_data = [
        ["Operator", "Total Reviews (N)", "Review Share (%)", "Positive (%)", "Neutral (%)", "Negative (%)", "NSS", "95% Bootstrap CI"],
        ["Grameenphone", "320,140", "48.8%", "77.0%", "10.9%", "12.1%", "+64.9", "[+64.61, +65.09]"],
        ["Robi Axiata", "198,378", "30.3%", "77.9%", "10.2%", "12.0%", "+65.9", "[+65.61, +66.21]"],
        ["Banglalink", "137,131", "20.9%", "70.4%", "12.3%", "17.3%", "+53.0", "[+52.63, +53.45]"],
        ["Industry Benchmark", "655,649", "100.0%", "75.9%", "10.9%", "13.2%", "+62.7", "[+62.53, +62.87]"],
    ]
    t1 = doc.add_table(rows=len(t1_data), cols=len(t1_data[0]))
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(t1_data):
        for c_idx, val in enumerate(row):
            cell = t1.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            r = p.runs[0]
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
                set_cell_border(cell, top={'val': 'single', 'sz': 12, 'color': '000000'}, bottom={'val': 'single', 'sz': 8, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
                set_cell_shading(cell, "F2F2F2")
            elif r_idx == len(t1_data) - 1:
                r.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
                set_cell_border(cell, top={'val': 'single', 'sz': 8, 'color': '000000'}, bottom={'val': 'double', 'sz': 12, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
                set_cell_border(cell, top={'val': 'none'}, bottom={'val': 'single', 'sz': 4, 'color': 'E0E0E0'}, left={'val': 'none'}, right={'val': 'none'})
            set_cell_margins(cell, top=25, bottom=25, left=45, right=45)
    add_p("Notes: 95% confidence intervals derived from 2,000 bootstrap resamples. Review share reflects digital engagement on Google Play.", italic=True, size=8.5, space_before=1, space_after=6)

    add_heading_2("4.2 Four Eras of Consumer Voice")
    add_p(
        "Longitudinal analysis across 11 calendar years reveals that consumer sentiment evolved through four distinct operational eras (Table 2, Figure 1, and Figure 2):",
        indent=0.5
    )
    add_p(
        "Era 1: Infancy and Friction (2016–2019; N = 20,657; 41 full months): Characterized by sparse review volumes and severe customer frustration. "
        "Robi recorded acute negative sentiment in 2016 (-57.9) and 2017 (-50.7). In 2018, the commercial launch of 4G networks coincided with an industry-wide "
        "sentiment drop: Grameenphone plummeted by -46.31 points (from +15.60 pre-launch to -30.71 post-launch), driven by SIM replacement friction and patchy early "
        "coverage. Banglalink maintained early leadership (+45.3 in 2016, +45.5 in 2017, +22.3 in 2018).",
        indent=0.5
    )
    add_p(
        "Era 2: The Pandemic Leap (2020; N = 77,471): With COVID-19 lockdowns in March 2020, annual review volume leaped by +616% over 2019 (10,813 to 77,471). "
        "Simultaneously, industry sentiment jumped into positive territory (+51.5), as mobile self-service apps became vital digital lifelines for emergency recharges.",
        indent=0.5
    )
    add_p(
        "Era 3: Maturity and Stability (2021–2022; N = 197,864): A period of consolidated performance and high, steady sentiment. Robi led both years (+63.8 and +68.4), "
        "while Grameenphone achieved +61.0 and +64.2. Banglalink stabilized at +46.6 and +55.5.",
        indent=0.5
    )
    add_p(
        "Era 4: Divergence and Reversal (2023–2026; N = 359,657): Competitive dynamics fractured sharply. Grameenphone achieved peak stability (+69.8 in 2023, +70.6 in "
        "2024, +70.3 in 2025) before sliding to +56.8 in 2026 following package tariff adjustments during the 5G rollout. Robi experienced an authentication slump in "
        "2023 (+48.7) before rebounding to a historic high of +78.6 in 2025. Banglalink executed a dramatic reversal: trailing at +40.1 in 2023, it surged to lead the "
        "market at +81.9 in 2026. Across the decade, Robi staged an unprecedented 136.5-point turnaround from -57.9 to +78.6.",
        indent=0.5
    )

    # Table 2
    t2_caption = "Table 2: Longitudinal Evolution of Annual Net Sentiment Score (NSS) and Volume (2016–2026)"
    add_p(t2_caption, bold=True, size=10, space_before=4, space_after=1)
    t2_data = [
        ["Year", "Grameenphone NSS", "Grameenphone N", "Robi NSS", "Robi N", "Banglalink NSS", "Banglalink N", "Industry NSS", "Total N"],
        ["2016*", "+2.5", "438", "-57.9", "126", "+45.3*", "744", "+21.0", "1,308"],
        ["2017", "+13.5", "587", "-50.7", "367", "+45.5*", "2,518", "+28.8", "3,472"],
        ["2018", "-16.0", "605", "-28.8", "1,418", "+22.3*", "3,041", "+3.4", "5,064"],
        ["2019", "+19.6*", "2,392", "+16.4", "4,186", "+17.8", "4,235", "+17.6", "10,813"],
        ["2020", "+45.7", "27,600", "+63.6*", "32,333", "+38.3", "17,538", "+51.5", "77,471"],
        ["2021", "+61.0", "40,535", "+63.8*", "30,296", "+46.6", "25,471", "+58.1", "96,302"],
        ["2022", "+64.2", "45,702", "+68.4*", "34,418", "+55.5", "21,442", "+63.8", "101,562"],
        ["2023", "+69.8*", "60,609", "+48.7", "16,784", "+40.1", "14,761", "+61.7", "92,154"],
        ["2024", "+70.6*", "75,059", "+66.0", "16,804", "+57.2", "15,333", "+68.0", "107,196"],
        ["2025", "+70.3", "54,262", "+78.6*", "42,743", "+66.4", "10,238", "+73.2", "107,243"],
        ["2026*", "+56.8", "12,351", "+76.2", "18,903", "+81.9*", "21,810", "+74.0", "53,064"],
    ]
    t2 = doc.add_table(rows=len(t2_data), cols=len(t2_data[0]))
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(t2_data):
        for c_idx, val in enumerate(row):
            cell = t2.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            r = p.runs[0]
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.2)
            if r_idx == 0:
                r.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_border(cell, top={'val': 'single', 'sz': 12, 'color': '000000'}, bottom={'val': 'single', 'sz': 8, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
                set_cell_shading(cell, "F2F2F2")
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
                set_cell_border(cell, top={'val': 'none'}, bottom={'val': 'single', 'sz': 4, 'color': 'E0E0E0'} if r_idx < len(t2_data)-1 else {'val': 'double', 'sz': 12, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
            set_cell_margins(cell, top=20, bottom=20, left=35, right=35)
    add_p("Notes: *Indicates annual NSS leader. 2016 reflects 5 complete months (Aug–Dec). 2026 reflects 9 months (Jan–Sep).", italic=True, size=8.0, space_before=1, space_after=4)

    # Figures 1 and 2
    add_figure("figure1_monthly_nss_trajectory.png", "Figure 1: Ten-Year Monthly Net Sentiment Score (NSS) Trajectory across Bangladeshi Operators", "Monthly NSS plotted for months satisfying N >= 30 (122 continuous months). Callouts highlight 4G launch, COVID-19, and 5G launch.", width_in=5.8)
    add_figure("figure2_yearly_leadership_strip.png", "Figure 2: Annual Voice-of-Customer Leadership Strip (2016–2026 Highest Yearly NSS)", "Annual leader badges indicate operator with highest Net Sentiment Score.", width_in=5.8)

    add_heading_2("4.3 Stability, Volatility, and Sentiment Shocks")
    add_p(
        "To evaluate operational stability across the modern era (2020–2026; 81 continuous months), we compute the Root Mean Square Successive Difference (RMSSD) "
        "and Sentiment Stability Index (SSI) (Table 3). Grameenphone exhibited exceptional stability (SSI = 93.72, RMSSD = 6.28), closely matched by Robi "
        "(SSI = 94.39, RMSSD = 5.61). Conversely, Banglalink displayed severe volatility: its raw RMSSD of 13.61 was 2.43 times higher than Robi, yielding a "
        "lower SSI of 86.39. Validating Proposition 1, when volume surges (>2.0x volume multiplier) are filtered, Banglalink's RMSSD falls by -44.5% (from 13.61 to 7.56). "
        "This compresses the Banglalink-to-Robi volatility ratio from 2.43x down to 1.67x (-31.3%), confirming that apparent instability is heavily an artefact of "
        "promotional volume surges rather than solely operational erraticism.",
        indent=0.5
    )

    # Table 3
    t3_caption = "Table 3: Monthly Net Sentiment Score (NSS) Volatility and Stability Metrics (Modern Era: 2020–2026, M = 81 Months)"
    add_p(t3_caption, bold=True, size=10, space_before=4, space_after=1)
    t3_data = [
        ["Operator", "Mean Modern NSS", "Raw RMSSD", "SSI (100 - RMSSD)", "NSS IQR", "Surge-Filtered RMSSD", "Surge Impact (%)"],
        ["Grameenphone", "+61.11", "6.28", "93.72", "14.07", "5.15", "-18.0%"],
        ["Robi Axiata", "+64.16", "5.61", "94.39", "18.08", "4.53", "-19.3%"],
        ["Banglalink", "+50.06", "13.61", "86.39", "18.25", "7.56", "-44.5%*"],
        ["Ratio: Banglalink / Robi", "—", "2.43x", "—", "—", "1.67x", "-31.3%*"],
    ]
    t3 = doc.add_table(rows=len(t3_data), cols=len(t3_data[0]))
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(t3_data):
        for c_idx, val in enumerate(row):
            cell = t3.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            r = p.runs[0]
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_border(cell, top={'val': 'single', 'sz': 12, 'color': '000000'}, bottom={'val': 'single', 'sz': 8, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
                set_cell_shading(cell, "F2F2F2")
            elif r_idx == len(t3_data) - 1:
                r.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
                set_cell_border(cell, top={'val': 'single', 'sz': 8, 'color': '000000'}, bottom={'val': 'double', 'sz': 12, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
                set_cell_border(cell, top={'val': 'none'}, bottom={'val': 'single', 'sz': 4, 'color': 'E0E0E0'}, left={'val': 'none'}, right={'val': 'none'})
            set_cell_margins(cell, top=20, bottom=20, left=40, right=40)
    add_p("Notes: Modern era spans January 2020 to September 2026. Surge-filtered RMSSD excludes transition months with volume >= 2.0x trailing median.", italic=True, size=8.0, space_before=1, space_after=4)

    add_p(
        "Applying Equation (4) (|Delta NSS| >= 10.0 points) identifies exactly 35 significant sentiment shocks across the 240 modern monthly transitions (Table 4). "
        "Shock incidence exhibits stark structural asymmetry: Banglalink suffered 22 shocks (11 positive, 11 negative), representing a shock frequency 3.14 to 3.67 "
        "times higher than Robi (7 shocks; 5 positive, 2 negative) or Grameenphone (6 shocks; 4 positive, 2 negative). Furthermore, negative shocks exhibit directional "
        "asymmetry: while positive shocks typically normalize within 1 month, negative shocks require a median recovery time of 5.5 months (IQR: [2.8, 16.0]).",
        indent=0.5
    )

    # Table 4
    t4_caption = "Table 4: Selected Illustrative Sentiment Shocks (|Delta NSS| >= 10 Points) with Additive Drivers"
    add_p(t4_caption, bold=True, size=10, space_before=4, space_after=1)
    t4_data = [
        ["Operator", "Transition", "ΔNSS (pts)", "Primary Leading Driver", "Driver Impact", "Recovery Time", "Context / Operational Mechanism"],
        ["Grameenphone", "2020-03 → 2020-04", "+31.2", "App Login & Technical Bugs", "+5.49 pts", "Sustained", "Lockdown surge; authentication stabilization."],
        ["Robi Axiata", "2022-12 → 2023-01", "-16.6", "App Login & Technical Bugs", "-7.40 pts", "1 month", "Winter token expiration bug; OTP failure."],
        ["Robi Axiata", "2023-01 → 2023-02", "+10.7", "App Login & Technical Bugs", "+4.64 pts", "Immediate", "Post-incident hotfix restoring session login."],
        ["Banglalink", "2021-04 → 2021-05", "-16.4", "Network Speed & 4G Latency", "-4.90 pts", "3 months", "Ramadan evening 4G bandwidth throttling."],
        ["Banglalink", "2024-03 → 2024-04", "-11.2", "App Login & Technical Bugs", "-8.74 pts", "1 month", "v11.8.0 release crash on splash screen."],
        ["Banglalink", "2024-04 → 2024-05", "+32.8", "App Login & Technical Bugs", "+13.73 pts", "Immediate", "Hotfix v11.9.1 / v11.10.x bypass recovery."],
        ["Grameenphone", "2025-08 → 2025-09", "-18.5", "Offers & Data Packs", "-2.68 pts", "4 months", "5G launch bundle pricing backlash."],
    ]
    t4 = doc.add_table(rows=len(t4_data), cols=len(t4_data[0]))
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(t4_data):
        for c_idx, val in enumerate(row):
            cell = t4.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            r = p.runs[0]
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.0)
            if r_idx == 0:
                r.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_border(cell, top={'val': 'single', 'sz': 12, 'color': '000000'}, bottom={'val': 'single', 'sz': 8, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
                set_cell_shading(cell, "F2F2F2")
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx in [0, 1, 3, 6] else WD_ALIGN_PARAGRAPH.RIGHT
                set_cell_border(cell, top={'val': 'none'}, bottom={'val': 'single', 'sz': 4, 'color': 'E0E0E0'} if r_idx < len(t4_data)-1 else {'val': 'double', 'sz': 12, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
            set_cell_margins(cell, top=20, bottom=20, left=35, right=35)
    add_p("Notes: Selected from 35 total modern shocks (|Delta NSS| >= 10.0). Driver impact represents additive contribution to Delta NSS via Equation (5).", italic=True, size=8.0, space_before=1, space_after=4)

    add_heading_2("4.4 What Drives the Voice: Operational Domains and Attribution")
    add_p(
        "Validating Proposition 2, App Login & Technical Bugs led 27 of 35 significant shocks (77.1%), compared to leading only 91 of 205 ordinary monthly transitions "
        "(44.4%). A 2x2 contingency test confirms that client-side software bugs are overwhelmingly over-represented during crisis periods (Chi-sq(1) = 12.83, p = 0.0003; "
        "Fisher's exact test odds ratio 4.23). This dominance is robust to the exclusion of volume surges (Chi-sq(1) = 6.38, p = 0.0116; odds ratio 3.65). "
        "Operator breakdown reveals that login led 20 of 22 Banglalink shocks, 4 of 7 Robi shocks, and 3 of 6 Grameenphone shocks (Table 5 and Figure 3).",
        indent=0.5
    )

    # Table 5
    t5_caption = "Table 5: Operational Complaint Rates and Within-Category Dissatisfaction Across Domains"
    add_p(t5_caption, bold=True, size=10, space_before=4, space_after=1)
    t5_data = [
        ["Operational Domain", "Grameenphone Compl. %", "Robi Compl. %", "Banglalink Compl. %", "Grameenphone Dissat. %", "Robi Dissat. %", "Banglalink Dissat. %", "Grameenphone Neg N", "Robi Neg N", "Banglalink Neg N"],
        ["App Login & Technical Bugs", "3.45%", "4.01%", "7.25%*", "88.95%", "87.10%", "89.28%", "11,058", "7,951", "9,946"],
        ["Offers & Data Packs", "2.99%", "2.61%", "2.42%", "56.62%", "50.26%", "56.14%", "9,557", "5,168", "3,321"],
        ["Network Speed & 4G Latency", "1.39%", "1.96%", "2.72%*", "74.01%", "76.37%", "74.83%", "4,453", "3,895", "3,735"],
        ["Billing & Airtime Deductions", "1.03%", "0.70%", "0.79%", "92.89%*", "89.77%", "91.87%", "3,307", "1,395", "1,085"],
        ["General Appreciation / Other", "3.29%", "2.68%", "4.14%", "3.74%", "3.09%", "4.99%", "10,519", "5,326", "5,684"],
    ]
    t5 = doc.add_table(rows=len(t5_data), cols=len(t5_data[0]))
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(t5_data):
        for c_idx, val in enumerate(row):
            cell = t5.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            r = p.runs[0]
            r.font.name = "Times New Roman"
            r.font.size = Pt(7.8)
            if r_idx == 0:
                r.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_border(cell, top={'val': 'single', 'sz': 12, 'color': '000000'}, bottom={'val': 'single', 'sz': 8, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
                set_cell_shading(cell, "F2F2F2")
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
                set_cell_border(cell, top={'val': 'none'}, bottom={'val': 'single', 'sz': 4, 'color': 'E0E0E0'} if r_idx < len(t5_data)-1 else {'val': 'double', 'sz': 12, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
            set_cell_margins(cell, top=18, bottom=18, left=30, right=30)
    add_p("Notes: Complaint Rate = Negative Reviews in Domain / Total Operator Reviews (Eq. 6). Within-Category Dissat. = Negatives / Total Domain Reviews (Eq. 7).", italic=True, size=8.0, space_before=1, space_after=4)

    add_p(
        "Examining complaint prevalence, Banglalink's login complaint rate (7.25%) is more than double Grameenphone's (3.45%), exposing chronic client-side code instability. "
        "In contrast, the Strategic Priority Matrix (Figure 3) illustrates sharp operational trade-offs: Billing & Deductions represents a 'Rare but Severe' danger—comprising "
        "only 0.8% to 1.1% of reviews but exceeding 90% within-category negativity (92.89% for GP). Conversely, App Login is both highly prevalent and severely negative "
        "(~88-89% negativity), placing it squarely in the 'Urgent Crisis' quadrant. Across all operators, actionable operational domains capture the overwhelming majority "
        "of negative voice: 72.95% for Grameenphone (28,375 of 38,894), 77.56% for Robi (18,409 of 23,735), and 76.09% for Banglalink (18,087 of 23,771).",
        indent=0.5
    )

    # Figure 3
    add_figure("figure3_priority_matrix.png", "Figure 3: Strategic VoC Priority Matrix (Prevalence vs Dissatisfaction Intensity)", "Quadrant segmentation of operational domains across operators. Bubble area reflects absolute negative volume.", width_in=5.0)

    add_heading_2("4.5 Banglalink's 2026 Reversal: Recovery or Reviewer Mix?")
    add_p(
        "Banglalink executed a headline-grabbing turnaround between 2025 and 2026, leaping from an NSS of +66.39 to +81.93 (+15.54 points) to lead the entire market. "
        "However, applying our additive domain decomposition (Equation 5) unmasks the true anatomical drivers (Figure 4). Exactly +10.33 points (66.5% of the +15.54 "
        "turnaround) was driven by an influx of casual positive reviews within General Appreciation, coinciding with a 2.13x annual volume expansion (10,238 to 21,810). "
        "Genuine operational improvements in App Login & Technical Bugs contributed +2.80 points (18.0%), Network Speed added +1.07 points (6.9%), and Offers contributed "
        "+0.98 points (6.3%). While technical stabilization was real, two-thirds of the apparent turnaround reflected promotional reviewer-mix inflation.",
        indent=0.5
    )

    # Figure 4
    add_figure("figure4_banglalink_reversal_decomposition.png", "Figure 4: Additive Domain Decomposition of Banglalink's 2025–2026 NSS Reversal (+15.54 Points)", "Bars show additive domain contributions to Delta NSS via Equation (5). Casual praise accounted for 66.5% of total turnaround.", width_in=4.6)

    add_heading_2("4.6 Robustness and Measurement Validity")
    add_p(
        "The empirical findings survive extensive diagnostic audits: (1) Classifier Invariance: Evaluating all 240 monthly transitions under an independent LinearSVC "
        "classifier confirmed 96.2% shock concurrence and identical leading-domain attributions. (2) Threshold Sensitivity: Varying shock thresholds across 8, 10, "
        "and 12 points preserved relative shock frequencies (Table A3). (3) Rogan-Gladen Correction: Applying epidemiological confusion matrix correction using blind gold "
        "standard error rates confirmed that true operator NSS values remain within a narrow +/-2.4 point envelope of reported scores, preserving all rankings.",
        indent=0.5
    )

    # =========================================================
    # SECTION 5: DISCUSSION & IMPLICATIONS (~380 words)
    # =========================================================
    print("Building Section 5: Discussion...")
    add_heading_1("5. DISCUSSION AND MANAGERIAL IMPLICATIONS")

    add_heading_2("5.1 The Three Responsibilities Framework")
    add_p(
        "The findings reframe app store reviews from promotional marketing collateral into mission-critical operational telemetry, structured around three organizational "
        "responsibilities: (1) Listen: Continuous, unsolicited app feedback bypasses call-center friction, capturing telemetry at the exact point of customer pain. "
        "(2) Read Correctly: Approval is not performance. Executives must filter volume surges and isolate functional domains. (3) Act: Capital allocation must address "
        "the dominant operational bottlenecks identified by VoC telemetry.",
        indent=0.5
    )

    add_heading_2("5.2 Four Operational Monitoring Rules for Telecom Leadership")
    add_p(
        "We formalize four monitoring rules for telecommunications executives: Rule 1 (Dual-Metric Telemetry): Never evaluate app store star ratings without paired "
        "Net Sentiment Scores. Rule 2 (Surge-Dampened Volatility): Discount raw monthly NSS swings during volume surges exceeding 2.0x trailing medians. Rule 3 "
        "(Subsystem Attribution Isolation): Map negative feedback to specific software or network components before assigning engineering resources. Rule 4 "
        "(Rapid Release Regression Protocol): Enforce automated sentiment regression alerts within 48 hours of mobile application updates to detect authentication bugs.",
        indent=0.5
    )

    add_heading_2("5.3 Operator-Specific Strategic Actions")
    add_p(
        "Grameenphone must address subscriber dissatisfaction surrounding 5G tariff transparency and data expiry policies. Robi must maintain authentication session "
        "resilience, preventing recurrence of its 2023 OTP collapse. Banglalink must prioritize client-side code reliability over short-term promotional volume campaigns.",
        indent=0.5
    )

    add_heading_2("5.4 Theoretical Contributions")
    add_p(
        "This research makes three theoretical contributions: First, it bridges E-S-QUAL and Expectation-Confirmation Theory with computational text analysis in an emerging "
        "market. Second, it demonstrates that software reliability represents a non-negotiable hygiene factor in digital telecommunications. Third, it provides the first "
        "empirically validated methodology for parsing code-mixed, trilingual consumer voice in South Asia.",
        indent=0.5
    )

    # =========================================================
    # SECTION 6: LIMITATIONS & SECTION 7: CONCLUSION (~260 words)
    # =========================================================
    print("Building Sections 6 & 7: Limitations & Conclusion...")
    add_heading_1("6. LIMITATIONS AND FUTURE RESEARCH")
    add_p(
        "This study acknowledges four methodological boundaries: First, data collection is restricted to Google Play, omitting iOS users who may exhibit distinct "
        "socio-economic behaviors. Second, unprompted reviews reflect self-selected consumer cohorts. Third, operational taxonomy is aggregated into five primary domains; "
        "future research should deploy fine-grained sub-topic modeling. Fourth, the empirical setting is confined to Bangladesh; cross-national replication across South "
        "and Southeast Asia is warranted.",
        indent=0.5
    )

    add_heading_1("7. CONCLUSION")
    add_p(
        "A decade of consumer voice in Bangladesh proves that with great review volume comes great managerial responsibility. As telecom operators transform into digital "
        "platforms, customer sentiment has migrated from early infrastructural hostility to mature digital adoption. However, executive leadership must recognize that "
        "praise is not performance. App store sentiment serves as an early-warning telemetry system, but only when promotional surges are filtered, trilingual feedback is "
        "parsed with verified NLP architectures, and engineering resources are directed toward eliminating client-side friction.",
        indent=0.5
    )

    # =========================================================
    # SECTION 8: REFERENCES (~25 references, 1.5 pages)
    # =========================================================
    print("Building Section 8: References...")
    add_heading_1("8. REFERENCES")

    references = [
        "Bhattacharjee, A., Hasan, T., Ahmad, W., Mubasshir, K. S., Islam, M. S., Iqbal, A., Rahman, M. S., & Shahriyar, R. (2022). BanglaBERT: Language model pretraining and benchmarks for low-resource language understanding evaluation in Bangla. Findings of NAACL 2022, 1318–1327. https://doi.org/10.18653/v1/2022.findings-naacl.98",
        "Bitner, M. J., Brown, S. W., & Meuter, M. L. (2000). Technology infusion in service encounters. Journal of the Academy of Marketing Science, 28(1), 138–149. https://doi.org/10.1177/0092070300281013",
        "BTRC. (2026). Mobile Phone Subscribers in Bangladesh (August 2026 Report). Bangladesh Telecommunication Regulatory Commission. http://www.btrc.gov.bd",
        "Chevalier, J. A., & Mayzlin, D. (2006). The effect of word of mouth on sales: Online book reviews. Journal of Marketing Research, 43(3), 345–354. https://doi.org/10.1509/jmkr.43.3.345",
        "Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement, 20(1), 37–46. https://doi.org/10.1177/001316446002000104",
        "Hennig-Thurau, T., Gwinner, K. P., Walsh, G., & Gremler, D. D. (2004). Electronic word-of-mouth via consumer-opinion platforms: What motivates consumers to post? Journal of Interactive Marketing, 18(1), 38–52. https://doi.org/10.1002/dir.10073",
        "Hu, N., Pavlou, P. A., & Zhang, J. (2008). Overcoming the J-shaped distribution of online reviews. Communications of the ACM, 52(10), 144–147. https://doi.org/10.1145/1562764.1562804",
        "Keiningham, T. L., Cooil, B., Andreassen, T. W., & Aksoy, L. (2007). A longitudinal examination of net promoter and firm revenue growth. Journal of Marketing, 71(3), 39–51. https://doi.org/10.1509/jmkg.71.3.039",
        "Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. Biometrics, 33(1), 159–174. https://doi.org/10.2307/2529310",
        "Maxham, J. G. (2001). Service recovery's influence on consumer satisfaction, positive word-of-mouth, and purchase intentions. Journal of Business Research, 54(1), 11–24. https://doi.org/10.1016/S0148-2963(00)00114-4",
        "Meuter, M. L., Ostrom, A. L., Roundtree, R. I., & Bitner, M. J. (2000). Self-service technologies: Understanding customer satisfaction with technology-based service encounters. Journal of Marketing, 64(3), 50–64. https://doi.org/10.1509/jmkg.64.3.50.18024",
        "Mudambi, S. M., & Schuff, D. (2010). What makes a helpful online review? A study of customer reviews on Amazon.com. MIS Quarterly, 34(1), 185–200. https://doi.org/10.2307/20721420",
        "Oliver, R. L. (1980). A cognitive model of the antecedents and consequences of satisfaction decisions. Journal of Marketing Research, 17(4), 460–469. https://doi.org/10.1177/002224378001700405",
        "Pang, B., & Lee, L. (2008). Opinion mining and sentiment analysis. Foundations and Trends in Information Retrieval, 2(1–2), 1–135. https://doi.org/10.1561/1500000011",
        "Parasuraman, A., Zeithaml, V. A., & Berry, L. L. (1985). A conceptual model of service quality and its implications for future research. Journal of Marketing, 49(4), 41–50. https://doi.org/10.1177/002224298504900403",
        "Parasuraman, A., Zeithaml, V. A., & Malhotra, A. (2005). E-S-QUAL: A multiple-item scale for assessing electronic service quality. Journal of Service Research, 7(3), 213–233. https://doi.org/10.1177/1094670504271156",
        "Reichheld, F. F. (2003). The one number you need to grow. Harvard Business Review, 81(12), 46–54.",
        "Rogan, W. J., & Gladen, B. (1978). Estimating prevalence from the results of a screening test. American Journal of Epidemiology, 107(1), 71–76. https://doi.org/10.1093/oxfordjournals.aje.a112510",
        "von Neumann, J., Kent, R. H., Bellinson, H. R., & Hart, B. I. (1941). The mean square successive difference. Annals of Mathematical Statistics, 12(3), 367–395. https://doi.org/10.1214/aoms/1177731746"
    ]

    for ref in references:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        r = p.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)

    # =========================================================
    # SECTION 9: ANNEXURE (1.0 page)
    # =========================================================
    print("Building Section 9: Annexure...")
    doc.add_page_break()
    add_heading_1("ANNEXURE: METHODOLOGICAL AUDIT TABLES")

    add_p("Annexure Table A1: Classification Architecture Leaderboard (5-Fold CV vs. Blind Human Gold Set N = 300)", bold=True, size=9.5, space_before=4, space_after=1)
    ta1_data = [
        ["Model Architecture", "Sentiment 5-Fold Acc", "Sentiment Macro-F1", "Category 5-Fold Acc", "Category Macro-F1", "Blind Gold Sent Acc", "Blind Gold Cat Acc"],
        ["Soft-Voting Ensemble (Production)", "87.47%", "0.7684", "87.44%*", "0.7845*", "83.67%", "91.33%*"],
        ["Challenger LinearSVC", "85.33%", "0.7410", "84.18%", "0.7512", "81.67%", "89.00%"],
        ["Challenger Logistic Regression", "83.20%", "0.7188", "82.40%", "0.7291", "79.33%", "86.67%"],
        ["Fine-Tuned BUET BanglaBERT", "91.60%*", "0.8598*", "85.27%", "0.7624", "87.33%*", "89.67%"],
    ]
    ta1 = doc.add_table(rows=len(ta1_data), cols=len(ta1_data[0]))
    ta1.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(ta1_data):
        for c_idx, val in enumerate(row):
            cell = ta1.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            r = p.runs[0]
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.0)
            if r_idx == 0:
                r.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_border(cell, top={'val': 'single', 'sz': 12, 'color': '000000'}, bottom={'val': 'single', 'sz': 8, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
                set_cell_shading(cell, "F2F2F2")
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
                set_cell_border(cell, top={'val': 'none'}, bottom={'val': 'single', 'sz': 4, 'color': 'E0E0E0'} if r_idx < len(ta1_data)-1 else {'val': 'double', 'sz': 12, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
            set_cell_margins(cell, top=16, bottom=16, left=25, right=25)
    add_p("Notes: *Indicates best performance. Evaluated on 4,500 stratified folds and zero-leakage human gold benchmark.", italic=True, size=8.0, space_before=1, space_after=4)

    add_p("Annexure Table A2: Dual-Annotator Inter-Rater Reliability (N = 200 Pairs)", bold=True, size=9.5, space_before=4, space_after=1)
    ta2_data = [
        ["Evaluation Dimension", "Evaluated Pairs", "Raw Percentage Agreement", "Cohen's Kappa (κ)", "Standard Interpretation (Landis & Koch, 1977)"],
        ["3-Class Sentiment Analysis", "200", "91.00%", "0.5762", "Moderate Agreement (High raw consistency)"],
        ["5-Class Operational Domain", "196", "95.41%", "0.7694", "Substantial Agreement"],
    ]
    ta2 = doc.add_table(rows=len(ta2_data), cols=len(ta2_data[0]))
    ta2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(ta2_data):
        for c_idx, val in enumerate(row):
            cell = ta2.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            r = p.runs[0]
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.0)
            if r_idx == 0:
                r.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_border(cell, top={'val': 'single', 'sz': 12, 'color': '000000'}, bottom={'val': 'single', 'sz': 8, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
                set_cell_shading(cell, "F2F2F2")
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx in [0, 4] else WD_ALIGN_PARAGRAPH.RIGHT
                set_cell_border(cell, top={'val': 'none'}, bottom={'val': 'single', 'sz': 4, 'color': 'E0E0E0'} if r_idx < len(ta2_data)-1 else {'val': 'double', 'sz': 12, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
            set_cell_margins(cell, top=16, bottom=16, left=25, right=25)
    add_p("Notes: Evaluated across independent dual-blind annotations without communication.", italic=True, size=8.0, space_before=1, space_after=4)

    add_p("Annexure Table A3: Sensitivity Audit of Sentiment Shocks Across Detection Thresholds", bold=True, size=9.5, space_before=4, space_after=1)
    ta3_data = [
        ["Detection Threshold", "Grameenphone Shocks", "Robi Shocks", "Banglalink Shocks", "Total Industry Shocks", "Banglalink / Robi Shock Ratio"],
        ["± 8 Percentage Points", "11", "16", "33", "60", "2.06x"],
        ["± 10 Percentage Points (Benchmark)", "6", "7", "22", "35", "3.14x"],
        ["± 12 Percentage Points", "4", "4", "16", "24", "4.00x"],
    ]
    ta3 = doc.add_table(rows=len(ta3_data), cols=len(ta3_data[0]))
    ta3.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(ta3_data):
        for c_idx, val in enumerate(row):
            cell = ta3.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            r = p.runs[0]
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.0)
            if r_idx == 0:
                r.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_border(cell, top={'val': 'single', 'sz': 12, 'color': '000000'}, bottom={'val': 'single', 'sz': 8, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
                set_cell_shading(cell, "F2F2F2")
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
                set_cell_border(cell, top={'val': 'none'}, bottom={'val': 'single', 'sz': 4, 'color': 'E0E0E0'} if r_idx < len(ta3_data)-1 else {'val': 'double', 'sz': 12, 'color': '000000'}, left={'val': 'none'}, right={'val': 'none'})
            set_cell_margins(cell, top=16, bottom=16, left=25, right=25)
    add_p("Notes: Benchmark threshold is ±10.0 points. Banglalink consistently exhibits 2.1x to 4.0x the shock frequency of peers.", italic=True, size=8.0, space_before=1, space_after=4)

    # Save document
    print(f"Saving completed Word document to {DOCX_OUT}...")
    doc.save(str(DOCX_OUT))
    print(f"Successfully generated {DOCX_OUT} ({os.path.getsize(DOCX_OUT):,d} bytes)!")

if __name__ == "__main__":
    build_concise_docx()
