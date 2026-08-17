import pandas as pd

PATH = "outputs/tables/surface_heterogeneity_features.csv"

df = pd.read_csv(PATH)

summary = (
    df.groupby("dominant_tab")
    .agg(
        rows=("user_id", "size"),
        users=("user_id", "nunique"),

        avg_long_view_rate=("long_view_rate_t", "mean"),
        median_long_view_rate=("long_view_rate_t", "median"),

        avg_prior_sessions_per_day=(
            "prior_7d_sessions_per_day", "mean"
        ),

        avg_prior_minutes_per_session=(
            "prior_7d_avg_minutes_per_session", "mean"
        ),

        avg_same_day_sessions=(
            "sessions_t", "mean"
        ),

        avg_future_7d_sessions=(
            "future_7d_sessions", "mean"
        )
    )
    .reset_index()
)

summary.to_csv(
    "outputs/tables/surface_user_composition.csv",
    index=False
)

print(summary.to_string(index=False))