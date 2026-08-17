# 14 — Within-User Surface Robustness

## Executive Summary

A within-user analysis tested whether the positive Tab 2 relationship remained when comparing only users who interacted with both Tabs 1 and 2.

The restricted sample contained **957 user-days across 72 users**.

| Effect                        |      IRR | p-value |
| ----------------------------- | -------: | ------: |
| Long-view rate on Tab 1       |     0.97 |   0.783 |
| Tab 2 × long-view interaction | **1.27** |   0.100 |

### Conclusion

The Tab 2 interaction remained positive but was no longer statistically significant after controlling for stable user differences.

The reduced sample substantially limits statistical power, so the evidence supports **possible surface-specific heterogeneity**, but not a definitive Tab 2 effect.

Overall, `long_view` remains a strong measure of **same-session engagement quality**, but its relationship with future usage is not consistent enough to justify optimizing long-view rate universally.

### Product Decision

Stop further observational investigation of individual surfaces and move to **ranking-policy evaluation and experimentation**, where recommendation strategies can be compared directly.
