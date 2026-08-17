-- ============================================================
-- Personalized Feed Experimentation
-- 04 — Sessionization & Product Health
--
-- Objectives:
-- 1. Construct user sessions from event logs.
-- 2. Test sensitivity to session timeout assumptions.
-- 3. Measure session-level product health.
-- 4. Test whether meaningful engagement intensity is associated
--    with subsequent observed usage.
-- ============================================================


-- ------------------------------------------------------------
-- 1. Session timeout sensitivity
-- ------------------------------------------------------------

COPY (
    WITH ordered AS (
        SELECT
            user_id,
            time_ms,

            LAG(time_ms) OVER (
                PARTITION BY user_id
                ORDER BY time_ms
            ) AS previous_time_ms

        FROM standard_all
    )

    SELECT
        '15_minutes' AS timeout,
        SUM(
            CASE
                WHEN previous_time_ms IS NULL
                  OR time_ms - previous_time_ms > 15 * 60 * 1000
                THEN 1 ELSE 0
            END
        ) AS sessions
    FROM ordered

    UNION ALL

    SELECT
        '30_minutes',
        SUM(
            CASE
                WHEN previous_time_ms IS NULL
                  OR time_ms - previous_time_ms > 30 * 60 * 1000
                THEN 1 ELSE 0
            END
        )
    FROM ordered

    UNION ALL

    SELECT
        '60_minutes',
        SUM(
            CASE
                WHEN previous_time_ms IS NULL
                  OR time_ms - previous_time_ms > 60 * 60 * 1000
                THEN 1 ELSE 0
            END
        )
    FROM ordered
)
TO 'outputs/tables/session_threshold_sensitivity.csv'
(HEADER, DELIMITER ',');


-- ------------------------------------------------------------
-- 2. Build 30-minute sessionized event view
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW sessionized_events AS

WITH ordered AS (
    SELECT
        *,

        LAG(time_ms) OVER (
            PARTITION BY user_id
            ORDER BY time_ms, video_id
        ) AS previous_time_ms

    FROM standard_all
),

boundaries AS (
    SELECT
        *,

        CASE
            WHEN previous_time_ms IS NULL
              OR time_ms - previous_time_ms > 30 * 60 * 1000
            THEN 1
            ELSE 0
        END AS new_session

    FROM ordered
),

