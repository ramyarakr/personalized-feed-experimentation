-- ============================================================
-- 05 — D1 Return Modeling Dataset
--
-- Question:
-- Does day-t long-view rate predict D1 return after controlling
-- for baseline user activity?
-- ============================================================

COPY (
    WITH date_bounds AS (
        SELECT
            MIN(activity_date) AS first_observed_date,
            MAX(activity_date) AS last_observed_date
        FROM user_days
    ),

    -- Day t must have:
    -- 1. a full 7-day lookback
    -- 2. an observable day t+1
    eligible_days AS (
        SELECT
            u.user_id,
            u.activity_date,
            u.long_view_rate AS long_view_rate_t,
            u.interactions AS interactions_t

        FROM user_days u
        CROSS JOIN date_bounds d

        WHERE u.activity_date >=
              d.first_observed_date + INTERVAL 7 DAY

          AND u.activity_date <=
              d.last_observed_date - INTERVAL 1 DAY
    ),

    -- Baseline activity from t-7 through t-1
    prior_activity AS (
        SELECT
            e.user_id,
            e.activity_date,

            COUNT(s.session_id) / 7.0
                AS prior_7d_sessions_per_day,

            AVG(s.session_duration_minutes)
                AS prior_7d_avg_minutes_per_session

        FROM eligible_days e

        LEFT JOIN sessions s
            ON s.user_id = e.user_id
           AND s.session_date >=
               e.activity_date - INTERVAL 7 DAY
           AND s.session_date <
               e.activity_date

        GROUP BY
            e.user_id,
            e.activity_date
    ),

    -- Same-day sessions for later robustness model
    same_day_activity AS (
        SELECT
            e.user_id,
            e.activity_date,
            COUNT(s.session_id) AS sessions_t

        FROM eligible_days e

        LEFT JOIN sessions s
            ON s.user_id = e.user_id
           AND s.session_date = e.activity_date

        GROUP BY
            e.user_id,
            e.activity_date
    ),

    -- Outcome: user appears again on calendar day t+1
    d1_labels AS (
        SELECT
            e.user_id,
            e.activity_date,

            CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM user_days future
                    WHERE future.user_id = e.user_id
                      AND future.activity_date =
                          e.activity_date + INTERVAL 1 DAY
                )
                THEN 1
                ELSE 0
            END AS returned_d1

        FROM eligible_days e
    )

    SELECT
        e.user_id,
        e.activity_date,

        e.long_view_rate_t,
        e.interactions_t,

        p.prior_7d_sessions_per_day,
        p.prior_7d_avg_minutes_per_session,

        s.sessions_t,

        d.returned_d1

    FROM eligible_days e

    INNER JOIN prior_activity p
        USING (user_id, activity_date)

    INNER JOIN same_day_activity s
        USING (user_id, activity_date)

    INNER JOIN d1_labels d
        USING (user_id, activity_date)

    -- Users with no prior sessions have NULL average duration.
    -- Exclude them from the primary regression rather than
    -- falsely assigning 0 minutes/session.
    WHERE p.prior_7d_avg_minutes_per_session IS NOT NULL

    ORDER BY
        e.user_id,
        e.activity_date
)
TO 'outputs/tables/d1_model_features.csv'
(HEADER, DELIMITER ',');