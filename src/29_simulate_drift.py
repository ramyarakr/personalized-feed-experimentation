import pandas as pd


INPUT_PATH = (
    "outputs/experience_demo/"
    "synthetic_interactions.csv"
)

OUTPUT_PATH = (
    "outputs/experience_demo/"
    "synthetic_interactions_drifted.csv"
)


df = pd.read_csv(INPUT_PATH)

# Simulate upstream distribution changes
df["quality_score"] *= 0.75
df["popularity_score"] *= 1.20

# Keep bounded features valid
df["quality_score"] = (
    df["quality_score"].clip(0, 1)
)

df["popularity_score"] = (
    df["popularity_score"].clip(0, 1)
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"Drifted dataset saved to: {OUTPUT_PATH}"
)

print(
    f"Quality mean: {df['quality_score'].mean():.4f}"
)

print(
    f"Popularity mean: {df['popularity_score'].mean():.4f}"
)