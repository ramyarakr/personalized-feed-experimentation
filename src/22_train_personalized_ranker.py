import os
import pandas as pd

from src.personalized_ranker import (
    train_model,
    save_model,
)


DATA_PATH = (
    "outputs/tables/randomized_ranking_dataset.csv"
)

MODEL_PATH = (
    "outputs/models/personalized_ranker.joblib"
)


df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(
    df["date"].astype(str)
)

dates = sorted(df["date"].unique())

split_idx = int(len(dates) * 0.65)
split_date = dates[split_idx]

train = df[
    df["date"] < split_date
].copy()

print(f"Training rows: {len(train):,}")
print(f"Split date: {pd.Timestamp(split_date).date()}")

model = train_model(train)

os.makedirs(
    "outputs/models",
    exist_ok=True,
)

save_model(
    model,
    MODEL_PATH,
)

print(f"Model saved to: {MODEL_PATH}")