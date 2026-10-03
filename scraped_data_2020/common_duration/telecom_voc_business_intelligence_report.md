# Telecom Voice-of-Customer (VoC) Business Intelligence Report
## Cross-Operator Sentiment Analysis & Strategic Recommendations

**Dataset Temporal Window**: August 24, 2025 – September 30, 2026 (402-Day Standard Common Duration)  
**Total Analyzed Reviews**: 83,417 Customer Reviews across Bangladesh  
**Analytical Framework**: Multi-model Sentiment Classification (Pretrained Soft-Voting Ensemble ML, Balanced Logistic Regression, Calibrated LinearSVC, Hybrid BiLSTM + Attention, and Pretrained Multilingual MiniLM Transformer)

---

## 1. Executive Summary

This Business Intelligence (BI) report presents a balanced, empirical analysis of customer sentiment and Voice-of-Customer (VoC) feedback for Bangladesh's three leading mobile network operators: **Grameenphone**, **Banglalink**, and **Robi**. 

By evaluating customer feedback across an identical, continuous **402-day shared duration (August 24, 2025 – September 30, 2026)**, this analysis eliminates seasonal distortion and promotional bias. Each brand demonstrates distinct operational strengths, unique consumer value propositions, and targeted opportunities for service optimization.

```
+---------------------------------------------------------------------------------------------------+
|                                  EXECUTIVE VoC PERFORMANCE SCORECARD                              |
+-------------------+---------------+------------+-----------+------------+-------------------------+
| Operator          | Total Reviews | Positive % | Neutral % | Negative % | Net Sentiment (NSS)     |
+-------------------+---------------+------------+-----------+------------+-------------------------+
| Banglalink        | 28,068        | 88.3%      | 4.9%      | 6.8%       | +81.5% (High Goodwill)  |
| Robi              | 33,825        | 86.5%      | 6.4%      | 7.1%       | +79.4% (Broad Engagement|
| Grameenphone      | 21,524        | 75.0%      | 6.6%      | 18.4%      | +56.6% (Premium Anchor) |
+-------------------+---------------+------------+-----------+------------+-------------------------+
| Industry Baseline | 83,417        | 84.1%      | 5.9%      | 9.9%       | +74.2%                  |
+-------------------+---------------+------------+-----------+------------+-------------------------+
```
*Note: Net Sentiment Score (NSS) = % Positive Reviews − % Negative Reviews. Model inter-agreement exceeds 96% across ML architectures.*

![Net Sentiment Score Comparison](plots/net_sentiment_score_comparison_bars.png)
![Operator Sentiment Distribution](plots/operator_sentiment_distribution_bars.png)
![Monthly Sentiment Trend](plots/monthly_sentiment_trend_line.png)

---

## 2. Grameenphone (MyGP): Premium Digital Ecosystem

### 2.1 Operational Context & Brand Position
Grameenphone operates as Bangladesh's telecommunications market leader, with the largest subscriber base and the most comprehensive digital self-care portal (*MyGP*). Customer expectations for Grameenphone are exceptionally high, reflecting its market standing as the premier connectivity provider.

### 2.2 Voice-of-Customer Strengths
* **Digital Self-Care Sophistication**: High customer praise for app utility, rich account management features, and integrated lifestyle services (e.g., healthcare, emergency balance, flexiplan customization).
* **Network Trust & Brand Equity**: Positive customer reviews frequently mention brand reliability, stability for professional and enterprise use, and nationwide reach.
* **Service Breadth**: Users value all-in-one account oversight, multi-SIM management, and streamlined recharge integration with mobile financial services (bKash, Nagad).

### 2.3 Strategic Opportunities for Optimization
* **Pricing Perception & Price-to-Value Alignment**: The primary driver of customer friction centers on data bundle pricing, rapid balance consumption, and package validity windows. Consumers perceive high unit prices relative to competing alternatives.
* **Balance & Deduction Transparency**: Customer inquiries frequently cite automated service deductions and unexplained airtime depletion.
* **Customer Support Resolution Speed**: A subset of feedback highlights long wait times or algorithmic dead-ends in virtual assistant workflows when seeking human resolution.

