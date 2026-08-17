# 17–18 - Experiment Design & Power Analysis

## Executive Summary

An online A/B experiment was designed to test the personalized ranking policy against the historical-ranking baseline.

**Experiment design**

* Randomization: **user level**
* Allocation: **50% control / 50% treatment**
* Primary metric: **long-view rate**
* Secondary metrics: like, follow, comment, future 7-day sessions
* Guardrail: hate rate
* Significance level: **5%**
* Power: **80%**

## Power Requirement

Baseline long-view rate is **8.42%**. A 5% relative lift corresponds to a treatment target of **8.84%**, or a **0.42 percentage-point absolute increase**.

User interactions are clustered:

* Average interactions/user: **43.0**
* Estimated ICC: **0.086**
* Design effect: **4.62×**

After adjusting for clustering, approximately **15,000 users** are required to detect a 5% relative lift.

### Conclusion

Interaction-level power calculations substantially underestimate sample requirements when repeated observations from the same users are treated as independent.

The experiment should therefore use **user-level randomization and cluster-aware inference**.

Offline ranking improvements justify testing the challenger, but a launch decision requires statistically significant online improvement in the primary metric without unacceptable guardrail deterioration.
