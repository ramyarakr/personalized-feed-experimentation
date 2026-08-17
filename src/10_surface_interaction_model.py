import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

PATH = "outputs/tables/surface_heterogeneity_features.csv"

df = pd.read_csv(PATH)

# Remove extremely tiny surfaces
df = df[df["dominant_tab"].isin([0, 1, 2, 4])].copy()


model = smf.negativebinomial(
    """
    future_7d_sessions
    ~ long_view_rate_t
      * C(dominant_tab, Treatment(reference=1))
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

results = pd.DataFrame({
    "coefficient": model.params,
    "exp_coefficient": np.exp(model.params),
    "p_value": model.pvalues
})

ci = model.conf_int()

results["ci_lower"] = np.exp(ci[0])
results["ci_upper"] = np.exp(ci[1])

results.to_csv(
    "outputs/tables/surface_interaction_model.csv"
)

print(results.to_string())