import json

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import chisquare


DATA_PATH = "outputs/tables/randomized_ranking_dataset.csv"
SEED = 42

df = pd.read_csv(DATA_PATH)


# ============================================================
# 1. USER-LEVEL RANDOMIZATION
# ============================================================

users = np.sort(df["user_id"].unique())

rng = np.random.default_rng(SEED)
rng.shuffle(users)

midpoint = len(users) // 2

control_users = set(users[:midpoint])
treatment_users = set(users[midpoint:])

assignment = pd.DataFrame({
    "user_id": users
})

assignment["experiment_group"] = assignment["user_id"].apply(
    lambda x: (
        "control"
        if x in control_users
        else "treatment"
    )
)

assignment.to_csv(
    "outputs/tables/experiment_aa_assignment.csv",
    index=False
)

df = df.merge(
    assignment,
    on="user_id",
    how="inner"
)

df["treatment"] = (
    df["experiment_group"] == "treatment"
).astype(int)


# ============================================================
# 2. SAMPLE RATIO MISMATCH CHECK
# ============================================================

user_counts = (
    assignment["experiment_group"]
    .value_counts()
    .reindex(["control", "treatment"])
)

observed = user_counts.values

expected = np.array([
    len(assignment) / 2,
    len(assignment) / 2
])

srm_stat, srm_p = chisquare(
    observed,
    f_exp=expected
)

print("=== USER ASSIGNMENT ===")
print(user_counts)

print(f"\nSRM p-value: {srm_p:.4f}")


# ============================================================
# 3. CLUSTER-AWARE METRIC ANALYSIS
#
# GLM is fitted at interaction level but standard errors
# are clustered by user_id.
# ============================================================

def analyze_binary_metric(data, metric):

    control = data[
        data["experiment_group"] == "control"
    ]

    treatment = data[
        data["experiment_group"] == "treatment"
    ]

    control_rate = control[metric].mean()
    treatment_rate = treatment[metric].mean()

    absolute_lift = (
        treatment_rate - control_rate
    )

    relative_lift = (
        absolute_lift / control_rate
        if control_rate > 0
        else np.nan
    )

    X = sm.add_constant(
        data[["treatment"]]
    )

    model = sm.GLM(
        data[metric],
        X,
        family=sm.families.Binomial()
    ).fit(
        cov_type="cluster",
        cov_kwds={
            "groups": data["user_id"]
        }
    )

    coefficient = model.params["treatment"]
    ci = model.conf_int().loc["treatment"]

    return {
        "metric": metric,

        "control_rate": control_rate,
        "treatment_rate": treatment_rate,

        "absolute_lift_pp":
            absolute_lift * 100,

        "relative_lift":
            relative_lift,

        "odds_ratio":
            np.exp(coefficient),

        "ci_lower":
            np.exp(ci[0]),

        "ci_upper":
            np.exp(ci[1]),

        "p_value":
            model.pvalues["treatment"]
    }


# ============================================================
# 4. PRIMARY, SECONDARY, GUARDRAIL METRICS
# ============================================================

metrics = {
    "primary": [
        "long_view"
    ],

    "secondary": [
        "is_like",
        "is_follow",
        "is_comment"
    ],

    "guardrail": [
        "is_hate"
    ]
}


results = []

for metric_type, metric_list in metrics.items():

    for metric in metric_list:

        result = analyze_binary_metric(
            df,
            metric
        )

        result["metric_type"] = metric_type

        results.append(result)


results = pd.DataFrame(results)

results = results[
    [
        "metric_type",
        "metric",
        "control_rate",
        "treatment_rate",
        "absolute_lift_pp",
        "relative_lift",
        "odds_ratio",
        "ci_lower",
        "ci_upper",
        "p_value"
    ]
]


results.to_csv(
    "outputs/tables/experiment_aa_results.csv",
    index=False
)


# ============================================================
# 5. A/A SANITY CHECK
# ============================================================

primary_p = results.loc[
    results["metric"] == "long_view",
    "p_value"
].iloc[0]

hate_row = results[
    results["metric"] == "is_hate"
].iloc[0]

srm_pass = srm_p > 0.01
primary_pass = primary_p > 0.05

# In an A/A test, we do not expect a significant increase
# in the negative-feedback guardrail.
guardrail_pass = not (
    hate_row["p_value"] < 0.05
    and hate_row["treatment_rate"]
        > hate_row["control_rate"]
)

aa_pass = (
    srm_pass
    and primary_pass
    and guardrail_pass
)


summary = {
    "test_type": "A/A sanity check",

    "users": int(
        assignment["user_id"].nunique()
    ),

    "control_users":
        int(user_counts["control"]),

    "treatment_users":
        int(user_counts["treatment"]),

    "srm_p_value":
        float(srm_p),

    "primary_metric_p_value":
        float(primary_p),

    "srm_pass":
        bool(srm_pass),

    "primary_metric_pass":
        bool(primary_pass),

    "guardrail_pass":
        bool(guardrail_pass),

    "overall_aa_pass":
        bool(aa_pass)
}


with open(
    "outputs/tables/experiment_aa_summary.json",
    "w"
) as f:
    json.dump(summary, f, indent=2)


# ============================================================
# 6. OUTPUT
# ============================================================

print("\n=== A/A METRIC RESULTS ===")
print(results.to_string(index=False))

print("\n=== SANITY CHECK ===")

print(
    "PASS"
    if aa_pass
    else "REVIEW"
)

print(
    "\nNote: This is an A/A validation of the experiment "
    "analysis pipeline, not evidence of treatment impact."
)