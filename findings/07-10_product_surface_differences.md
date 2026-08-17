# 07–10 — Product Surface Heterogeneity

## Executive Summary

The relationship between meaningful engagement and future session frequency varies materially by product surface.

| Dominant Surface | Long-View Incidence Rate Ratio (IRR) | p-value | Relationship          |
| ---------------- | ------------: | ------: | --------------------- |
| Tab 0            |         0.946 |   0.501 | No significant effect |
| Tab 1            |         0.917 |   0.003 | Negative              |
| Tab 2            |     **1.323** |   0.016 | **Positive**          |
| Tab 4            |         0.773 |   0.004 | Negative              |

Tab 2 is the key exception: higher long-view rates are associated with **more future sessions**, while Tabs 1 and 4 show the opposite relationship.

Baseline user activity on Tab 2 is broadly comparable to Tabs 1 and 4, suggesting that simple differences in user activity do not fully explain the result.

### Conclusion

Meaningful engagement should **not be interpreted or optimized uniformly across product surfaces**. Product context materially changes its relationship with future usage.

The pooled negative relationship masks important surface-level heterogeneity.

### Limitation

The combined interaction model produced a convergence warning, and Tab 2 contains only **565 user-days from 84 users**. The interaction effect therefore requires a robustness check before being treated as definitive.

### Robustness check

A converged GLM Negative Binomial specification reproduced the surface interaction result. Tab 2 remained significantly different from Tab 1 (interaction IRR = 1.47, p = 0.001), supporting the conclusion that product surface materially moderates the relationship between meaningful engagement and future usage.