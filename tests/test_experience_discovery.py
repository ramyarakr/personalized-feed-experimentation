import pandas as pd

from src.experience_discovery import (
    train_experience_model,
    score_experiences,
    rank_experiences,
)


def sample_data():

    return pd.DataFrame({
        "user_id": [
            1, 1, 1, 2, 2, 2
        ],

        "experience_id": [
            10, 20, 30, 10, 20, 30
        ],

        "category": [
            "Action",
            "Strategy",
            "Puzzle",
            "Action",
            "Strategy",
            "Puzzle",
        ],

        "quality_score": [
            .8, .7, .6,
            .8, .7, .6
        ],

        "popularity_score": [
            .5, .6, .4,
            .5, .6, .4
        ],

        "novelty_score": [
            .4, .5, .7,
            .4, .5, .7
        ],

        "difficulty": [
            .5, .6, .4,
            .5, .6, .4
        ],

        "avg_session_minutes": [
            20, 40, 15,
            20, 40, 15
        ],

        "preferred_category": [
            "Action",
            "Action",
            "Action",
            "Strategy",
            "Strategy",
            "Strategy",
        ],

        "secondary_category": [
            "Puzzle",
            "Puzzle",
            "Puzzle",
            "Action",
            "Action",
            "Action",
        ],

        "novelty_preference": [
            .5, .5, .5,
            .7, .7, .7
        ],

        "social_preference": [
            .3, .3, .3,
            .6, .6, .6
        ],

        "preferred_session_minutes": [
            20, 20, 20,
            40, 40, 40
        ],

        "primary_category_match": [
            1, 0, 0,
            0, 1, 0
        ],

        "secondary_category_match": [
            0, 0, 1,
            1, 0, 0
        ],

        "session_length_gap": [
            0,
            .33,
            .08,
            .33,
            0,
            .42,
        ],

        "novelty_alignment": [
            .9, 1, .8,
            .7, .8, 1
        ],

        "meaningful_engagement": [
            1, 0, 1,
            0, 1, 0
        ],
    })


def test_experience_ranker():

    df = sample_data()

    model = train_experience_model(
        df
    )

    scores = score_experiences(
        model,
        df
    )

    assert len(scores) == len(df)

    assert scores.between(
        0,
        1
    ).all()


def test_rank_experiences_top_k():

    df = pd.DataFrame({
        "user_id": [1, 1, 1],
        "experience_id": [10, 20, 30],
        "score": [.2, .9, .5],
    })

    result = rank_experiences(
        df,
        score_column="score",
        k=2,
    )

    assert (
        result[
            "experience_id"
        ].tolist()
        == [20, 30]
    )

    assert (
        result[
            "rank"
        ].tolist()
        == [1, 2]
    )