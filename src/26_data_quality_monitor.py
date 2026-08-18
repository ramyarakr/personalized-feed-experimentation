import pandas as pd

from src.data_quality import (
    run_quality_checks
)


DATA_PATH = (
    "outputs/experience_demo/"
    "synthetic_interactions.csv"
)

OUTPUT_PATH = (
    "outputs/experience_demo/"
    "data_quality_report.csv"
)


df = pd.read_csv(DATA_PATH)

results = run_quality_checks(df)

results.to_csv(
    OUTPUT_PATH,
    index=False
)

print("=== DATA QUALITY REPORT ===")
print(results.to_string(index=False))

failed = results[
    results["passed"] == False
]

if len(failed) > 0:
    raise RuntimeError(
        f"{len(failed)} data-quality checks failed"
    )

print("\nAll data-quality checks passed.")