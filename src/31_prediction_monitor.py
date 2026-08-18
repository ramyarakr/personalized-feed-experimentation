import argparse
import json

import joblib
import pandas as pd

from src.experience_discovery import score_experiences


MODEL_PATH = (
    "outputs/experience_demo/"
    "experience_ranker.joblib"
)

REFERENCE_PATH = (
    "outputs/experience_demo/"
    "prediction_reference.json"
)


def prediction_metrics(scores):

    return {
        "mean_score": float(scores.mean()),
        "median_score": float(scores.median()),
        "p10_score": float(scores.quantile(0.10)),
        "p90_score": float(scores.quantile(0.90)),
    }


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data",
        required=True,
    )

    parser.add_argument(
        "--mode",
        choices=["reference", "check"],
        required=True,
    )

    args = parser.parse_args()

    df = pd.read_csv(args.data)

    model = joblib.load(MODEL_PATH)

    scores = score_experiences(
        model,
        df,
    )

    current = prediction_metrics(scores)

    print("=== PREDICTION HEALTH ===")

    for key, value in current.items():
        print(f"{key}: {value:.4f}")

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
            "\nPrediction reference saved."
        )

        return

    with open(
        REFERENCE_PATH
    ) as f:
        reference = json.load(f)

    threshold = 0.10

    print("\n=== PREDICTION DRIFT ===")

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
            abs(relative_change)
            <= threshold
        )

        if not passed:
            failed += 1

        print(
            f"{metric:15s} "
            f"reference={ref:.4f} "
            f"current={cur:.4f} "
            f"change={relative_change:.2%} "
            f"{'PASS' if passed else 'ALERT'}"
        )

    if failed:
        print(
            f"\nALERT: {failed} prediction "
            f"metrics exceeded thresholds."
        )
    else:
        print(
            "\nNo material prediction drift detected."
        )


if __name__ == "__main__":
    main()