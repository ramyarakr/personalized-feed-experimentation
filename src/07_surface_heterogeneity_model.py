import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

PATH = "outputs/tables/surface_heterogeneity_features.csv"

df = pd.read_csv(PATH)

print("Rows by dominant tab:")
print(df["dominant_tab"].value_counts().sort_index())


results = []

for tab in sorted(df["dominant_tab"].unique()):

    subset = df[df["dominant_tab"] == tab].copy()

    # Avoid fitting very small surfaces
    if len(subset) < 100:
        continue

    model = smf.negativebinomial(
        """
        future_7d_sessions
        ~ long_view_rate_t
        + prior_7d_sessions_per_day
        + prior_7d_avg_minutes_per_session
        + sessions_t
        """,
        data=subset
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": subset["user_id"]},
        disp=False
    )

    coef = model.params["long_view_rate_t"]
    ci = model.conf_int().loc["long_view_rate_t"]

    results.append({
        "dominant_tab": tab,
        "rows": len(subset),
        "users": subset["user_id"].nunique(),
        "long_view_coefficient": coef,
        "incidence_rate_ratio": np.exp(coef),
        "ci_lower": np.exp(ci[0]),
        "ci_upper": np.exp(ci[1]),
        "p_value": model.pvalues["long_view_rate_t"]
    })


results = pd.DataFrame(results)

results.to_csv(
    "outputs/tables/surface_heterogeneity_results.csv",
    index=False
)

print("\nLong-view effect by dominant product surface:")
print(results.to_string(index=False))