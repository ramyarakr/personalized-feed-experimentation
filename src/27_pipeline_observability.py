import json
from datetime import datetime, timezone

import pandas as pd


DATA_PATH = (
    "outputs/experience_demo/"
    "synthetic_interactions.csv"
)

OUTPUT_PATH = (
    "outputs/experience_demo/"
    "pipeline_health.json"
)


df = pd.read_csv(DATA_PATH)


metrics = {
    "generated_at_utc":
        datetime.now(timezone.utc).isoformat(),

    "row_count":
        int(len(df)),

    "unique_users":
        int(df["user_id"].nunique()),

    "unique_experiences":
        int(df["experience_id"].nunique()),

    "meaningful_engagement_rate":
        float(
            df["meaningful_engagement"].mean()
        ),

    "average_candidates_per_user":
        float(
            df.groupby("user_id")
            .size()
            .mean()
        ),

    "missing_value_rate":
        float(
            df.isna().mean().mean()
        ),

    "duplicate_user_experience_rows":
        int(
            df.duplicated(
                ["user_id", "experience_id"]
            ).sum()
        ),

    "feature_means": {
        "quality_score":
            float(df["quality_score"].mean()),

        "popularity_score":
            float(df["popularity_score"].mean()),

        "novelty_score":
            float(df["novelty_score"].mean()),
    },
}


with open(
    OUTPUT_PATH,
    "w"
) as f:
    json.dump(
        metrics,
        f,
        indent=2
    )


print("=== PIPELINE HEALTH ===")

for key, value in metrics.items():

    if key == "feature_means":
        continue

    print(
        f"{key}: {value}"
    )


print("\nFeature means:")

for feature, value in (
    metrics["feature_means"].items()
):
    print(
        f"  {feature}: {value:.4f}"
    )


print(
    f"\nSaved to: {OUTPUT_PATH}"
)