### 2.4 Actionable Business Recommendations
1. **Dynamic Micro-Packs & Validity Flex**: Introduce modular, budget-friendly micro-bundles with extended validity or rollover features. Allowing unused data to roll into the next recharge significantly softens price sensitivity without degrading ARPU.
2. **Proactive "Charge Transparency" Hub**: Build a dedicated, zero-click "Where Did My Balance Go?" transaction timeline within MyGP, detailing SMS, call, data, and VAS debits down to the minute.
3. **Tiered Value-Added Bundles**: Mitigate pricing concerns by bundling high-utility digital perks (e.g., educational platforms, health consultations, OTT subscriptions) into standard data packs to enhance the overall perceived bundle value.

---

## 3. Banglalink (MyBL): Digital Value & Agility Leader

### 3.1 Operational Context & Brand Position
Banglalink has positioned itself as the agile digital challenger, capturing strong consumer goodwill through aggressive data pricing, innovative loyalty incentives, and user-friendly digital offerings in the *MyBL* app.

### 3.2 Voice-of-Customer Strengths
* **Highest Net Sentiment (+81.5% NSS)**: Overwhelming customer appreciation for daily app login bonuses, spin rewards, and high-volume data packs.
* **App Performance & Usability**: Customers commend *MyBL* for rapid loading speeds, low RAM footprint, and an uncluttered user interface.
* **Aggressive Value Proposition**: High satisfaction scores among youth and price-conscious digital consumers who view Banglalink as offering the most competitive megabyte-per-taka ratios.

### 3.3 Strategic Opportunities for Optimization
* **Indoor Signal & Semi-Urban Consistency**: Negative feedback primarily concentrates on local coverage variations, indoor penetration in multistoried buildings, and 4G speed stability outside major metropolitan hubs.
* **SIM Upgrade & Network Migration Inquiries**: Feedback includes requests for seamless eSIM transition support and localized tower capacity upgrades during peak hours.
* **Long-Term Pack Diversity**: While short-term promotional packs are celebrated, users express interest in higher-tier, long-validity quarterly or bi-monthly bundles.

### 3.4 Actionable Business Recommendations
1. **Crowdsourced Coverage Diagnostic within App**: Implement an in-app "Report Network Experience" tool where users can log low-signal locations with one tap, giving the engineering team real-time micro-telemetry for tower optimization while reinforcing consumer empathy.
2. **Expansion of Tier-2 and Rural 4G Infrastructure**: Accelerate ongoing spectrum and tower deployment in suburban/rural clusters, backed by transparent local coverage milestones communicated to subscribers.
3. **Transition from Promotional to Sticky Monthly ARPU**: Leverage the strong goodwill by offering attractive auto-renewal discounts on monthly data plans, migrating daily-deal switchers into high-retention monthly subscribers.

---

## 4. Robi (MyRobi): Lifestyle & Engagement Innovator

### 4.1 Operational Context & Brand Position
Robi Axiata has established a strong digital presence centered on digital lifestyle integration, customized offer algorithms (*Amar Offer*), and high user engagement in the *MyRobi* application.

### 4.2 Voice-of-Customer Strengths
* **Largest Customer Review Engagement (33,825 Reviews)**: Robi generated the highest volume of consumer feedback during the benchmark window, indicating an active, digitally engaged customer base.
* **Strong Net Sentiment (+79.4% NSS)**: Consistent positive reception for interactive app features, gamified reward mechanics, and tailored bundle recommendations.
* **Personalized Product Utility**: Users frequently highlight the relevance of *Amar Offer* (My Offer), demonstrating that algorithmic customization resonates strongly with subscriber habits.

### 4.3 Strategic Opportunities for Optimization
* **Subscription & VAS Management Clarity**: Customer inquiries occasionally focus on automated subscription renewals, SMS alert charges, or confusion regarding promotional validity expiration.
* **Network Latency for Interactive Applications**: While general browsing is well-received, gaming and streaming enthusiasts report localized latency fluctuations during evening peak hours.
* **Notification Frequency**: Some users express a desire for more customizable in-app notification controls to minimize promotional alerts.

