# Personalized Feed Experimentation Roadmap

## Phase 0 — Foundation
- [x] Lock zero-cost architecture
- [x] Select primary dataset
- [x] Define initial product decision
- [x] Create repo structure
- [ ] Download KuaiRand-1K
- [ ] Build local DuckDB views

## Phase 1 — Data audit + instrumentation
- [ ] Verify row counts and date coverage
- [ ] Inspect nulls, duplicates, IDs, timestamp ordering
- [ ] Validate engagement fields
- [ ] Define sessionization rule
- [ ] Build analytics-ready event/session tables
- [ ] Create data dictionary

**Deliverable:** trustworthy analytical layer + instrumentation memo

## Phase 2 — Product health + behavior deep dive
- [ ] Baseline metric dashboard
- [ ] Engagement funnel
- [ ] Cohort/repeat-usage analysis
- [ ] User segmentation
- [ ] Session-depth analysis
- [ ] Root-cause deep dive

**Deliverable:** product-health narrative identifying one concrete product opportunity

## Phase 3 — Experiment design
- [ ] Define control/treatment concept
- [ ] Select primary/secondary/guardrail metrics
- [ ] Estimate baseline variance
- [ ] Choose MDE
- [ ] Power/sample-size analysis
- [ ] Randomization-unit rationale
- [ ] SRM and validity checks
- [ ] Multiple-testing plan

**Deliverable:** preregistered experiment-analysis plan

## Phase 4 — Causal measurement
- [ ] Compare standard vs randomized exposure logs
- [ ] Quantify exposure bias
- [ ] Naive observational estimate
- [ ] Propensity-based estimate
- [ ] Doubly robust estimate
- [ ] Sensitivity/assumption discussion

**Deliverable:** causal-inference case study

## Phase 5 — Personalization model
- [ ] Define meaningful-engagement label
- [ ] Build leakage-safe feature set
- [ ] Logistic-regression baseline
- [ ] Tree-based challenger
- [ ] Evaluate AUC/calibration/ranking metrics
- [ ] Translate offline model metrics to product implications

**Deliverable:** model comparison tied to product metrics

## Phase 6 — Heterogeneous effects + decision
- [ ] Segment-level treatment/impact analysis
- [ ] Identify likely winners/losers
- [ ] Check guardrails
- [ ] Recommend broad vs segmented rollout

**Deliverable:** one-page executive launch memo

## Phase 7 — Portfolio publication
- [ ] Final README
- [ ] Curate 5–7 strongest visuals
- [ ] Build interactive/static project page
- [ ] Publish via GitHub Pages
- [ ] Create resume bullets
- [ ] Create 60-second and 5-minute interview walkthroughs

**Deliverable:** recruiter-facing public case study
