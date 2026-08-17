import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


DATA_PATH = "outputs/tables/d1_model_features.csv"

df = pd.read_csv(DATA_PATH)

print(f"Rows: {len(df):,}")
print(f"Users: {df['user_id'].nunique():,}")
print(f"D1 return rate: {df['returned_d1'].mean():.3%}")


# ------------------------------------------------------------
# Model A — Primary
#
# D1 return ~ meaningful engagement + PRIOR activity
# ------------------------------------------------------------

model_a = smf.glm(
    formula="""
        returned_d1
        ~ long_view_rate_t
        + prior_7d_sessions_per_day
        + prior_7d_avg_minutes_per_session
    """,
    data=df,
    family=sm.families.Binomial()
).fit(
    cov_type="cluster",
    cov_kwds={"groups": df["user_id"]}
)

print("\n=== MODEL A: BASELINE-CONTROLLED ===")
print(model_a.summary())


# ------------------------------------------------------------
# Model B — Robustness
#
# Adds same-day session count.
# ------------------------------------------------------------

model_b = smf.glm(
    formula="""
        returned_d1
        ~ long_view_rate_t
        + prior_7d_sessions_per_day
        + prior_7d_avg_minutes_per_session
        + sessions_t
    """,
    data=df,
    family=sm.families.Binomial()
).fit(
    cov_type="cluster",
    cov_kwds={"groups": df["user_id"]}
)

print("\n=== MODEL B: + SAME-DAY SESSIONS ===")
print(model_b.summary())


# ------------------------------------------------------------
# Odds ratios for easier interpretation
# ------------------------------------------------------------

def odds_ratios(model):
    result = pd.DataFrame({
        "coefficient": model.params,
        "odds_ratio": model.params.apply(lambda x: float(pd.np.exp(x)))
    })
    return result


import numpy as np

def odds_ratios(model):
    ci = model.conf_int()

    return pd.DataFrame({
        "coefficient": model.params,
        "odds_ratio": np.exp(model.params),
        "ci_lower": np.exp(ci[0]),
        "ci_upper": np.exp(ci[1]),
        "p_value": model.pvalues
    })


results_a = odds_ratios(model_a)
results_b = odds_ratios(model_b)

results_a.to_csv(
    "outputs/tables/d1_logit_model_a.csv"
)

results_b.to_csv(
    "outputs/tables/d1_logit_model_b.csv"
)

print("\n=== MODEL A ODDS RATIOS ===")
print(results_a)

print("\n=== MODEL B ODDS RATIOS ===")
print(results_b)