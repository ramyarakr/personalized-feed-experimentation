import pandas as pd

from src.personalized_ranker import (
    train_model,
    score_candidates,
)


def sample_data():

    return pd.DataFrame({
        "prior_user_interactions": [10, 20, 30, 40],
        "prior_user_long_view_rate": [0.1, 0.2, 0.3, 0.4],
        "prior_user_like_rate": [0.01, 0.02, 0.03, 0.04],
        "prior_user_follow_rate": [0.0, 0.01, 0.0, 0.01],
        "prior_user_avg_play_time_ms": [1000, 2000, 3000, 4000],

        "prior_video_interactions": [100, 200, 300, 400],
        "prior_video_long_view_rate": [0.1, 0.2, 0.3, 0.4],
        "prior_video_like_rate": [0.01, 0.02, 0.03, 0.04],
        "prior_video_follow_rate": [0.0, 0.01, 0.0, 0.01],
        "prior_video_avg_play_time_ms": [1000, 2000, 3000, 4000],

        "video_duration": [10000, 20000, 30000, 40000],
        "hourmin": [900, 1000, 1100, 1200],

        "tab": [1, 1, 2, 2],
        "video_type": ["NORMAL"] * 4,
        "upload_type": ["Web"] * 4,

        "long_view": [0, 0, 1, 1],
    })


def test_personalized_ranker_scores_candidates():

    df = sample_data()

    model = train_model(df)

    scores = score_candidates(
        model,
        df,
    )

    assert len(scores) == len(df)

    assert scores.between(
        0,
        1
    ).all()