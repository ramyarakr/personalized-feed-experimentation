import time
import joblib
import numpy as np
import pandas as pd


DATA_PATH = (
    "outputs/experience_demo/"
    "synthetic_interactions.csv"
)

MODEL_PATH = (
    "outputs/experience_demo/"
    "experience_ranker.joblib"
)

OUTPUT_PATH = (
    "outputs/experience_demo/"
    "scale_benchmark.csv"
)


FEATURES = [
    "quality_score",
    "popularity_score",
    "novelty_score",
    "difficulty",
    "avg_session_minutes",
    "novelty_preference",
    "social_preference",
    "preferred_session_minutes",
    "primary_category_match",
    "secondary_category_match",
    "session_length_gap",
    "novelty_alignment",
    "category",
    "preferred_category",
    "secondary_category",
]


base = pd.read_csv(DATA_PATH)

model = joblib.load(MODEL_PATH)


# ============================================================
# Score data in chunks instead of creating huge files.
# ============================================================

TARGET_SIZES = [
    100_000,
    500_000,
    1_000_000,
]

CHUNK_SIZE = 50_000

results = []


for target_size in TARGET_SIZES:

    scored = 0

    start = time.perf_counter()

    while scored < target_size:

        remaining = target_size - scored

        current_size = min(
            CHUNK_SIZE,
            remaining
        )

        sample = base.sample(
            n=current_size,
            replace=True,
            random_state=scored + 42
        )

        scores = model.predict_proba(
            sample[FEATURES]
        )[:, 1]

        # Force computation to complete
        _ = np.mean(scores)

        scored += current_size

    elapsed = (
        time.perf_counter()
        - start
    )

    throughput = (
        target_size / elapsed
    )

    results.append({
        "candidate_rows": target_size,
        "elapsed_seconds": elapsed,
        "rows_per_second": throughput,
        "chunk_size": CHUNK_SIZE,
    })

    print(
        f"{target_size:,} candidates | "
        f"{elapsed:.2f}s | "
        f"{throughput:,.0f} rows/sec"
    )


results = pd.DataFrame(results)

results.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nSaved benchmark to: "
    f"{OUTPUT_PATH}"
)