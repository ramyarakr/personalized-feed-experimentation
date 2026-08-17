-- ============================================================
-- 06 — Future 7-Day Activity Modeling Dataset
--
-- Question:
-- Does day-t long-view rate predict how many of the next
-- 7 calendar days a user will be active, after controlling
-- for prior activity?
-- ============================================================

COPY (
    WITH date_bounds AS (
        SELECT
            MIN(activity_date) AS first_observed_date,
            MAX(activity_date) AS last_observed_date
        FROM user_days
    ),

    eligible_days AS (
        SELECT
            u.user_id,
            u.activity_date,
            u.long_view_rate AS long_view_rate_t

        FROM user_days u
        CROSS JOIN date_bounds d

        WHERE u.activity_date >=
              d.first_observed_date + INTERVAL 7 DAY

          AND u.activity_date <=
              d.last_observed_date - INTERVAL 7 DAY
    ),

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

    future_activity AS (
        SELECT
            e.user_id,
            e.activity_date,

            COUNT(DISTINCT f.activity_date)
                AS future_active_days

        FROM eligible_days e

        LEFT JOIN user_days f
            ON f.user_id = e.user_id

           AND f.activity_date >
               e.activity_date

           AND f.activity_date <=
               e.activity_date + INTERVAL 7 DAY

        GROUP BY
            e.user_id,
            e.activity_date
    )

    SELECT
        e.user_id,
        e.activity_date,
        e.long_view_rate_t,

        p.prior_7d_sessions_per_day,
        p.prior_7d_avg_minutes_per_session,

        f.future_active_days

    FROM eligible_days e

    INNER JOIN prior_activity p
        USING (user_id, activity_date)

    INNER JOIN future_activity f
        USING (user_id, activity_date)

    WHERE p.prior_7d_avg_minutes_per_session IS NOT NULL

    ORDER BY
        e.user_id,
        e.activity_date
)
TO 'outputs/tables/future_active_days_features.csv'
(HEADER, DELIMITER ',');