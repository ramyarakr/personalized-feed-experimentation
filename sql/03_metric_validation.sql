-- ============================================================
-- Personalized Feed Experimentation
-- 03 — Candidate Metric Validation
--
-- Product question:
-- Does long-view behavior represent meaningfully higher-quality
-- engagement than shallow consumption?
--
-- Validating the candidate metric against downstream,
-- higher-intent behaviors before using it in product decisions.
-- ============================================================

-- ------------------------------------------------------------
-- 1. Downstream engagement conditional on long_view
-- ------------------------------------------------------------

COPY (
    SELECT
        long_view,

        COUNT(*) AS interactions,

        AVG(is_like) AS like_rate,
        AVG(is_follow) AS follow_rate,
        AVG(is_comment) AS comment_rate,
        AVG(is_forward) AS forward_rate,
        AVG(is_profile_enter) AS profile_enter_rate,
        AVG(is_hate) AS hate_rate,

        AVG(play_time_ms) AS avg_play_time_ms

    FROM standard_all

    GROUP BY long_view
    ORDER BY long_view
)
TO 'outputs/tables/metric_validation_long_view.csv'
(HEADER, DELIMITER ',');


-- ------------------------------------------------------------
-- 2. Validation by major product surface
--
-- Restrict to tabs covering at least 1% of interactions.
-- This prevents tiny surfaces from dominating interpretation.
-- ------------------------------------------------------------

COPY (
    WITH tab_sizes AS (
        SELECT
            tab,
            COUNT(*) AS interactions
        FROM standard_all
        GROUP BY tab
    ),

    major_tabs AS (
        SELECT tab
        FROM tab_sizes
        WHERE interactions >= 0.01 * (
            SELECT COUNT(*) FROM standard_all
        )
    )

    SELECT
        s.tab,
        s.long_view,

        COUNT(*) AS interactions,

        AVG(s.is_like) AS like_rate,
        AVG(s.is_follow) AS follow_rate,
        AVG(s.is_comment) AS comment_rate,
        AVG(s.is_forward) AS forward_rate,
        AVG(s.is_profile_enter) AS profile_enter_rate,
        AVG(s.is_hate) AS hate_rate

    FROM standard_all s

    INNER JOIN major_tabs m
        ON s.tab = m.tab

    GROUP BY
        s.tab,
        s.long_view

    ORDER BY
        s.tab,
        s.long_view
)
TO 'outputs/tables/metric_validation_by_tab.csv'
(HEADER, DELIMITER ',');


-- ------------------------------------------------------------
-- 3. Relative lift associated with long_view
--
-- This produces an interpretable comparison such as:
-- "Like rate is X times higher among long-view interactions."
--
-- IMPORTANT:
-- These are ASSOCIATIONS, not causal treatment effects.
-- ------------------------------------------------------------

COPY (
    WITH rates AS (
        SELECT
            long_view,

            AVG(is_like) AS like_rate,
            AVG(is_follow) AS follow_rate,
            AVG(is_comment) AS comment_rate,
            AVG(is_forward) AS forward_rate,
            AVG(is_profile_enter) AS profile_enter_rate,
            AVG(is_hate) AS hate_rate

        FROM standard_all

        GROUP BY long_view
    ),

    shallow AS (
        SELECT * FROM rates WHERE long_view = 0
    ),

    long AS (
        SELECT * FROM rates WHERE long_view = 1
    )

    SELECT
        long.like_rate / NULLIF(shallow.like_rate, 0)
            AS like_rate_ratio,

        long.follow_rate / NULLIF(shallow.follow_rate, 0)
            AS follow_rate_ratio,

        long.comment_rate / NULLIF(shallow.comment_rate, 0)
            AS comment_rate_ratio,

        long.forward_rate / NULLIF(shallow.forward_rate, 0)
            AS forward_rate_ratio,

        long.profile_enter_rate / NULLIF(shallow.profile_enter_rate, 0)
            AS profile_enter_rate_ratio,

        long.hate_rate / NULLIF(shallow.hate_rate, 0)
            AS hate_rate_ratio

    FROM long
    CROSS JOIN shallow
)
TO 'outputs/tables/metric_validation_relative_lift.csv'
(HEADER, DELIMITER ',');


-- ------------------------------------------------------------
-- 4. Duration quality issue by product surface
--
-- We do NOT globally remove these rows.
-- This determines whether invalid duration is concentrated
-- within particular product surfaces.
-- ------------------------------------------------------------

COPY (
    SELECT
        tab,

        COUNT(*) AS interactions,

        SUM(
            CASE WHEN duration_ms <= 0 THEN 1 ELSE 0 END
        ) AS nonpositive_duration_rows,

        AVG(
            CASE WHEN duration_ms <= 0 THEN 1.0 ELSE 0.0 END
        ) AS nonpositive_duration_rate

    FROM standard_all

    GROUP BY tab

    ORDER BY interactions DESC
)
TO 'outputs/tables/metric_validation_duration_quality_by_tab.csv'
(HEADER, DELIMITER ',');


-- ------------------------------------------------------------
-- 5. Watch-depth distribution for valid-duration interactions
--
-- play_time can exceed duration because users may replay content.
-- Therefore we preserve raw watch ratio and separately calculate
-- a capped completion fraction for product interpretation.
-- ------------------------------------------------------------

COPY (
    SELECT

        COUNT(*) AS valid_duration_interactions,

        AVG(
            CAST(play_time_ms AS DOUBLE) / duration_ms
        ) AS avg_raw_watch_ratio,

        MEDIAN(
            CAST(play_time_ms AS DOUBLE) / duration_ms
        ) AS median_raw_watch_ratio,

        AVG(
            LEAST(
                CAST(play_time_ms AS DOUBLE) / duration_ms,
                1.0
            )
        ) AS avg_capped_completion_fraction,

        MEDIAN(
            LEAST(
                CAST(play_time_ms AS DOUBLE) / duration_ms,
                1.0
            )
        ) AS median_capped_completion_fraction

    FROM standard_all

    WHERE duration_ms > 0
)
TO 'outputs/tables/metric_validation_watch_depth.csv'
(HEADER, DELIMITER ',');