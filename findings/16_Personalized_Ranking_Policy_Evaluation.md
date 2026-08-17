# 16 — Personalized Ranking Policy Evaluation

## Executive Summary

A personalized ranking model was compared with a historical content-performance baseline using **23,752 held-out randomized exposures**.

| Metric            | Baseline | Personalized | Relative Lift |
| ----------------- | -------: | -----------: | ------------: |
| ROC-AUC           |    0.570 |    **0.681** |        +19.6% |
| Average Precision |    0.115 |    **0.176** |        +53.0% |
| Precision@1       |   11.95% |   **12.66%** |         +5.9% |
| Precision@3       |   11.58% |   **11.84%** |         +2.2% |
| Precision@5       |   10.88% |   **11.28%** |         +3.6% |

### Conclusion

The personalized policy consistently outperformed ranking based primarily on historical content performance.

The largest product-relevant improvement occurred at **Precision@1**, indicating better identification of content likely to produce meaningful engagement in the highest-value recommendation position.

Because evaluation used randomized exposures, the comparison is less affected by historical recommendation exposure bias.

### Decision

The challenger is strong enough to justify an **online A/B experiment**, but offline ranking gains alone are insufficient evidence for launch.
