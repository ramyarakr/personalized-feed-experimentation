import argparse
import pandas as pd

from src.ranking import (
    historical_quality_score,
    rank_candidates,
)

from src.personalized_ranker import (
    load_model,
    score_candidates,
)


MODEL_PATH = "outputs/models/personalized_ranker.joblib"


def run_ranking(input_path, output_path, k, policy):

    df = pd.read_csv(input_path)

    if policy == "baseline":

        global_prior = df["long_view"].mean()

        df["ranking_score"] = historical_quality_score(
            df,
            global_prior=global_prior,
            smoothing=20,
        )

    elif policy == "personalized":

        model = load_model(MODEL_PATH)

        df["ranking_score"] = score_candidates(
            model,
            df,
        )

    else:
        raise ValueError(
            f"Unknown policy: {policy}"
        )

    ranked = rank_candidates(
        df,
        score_column="ranking_score",
        k=k,
    )

    ranked.to_csv(
        output_path,
        index=False,
    )

    print(f"Policy: {policy}")
    print(f"Ranked {len(ranked):,} candidates")
    print(f"Saved to: {output_path}")


def main():

    parser = argparse.ArgumentParser(
        description="Personalized Feed Ranking CLI"
    )

    parser.add_argument(
        "--input",
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

    parser.add_argument(
        "--policy",
        choices=[
            "baseline",
            "personalized",
        ],
        required=True,
    )

    args = parser.parse_args()

    run_ranking(
        args.input,
        args.output,
        args.k,
        args.policy,
    )


if __name__ == "__main__":
    main()