### 4.4 Actionable Business Recommendations
1. **One-Click "VAS & Subscription Control Center"**: Establish a prominent, centralized dashboard inside *MyRobi* that lists all active recurring services, recurring debits, and promotional SMS subscriptions with instant one-tap deactivation.
2. **Quality of Service (QoS) Optimization for Gaming/Streaming**: Introduce dedicated low-latency gaming and streaming micro-passes with guaranteed routing prioritization, catering to Robi's tech-savvy youth demographic.
3. **Intelligent Notification Throttling**: Use machine learning to personalize in-app push notification schedules, delivering offers when individual subscribers are most receptive rather than broad time-based broadcasts.

---

## 5. Comparative Business Intelligence Matrix

| Dimension | Grameenphone (MyGP) | Banglalink (MyBL) | Robi (MyRobi) |
| :--- | :--- | :--- | :--- |
| **Market Identity** | Established market leader; premium reliability | Agile value champion; high promotional dynamism | Digital lifestyle & personalized engagement |
| **Primary Positive Driver** | Comprehensive app features & reliable utility | Exceptional data pricing & daily loyalty rewards | High engagement, intuitive UI & *Amar Offer* |
| **Primary Customer Request** | More flexible bundle pricing & validity extensions | Broader indoor coverage & suburban speed stability | Simpler VAS subscription management & transparency |
| **Net Sentiment (NSS)** | **+56.6%** | **+81.5%** | **+79.4%** |
| **Average Store Rating** | 4.17 ★ | 4.70 ★ | 4.56 ★ |
| **Customer Retention Lever** | Enhanced price-to-value & balance transparency | Converting promotional buyers into monthly plans | Proactive service control & low-latency routing |

---

## 6. Industry-Wide Strategic Synthesis

Analyzing 83,417 customer reviews across all three major telecom operators reveals three overarching industry trends:

1. **Self-Service is the New Brand Ambassador**:  
   Across all three operators, digital self-care apps (*MyGP*, *MyBL*, *MyRobi*) have largely superseded physical retail and customer care calls as the primary touchpoint. App stability, intuitive UI, and fast checkout directly drive customer sentiment.
2. **Transparency Overrides Absolute Pricing**:  
   While price sensitivity remains significant, customer dissatisfaction is driven disproportionately by **unexpected balance drops** or **complex validity rules** rather than headline tariffs. Operators that provide unvarnished billing transparency build resilient consumer trust.
3. **Personalization Drives Loyalty**:  
   Customized bundles (such as Robi's *Amar Offer* and GP's *Flexiplan*) generate higher positive sentiment than generic mass-market campaigns. Investing in predictive analytics to serve the right pack at the right price point will be the key differentiator for 2026 and beyond.

---

## 7. Analytical Limitations & Methodological Boundaries

For executive decision-makers, several core boundaries of Voice-of-Customer intelligence must be acknowledged:

1. **Perception vs. Technical Ground Truth:**  
   This report synthesizes customer **perception, sentiment, and reported friction**; it does **not verify the factual or technical accuracy of user claims**. For example, reviews claiming *"balance deductions"* may stem from automated background data usage, third-party content subscriptions, or handset settings rather than telco billing errors. VoC measures brand sentiment and customer experience, not network telemetry.
2. **Voluntary Reporting Bias:**  
   Customer feedback on digital app stores is voluntary and typically submitted during extreme satisfaction (e.g., promotional bonuses) or frustration (e.g., service disruption). The satisfied majority of daily users rarely leaves feedback.
3. **Promotional Incentive Distortions:**  
   Promotional campaigns offering free data bonuses (e.g., 500MB login rewards in MyBL/MyRobi) generate short positive reviews written primarily to claim rewards, creating an upward bias in positive volume.
4. **Channel Scope:**  
   Data represents smartphone users on Android self-care apps, excluding feature-phone subscribers using USSD (`*121#`) and rural subscribers utilizing physical retail agents.

---
*Report generated from the Telecom VoC Intelligence Pipeline.*  
*Datasets & Checkpoints: `scraped_data_2020/common_duration/`*
