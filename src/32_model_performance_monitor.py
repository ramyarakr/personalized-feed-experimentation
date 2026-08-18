import argparse
import json

import joblib
import pandas as pd

from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
)

from src.experience_discovery import (
    score_experiences,
)


MODEL_PATH = (
    "outputs/experience_demo/"
    "experience_ranker.joblib"
)

REFERENCE_PATH = (
    "outputs/experience_demo/"
    "model_performance_reference.json"
)


def calculate_metrics(df, model):

    scores = score_experiences(
        model,
        df,
    )

    y = df["meaningful_engagement"]

    return {
        "roc_auc": float(
            roc_auc_score(
                y,
                scores,
            )
        ),

        "average_precision": float(
            average_precision_score(
                y,
                scores,
            )
        ),
    }


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data",
        required=True,
    )

    parser.add_argument(
        "--mode",
        choices=[
            "reference",
            "check",
        ],
        required=True,
    )

    args = parser.parse_args()

    df = pd.read_csv(args.data)

    model = joblib.load(
        MODEL_PATH
    )

    current = calculate_metrics(
        df,
        model,
    )

    print(
        "=== MODEL PERFORMANCE ==="
    )

    for metric, value in current.items():

        print(
            f"{metric}: {value:.4f}"
        )

    if args.mode == "reference":

        with open(
            REFERENCE_PATH,
            "w",
        ) as f:

            json.dump(
                current,
                f,
                indent=2,
            )

        print(
            "\nPerformance reference saved."
        )

        return


    with open(
        REFERENCE_PATH
    ) as f:

        reference = json.load(f)


    # Alert if model quality falls
    # more than 10% relative.
    threshold = -0.10

    print(
        "\n=== PERFORMANCE CHANGE ==="
    )

    failed = 0

    for metric in current:

        ref = reference[metric]
        cur = current[metric]

        relative_change = (
            (cur - ref) / ref
            if ref != 0
            else 0
        )

        passed = (
            relative_change >= threshold
        )

        if not passed:
            failed += 1

        print(
            f"{metric:18s} "
            f"reference={ref:.4f} "
            f"current={cur:.4f} "
            f"change={relative_change:.2%} "
            f"{'PASS' if passed else 'ALERT'}"
        )


    if failed:

        print(
            f"\nALERT: {failed} model "
            f"performance metrics degraded."
        )

    else:

        print(
            "\nNo material model "
            "performance degradation detected."
        )


if __name__ == "__main__":
    main()