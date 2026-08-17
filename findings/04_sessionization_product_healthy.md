# 04 — Sessionization & Product Health

## Executive Summary

A 30-minute inactivity threshold produces **147,752 sessions** across 1,000 users and provides a reasonable middle ground between more fragmented 15-minute sessions and broader 60-minute sessions.

Sessions containing meaningful consumption are substantially healthier than sessions with no long views. However, increasing the share of long views does **not** correspond to steadily increasing session depth or repeat usage.

Key findings:

* **86.1% of sessions contain at least one long view**
* **50.9% contain at least one explicit positive action**
* Sessions with no long views are short and shallow: **8.9 interactions and 3.3 minutes on average**
* Sessions with some long-view activity are much deeper, averaging **35–42 minutes**
* Moderate long-view intensity produces the highest explicit positive-action rate
* D1 return rises sharply once meaningful consumption occurs but declines slightly at very high long-view shares
* 7-day return exceeds **98.9% in every segment**, making it ineffective for distinguishing product quality within this cohort

`long_view` remains useful as a quality-engagement signal, but the results do not support maximizing long-view rate as a standalone product objective.

---

## 1. Session Definition

Session counts were tested under three inactivity thresholds:

| Inactivity Threshold | Sessions |
| -------------------- | -------: |
| 15 minutes           |  201,839 |
| 30 minutes           |  147,752 |
| 60 minutes           |  103,999 |

The 30-minute threshold reduces fragmentation relative to 15 minutes while avoiding the substantial merging produced by the 60-minute definition.

### Decision

Use a **30-minute inactivity threshold** as the working session definition for subsequent analysis.

Sensitivity to the threshold should remain documented because session-based metrics depend on this assumption.

---

## 2. Overall Session Health

Across the 147,752 constructed sessions:

| Metric                                    |   Result |
| ----------------------------------------- | -------: |
| Users                                     |    1,000 |
| Average interactions/session              |     79.3 |
| Median interactions/session               |       31 |
| Average session duration                  | 34.3 min |
| Median session duration                   | 17.2 min |
| Average long views/session                |     20.8 |
| Median long views/session                 |        9 |
| Average session long-view rate            |    34.3% |
| Sessions with ≥1 long view                |    86.1% |
| Sessions with ≥1 explicit positive action |    50.9% |
| Sessions with hate feedback               |     1.1% |

### Conclusion

Session behavior is highly right-skewed.

The average session contains more than twice as many interactions as the median session, and average session duration is approximately twice the median. A relatively small number of large sessions therefore have substantial influence on mean-based product metrics.

Median values should be retained alongside averages in product-health reporting.

---

## 3. Meaningful Consumption Separates Shallow from Healthy Sessions

| Long-View Share | Sessions | Avg. Interactions | Avg. Duration | Avg. Explicit Positive Interactions | Sessions with Positive Action |
| --------------- | -------: | ----------------: | ------------: | ----------------------------------: | ----------------------------: |
| 0%              |   20,542 |               8.9 |       3.3 min |                                0.14 |                          9.3% |
| >0–25%          |   43,173 |             146.5 |      40.2 min |                                3.23 |                         54.7% |
| >25–50%         |   45,820 |              78.5 |      42.0 min |                                3.52 |                     **60.2%** |
| >50%            |   38,217 |              42.1 |      35.2 min |                                2.91 |                         57.9% |

### Conclusion

The strongest distinction is between **sessions with no meaningful consumption and sessions with at least some meaningful consumption**.

Sessions with zero long views average:

* only **8.9 interactions**
* only **3.3 minutes**
* explicit positive actions in just **9.3%** of sessions

Once long views occur, session duration increases to approximately **35–42 minutes**, and more than half of sessions contain an explicit positive action.

However, session health does not increase continuously with long-view share.

The `>25–50%` segment has the highest rate of sessions containing explicit positive actions, while the `>50%` segment has fewer interactions and shorter sessions than the two moderate long-view groups.

### Product Implication

