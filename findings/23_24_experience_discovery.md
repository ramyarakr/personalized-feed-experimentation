# 23-24 - Experience Discovery Ranking Demo

## Executive Summary

A synthetic experience-discovery environment was built to test whether the ranking architecture generalizes beyond the original behavioral dataset.

The demo contained:

- 500 users
- 120 experiences
- 20,000 randomized user-experience interactions
- 23.9% meaningful-engagement rate

The personalized model was compared against an unpersonalized historical-engagement baseline.

## Predictive Performance

| Policy | ROC-AUC | Average Precision |
|---|---:|---:|
| Historical baseline | 0.532 | 0.255 |
| Personalized model | **0.657** | **0.390** |

The personalized model improved Average Precision by approximately **52.8% relative**.

## Ranking Performance

| Metric | Baseline | Personalized | Relative Lift |
|---|---:|---:|---:|
| Precision@1 | 28.6% | **44.4%** | **+55.2%** |
| Precision@3 | 25.9% | **37.3%** | **+43.7%** |
| Precision@5 | 24.6% | **32.1%** | **+30.1%** |

The largest gain occurred at the highest-ranked recommendation position.

## Personalization Behavior

Users with different preferences received different recommendation orders.

For example:

- A user preferring **Puzzle** received Puzzle experiences in the first two positions.
- A user preferring **Strategy** received Strategy first, followed by experiences aligned with the user's secondary Sports preference.

This demonstrates that the ranking pipeline can combine user preferences, experience characteristics, and contextual features rather than applying one global popularity ranking.

## Engineering Validation

The recommendation system now includes:

- reusable ranking components,
- baseline and personalized policies,
- saved model artifacts,
- top-K candidate ranking,
- command-line execution,
- automated unit tests,
- GitHub Actions continuous integration.

All **6 automated tests passed**.

## Limitation

All experience data and outcomes in this demo are synthetic.

The measured ranking improvements therefore demonstrate system behavior and architecture, not evidence of real-world product impact.