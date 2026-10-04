# 📘 Telecom Voice-of-Customer Annotation Rulebook & Sorting Guidelines
**Prepared for Blind Ground Truth Annotation (Sentiment & Operational Comment Types)**  
*Language Scope: Bengali (বাংলা), Phonetic Banglish (Romanized Bengali), and English.*

---

## 🎯 Purpose of This Rulebook
This rulebook establishes clear, consistent, and objective annotation standards for sorting ambiguous and complex customer reviews across **Grameenphone (MyGP)**, **Banglalink (MyBL)**, and **Robi (MyRobi)**. 

To eliminate unintentional confirmation bias, **all model suggestions are hidden**. When annotating, base your decision strictly on the semantic content of the text using the principles below.

---

## 🏷️ 1. Sentiment Annotation Guidelines (3 Classes)

Target classes: `Positive`, `Neutral`, `Negative`.

| Sentiment | Definition | Core Indicator |
| :--- | :--- | :--- |
| **`Positive`** | Expresses satisfaction, gratitude, happiness, praise, or enthusiasm. | Satisfied user experience, value appreciation, compliments. |
| **`Neutral`** | Objective statements, feature requests without anger, questions, or mixed/unclear emotion. | Factual inquiries, calm suggestions, neither happy nor angry. |
| **`Negative`** | Expresses dissatisfaction, anger, frustration, technical failure, or financial complaint. | Service disruption, billing grievances, slow speeds, bugs, insults. |

---

### 🔍 Edge-Case Decision Matrix (How to Handle Confusing Reviews)

### Case 1: Sarcasm, Mockery & Irony
* **The Trap**: The reviewer gives 5 stars and writes words like *"সেরা"* (best), *"দারুণ"* (great), or *"ধন্যবাদ"* (thanks), but the context is mockery.
* **Examples**:
  * *"লোট পাটের জন্য সেরা রে"* (5★) ➔ **`Negative`** *(Meaning: "Best for looting customers")*
  * *"টাকা কাটার চমৎকার নিয়ম"* (5★) ➔ **`Negative`** *(Meaning: "Wonderful system for deducting money")*
  * *"Best scam company ever"* (5★) ➔ **`Negative`**
* **Golden Rule**: **Always label sarcastic grievances as `Negative`**. The star rating is intentional sarcasm.

---

### Case 2: Star-Rating vs. Review Text Contradiction
* **The Trap**: Touchscreen slips often lead to 1-star ratings with glowing praise, or 5-star ratings with furious complaints.
* **Examples**:
  * *"Onek valo app, sob service sundor"* (1★) ➔ **`Positive`** *(User clearly loves the app; 1★ was an accidental click).*
  * *"Faltu network, mb kete ney"* (5★) ➔ **`Negative`** *(User expresses anger; 5★ was accidental or sarcastic).*
* **Golden Rule**: **Text ALWAYS overrides the Star Rating.** If the text has clear semantic meaning, ignore the star rating. Only look at star rating if the text is pure gibberish (e.g. *"ghjkl"*).

---

### Case 3: Mixed Reviews (Praise + Complaint)
* **The Trap**: A single review contains both a compliment and a grievance.
* **Examples**:
  * *"App interface is very good, but network speed is extremely slow and cuts balance."*
  * *"MyBL app is fast, but recharge offer price is too high."*
* **Resolution Precedence**:
  1. In Voice-of-Customer operations, **functional service grievances take priority over aesthetic praise**.
  2. If the user criticizes core service (network, billing, bugs, pricing), label as **`Negative`**.
  3. If the praise is dominant and the complaint is merely a mild, polite wish (*"Love the app! Please add dark mode"*), label as **`Positive`**.

---

### Case 4: The Boundary of `Neutral` (Lukewarm vs. Truly Neutral)
* **Rule**:
  * Single lukewarm words with 3★ rating (*"ok"*, *"hmm"*, *"normal"*, *"cholbe"*, *"thik ache"*, *"so so"*): ➔ **`Neutral`**.
  * Clearly positive words (*"good"*, *"valo"*, *"nice"*, *"besh"*, *"superb"*): ➔ **`Positive`**.
  * Purely informative/factual statements without emotion (*"Login completed"*, *"Update korlam"*): ➔ **`Neutral`**.

