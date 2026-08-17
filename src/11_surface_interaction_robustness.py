import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

PATH = "outputs/tables/surface_heterogeneity_features.csv"

df = pd.read_csv(PATH)

df = df[df["dominant_tab"].isin([0, 1, 2, 4])].copy()

# Dispersion estimated from the previous pooled NB model
ALPHA = 0.073

model = smf.glm(
    formula="""
        future_7d_sessions
        ~ long_view_rate_t
          * C(dominant_tab, Treatment(reference=1))
        + prior_7d_sessions_per_day
        + prior_7d_avg_minutes_per_session
        + sessions_t
    """,
    data=df,
    family=sm.families.NegativeBinomial(alpha=ALPHA)
).fit(
    cov_type="cluster",
    cov_kwds={"groups": df["user_id"]}
)

ci = model.conf_int()

results = pd.DataFrame({
    "coefficient": model.params,
    "exp_coefficient": np.exp(model.params),
    "ci_lower": np.exp(ci[0]),
    "ci_upper": np.exp(ci[1]),
    "p_value": model.pvalues
})

results.to_csv(
    "outputs/tables/surface_interaction_robustness.csv"
)

print(model.summary())
print("\n=== ROBUSTNESS RESULTS ===")
print(results.to_string())