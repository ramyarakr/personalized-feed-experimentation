import argparse
import os

import joblib
import pandas as pd

from src.data_quality import run_quality_checks
from src.drift_monitor import run_drift_check
from src.experience_discovery import (
    score_experiences,
    rank_experiences,
)


MODEL_PATH = (
    "outputs/experience_demo/"
    "experience_ranker.joblib"
)


def run_pipeline(
    data_path,
    output_path,
    k,
):

    print("=== RANKING PIPELINE ===")

    # --------------------------------------------------------
    # 1. Load
    # --------------------------------------------------------

    df = pd.read_csv(data_path)

    print(
        f"\nLoaded {len(df):,} candidate rows."
    )


    # --------------------------------------------------------
    # 2. Data quality gate
    # --------------------------------------------------------

    print("\n[1/4] Data quality checks")

    quality = run_quality_checks(df)

    failed_quality = quality[
        quality["passed"] == False
    ]

    if len(failed_quality):
        print(
            failed_quality.to_string(
                index=False
            )
        )

        raise RuntimeError(
            "Pipeline stopped: "
            "data-quality checks failed."
        )

    print("PASS")


    # --------------------------------------------------------
    # 3. Drift gate
    # --------------------------------------------------------

    print("\n[2/4] Drift monitoring")

    drift_output = (
        "outputs/experience_demo/"
        "pipeline_drift_report.csv"
    )

    drift = run_drift_check(
        data_path,
        drift_output,
    )

    failed_drift = drift[
        drift["passed"] == False
    ]

    if len(failed_drift):

        print(
            "\nWARNING: material drift detected."
        )

        print(
            failed_drift[
                [
                    "metric",
                    "relative_change",
                    "threshold",
                ]
            ].to_string(
                index=False
            )
        )

        raise RuntimeError(
            "Pipeline stopped: "
            "drift thresholds exceeded."
        )

    print("PASS")


    # --------------------------------------------------------
    # 4. Model scoring
    # --------------------------------------------------------

    print("\n[3/4] Personalized scoring")

    model = joblib.load(
        MODEL_PATH
    )

    df["personalized_score"] = (
        score_experiences(
            model,
            df,
        )
    )

    print("PASS")


    # --------------------------------------------------------
    # 5. Top-K ranking
    # --------------------------------------------------------

    print(
        f"\n[4/4] Generate top-{k} rankings"
    )

    ranked = rank_experiences(
        df,
        score_column="personalized_score",
        k=k,
    )

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True,
    )

    ranked.to_csv(
        output_path,
        index=False,
    )

    print("PASS")

    print(
        f"\nUsers ranked: "
        f"{ranked['user_id'].nunique():,}"
    )

    print(
        f"Recommendations generated: "
        f"{len(ranked):,}"
    )

    print(
        f"Saved to: {output_path}"
    )

    print(
        "\n=== PIPELINE COMPLETE ==="
    )


def main():

    parser = argparse.ArgumentParser(
        description=(
            "End-to-end personalized "
            "ranking pipeline"
        )
    )

    parser.add_argument(
        "--data",
        required=True,
    )

    parser.add_argument(
        "--output",
        required=True,
    )

    parser.add_argument(
        "--k",
        type=int,
        default=5,
    )

    args = parser.parse_args()

    run_pipeline(
        args.data,
        args.output,
        args.k,
    )


if __name__ == "__main__":
    main()