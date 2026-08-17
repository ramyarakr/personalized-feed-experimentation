# 05 - D1 Return Modeling

## Executive Summary

A logistic regression analysis tested whether day-level `long_view_rate` predicts next-day return after controlling for baseline user activity.

Across **20,839 user-days** and 1,000 users, D1 return was highly saturated at **96.3%**.

`long_view_rate` was **not statistically significant** in either model:

| Model               | Odds Ratio | p-value |
| ------------------- | ---------: | ------: |
| Baseline controls   |       1.09 |   0.695 |
| + Same-day sessions |       1.21 |   0.356 |

### Conclusion

Higher long-view rate was directionally associated with higher D1-return odds, but the relationship was not statistically significant after controlling for activity.

The strongest predictors of D1 return were user activity measures:

* **Prior 7-day sessions/day:** OR 1.63 in the robustness model
* **Same-day sessions:** OR 1.39

This suggests that **usage frequency is a much stronger predictor of next-day return than long-view rate alone**.

## Limitation

D1 return is heavily imbalanced: only about **3.7% of observations are non-returns**. This limits the model’s ability to identify factors associated with churn or non-return.

### Decision

`long_view` remains useful as a quality-engagement metric, but it is **not validated as an independent predictor of D1 retention**.

A less saturated future-activity outcome should be used next, such as **number of active days in the following 7 days**.
