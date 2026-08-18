# 32 - Model Performance Monitoring

## Executive Summary

Model-performance monitoring was added to detect deterioration in predictive quality after deployment.

Reference performance:

- ROC-AUC: **0.6625**
- Average Precision: **0.4036**

After introducing upstream feature drift:

- ROC-AUC: **0.6620**
- Average Precision: **0.4031**

## Results

| Metric | Reference | Drifted | Change | Result |
|---|---:|---:|---:|---|
| ROC-AUC | 0.6625 | 0.6620 | -0.07% | PASS |
| Average Precision | 0.4036 | 0.4031 | -0.12% | PASS |

## Conclusion

The upstream feature shift did not materially degrade model discrimination.

This illustrates that:

- input drift can occur without prediction drift,
- prediction drift can occur without performance degradation,
- production monitoring should evaluate these failure modes separately.

The ranking system therefore monitors four layers:

**data quality → input drift → prediction drift → model performance**