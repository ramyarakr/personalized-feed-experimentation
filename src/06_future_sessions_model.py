import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

PATH = "outputs/tables/future_7d_sessions_features.csv"

df = pd.read_csv(PATH)

y = df["future_7d_sessions"]

print(f"Rows: {len(df):,}")
print(f"Users: {df['user_id'].nunique():,}")
print(f"Mean future sessions: {y.mean():.2f}")
print(f"Variance: {y.var():.2f}")
print(f"Variance / mean: {y.var() / y.mean():.2f}")

print("\nPercentiles:")
print(y.quantile([0.50, 0.75, 0.90, 0.95, 0.99]))

print(f"\nMax: {y.max()}")


# ------------------------------------------------------------
# Model A
# Long-view rate + baseline activity
# ------------------------------------------------------------

model_a = smf.negativebinomial(
    """
    future_7d_sessions
    ~ long_view_rate_t
    + prior_7d_sessions_per_day
    + prior_7d_avg_minutes_per_session
    """,
    data=df
).fit(
    cov_type="cluster",
    cov_kwds={"groups": df["user_id"]},
    disp=False
)


# ------------------------------------------------------------
# Model B
# Robustness model adding same-day session activity
# ------------------------------------------------------------

model_b = smf.negativebinomial(
    """
    future_7d_sessions
    ~ long_view_rate_t
    + prior_7d_sessions_per_day
    + prior_7d_avg_minutes_per_session
    + sessions_t
    """,
    data=df
).fit(
    cov_type="cluster",
    cov_kwds={"groups": df["user_id"]},
    disp=False
)


def model_results(model):
    ci = model.conf_int()

    result = pd.DataFrame({
        "coefficient": model.params,
        "incidence_rate_ratio": np.exp(model.params),
        "ci_lower": np.exp(ci[0]),
        "ci_upper": np.exp(ci[1]),
        "p_value": model.pvalues
    })

    return result


results_a = model_results(model_a)
results_b = model_results(model_b)

results_a.to_csv(
    "outputs/tables/future_sessions_model_a.csv"
)

results_b.to_csv(
    "outputs/tables/future_sessions_model_b.csv"
)


print("\n=== MODEL A ===")
print(results_a)

print("\n=== MODEL B ===")
print(results_b)