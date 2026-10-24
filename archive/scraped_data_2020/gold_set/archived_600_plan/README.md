# Archived Exploratory 600-Sample Gold Standard Plan

> **Archive Notice**: The files in this directory are preserved strictly for historical record and experimental provenance. They represent an early, exploratory 600-sample evaluation plan that was **discarded and never executed** as a human annotation study.

---

## 1. Historical Context

During early pipeline prototyping, an initial concept proposed drawing an $N = 600$ candidate pool (200 reviews per operator across Grameenphone, Banglalink, and Robi) for gold standard validation. Preliminary scripts and heuristic tests were run against this pool.

However, comprehensive manual human annotation for 600 reviews was **never performed**. The plan was formally discarded in favor of a scoped, rigorously controlled blind human study:

* **Authentic Primary Ground Truth ($N = 300$)**: 300 reviews manually and independently annotated under blind conditions by Ratul ([`../blind_annotation_300_ratul.csv`](../blind_annotation_300_ratul.csv)).
* **Dual-Annotator Reliability Benchmark ($N = 200$)**: 200 overlapping reviews independently annotated under blind conditions by a second reviewer ([`../blind_annotation_200_friend.csv`](../blind_annotation_200_friend.csv)) to measure inter-annotator reliability via Cohen's Kappa ($\kappa$).

All active project reports, paper manuscripts, and repository documentation reference the authentic $N = 300$ / $N = 200$ human ground truth.

---

## 2. Directory Contents

| File / Folder | Original Purpose | Archival Reason |
| :--- | :--- | :--- |
| [`blind_annotation_600_ratul.csv`](blind_annotation_600_ratul.csv) | Early 600-sample template generated for blind annotation | Discarded when actual annotation was scoped to $N = 300$ ([`../blind_annotation_300_ratul.csv`](../blind_annotation_300_ratul.csv)). |
| [`gold_set_candidates.csv`](gold_set_candidates.csv) | Stratified 600-sample candidate pool | Initial candidate pool drafted before blind sampling protocol. |
| [`gold_set_verified.csv`](gold_set_verified.csv) | Preliminary 600-sample dataset used in early tests | Replaced by verified blind human annotations ($N = 300$ / $N = 200$). |
| [`evaluate_gold_set.py`](evaluate_gold_set.py) | Benchmark evaluation script for `gold_set_verified.csv` | Replaced by [`../calculate_agreement.py`](../calculate_agreement.py). |
| [`prepare_gold_set.py`](prepare_gold_set.py) | Interactive CLI candidate sampler & verifier | Prototype utility replaced by standard blind annotation workflow. |
| [`generate_blind_samples.py`](generate_blind_samples.py) | Script that sampled 600 candidates for Ratul | Archived; actual study executed on 300 primary reviews. |
| [`plots/`](plots/) | 4 publication plots based on preliminary $N = 600$ dataset | Visualized the preliminary 600-sample benchmark (Confusion matrices, F1 bars, operator breakdown). |

---

## 3. Active Ground-Truth Benchmark

For active benchmarks, reports, and methodology, refer to the parent directory:
- **Primary Human Dataset**: [`../blind_annotation_300_ratul.csv`](../blind_annotation_300_ratul.csv)
- **Consensus / Verification Dataset**: [`../blind_annotation_200_friend.csv`](../blind_annotation_200_friend.csv)
- **Annotation Guidelines**: [`../ANNOTATION_RULEBOOK.md`](../ANNOTATION_RULEBOOK.md)
- **Empirical Evaluation Report**: [`../gold_standard_evaluation_report.md`](../gold_standard_evaluation_report.md)
- **Agreement & Reliability Calculator**: [`../calculate_agreement.py`](../calculate_agreement.py)
