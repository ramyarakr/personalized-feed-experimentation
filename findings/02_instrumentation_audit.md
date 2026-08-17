# 02 — Instrumentation & Data Quality Audit

## Executive Summary

The KuaiRand-1K standard recommendation logs contain **11.7M interaction records** across two observation windows and nearly the full 1,000-user cohort. Core behavioral fields are complete and suitable for product analysis, but three material constraints affect downstream metric design:

* `is_click` cannot be treated as a universal CTR metric because its meaning varies by product surface (product tab).
* **8.0% of interactions have nonpositive video duration**, requiring selective exclusion from duration-based metrics.
* **86.4% of all interactions occur on tabs 0 and 1**, so pooled metrics are heavily influenced by those two surfaces.

The audit supports using the standard logs for product-health analysis and reserving the randomized sample for later causal and exposure-bias analysis. No North Star metric should be finalized until candidate engagement signals are validated across major product surfaces.

---

## 1. Dataset Coverage

| Observation Window |               Dates | Interactions | Users | Unique Videos |
| ------------------ | ------------------: | -----------: | ----: | ------------: |
| Prior              |     Apr. 8–21, 2022 |    5,055,984 |   983 |     2,119,510 |
| Current            | Apr. 22–May 8, 2022 |    6,657,061 | 1,000 |     2,664,050 |

**Total standard interactions:** 11,713,045

A separate randomized sample contains:

| Metric             |               Value |
| ------------------ | ------------------: |
| Interactions       |              43,028 |
| Users              |               1,000 |
| Unique Videos      |               7,388 |
| Observation Period | Apr. 22–May 8, 2022 |
| Random Flag Rate   |                100% |

### Conclusion

The standard logs provide sufficient scale for product-health and behavioral analysis. The randomized sample is substantially smaller and should be used primarily for later causal-inference and exposure-bias analysis.

The 17 users appearing in the current period but not the prior period should be treated as **new to observed history**, not confirmed new users, because account-creation dates are unavailable.

---

## 2. Click and Long-View Behavior

| `is_click` | `long_view` | Interactions |  Share |
| ---------: | ----------: | -----------: | -----: |
|          0 |           0 |    7,260,612 | 61.99% |
|          0 |           1 |       22,593 |  0.19% |
|          1 |           0 |    1,382,972 | 11.81% |
|          1 |           1 |    3,046,868 | 26.01% |

Derived rates:

* `is_click = 1`: **37.8%** of interactions
* `long_view = 1`: **26.2%** of interactions
* **99.3% of long views also occur with `is_click = 1`**

### Conclusion

`long_view` represents a substantially stricter engagement threshold than the broader click/valid-play signal.

However, `is_click` should **not** be interpreted as universal CTR because its meaning differs across product surfaces. `long_view` is a stronger candidate for meaningful engagement, but it requires validation against higher-intent behaviors before adoption as a KPI.

---

## 3. Product Surface Concentration

|   Tab | Interactions |  Share |
| ----: | -----------: | -----: |
|     1 |    7,717,601 | 65.89% |
|     0 |    2,407,352 | 20.55% |
|     4 |      895,385 |  7.64% |
|     2 |      402,293 |  3.44% |
|     6 |      183,403 |  1.57% |
| Other |      107,011 |  0.91% |

Tabs 0 and 1 account for approximately **86.4% of all standard interactions**.

### Conclusion

Pooled product metrics will largely reflect behavior on tabs 0 and 1. Major conclusions should therefore be validated at the product-surface level rather than relying exclusively on global averages.

Numerical tab identifiers will be retained because the available data does not support reliable semantic labels for every surface.

---

## 4. Data Quality

| Quality Check          | Affected Rows |
| ---------------------- | ------------: |
| Missing user ID        |             0 |
| Missing video ID       |             0 |
| Missing timestamp      |             0 |
| Missing play time      |             0 |
| Missing duration       |             0 |
| Negative play time     |             0 |
| Invalid click flag     |             0 |
| Invalid long-view flag |             0 |
| Invalid like flag      |             0 |
| Invalid hate flag      |             0 |
| Nonpositive duration   |   **937,643** |

Nonpositive duration affects approximately **8.0%** of standard interactions.

### Conclusion

Core event logging is highly complete. The primary quality issue is nonpositive video duration.

These rows should **not be removed globally** because their categorical engagement signals may remain valid. They should only be excluded from calculations requiring valid duration, including:

* watch percentage
* completion rate
* `play_time_ms / duration_ms`

This preserves usable behavioral data while preventing invalid duration-based calculations.

---

## 5. Decisions from the Audit

Based on the instrumentation review:

1. **Do not use pooled `is_click` as universal CTR.**
2. **Do not finalize a North Star metric yet.**
3. **Validate engagement metrics across major product surfaces.**
4. **Exclude nonpositive-duration rows only from duration-dependent analysis.**
5. **Use `new_to_observation` rather than claiming observed users are newly registered.**
6. **Keep observational findings separate from causal conclusions.**
7. **Reserve randomized exposure data for later causal and exposure-bias analysis.**

---

## Next Decision

The next analysis will test whether `long_view` is a credible proxy for meaningful engagement by measuring its relationship with:

* likes
* follows
* comments
* forwards
* profile entry
* negative feedback

The metric will only be adopted if the relationship is consistent across the major product surfaces.
