# 03 — Engagement Metric Validation

## Executive Summary

`long_view` is a credible proxy for higher-quality content consumption and should be used as the **primary quality-engagement signal** in subsequent product analysis.

Across **11.7M recommendation interactions**, long-view interactions are associated with:

* **2.4× higher like rate**
* **5.0× higher follow rate**
* **13.4× higher comment rate**
* **6.7× higher forward rate**
* **5.1× higher profile-entry rate**
* **75% lower hate rate**

The pattern remains directionally consistent across all five major product surfaces for positive downstream behaviors.

`long_view` therefore provides a stronger measure of consumption quality than the broader click/valid-play signal. However, these results are observational and do not establish causality.

---

## 1. Long Views Align with Higher-Intent Engagement

| Metric        | Non-Long View | Long View | Relative Rate |
| ------------- | ------------: | --------: | ------------: |
| Like          |         1.15% |     2.73% |     **2.38×** |
| Follow        |         0.05% |     0.24% |     **4.99×** |
| Comment       |         0.06% |     0.84% |    **13.41×** |
| Forward       |         0.03% |     0.21% |     **6.69×** |
| Profile Entry |         0.86% |     4.40% |     **5.10×** |
| Hate          |         0.12% |     0.03% |     **0.25×** |

Average viewing time also differs substantially:

| Interaction Type | Average Play Time |
| ---------------- | ----------------: |
| Non-Long View    |           3.0 sec |
| Long View        |          48.0 sec |

### Conclusion

Long-view interactions consistently coincide with behaviors requiring greater user intent than passive exposure or shallow consumption.

The strongest differences occur in:

* comments: **13.4×**
* forwards: **6.7×**
* profile entries: **5.1×**
* follows: **5.0×**

Negative feedback moves in the opposite direction: the hate rate among long-view interactions is approximately **75% lower** overall.

This provides strong evidence that `long_view` distinguishes higher-quality engagement from shallow consumption.

---

## 2. Validation Holds Across Major Product Surfaces

The relationship was tested separately across tabs representing at least 1% of total interactions.

### Like Rate

| Tab | Non-Long View | Long View |
| --: | ------------: | --------: |
|   0 |         0.32% |     3.08% |
|   1 |         1.53% |     2.79% |
|   2 |         0.99% |     2.07% |
|   4 |         1.42% |     2.48% |
|   6 |         0.50% |     2.86% |

Long-view interactions have a higher like rate on **all five major tabs**.

### Comment Rate

| Tab | Non-Long View | Long View |
| --: | ------------: | --------: |
|   0 |         0.04% |     1.21% |
|   1 |         0.07% |     0.85% |
|   2 |         0.07% |     0.81% |
|   4 |         0.11% |     0.68% |
|   6 |         0.01% |     0.49% |

Long-view interactions also have a higher comment rate on **all five major tabs**.

The same direction holds across every major tab for:

* likes
* follows
* comments
* forwards
* profile entries

### Negative Feedback

Hate rates are lower among long views on tabs 0, 1, 2, and 4.

Tab 6 is the only exception, where the hate rate rises slightly from approximately **0.032% to 0.038%**. The absolute rates remain extremely small, but this surface should be retained as a guardrail check in later analyses.

### Conclusion

The relationship between long views and higher-intent engagement is **not driven exclusively by the dominant tab 1 population**.

Positive downstream behaviors increase with long views across every major product surface, supporting the use of `long_view` as a cross-surface quality-engagement signal.

---

## 3. Why Long View Is Preferable to Sparse High-Intent Actions

Likes, follows, comments, and forwards provide strong evidence of user intent but occur infrequently.

For example:

* Long views occur in approximately **26.2%** of interactions.
* Likes occur in roughly **1–3%** of interactions depending on long-view status.
* Follows and forwards occur in well below **1%** of interactions.

### Conclusion

The higher frequency of `long_view` makes it more practical as a primary product metric than rare explicit actions.

This provides two advantages:

1. **Greater sensitivity to product changes** because the outcome occurs frequently enough to measure reliably.
2. **Broader coverage of user value**, including users who consume content meaningfully without explicitly liking, commenting, or following.

Likes, follows, comments, forwards, and profile entries should remain **supporting quality metrics**, while hate should function as a negative-feedback guardrail.

---

## 4. Overall Viewing Behavior Is Shallow

Among interactions with valid video duration:

| Watch Metric                |     Result |
| --------------------------- | ---------: |
| Valid-duration interactions | 10,775,402 |
| Average raw watch ratio     |      41.9% |
| Median raw watch ratio      |      11.1% |
| Average capped completion   |      31.9% |
| Median capped completion    |      11.1% |

The median interaction consumes only **11.1% of video duration**.

### Conclusion

Most feed interactions involve shallow consumption.

This strengthens the value of distinguishing between simple exposure/valid play and sustained viewing behavior. A metric focused only on initial interaction would fail to capture substantial variation in consumption quality.

---

## 5. Duration Quality Issue Is Surface-Dependent

Overall, **937,643 interactions** have nonpositive duration values.

The issue is concentrated disproportionately on certain surfaces:

| Tab | Nonpositive Duration Rate |
| --: | ------------------------: |
|   0 |                 **12.8%** |
|   1 |                      7.4% |
|   2 |                      6.7% |
|   3 |                      5.1% |
|   4 |                      2.6% |
|   6 |                      2.8% |

Tab 0 has the largest quality issue, with more than one in eight interactions lacking usable positive duration.

### Conclusion

Duration-dependent metrics should continue filtering to `duration_ms > 0`.

The affected observations should not be removed from analyses based on logged binary engagement outcomes because their behavioral fields remain usable.

Surface-level quality monitoring is particularly important for tab 0.

---

## Metric Decision

### Primary Quality-Engagement Signal

**`long_view`**

`long_view` is accepted as the primary signal of higher-quality content consumption for subsequent analysis because it:

* occurs frequently enough for robust measurement,
* strongly aligns with higher-intent behaviors,
* aligns with lower negative feedback overall,
* and behaves consistently across major product surfaces.

### Supporting Metrics

* Like rate
* Follow rate
* Comment rate
* Forward rate
* Profile-entry rate

### Guardrail Metric

* Hate rate

### Metric Not Used as Universal Success Measure

**Pooled `is_click` / CTR**

Its meaning varies by product surface and it captures a substantially broader, shallower level of engagement.

---

## Important Limitation

The observed relationships are **associations, not causal effects**.

For example, the analysis supports the statement:

> Long-view interactions have a 2.4× higher observed like rate.

It does **not** support:

> Increasing long views causes likes to increase 2.4×.

Causal effects will be evaluated separately using randomized-exposure data and later experimentation analysis.

---

## Next Decision

`long_view` has now been validated at the interaction level.

The next stage should determine whether higher-quality interaction behavior translates into **better product-level outcomes**, including:

* stronger sessions,
* greater repeat usage,
* higher observed retention,
* and differences across user segments.

Only after that analysis should a final North Star metric be selected.
