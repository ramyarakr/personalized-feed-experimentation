import numpy as np
import pandas as pd

# Hypothetical online experiment results
# Clearly labeled as simulation.

results = pd.DataFrame([
    {
        "metric": "long_view_rate",
        "type": "primary",
        "control": 0.0842,
        "treatment": 0.0890,
        "p_value": 0.012
    },
    {
        "metric": "like_rate",
        "type": "secondary",
        "control": 0.0051,
        "treatment": 0.0055,
        "p_value": 0.081
    },
    {
        "metric": "follow_rate",
        "type": "secondary",
        "control": 0.00020,
        "treatment": 0.00022,
        "p_value": 0.220
    },
    {
        "metric": "hate_rate",
        "type": "guardrail",
        "control": 0.00080,
        "treatment": 0.00083,
        "p_value": 0.610
    }
])

results["absolute_lift_pp"] = (
    results["treatment"] - results["control"]
) * 100

results["relative_lift"] = (
    results["treatment"] / results["control"] - 1
)

primary = results[
    results["type"] == "primary"
].iloc[0]

guardrails = results[
    results["type"] == "guardrail"
]

primary_pass = (
    primary["treatment"] > primary["control"]
    and primary["p_value"] < 0.05
)

guardrail_pass = not any(
    (guardrails["treatment"] > guardrails["control"])
    & (guardrails["p_value"] < 0.05)
)

if primary_pass and guardrail_pass:
    decision = "SHIP"
elif primary_pass:
    decision = "ITERATE"
else:
    decision = "DO NOT SHIP"

results.to_csv(
    "outputs/tables/simulated_experiment_results.csv",
    index=False
)

print(results.to_string(index=False))

print("\n=== LAUNCH DECISION ===")
print(decision)

print(
    "\nSimulation only; not an observed production experiment."
)