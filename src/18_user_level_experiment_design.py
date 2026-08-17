import json
import math

import numpy as np
import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


DATA_PATH = "outputs/tables/randomized_ranking_dataset.csv"

df = pd.read_csv(DATA_PATH)


# ============================================================
# Experiment definition
# ============================================================

experiment = {
    "randomization_unit": "user_id",
    "allocation": {
        "control": 0.50,
        "treatment": 0.50
    },

    "control": "historical_popularity_ranking",
    "treatment": "personalized_meaningful_engagement_ranking",

    "primary_metric": "long_view_rate",

    "secondary_metrics": [
        "like_rate",
        "follow_rate",
        "comment_rate",
        "future_7d_sessions"
    ],

    "guardrail_metrics": [
        "hate_rate"
    ],

    "alpha": 0.05,
    "power": 0.80,
    "target_relative_mde": 0.05
}


# ============================================================
# Baseline
# ============================================================

baseline = df["long_view"].mean()

experiment["baseline_long_view_rate"] = baseline


# ============================================================
# Estimate clustering by user
#
# Users generate multiple observations, so interaction-level
# sample-size calculations are too optimistic.
# ============================================================

user_stats = (
    df.groupby("user_id")
    .agg(
        interactions=("long_view", "size"),
        long_view_rate=("long_view", "mean")
    )
    .reset_index()
)

avg_cluster_size = user_stats["interactions"].mean()


# ------------------------------------------------------------
# Approximate ICC for binary outcome
# ------------------------------------------------------------

overall_mean = df["long_view"].mean()

between_variance = np.average(
    (user_stats["long_view_rate"] - overall_mean) ** 2,
    weights=user_stats["interactions"]
)

binary_variance = overall_mean * (1 - overall_mean)

icc = (
    between_variance / binary_variance
    if binary_variance > 0
    else 0
)

# Keep estimate in valid range
icc = max(0, min(icc, 1))


# ============================================================
# Design effect
#
# DE = 1 + (m - 1) * ICC
# ============================================================

design_effect = 1 + (avg_cluster_size - 1) * icc


# ============================================================
# Base power calculation
# ============================================================

relative_mde = experiment["target_relative_mde"]

treatment_rate = baseline * (1 + relative_mde)

effect_size = proportion_effectsize(
    baseline,
    treatment_rate
)

power_analysis = NormalIndPower()

independent_obs_per_group = power_analysis.solve_power(
    effect_size=effect_size,
    alpha=experiment["alpha"],
    power=experiment["power"],
    ratio=1,
    alternative="two-sided"
)


# ============================================================
# Cluster-adjusted requirement
# ============================================================

adjusted_obs_per_group = (
    independent_obs_per_group * design_effect
)

estimated_users_per_group = (
    adjusted_obs_per_group / avg_cluster_size
)

total_users = math.ceil(
    estimated_users_per_group * 2
)


# ============================================================
# Save experiment specification
# ============================================================

experiment.update({
    "treatment_long_view_rate_target": treatment_rate,

    "absolute_mde_percentage_points":
        (treatment_rate - baseline) * 100,

    "average_interactions_per_user":
        avg_cluster_size,

    "estimated_long_view_icc":
        icc,

    "design_effect":
        design_effect,

    "independent_observations_per_group":
        math.ceil(independent_obs_per_group),

    "cluster_adjusted_observations_per_group":
        math.ceil(adjusted_obs_per_group),

    "estimated_users_per_group":
        math.ceil(estimated_users_per_group),

    "estimated_total_users":
        total_users
})


with open(
    "outputs/tables/experiment_spec.json",
    "w"
) as f:
    json.dump(experiment, f, indent=2)


summary = pd.DataFrame([{
    "baseline_long_view_rate": baseline,
    "relative_mde": relative_mde,
    "treatment_target_rate": treatment_rate,
    "absolute_mde_pp":
        (treatment_rate - baseline) * 100,

    "avg_interactions_per_user":
        avg_cluster_size,

    "estimated_icc":
        icc,

    "design_effect":
        design_effect,

    "independent_obs_per_group":
        math.ceil(independent_obs_per_group),

    "cluster_adjusted_obs_per_group":
        math.ceil(adjusted_obs_per_group),

    "estimated_users_per_group":
        math.ceil(estimated_users_per_group),

    "estimated_total_users":
        total_users
}])


summary.to_csv(
    "outputs/tables/experiment_design_summary.csv",
    index=False
)


print("=== EXPERIMENT DESIGN ===")
print(summary.to_string(index=False))

print("\nPrimary metric:")
print("  long_view_rate")

print("\nSecondary metrics:")
for metric in experiment["secondary_metrics"]:
    print(f"  {metric}")

print("\nGuardrails:")
for metric in experiment["guardrail_metrics"]:
    print(f"  {metric}")