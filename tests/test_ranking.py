import pandas as pd
import pytest

from src.ranking import (
    historical_quality_score,
    rank_candidates
)


def test_historical_quality_score():

    df = pd.DataFrame({
        "prior_video_long_view_rate": [
            0.20,
            0.50
        ],
        "prior_video_interactions": [
            100,
            0
        ]
    })

    scores = historical_quality_score(
        df,
        global_prior=0.10,
        smoothing=20
    )

    expected_first = (
        0.20 * 100 + 0.10 * 20
    ) / 120

    assert scores.iloc[0] == pytest.approx(
        expected_first
    )

    # No history should fall back to global prior
    assert scores.iloc[1] == pytest.approx(
        0.10
    )


def test_rank_candidates_returns_top_k():

    df = pd.DataFrame({
        "user_id": [1, 1, 1],
        "date": [20220503] * 3,
        "video_id": [10, 20, 30],
        "score": [0.2, 0.9, 0.5]
    })

    result = rank_candidates(
        df,
        score_column="score",
        k=2
    )

    assert result["video_id"].tolist() == [
        20,
        30
    ]

    assert result["rank"].tolist() == [
        1,
        2
    ]


def test_rank_candidates_rejects_invalid_k():

    df = pd.DataFrame({
        "user_id": [1],
        "date": [20220503],
        "video_id": [10],
        "score": [0.5]
    })

    with pytest.raises(ValueError):
        rank_candidates(
            df,
            score_column="score",
            k=0
        )