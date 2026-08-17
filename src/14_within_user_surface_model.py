import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

PATH = "outputs/tables/within_user_surface_features.csv"

df = pd.read_csv(PATH)

print(f"Rows: {len(df):,}")
print(f"Users using both surfaces: {df['user_id'].nunique():,}")

print("\nRows by surface:")
print(df["dominant_tab"].value_counts().sort_index())


# Fixed dispersion based on prior pooled NB estimate
ALPHA = 0.073


# ------------------------------------------------------------
# Within-user model
#
# C(user_id) controls for stable differences between users.
# The long_view × surface interaction asks whether the same
# users show a different relationship on Tab 2 vs Tab 1.
# ------------------------------------------------------------

model = smf.glm(
    formula="""
        future_7d_sessions
        ~ long_view_rate_t
          * C(dominant_tab, Treatment(reference=1))
        + prior_7d_sessions_per_day
        + prior_7d_avg_minutes_per_session
        + sessions_t
        + C(user_id)
    """,
    data=df,
    family=sm.families.NegativeBinomial(alpha=ALPHA)
).fit(
    cov_type="cluster",
    cov_kwds={"groups": df["user_id"]}
)


interaction = (
    "long_view_rate_t:"
    "C(dominant_tab, Treatment(reference=1))[T.2]"
)

results = pd.DataFrame({
    "coefficient": model.params,
    "exp_coefficient": np.exp(model.params),
    "p_value": model.pvalues
})

ci = model.conf_int()

results["ci_lower"] = np.exp(ci[0])
results["ci_upper"] = np.exp(ci[1])

# Save full model
results.to_csv(
    "outputs/tables/within_user_surface_model.csv"
)

# Print only the important terms
terms = [
    "long_view_rate_t",
    "C(dominant_tab, Treatment(reference=1))[T.2]",
    interaction,
    "prior_7d_sessions_per_day",
    "prior_7d_avg_minutes_per_session",
    "sessions_t"
]

print("\n=== KEY WITHIN-USER RESULTS ===")
print(results.loc[terms].to_string())