The objective should not be:

> Maximize long-view rate.

The data instead suggests that **meaningful consumption is necessary for healthy sessions, but very high long-view concentration does not automatically imply greater product value**.

This supports treating long view as one component of a broader product-health framework rather than as the sole optimization target.

---

## 4. Negative Feedback Remains Low

| Long-View Share | Sessions with Hate Feedback |
| --------------- | --------------------------: |
| 0%              |                       0.14% |
| >0–25%          |                       1.50% |
| >25–50%         |                       1.38% |
| >50%            |                       0.89% |

### Conclusion

Negative feedback is uncommon across all session types.

The increase among moderate long-view sessions should not be interpreted as evidence that meaningful consumption causes negative feedback. These sessions contain substantially more interactions, creating more opportunities for any feedback event to occur.

Interaction-normalized hate rates should be preferred for future guardrail analysis.

---

## 5. Repeat Usage

Observed user-days were segmented by long-view share.

| Long-View Share | User-Days | Avg. Interactions | D1 Return | 7-Day Return |
| --------------- | --------: | ----------------: | --------: | -----------: |
| 0%              |       478 |               9.8 |     77.8% |        98.9% |
| >0–25%          |     9,339 |             685.9 | **97.6%** |   **99.94%** |
| >25–50%         |    11,203 |             350.1 |     96.5% |       99.85% |
| >50%            |     6,944 |             198.7 |     95.0% |       99.69% |

### D1 Conclusion

User-days with no long views have substantially lower next-day observed activity.

D1 return increases from:

**77.8% → approximately 95–98%**

once meaningful consumption occurs.

However, the relationship is not monotonic. The highest D1 return occurs in the `>0–25%` group rather than the highest long-view group.

This prevents interpreting higher long-view share as directly corresponding to higher retention.

---

## 6. Seven-Day Return Is Not a Useful KPI for This Cohort

Seven-day return ranges only from:

**98.9% to 99.94%**

across all long-view groups.

### Conclusion

The metric is effectively saturated within the observed population and therefore provides almost no useful separation between engagement levels.

Seven-day return should **not** be used as a primary success metric for this project.

More discriminating outcomes are needed, such as:

* next-day return
* number of active days in a future window
* future session frequency
* future meaningful-engagement volume
* time until next session

---

## 7. Activity Level Is a Major Confounder

Average daily interaction volume differs substantially across long-view groups:

| Long-View Share | Avg. Daily Interactions |
| --------------- | ----------------------: |
| 0%              |                     9.8 |
| >0–25%          |               **685.9** |
| >25–50%         |                   350.1 |
| >50%            |                   198.7 |

### Conclusion

The long-view groups represent users with very different activity intensity.

For example, the group with the highest D1 return also generates roughly:

* **3.4× more interactions** than the `>50%` group
* **70× more interactions** than the `0%` group

Therefore, the observed relationship between long-view share and future activity is heavily confounded by current activity level.

A simple comparison of return rates cannot establish whether meaningful engagement independently predicts repeat usage.

---

## Product Decision

`long_view` remains validated as a **quality-engagement signal**, but it should not be promoted to a standalone North Star metric.

The evidence supports the following framework:

**Primary quality signal**

* Long-view behavior

**Supporting session-health signals**

* Explicit positive actions
* Interactions per session
* Session depth/duration

**Repeat-usage outcome**

* D1 return or a more granular future-activity metric

**Guardrail**

* Hate / negative feedback

**Rejected as primary outcome**

* 7-day return, due to near-total saturation

---

## Next Analytical Question

The observed relationship between meaningful engagement and repeat usage may reflect differences in user activity rather than an independent effect of content quality.

The next analysis should answer:

> **Does meaningful engagement predict future product usage after controlling for how active the user already is?**

This requires controlling for factors such as:

* current interaction volume
* prior activity
* user-level differences
* product surface
* observation period

Only after accounting for these confounders should the relationship between meaningful engagement and repeat usage be interpreted further.
