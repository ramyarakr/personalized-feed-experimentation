# Product Brief — Personalized Feed Experimentation

## Decision to make

**Should the feed team replace a click-oriented ranking objective with a meaningful-engagement objective, and if so, for which users should it launch first?**

## Product context

Personalized Feed Experimentation represents a short-video discovery feed similar to a large consumer content platform. Users receive ranked video recommendations and can click/valid-play, watch, like, follow, comment, forward, enter a creator profile, or express negative feedback.

The existing ranking system may over-reward shallow engagement. A click or valid play is easy to optimize, but it may not represent a genuinely valuable user experience. Product leadership wants a measurement framework that better captures meaningful engagement and its relationship with repeat usage.

## Product hypothesis

> **H1:** Ranking toward meaningful engagement rather than click/valid-play probability will improve higher-quality user engagement and repeat usage without materially degrading discovery quality or creating unacceptable ecosystem concentration.

## Null hypothesis

> **H0:** A meaningful-engagement-oriented ranking strategy does not improve the primary product outcome relative to the click-oriented strategy.

## Users

Primary user segments to study:

- lower-activity vs higher-activity users
- newer vs established users, using registration-age bands available in the dataset
- users with narrow vs broad observed content interests
- creator-users vs non-creators, where relevant

## Proposed North Star

**Meaningfully Engaged Sessions per Active User**

A session-level composite will be defined after exploratory analysis. Candidate signals include long views, likes, follows, comments, forwards, and profile entry. The definition must be validated rather than chosen solely to maximize statistical significance.

## Primary product questions

1. Which behaviors best distinguish shallow consumption from meaningful engagement?
2. How do engagement patterns differ across user segments and over repeated sessions?
3. Which early behaviors are most associated with repeat activity?
4. How biased are conclusions drawn from standard recommendation logs compared with randomized exposure logs?
5. Would a meaningful-engagement ranking objective improve the selected primary metric?
6. Which users benefit most, and are any important segments harmed?
7. What guardrail tradeoffs appear in content diversity, negative feedback, or concentration?
8. Should the team ship broadly, run a segmented rollout, iterate, or reject the change?

## Guardrails

Candidate guardrails:

- negative-feedback rate (`is_hate`)
- short/low-quality viewing
- creator/content exposure concentration
- content diversity
- abandonment proxy / unusually short sessions
- loss of click/valid-play rate beyond an agreed tolerance

## What this project is NOT

- Not a Kaggle-style leaderboard exercise
- Not a recommendation-system demo whose only outcome is NDCG/AUC
- Not a dashboard with disconnected charts
- Not a fabricated online A/B test

Where the dataset does not contain a true online treatment/control experiment for our hypothetical ranker, we will **clearly label simulated experiment work as experiment design or simulation**. Causal claims will be restricted to analyses supported by the randomized exposure mechanism in KuaiRand or by explicitly stated assumptions.

## Final decision artifact

The project ends in a one-page launch recommendation containing:

- recommendation
- estimated impact
- uncertainty
- segment-level effects
- guardrail impact
- limitations
- proposed rollout
- next experiment
