import pandas as pd

from src.data_quality import run_quality_checks
from src.drift_monitor import run_drift_check


def test_quality_checks_pass_clean_data():

    df = pd.DataFrame({
        "user_id": [1, 2],
        "experience_id": [10, 20],
        "quality_score": [0.7, 0.8],
        "popularity_score": [0.4, 0.5],
        "novelty_score": [0.5, 0.6],
        "meaningful_engagement": [0, 1],
    })

    results = run_quality_checks(df)

    assert results["passed"].all()


def test_quality_checks_detect_invalid_score():

    df = pd.DataFrame({
        "user_id": [1],
        "experience_id": [10],
        "quality_score": [1.5],
        "popularity_score": [0.4],
        "novelty_score": [0.5],
        "meaningful_engagement": [1],
    })

    results = run_quality_checks(df)

    row = results[
        results["check"]
        == "quality_score_range"
    ].iloc[0]

    assert not bool(row["passed"])