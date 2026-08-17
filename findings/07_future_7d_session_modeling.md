# 06 - Future 7-Day Session Modeling

## Executive Summary

A Negative Binomial model tested whether day-level `long_view_rate` predicts **future 7-day session frequency** after controlling for prior activity.

The outcome showed substantial variation:

* Mean future sessions: **36.1**
* Variance: **259.8**
* Variance/mean: **7.21**

The strong overdispersion supported Negative Binomial regression over Poisson.

## Key Results

| Predictor                    |   Incidence Rate Ratio | p-value | Interpretation                                                      |
| ---------------------------- | --------: | ------: | ------------------------------------------------------------------- |
| `long_view_rate_t`           | **0.899** |  <0.001 | Higher long-view rate is associated with fewer future sessions      |
| Prior 7d sessions/day        | **1.134** |  <0.001 | Higher baseline session frequency strongly predicts future sessions |
| Prior 7d avg minutes/session | **1.001** |   0.006 | Small positive association                                          |
| Same-day sessions            | **1.040** |  <0.001 | More sessions on day t predict more future sessions                 |

### Conclusion

After controlling for baseline and same-day activity, higher long-view rate remains **significantly associated with lower future session frequency**.

A 10 percentage-point increase in long-view rate corresponds to approximately **1.1% fewer expected sessions over the following 7 days**, holding other variables constant.

This suggests that `long_view` measures **depth or quality of consumption**, but does not necessarily indicate greater future visit frequency.

### Product Implication

Long-view rate should **not be optimized as a standalone objective**. The results suggest a possible tradeoff between:

**consumption quality** and **engagement frequency**.

Further analysis should test why deeper viewing is associated with fewer future sessions before making any product recommendation.

### Limitation

These results are observational and establish association, not causation.