---

### Case 5: Feature Requests & Inquiries
* **Rule**:
  * Calm feature requests or questions: 
    * *"eSIM support kobe ashbe?"* ➔ **`Neutral`**
    * *"Please add bKash auto-recharge and dark mode"* ➔ **`Neutral`**
  * Feature requests coupled with frustration or anger:
    * *"Why doesn't this rubbish app have bKash yet? Worst service"* ➔ **`Negative`**
  * Feature requests paired with genuine gratitude:
    * *"Best app in Bangladesh! Please add widget feature"* ➔ **`Positive`**

---

### Case 6: Promotional "Free MB" & Bonus Comments
* **The Trap**: App stores are flooded with users claiming 500MB login bonuses or posting referral codes.
* **Rule**:
  * Simply claiming bonus or posting a code (*"500 MB"*, *"Referral code 12345"*): ➔ **`Neutral`**.
  * Expressing happiness over bonus (*"500MB free pailam onek khushi, thanks Robi"*): ➔ **`Positive`**.
  * Complaining that promised bonus was not given (*"Free 500MB bolar por o dilo na, fake promotion"*): ➔ **`Negative`**.

---

### Case 7: Religious Blessings & Salutations
* **Examples**: *"Alhamdulillah"*, *"Shukriya"*, *"MashaAllah"*, *"Valo thakun sobai"*, *"JazakAllah"*.
* **Rule**: Label as **`Positive`** unless followed by a negative grievance. Expressions of gratitude indicate positive customer sentiment.

---

### Case 8: Slang, Insults & Profanity
* **Words**: *"Faltu"*, *"Bakwas"*, *"Chor"*, *"Dakat"*, *"Baje"*, *"Bogus"*, *"Gadha"*, *"Fraud"*, *"Bal"*.
* **Rule**: Always **`Negative`**.

---

## 🏷️ 2. Operational Category Guidelines (5 Classes)

If annotating operational category, assign each review to exactly one primary bucket:

| Category Code | Category Name | Scope & Examples |
| :---: | :--- | :--- |
| **1** | **`Billing & Airtime Deductions`** | Unexplained balance deductions, airtime cuts, emergency balance fees, unwanted VAS subscriptions, SMS charges, recharge not reflecting. |
| **2** | **`App Login & Technical Bugs`** | OTP not received, fingerprint/biometric failures, app crashes on startup, update loops, black screen, UI frozen, loading spinner stuck. |
| **3** | **`Network Speed & 4G Latency`** | Slow internet, 4G dropping to 2G/3G, YouTube buffering, high ping/gaming lag, call drops, no network coverage indoors. |
| **4** | **`Offers & Data Packs`** | High data pack prices, short validity (e.g. 3-day validity complaints), request for cheaper GB, "Amar Offer" relevance, minute bundle pricing. |
| **5** | **`General Appreciation / Other`** | General app praise (*"Good app"*, *"Five star"*), store rating praise, non-telecom complaints, or general salutations. |

---

## ⚡ Quick-Reference Annotation Cheat Sheet

```text
Review Text                                          | Rating | Correct Sentiment | Primary Category
----------------------------------------------------------------------------------------------------------------------
"MB kete ney taka o nai kono offer o bhalo na"      | 1★     | Negative          | Billing & Airtime Deductions
"Emergency balance option ta khub kaje dey"          | 5★     | Positive          | Offers & Data Packs
"Update er por theke OTP ashe na login hoy na"      | 1★     | Negative          | App Login & Technical Bugs
"Net speed onek bhalo kintu dam ektu beshi"          | 3★     | Negative          | Offers & Data Packs
"Dark mode option ta add korle bhalo hoto"           | 4★     | Neutral           | General Appreciation / Other
"Looting er jonno 5 star dilam"                      | 5★     | Negative          | Billing & Airtime Deductions
"Valo"                                               | 1★     | Positive          | General Appreciation / Other
"Normal app cholbe"                                  | 3★     | Neutral           | General Appreciation / Other
"Alhamdulillah khub sundor service"                  | 5★     | Positive          | General Appreciation / Other
"Faltu network gram e kono 4G thake na"              | 1★     | Negative          | Network Speed & 4G Latency
```
