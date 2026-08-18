import argparse
import json

import pandas as pd


REFERENCE_PATH = (
    "outputs/experience_demo/"
    "pipeline_health.json"
)


def run_drift_check(
    data_path,
    output_path
):

    df = pd.read_csv(data_path)

    with open(REFERENCE_PATH) as f:
        reference = json.load(f)

    current = {
        "meaningful_engagement_rate":
            df["meaningful_engagement"].mean(),

        "quality_score":
            df["quality_score"].mean(),

        "popularity_score":
            df["popularity_score"].mean(),

        "novelty_score":
            df["novelty_score"].mean(),
    }

    reference_values = {
        "meaningful_engagement_rate":
            reference[
                "meaningful_engagement_rate"
            ],

        "quality_score":
            reference[
                "feature_means"
            ]["quality_score"],

        "popularity_score":
            reference[
                "feature_means"
            ]["popularity_score"],

        "novelty_score":
            reference[
                "feature_means"
            ]["novelty_score"],
    }

    THRESHOLDS = {
        "meaningful_engagement_rate": 0.10,
        "quality_score": 0.10,
        "popularity_score": 0.10,
        "novelty_score": 0.10,
    }

    rows = []

    for metric in current:

        ref = reference_values[metric]
        cur = current[metric]

        relative_change = (
            (cur - ref) / ref
            if ref != 0
            else 0
        )

        threshold = THRESHOLDS[metric]

        passed = (
            abs(relative_change)
            <= threshold
        )

        rows.append({
            "metric": metric,
            "reference_value": ref,
            "current_value": cur,
            "relative_change": relative_change,
            "threshold": threshold,
            "passed": passed,
        })

    results = pd.DataFrame(rows)

    results.to_csv(
        output_path,
        index=False
    )

    print("=== DRIFT REPORT ===")
    print(results.to_string(index=False))

    failed = results[
        results["passed"] == False
    ]

    if len(failed):
        print(
            f"\nALERT: "
            f"{len(failed)} drift checks "
            f"exceeded thresholds."
        )
    else:
        print(
            "\nNo material drift detected."
        )
    return results


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data",
        required=True
    )

    parser.add_argument(
        "--output",
        required=True
    )

    args = parser.parse_args()

    run_drift_check(
        args.data,
        args.output
    )


if __name__ == "__main__":
    main()