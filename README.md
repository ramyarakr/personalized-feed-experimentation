# Personalized Feed Experimentation

An end-to-end product data science and recommendation systems project exploring how meaningful engagement, personalization, experimentation, and production monitoring can improve ranking decisions.

**Live case study:**  
https://ramyarakr.github.io/personalized-feed-experimentation/

**Project Website:**  
https://ramyarakr.github.io/personalized-feed-experimentation/

---

## Product Question

**Should a recommendation system optimize for shallow interaction volume or meaningful engagement, and can personalization improve which content is ranked first?**

The project analyzes 11.7M+ behavioral interactions from KuaiRand-1K and progresses from instrumentation and product analytics through recommendation ranking, experiment design, and production-style monitoring.

---

## Key Results

### Behavioral Analytics

- Analyzed **11.7M+ behavioral interactions**
- Reconstructed **147,752 sessions**
- Long-view interactions were associated with:
  - **2.4×** higher like rate
  - **5.0×** higher follow rate
  - **13.4×** higher comment rate
  - approximately **75% lower** hate rate
- Found that long-view behavior is a strong same-session quality signal but not a universal predictor of future usage

### Personalized Ranking

Compared a historical content-quality baseline against a personalized ranking model on held-out randomized exposures.

| Metric | Baseline | Personalized |
|---|---:|---:|
| ROC-AUC | 0.570 | **0.681** |
| Average Precision | 0.115 | **0.176** |
| Precision@1 | 11.95% | **12.66%** |
| Precision@3 | 11.58% | **11.84%** |
| Precision@5 | 10.88% | **11.28%** |

The personalized challenger improved **Precision@1 by 5.9% relative**.

---

## Experimentation

Designed a user-randomized online experiment for the personalized challenger.

- Primary metric: long-view rate
- Baseline: 8.42%
- Target relative MDE: 5%
- Power: 80%
- Estimated requirement: approximately **15,000 users**
- User-level A/A framework validation: **PASS**

A simulated launch-decision exercise is included only to demonstrate experiment analysis logic and is explicitly separated from observed results.

---

## Recommendation System Engineering

The analytical workflow was extended into reusable software components including:

- historical and personalized ranking policies
- top-K candidate ranking
- command-line execution
- saved model artifacts
- automated unit tests
- GitHub Actions CI
- data-quality gates
- input-drift monitoring
- prediction-drift monitoring
- model-performance monitoring
- guarded end-to-end ranking pipeline

Current automated test suite:

**8 / 8 tests passing**

---

## Scale Benchmark

Local chunked inference benchmark:

| Candidates | Runtime | Throughput |
|---:|---:|---:|
| 100K | 0.32 s | 314K rows/s |
| 500K | 1.14 s | 440K rows/s |
| 1M | 3.03 s | 330K rows/s |

This is a local single-machine benchmark and is not presented as production serving or distributed-system throughput.

---

## Generalization Demo

A separate synthetic experience-discovery environment demonstrates how the same ranking architecture can generalize beyond the original feed dataset.

The synthetic demo is clearly separated from real-data results and should be interpreted as a system-design demonstration rather than evidence of real-world product impact.

---

## Production Monitoring

The final ranking system monitors four distinct failure modes:

```text
Data Quality
      ↓
Input Drift
      ↓
Prediction Drift
      ↓
Model Performance
