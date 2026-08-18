import os
import numpy as np
import pandas as pd


SEED = 42
N_USERS = 500
N_EXPERIENCES = 120
EXPOSURES_PER_USER = 40

OUTPUT_DIR = "outputs/experience_demo"

rng = np.random.default_rng(SEED)

os.makedirs(OUTPUT_DIR, exist_ok=True)


CATEGORIES = np.array([
    "Action",
    "Adventure",
    "Creative",
    "Puzzle",
    "Simulation",
    "Social",
    "Sports",
    "Strategy",
])


# ============================================================
# 1. EXPERIENCE CATALOG
# ============================================================

catalog = pd.DataFrame({
    "experience_id": np.arange(
        1000,
        1000 + N_EXPERIENCES
    ),

    "category": rng.choice(
        CATEGORIES,
        N_EXPERIENCES
    ),

    "quality_score": rng.beta(
        5,
        2,
        N_EXPERIENCES
    ),

    "popularity_score": rng.beta(
        2.5,
        3,
        N_EXPERIENCES
    ),

    "novelty_score": rng.beta(
        2,
        2,
        N_EXPERIENCES
    ),

    "difficulty": rng.uniform(
        0,
        1,
        N_EXPERIENCES
    ),

    "avg_session_minutes": rng.integers(
        8,
        61,
        N_EXPERIENCES
    ),
})


catalog["experience_name"] = (
    "Experience "
    + catalog["experience_id"].astype(str)
)


# ============================================================
# 2. USER PROFILES
# ============================================================

users = []

for user_id in range(N_USERS):

    preferred_category = rng.choice(
        CATEGORIES
    )

    secondary_category = rng.choice(
        CATEGORIES[
            CATEGORIES != preferred_category
        ]
    )

    users.append({
        "user_id": user_id,

        "preferred_category":
            preferred_category,

        "secondary_category":
            secondary_category,

        "novelty_preference":
            rng.beta(2.5, 2),

        "social_preference":
            rng.beta(2, 2),

        "preferred_session_minutes":
            rng.integers(10, 56),
    })


users = pd.DataFrame(users)


# ============================================================
# 3. SYNTHETIC RANDOM EXPOSURES
#
# Every user receives 40 randomly selected experiences.
# This creates a candidate/evaluation pool.
# ============================================================

catalog_indexed = catalog.set_index(
    "experience_id"
)

rows = []

for user in users.itertuples(index=False):

    candidate_ids = rng.choice(
        catalog["experience_id"].to_numpy(),
        size=EXPOSURES_PER_USER,
        replace=False,
    )

    for experience_id in candidate_ids:

        exp = catalog_indexed.loc[
            experience_id
        ]

        primary_match = float(
            exp["category"]
            == user.preferred_category
        )

        secondary_match = float(
            exp["category"]
            == user.secondary_category
        )

        session_length_gap = (
            abs(
                float(
                    exp["avg_session_minutes"]
                )
                - user.preferred_session_minutes
            )
            / 60
        )

        novelty_alignment = (
            1
            - abs(
                float(exp["novelty_score"])
                - user.novelty_preference
            )
        )

        social_match = (
            float(
                exp["category"] == "Social"
            )
            * user.social_preference
        )


        # ----------------------------------------------------
        # Synthetic engagement probability
        #
        # Higher when:
        # - category matches user interests
        # - experience quality is strong
        # - novelty matches user preference
        # - session length fits user preference
        #
        # This is the hidden data-generating process.
        # ----------------------------------------------------

        logit = (
            -3.0
            + 1.55 * primary_match
            + 0.70 * secondary_match
            + 1.30 * exp["quality_score"]
            + 0.45 * exp["popularity_score"]
            + 0.65 * novelty_alignment
            + 0.50 * social_match
            - 0.55 * session_length_gap
        )

        probability = (
            1
            / (
                1
                + np.exp(-logit)
            )
        )

        meaningful_engagement = (
            rng.binomial(
                1,
                probability
            )
        )


        rows.append({
            "user_id":
                user.user_id,

            "experience_id":
                experience_id,

            "experience_name":
                exp["experience_name"],

            "category":
                exp["category"],

            "quality_score":
                exp["quality_score"],

            "popularity_score":
                exp["popularity_score"],

            "novelty_score":
                exp["novelty_score"],

            "difficulty":
                exp["difficulty"],

            "avg_session_minutes":
                exp["avg_session_minutes"],

            "preferred_category":
                user.preferred_category,

            "secondary_category":
                user.secondary_category,

            "novelty_preference":
                user.novelty_preference,

            "social_preference":
                user.social_preference,

            "preferred_session_minutes":
                user.preferred_session_minutes,

            "primary_category_match":
                primary_match,

            "secondary_category_match":
                secondary_match,

            "session_length_gap":
                session_length_gap,

            "novelty_alignment":
                novelty_alignment,

            "meaningful_engagement":
                meaningful_engagement,
        })


interactions = pd.DataFrame(rows)


# ============================================================
# 4. SAVE
# ============================================================

catalog.to_csv(
    f"{OUTPUT_DIR}/experience_catalog.csv",
    index=False,
)

users.to_csv(
    f"{OUTPUT_DIR}/user_profiles.csv",
    index=False,
)

interactions.to_csv(
    f"{OUTPUT_DIR}/synthetic_interactions.csv",
    index=False,
)


print("=== EXPERIENCE DISCOVERY DATA ===")

print(
    f"Users: {len(users):,}"
)

print(
    f"Experiences: {len(catalog):,}"
)

print(
    f"Interactions: {len(interactions):,}"
)

print(
    "Meaningful engagement rate: "
    f"{interactions['meaningful_engagement'].mean():.2%}"
)

print(
    f"\nSaved to: {OUTPUT_DIR}"
)