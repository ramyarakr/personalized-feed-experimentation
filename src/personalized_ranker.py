import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = [
    "prior_user_interactions",
    "prior_user_long_view_rate",
    "prior_user_like_rate",
    "prior_user_follow_rate",
    "prior_user_avg_play_time_ms",
    "prior_video_interactions",
    "prior_video_long_view_rate",
    "prior_video_like_rate",
    "prior_video_follow_rate",
    "prior_video_avg_play_time_ms",
    "video_duration",
    "hourmin",
]

CATEGORICAL_FEATURES = [
    "tab",
    "video_type",
    "upload_type",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def build_model():

    numeric_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        (
            "onehot",
            OneHotEncoder(handle_unknown="ignore"),
        ),
    ])

    preprocessing = ColumnTransformer([
        ("numeric", numeric_pipeline, NUMERIC_FEATURES),
        ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
    ])

    return Pipeline([
        ("features", preprocessing),
        (
            "model",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
            ),
        ),
    ])


def train_model(df: pd.DataFrame):

    model = build_model()

    X = df[FEATURES]
    y = df["long_view"]

    model.fit(X, y)

    return model


def score_candidates(
    model,
    df: pd.DataFrame,
) -> pd.Series:

    return pd.Series(
        model.predict_proba(df[FEATURES])[:, 1],
        index=df.index,
        name="personalized_score",
    )


def save_model(model, path):
    joblib.dump(model, path)


def load_model(path):
    return joblib.load(path)