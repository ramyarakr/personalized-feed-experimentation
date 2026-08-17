import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score


PATH = "outputs/tables/randomized_ranking_dataset.csv"

df = pd.read_csv(PATH)

# ------------------------------------------------------------
# 1. Time-based train/test split
# ------------------------------------------------------------

df["date"] = pd.to_datetime(df["date"].astype(str))

dates = sorted(df["date"].unique())

split_idx = int(len(dates) * 0.65)
split_date = dates[split_idx]

train = df[df["date"] < split_date].copy()
test = df[df["date"] >= split_date].copy()

print(f"Train rows: {len(train):,}")
print(f"Test rows: {len(test):,}")
print(f"Split date: {pd.Timestamp(split_date).date()}")


# ------------------------------------------------------------
# 2. Baseline ranking policy
#
# Rank using historical video long-view performance.
# ------------------------------------------------------------

# Smoothed prior prevents tiny-history videos from dominating.
GLOBAL_PRIOR = train["long_view"].mean()
SMOOTHING = 20

test["baseline_score"] = (
    (
        test["prior_video_long_view_rate"]
        * test["prior_video_interactions"]
    )
    + GLOBAL_PRIOR * SMOOTHING
) / (
    test["prior_video_interactions"] + SMOOTHING
)


# ------------------------------------------------------------
# 3. Personalized challenger
# ------------------------------------------------------------

numeric_features = [
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
    "hourmin"
]

categorical_features = [
    "tab",
    "video_type",
    "upload_type"
]

numeric_pipeline = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler())
])

categorical_pipeline = Pipeline([
    (
        "impute",
        SimpleImputer(strategy="most_frequent")
    ),
    (
        "onehot",
        OneHotEncoder(
            handle_unknown="ignore"
        )
    )
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features)
])

model = Pipeline([
    ("features", preprocessor),

    (
        "model",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )
    )
])

X_train = train[numeric_features + categorical_features]
y_train = train["long_view"]

X_test = test[numeric_features + categorical_features]
y_test = test["long_view"]

model.fit(X_train, y_train)

test["challenger_score"] = model.predict_proba(X_test)[:, 1]


# ------------------------------------------------------------
# 4. Predictive evaluation
# ------------------------------------------------------------

metrics = []

for policy, score in [
    ("historical_popularity", "baseline_score"),
    ("personalized_model", "challenger_score")
]:
    metrics.append({
        "policy": policy,
        "roc_auc": roc_auc_score(
            test["long_view"],
            test[score]
        ),
        "average_precision": average_precision_score(
            test["long_view"],
            test[score]
        )
    })

metrics = pd.DataFrame(metrics)


# ------------------------------------------------------------
# 5. Offline ranking evaluation
#
# Treat each user-day's randomized exposures as that day's
# evaluation candidate pool.
# ------------------------------------------------------------

def precision_at_k(group, score_col, k):
    ranked = group.sort_values(
        score_col,
        ascending=False
    ).head(k)

    return ranked["long_view"].mean()


ranking_results = []

for score_col, policy in [
    ("baseline_score", "historical_popularity"),
    ("challenger_score", "personalized_model")
]:

    for k in [1, 3, 5]:

        values = []

        for _, group in test.groupby(
            ["user_id", "date"]
        ):
            if len(group) >= k:
                values.append(
                    precision_at_k(
                        group,
                        score_col,
                        k
                    )
                )

        ranking_results.append({
            "policy": policy,
            "k": k,
            "precision_at_k": np.mean(values),
            "eligible_user_days": len(values)
        })


ranking_results = pd.DataFrame(ranking_results)


# ------------------------------------------------------------
# 6. Save
# ------------------------------------------------------------

metrics.to_csv(
    "outputs/tables/ranking_policy_metrics.csv",
    index=False
)

ranking_results.to_csv(
    "outputs/tables/ranking_policy_precision.csv",
    index=False
)

print("\n=== PREDICTIVE METRICS ===")
print(metrics.to_string(index=False))

print("\n=== OFFLINE RANKING ===")
print(ranking_results.to_string(index=False))