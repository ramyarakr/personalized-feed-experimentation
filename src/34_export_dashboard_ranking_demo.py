import json
import os

import joblib
import numpy as np
import pandas as pd

from src.experience_discovery import (
    score_experiences,
)


DATA_PATH = (
    "outputs/experience_demo/"
    "synthetic_interactions.csv"
)

MODEL_PATH = (
    "outputs/experience_demo/"
    "experience_ranker.joblib"
)

OUTPUT_PATH = (
    "docs/assets/"
    "ranking_demo.json"
)

SEED = 123
SMOOTHING = 20


# ============================================================
# Load data
# ============================================================

df = pd.read_csv(DATA_PATH)

model = joblib.load(MODEL_PATH)


# ============================================================
# Reproduce the same train/test split used in the demo
# ============================================================

rng = np.random.default_rng(SEED)

df["split_random"] = rng.random(
    len(df)
)

train = df[
    df["split_random"] < 0.70
].copy()

test = df[
    df["split_random"] >= 0.70
].copy()


# ============================================================
# Historical baseline
# ============================================================

history = (
    train
    .groupby("experience_id")
    .agg(
        prior_exposures=(
            "meaningful_engagement",
            "size",
        ),

        prior_engagement_rate=(
            "meaningful_engagement",
            "mean",
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
    train["meaningful_engagement"]
    .mean()
)


test["prior_exposures"] = (
    test["prior_exposures"]
    .fillna(0)
)


test["prior_engagement_rate"] = (
    test["prior_engagement_rate"]
    .fillna(global_rate)
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
# Personalized model scores
# ============================================================

test["personalized_score"] = (
    score_experiences(
        model,
        test,
    )
)


# ============================================================
# Pick several users with different primary preferences
# ============================================================

profiles = (
    test[
        [
            "user_id",
            "preferred_category",
            "secondary_category",
            "novelty_preference",
            "social_preference",
            "preferred_session_minutes",
        ]
    ]
    .drop_duplicates("user_id")
    .sort_values("user_id")
)


selected_users = []

used_categories = set()


for row in profiles.itertuples(index=False):

    if (
        row.preferred_category
        not in used_categories
    ):

        selected_users.append(
            row.user_id
        )

        used_categories.add(
            row.preferred_category
        )

    if len(selected_users) == 6:
        break


# ============================================================
# Build dashboard JSON
# ============================================================

users_json = []


for user_id in selected_users:

    user_rows = (
        test[
            test["user_id"] == user_id
        ]
        .copy()
    )

    profile = user_rows.iloc[0]

    candidates = []


    for row in user_rows.itertuples(
        index=False
    ):

        candidates.append({
            "experience_id":
                int(row.experience_id),

            "experience_name":
                str(row.experience_name),

            "category":
                str(row.category),

            "quality_score":
                round(
                    float(row.quality_score),
                    4,
                ),

            "popularity_score":
                round(
                    float(row.popularity_score),
                    4,
                ),

            "novelty_score":
                round(
                    float(row.novelty_score),
                    4,
                ),

            "avg_session_minutes":
                int(
                    row.avg_session_minutes
                ),

            "primary_category_match":
                int(
                    row.primary_category_match
                ),

            "secondary_category_match":
                int(
                    row.secondary_category_match
                ),

            "novelty_alignment":
                round(
                    float(
                        row.novelty_alignment
                    ),
                    4,
                ),

            "session_length_gap":
                round(
                    float(
                        row.session_length_gap
                    ),
                    4,
                ),

            "baseline_score":
                round(
                    float(
                        row.baseline_score
                    ),
                    6,
                ),

            "personalized_score":
                round(
                    float(
                        row.personalized_score
                    ),
                    6,
                ),
        })


    users_json.append({
        "user_id":
            int(user_id),

        "preferred_category":
            str(
                profile[
                    "preferred_category"
                ]
            ),

        "secondary_category":
            str(
                profile[
                    "secondary_category"
                ]
            ),

        "novelty_preference":
            round(
                float(
                    profile[
                        "novelty_preference"
                    ]
                ),
                3,
            ),

        "social_preference":
            round(
                float(
                    profile[
                        "social_preference"
                    ]
                ),
                3,
            ),

        "preferred_session_minutes":
            int(
                profile[
                    "preferred_session_minutes"
                ]
            ),

        "candidates":
            candidates,
    })


output = {
    "description": (
        "Synthetic demonstration using the "
        "trained recommendation model."
    ),

    "global_engagement_rate":
        round(
            float(global_rate),
            6,
        ),

    "users":
        users_json,
}


os.makedirs(
    "docs/assets",
    exist_ok=True,
)


with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        output,
        f,
        indent=2,
    )


print(
    f"Exported {len(users_json)} "
    f"interactive user profiles."
)

print(
    f"Saved to: {OUTPUT_PATH}"
)