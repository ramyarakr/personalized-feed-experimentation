import pandas as pd


REQUIRED_COLUMNS = [
    "user_id",
    "experience_id",
    "quality_score",
    "popularity_score",
    "novelty_score",
    "meaningful_engagement",
]


def run_quality_checks(df: pd.DataFrame):

    checks = []

    # Required columns
    missing_columns = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    checks.append({
        "check": "required_columns",
        "passed": len(missing_columns) == 0,
        "details": (
            "OK"
            if not missing_columns
            else f"Missing: {missing_columns}"
        ),
    })

    # Missing IDs
    missing_ids = (
        df["user_id"].isna().sum()
        + df["experience_id"].isna().sum()
    )

    checks.append({
        "check": "missing_ids",
        "passed": missing_ids == 0,
        "details": f"{missing_ids} missing IDs",
    })

    # Binary outcome
    invalid_outcomes = (
        ~df["meaningful_engagement"]
        .isin([0, 1])
    ).sum()

    checks.append({
        "check": "valid_binary_outcome",
        "passed": invalid_outcomes == 0,
        "details": (
            f"{invalid_outcomes} invalid values"
        ),
    })

    # Score ranges
    for column in [
        "quality_score",
        "popularity_score",
        "novelty_score",
    ]:

        invalid = (
            ~df[column].between(0, 1)
        ).sum()

        checks.append({
            "check": f"{column}_range",
            "passed": invalid == 0,
            "details": (
                f"{invalid} values outside [0,1]"
            ),
        })

    # Duplicate user-experience rows
    duplicates = df.duplicated(
        ["user_id", "experience_id"]
    ).sum()

    checks.append({
        "check": "duplicate_user_experience",
        "passed": duplicates == 0,
        "details": f"{duplicates} duplicates",
    })

    return pd.DataFrame(checks)