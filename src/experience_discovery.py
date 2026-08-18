import pandas as pd

from sklearn.compose import (
    ColumnTransformer
)

from sklearn.impute import (
    SimpleImputer
)

from sklearn.linear_model import (
    LogisticRegression
)

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)


NUMERIC_FEATURES = [
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
]


CATEGORICAL_FEATURES = [
    "category",
    "preferred_category",
    "secondary_category",
]


FEATURES = (
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
)


def build_experience_model():

    numeric_pipeline = Pipeline([
        (
            "impute",
            SimpleImputer(
                strategy="median"
            )
        ),
        (
            "scale",
            StandardScaler()
        ),
    ])

    categorical_pipeline = Pipeline([
        (
            "impute",
            SimpleImputer(
                strategy="most_frequent"
            )
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        ),
    ])

    preprocessing = ColumnTransformer([
        (
            "numeric",
            numeric_pipeline,
            NUMERIC_FEATURES
        ),
        (
            "categorical",
            categorical_pipeline,
            CATEGORICAL_FEATURES
        ),
    ])

    model = Pipeline([
        (
            "features",
            preprocessing
        ),
        (
            "model",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        ),
    ])

    return model


def train_experience_model(
    df: pd.DataFrame
):

    model = build_experience_model()

    model.fit(
        df[FEATURES],
        df["meaningful_engagement"]
    )

    return model


def score_experiences(
    model,
    df: pd.DataFrame
):

    scores = model.predict_proba(
        df[FEATURES]
    )[:, 1]

    return pd.Series(
        scores,
        index=df.index,
        name="personalized_score"
    )


def rank_experiences(
    df: pd.DataFrame,
    score_column: str,
    k: int = 5
):

    if k <= 0:
        raise ValueError(
            "k must be greater than 0"
        )

    required = {
        "user_id",
        "experience_id",
        score_column,
    }

    missing = required - set(
        df.columns
    )

    if missing:
        raise ValueError(
            f"Missing columns: "
            f"{sorted(missing)}"
        )

    ranked = (
        df
        .sort_values(
            [
                "user_id",
                score_column,
            ],
            ascending=[
                True,
                False,
            ]
        )
        .groupby(
            "user_id",
            group_keys=False
        )
        .head(k)
        .copy()
    )

    ranked["rank"] = (
        ranked
        .groupby("user_id")
        .cumcount()
        + 1
    )

    return ranked