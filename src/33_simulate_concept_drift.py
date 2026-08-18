import numpy as np
import pandas as pd


INPUT_PATH = (
    "outputs/experience_demo/"
    "synthetic_interactions.csv"
)

OUTPUT_PATH = (
    "outputs/experience_demo/"
    "synthetic_interactions_concept_drift.csv"
)

SEED = 42

rng = np.random.default_rng(SEED)

df = pd.read_csv(INPUT_PATH)


# ============================================================
# Simulate concept drift
#
# For 40% of observations, replace the original engagement
# outcome with random behavior.
#
# Features remain unchanged.
# The relationship between features and outcome degrades.
# ============================================================

drift_mask = (
    rng.random(len(df)) < 0.40
)

baseline_rate = (
    df["meaningful_engagement"].mean()
)

replacement_labels = rng.binomial(
    1,
    baseline_rate,
    drift_mask.sum()
)

df.loc[
    drift_mask,
    "meaningful_engagement"
] = replacement_labels


df.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    f"Concept-drift dataset saved to: "
    f"{OUTPUT_PATH}"
)

print(
    f"Rows affected: "
    f"{drift_mask.sum():,} "
    f"({drift_mask.mean():.1%})"
)

print(
    "Engagement rate before: "
    f"{baseline_rate:.2%}"
)

print(
    "Engagement rate after: "
    f"{df['meaningful_engagement'].mean():.2%}"
)