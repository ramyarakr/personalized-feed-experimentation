import os

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
)

from src.experience_discovery import (
    train_experience_model,
    score_experiences,
    rank_experiences,
)


DATA_PATH = (
    "outputs/experience_demo/"
    "synthetic_interactions.csv"
)

OUTPUT_DIR = (
    "outputs/experience_demo"
)

MODEL_PATH = (
    f"{OUTPUT_DIR}/"
    "experience_ranker.joblib"
)

SEED = 123

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# 1. LOAD
# ============================================================

df = pd.read_csv(
    DATA_PATH
)


# ============================================================
# 2. TRAIN / TEST SPLIT
#
# Random exposures are split into historical observations
# and held-out candidate exposures.
# ============================================================

rng = np.random.default_rng(
    SEED
)

df["split_random"] = rng.random(
    len(df)
)

train = df[
    df["split_random"] < 0.70
].copy()

test = df[
    df["split_random"] >= 0.70
].copy()


print(
    f"Train rows: {len(train):,}"
)

print(
    f"Test rows: {len(test):,}"
)


# ============================================================
# 3. BASELINE
#
# Unpersonalized ranking:
# smoothed historical engagement rate by experience.
# ============================================================

history = (
    train
    .groupby("experience_id")
    .agg(
        prior_exposures=(
            "meaningful_engagement",
            "size"
        ),

        prior_engagement_rate=(
            "meaningful_engagement",
            "mean"
        ),
    )
    .reset_index()
)


test = test.merge(
    history,
    on="experience_id",
    how="left",
)


global_rate = (
    train[
        "meaningful_engagement"
    ].mean()
)

SMOOTHING = 20


test[
    "prior_exposures"
] = (
    test[
        "prior_exposures"
    ].fillna(0)
)


test[
    "prior_engagement_rate"
] = (
    test[
        "prior_engagement_rate"
    ].fillna(global_rate)
)


test["baseline_score"] = (
    (
        test["prior_engagement_rate"]
        * test["prior_exposures"]
    )
    + global_rate * SMOOTHING
) / (
    test["prior_exposures"]
    + SMOOTHING
)


# ============================================================
# 4. PERSONALIZED CHALLENGER
# ============================================================

model = train_experience_model(
    train
)

joblib.dump(
    model,
    MODEL_PATH
)


test["personalized_score"] = (
    score_experiences(
        model,
        test,
    )
)


# ============================================================
# 5. PREDICTIVE METRICS
# ============================================================

predictive_results = pd.DataFrame([
    {
        "policy":
            "historical_baseline",

        "roc_auc":
            roc_auc_score(
                test[
                    "meaningful_engagement"
                ],
                test[
                    "baseline_score"
                ],
            ),

        "average_precision":
            average_precision_score(
                test[
                    "meaningful_engagement"
                ],
                test[
                    "baseline_score"
                ],
            ),
    },

    {
        "policy":
            "personalized_model",

        "roc_auc":
            roc_auc_score(
                test[
                    "meaningful_engagement"
                ],
                test[
                    "personalized_score"
                ],
            ),

        "average_precision":
            average_precision_score(
                test[
                    "meaningful_engagement"
                ],
                test[
                    "personalized_score"
                ],
            ),
    },
])


# ============================================================
# 6. PRECISION @ K
# ============================================================

def precision_at_k(
    data,
    score_column,
    k
):

    values = []

    for _, group in data.groupby(
        "user_id"
    ):

        if len(group) < k:
            continue

        ranked = group.nlargest(
            k,
            score_column
        )

        values.append(
            ranked[
                "meaningful_engagement"
            ].mean()
        )

    return (
        np.mean(values),
        len(values),
    )


ranking_results = []

for policy, score_column in [
    (
        "historical_baseline",
        "baseline_score"
    ),
    (
        "personalized_model",
        "personalized_score"
    ),
]:

    for k in [1, 3, 5]:

        precision, users = (
            precision_at_k(
                test,
                score_column,
                k,
            )
        )

        ranking_results.append({
            "policy":
                policy,

            "k":
                k,

            "precision_at_k":
                precision,

            "eligible_users":
                users,
        })


ranking_results = pd.DataFrame(
    ranking_results
)


# ============================================================
# 7. TOP-5 RANKINGS
# ============================================================

baseline_top5 = rank_experiences(
    test,
    score_column="baseline_score",
    k=5,
)

personalized_top5 = rank_experiences(
    test,
    score_column="personalized_score",
    k=5,
)


baseline_top5.to_csv(
    f"{OUTPUT_DIR}/"
    "baseline_top5.csv",
    index=False,
)

personalized_top5.to_csv(
    f"{OUTPUT_DIR}/"
    "personalized_top5.csv",
    index=False,
)


# ============================================================
# 8. FIND TWO USERS WITH DIFFERENT PREFERENCES
# ============================================================

profiles = (
    test[
        [
            "user_id",
            "preferred_category",
            "secondary_category",
        ]
    ]
    .drop_duplicates(
        "user_id"
    )
)


first_user = profiles.iloc[0]

different = profiles[
    profiles[
        "preferred_category"
    ]
    != first_user[
        "preferred_category"
    ]
]

second_user = different.iloc[0]


demo_users = [
    int(first_user["user_id"]),
    int(second_user["user_id"]),
]


demo = personalized_top5[
    personalized_top5[
        "user_id"
    ].isin(demo_users)
][
    [
        "user_id",
        "rank",
        "experience_id",
        "experience_name",
        "category",
        "preferred_category",
        "secondary_category",
        "personalized_score",
        "meaningful_engagement",
    ]
]


demo.to_csv(
    f"{OUTPUT_DIR}/"
    "example_personalized_recommendations.csv",
    index=False,
)


# ============================================================
# 9. SAVE METRICS
# ============================================================

predictive_results.to_csv(
    f"{OUTPUT_DIR}/"
    "predictive_metrics.csv",
    index=False,
)

ranking_results.to_csv(
    f"{OUTPUT_DIR}/"
    "ranking_metrics.csv",
    index=False,
)


# ============================================================
# 10. OUTPUT
# ============================================================

print(
    "\n=== PREDICTIVE PERFORMANCE ==="
)

print(
    predictive_results.to_string(
        index=False
    )
)


print(
    "\n=== RANKING PERFORMANCE ==="
)

print(
    ranking_results.to_string(
        index=False
    )
)


print(
    "\n=== EXAMPLE PERSONALIZED RANKINGS ==="
)

for user_id in demo_users:

    user_demo = demo[
        demo["user_id"] == user_id
    ]

    preference = (
        user_demo[
            "preferred_category"
        ].iloc[0]
    )

    secondary = (
        user_demo[
            "secondary_category"
        ].iloc[0]
    )

    print(
        f"\nUser {user_id}"
        f" | Primary: {preference}"
        f" | Secondary: {secondary}"
    )

    print(
        user_demo[
            [
                "rank",
                "experience_name",
                "category",
                "personalized_score",
            ]
        ].to_string(
            index=False
        )
    )


print(
    f"\nModel saved to: "
    f"{MODEL_PATH}"
)

print(
    "\nNOTE: All experience data and "
    "engagement outcomes in this demo "
    "are synthetic."
)