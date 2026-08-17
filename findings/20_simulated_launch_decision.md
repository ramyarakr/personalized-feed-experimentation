# 20 - Simulated Launch Decision

## Executive Summary

A simulated online experiment was used to exercise the launch-decision framework for the personalized ranking policy.

| Metric         | Control | Treatment | Relative Lift |   p-value |
| -------------- | ------: | --------: | ------------: | --------: |
| Long-view rate |   8.42% | **8.90%** |     **+5.7%** | **0.012** |
| Like rate      |   0.51% |     0.55% |         +7.8% |     0.081 |
| Follow rate    |  0.020% |    0.022% |        +10.0% |     0.220 |
| Hate rate      |  0.080% |    0.083% |         +3.8% |     0.610 |

### Decision

**SHIP**

The simulated treatment produced a statistically significant **5.7% relative improvement in the primary long-view metric**.

Secondary engagement metrics moved positively but were not statistically significant. The hate-rate guardrail showed no statistically significant deterioration.

### Product Interpretation

Under these hypothetical results, the personalized ranking policy would satisfy the predefined launch criteria:

* primary metric improves significantly,
* no significant guardrail regression,
* supporting engagement metrics do not show concerning deterioration.

### Limitation

These values are **synthetic and used only to demonstrate experiment decision logic**. They are not observed production A/B test results.
