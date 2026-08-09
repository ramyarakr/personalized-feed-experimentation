# Metric Tree — v0.1

This is the starting metric framework. Final definitions will be revised after data quality checks and exploratory analysis.

## North Star

### Meaningfully Engaged Sessions per Active User

Goal: capture sessions in which the user demonstrated sustained or intentional engagement rather than a shallow impression/click.

Candidate qualifying signals:

- at least one `long_view`
- meaningful play-time ratio
- `is_like`
- `is_follow`
- `is_comment`
- `is_forward`
- `is_profile_enter`

We will avoid arbitrarily weighting all actions equally. The composite definition will be justified using behavior distributions and sensitivity analysis.

## Engagement inputs

- valid-play / click rate
- long-view rate
- average play time
- play-time / video-duration ratio
- like rate
- follow rate
- comment rate
- forward rate
- profile-entry rate

## Repeat-usage / retention proxies

Because the public logs cover fixed historical windows rather than a production analytics system, retention will be represented carefully using observed repeat activity:

- active on next observed day
- active in next 7 observed days
- active days per user
- sessions per active day
- time between active sessions

We will explicitly call these **observed retention proxies** where full product-retention measurement is not supported.

## Discovery / ecosystem

- unique videos exposed per user
- category diversity where category metadata is used
- creator exposure concentration
- Gini coefficient of impressions/exposure
- share of exposure going to top 1% / 5% / 10% of content or creators

## Guardrails

- hate/negative-feedback rate
- short-view rate
- click/valid-play degradation
- session abandonment proxy
- exposure concentration
- content diversity decline

## Segments

- `user_active_degree`
- `is_lowactive_period`
- registration-age band
- follow-count band
- fan-count band
- creator status
- inferred interest breadth
- session-depth band

## Experiment metrics

When we design the hypothetical ranking A/B test:

**Primary:** Meaningfully Engaged Sessions per Active User

**Secondary:**
- long-view rate
- meaningful actions / session
- average watch time / session
- repeat-activity proxy

**Guardrails:**
- negative feedback
- shallow-view rate
- content/creator concentration
- overall click/valid-play rate