numbered AS (
    SELECT
        *,

        SUM(new_session) OVER (
            PARTITION BY user_id
            ORDER BY time_ms, video_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS session_number

    FROM boundaries
)

SELECT
    *,
    CAST(user_id AS VARCHAR)
        || '_'
        || CAST(session_number AS VARCHAR)
        AS session_id

FROM numbered;


-- ------------------------------------------------------------
-- 3. Session-level analytical table
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW sessions AS

SELECT
    user_id,
    session_id,

    MIN(time_ms) AS session_start_ms,
    MAX(time_ms) AS session_end_ms,

    CAST(
        strptime(
            CAST(MIN(date) AS VARCHAR),
            '%Y%m%d'
        )
        AS DATE
    ) AS session_date,

    (MAX(time_ms) - MIN(time_ms)) / 60000.0
        AS session_duration_minutes,

    COUNT(*) AS interactions,

    SUM(long_view) AS long_views,

    AVG(long_view) AS long_view_rate,

    SUM(is_like) AS likes,
    SUM(is_follow) AS follows,
    SUM(is_comment) AS comments,
    SUM(is_forward) AS forwards,
    SUM(is_profile_enter) AS profile_entries,
    SUM(is_hate) AS hates,

    SUM(
        CASE
            WHEN is_like = 1
              OR is_follow = 1
              OR is_comment = 1
              OR is_forward = 1
              OR is_profile_enter = 1
            THEN 1
            ELSE 0
        END
    ) AS explicit_positive_interactions

FROM sessionized_events

GROUP BY
    user_id,
    session_id;


-- ------------------------------------------------------------
-- 4. Overall session health
-- ------------------------------------------------------------

COPY (
    SELECT
        COUNT(*) AS sessions,
        COUNT(DISTINCT user_id) AS users,

        AVG(interactions) AS avg_interactions_per_session,
        MEDIAN(interactions) AS median_interactions_per_session,

        AVG(session_duration_minutes)
            AS avg_session_duration_minutes,

        MEDIAN(session_duration_minutes)
            AS median_session_duration_minutes,

        AVG(long_views)
            AS avg_long_views_per_session,

        MEDIAN(long_views)
            AS median_long_views_per_session,

        AVG(long_view_rate)
            AS avg_session_long_view_rate,

        AVG(
            CASE WHEN long_views > 0 THEN 1.0 ELSE 0.0 END
        ) AS pct_sessions_with_long_view,

        AVG(
            CASE
                WHEN explicit_positive_interactions > 0
                THEN 1.0 ELSE 0.0
            END
        ) AS pct_sessions_with_explicit_positive_action,

        AVG(
            CASE WHEN hates > 0 THEN 1.0 ELSE 0.0 END
        ) AS pct_sessions_with_hate

    FROM sessions
)
TO 'outputs/tables/session_summary.csv'
(HEADER, DELIMITER ',');


-- ------------------------------------------------------------
-- 5. Session quality by meaningful consumption
-- ------------------------------------------------------------

COPY (
    SELECT

        CASE
            WHEN long_view_rate = 0
                THEN '0%'
            WHEN long_view_rate <= 0.25
                THEN '>0-25%'
            WHEN long_view_rate <= 0.50
                THEN '>25-50%'
            ELSE '>50%'
        END AS long_view_share,

        COUNT(*) AS sessions,

        AVG(interactions)
            AS avg_interactions,

        AVG(session_duration_minutes)
            AS avg_duration_minutes,

        AVG(explicit_positive_interactions)
            AS avg_explicit_positive_interactions,

        AVG(
            CASE
                WHEN explicit_positive_interactions > 0
                THEN 1.0 ELSE 0.0
            END
        ) AS pct_sessions_with_explicit_positive_action,

        AVG(
            CASE
                WHEN hates > 0
                THEN 1.0 ELSE 0.0
            END
        ) AS pct_sessions_with_hate

    FROM sessions

    GROUP BY long_view_share

    ORDER BY
        CASE long_view_share
            WHEN '0%' THEN 1
            WHEN '>0-25%' THEN 2
            WHEN '>25-50%' THEN 3
            WHEN '>50%' THEN 4
        END
)
TO 'outputs/tables/session_quality_by_long_view.csv'
(HEADER, DELIMITER ',');


-- ------------------------------------------------------------
-- 6. Daily product-health table
-- ------------------------------------------------------------

COPY (
    SELECT
        session_date,

        COUNT(DISTINCT user_id)
            AS daily_active_users,

        COUNT(*) AS sessions,

        SUM(interactions) AS interactions,

        SUM(long_views) AS long_views,

        SUM(long_views) * 1.0
            / NULLIF(SUM(interactions), 0)
            AS long_view_rate,

        AVG(interactions)
            AS avg_interactions_per_session,

        AVG(session_duration_minutes)
            AS avg_session_duration_minutes,

        SUM(explicit_positive_interactions) * 1.0
            / NULLIF(SUM(interactions), 0)
            AS explicit_positive_action_rate,

        SUM(hates) * 1.0
            / NULLIF(SUM(interactions), 0)
            AS hate_rate

    FROM sessions

    GROUP BY session_date
    ORDER BY session_date
)
TO 'outputs/tables/daily_product_health.csv'
(HEADER, DELIMITER ',');


-- ------------------------------------------------------------
-- 7. User-day analytical view
--
-- This avoids calling first appearance "signup".
-- Each row represents observed activity for one user-day.
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW user_days AS

SELECT
    user_id,

    CAST(
        strptime(
            CAST(date AS VARCHAR),
            '%Y%m%d'
        )
        AS DATE
    ) AS activity_date,

    COUNT(*) AS interactions,

    SUM(long_view) AS long_views,

    AVG(long_view) AS long_view_rate,

    SUM(is_like) AS likes,
    SUM(is_follow) AS follows,
    SUM(is_comment) AS comments,
    SUM(is_forward) AS forwards,
    SUM(is_profile_enter) AS profile_entries,
    SUM(is_hate) AS hates

FROM standard_all

GROUP BY
    user_id,
    activity_date;


-- ------------------------------------------------------------
-- 8. Repeat usage by meaningful-engagement intensity
--
-- IMPORTANT:
-- This is observational association, not causal retention lift.
--
-- D1 = active on the following calendar day.
-- 7D = active at least once within the next seven days.
--
-- Right-censored days are removed from the relevant denominator.
-- ------------------------------------------------------------

COPY (
    WITH max_date AS (
        SELECT MAX(activity_date) AS last_observed_date
        FROM user_days
    ),

    scored AS (
        SELECT
            d.*,
            m.last_observed_date,

            CASE
                WHEN d.long_view_rate = 0
                    THEN '0%'
                WHEN d.long_view_rate <= 0.25
                    THEN '>0-25%'
                WHEN d.long_view_rate <= 0.50
                    THEN '>25-50%'
                ELSE '>50%'
            END AS long_view_share,

            CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM user_days d2
                    WHERE d2.user_id = d.user_id
                      AND d2.activity_date =
                          d.activity_date + INTERVAL 1 DAY
                )
                THEN 1 ELSE 0
            END AS returned_d1,

            CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM user_days d2
                    WHERE d2.user_id = d.user_id
                      AND d2.activity_date >
                          d.activity_date
                      AND d2.activity_date <=
                          d.activity_date + INTERVAL 7 DAY
                )
                THEN 1 ELSE 0
            END AS returned_within_7d

        FROM user_days d
        CROSS JOIN max_date m
    )

    SELECT
        long_view_share,

        COUNT(*) AS observed_user_days,

        AVG(interactions)
            AS avg_interactions,

        AVG(long_view_rate)
            AS avg_long_view_rate,

        SUM(
            CASE
                WHEN activity_date <=
                     last_observed_date - INTERVAL 1 DAY
                THEN 1 ELSE 0
            END
        ) AS d1_eligible_user_days,

        AVG(
            CASE
                WHEN activity_date <=
                     last_observed_date - INTERVAL 1 DAY
                THEN returned_d1
            END
        ) AS d1_return_rate,

        SUM(
            CASE
                WHEN activity_date <=
                     last_observed_date - INTERVAL 7 DAY
                THEN 1 ELSE 0
            END
        ) AS seven_day_eligible_user_days,

        AVG(
            CASE
                WHEN activity_date <=
                     last_observed_date - INTERVAL 7 DAY
                THEN returned_within_7d
            END
        ) AS seven_day_return_rate

    FROM scored

    GROUP BY long_view_share

    ORDER BY
        CASE long_view_share
            WHEN '0%' THEN 1
            WHEN '>0-25%' THEN 2
            WHEN '>25-50%' THEN 3
            WHEN '>50%' THEN 4
        END
)
TO 'outputs/tables/repeat_usage_by_long_view.csv'
(HEADER, DELIMITER ',');