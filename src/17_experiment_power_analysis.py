import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Randomized sample gives us an empirical baseline
df = pd.read_csv(
    "outputs/tables/randomized_ranking_dataset.csv"
)

baseline = df["long_view"].mean()

POWER = 0.80
ALPHA = 0.05

# Test several plausible relative improvements
relative_lifts = [0.01, 0.02, 0.05, 0.10]

analysis = NormalIndPower()

rows = []

for lift in relative_lifts:

    treatment = baseline * (1 + lift)

    effect_size = proportion_effectsize(
        baseline,
        treatment
    )

    n_per_group = analysis.solve_power(
        effect_size=effect_size,
        power=POWER,
        alpha=ALPHA,
        ratio=1.0,
        alternative="two-sided"
    )

    rows.append({
        "baseline_long_view_rate": baseline,
        "relative_lift": lift,
        "treatment_rate": treatment,
        "absolute_lift_pp": (treatment - baseline) * 100,
        "required_users_per_group": int(n_per_group) + 1,
        "total_required_users": 2 * (int(n_per_group) + 1)
    })


results = pd.DataFrame(rows)

results.to_csv(
    "outputs/tables/experiment_power_analysis.csv",
    index=False
)

print(f"Baseline long-view rate: {baseline:.3%}")
print("\n=== POWER ANALYSIS ===")
print(results.to_string(index=False))