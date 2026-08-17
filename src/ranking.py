import pandas as pd


def historical_quality_score(
    df: pd.DataFrame,
    global_prior: float,
    smoothing: int = 20
) -> pd.Series:
    """
    Smoothed historical long-view score.

    Prevents videos with very small historical sample sizes
    from receiving extreme ranking scores.
    """

    numerator = (
        df["prior_video_long_view_rate"]
        * df["prior_video_interactions"]
        + global_prior * smoothing
    )

    denominator = (
        df["prior_video_interactions"]
        + smoothing
    )

    return numerator / denominator


def rank_candidates(
    df: pd.DataFrame,
    score_column: str,
    k: int = 10
) -> pd.DataFrame:
    """
    Return the highest-ranked K candidates for each user-day.
    """

    required = {
        "user_id",
        "date",
        "video_id",
        score_column
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if k <= 0:
        raise ValueError("k must be greater than 0")

    ranked = (
        df.sort_values(
            ["user_id", "date", score_column],
            ascending=[True, True, False]
        )
        .groupby(
            ["user_id", "date"],
            group_keys=False
        )
        .head(k)
        .copy()
    )

    ranked["rank"] = (
        ranked
        .groupby(["user_id", "date"])
        .cumcount()
        + 1
    )

    return ranked