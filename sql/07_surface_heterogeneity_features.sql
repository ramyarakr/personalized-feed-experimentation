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
        WHERE u.activity_date >= d.first_observed_date + INTERVAL 7 DAY
          AND u.activity_date <= d.last_observed_date - INTERVAL 7 DAY
    ),

    prior_activity AS (
        SELECT
            e.user_id,
            e.activity_date,
            COUNT(s.session_id) / 7.0 AS prior_7d_sessions_per_day,
            AVG(s.session_duration_minutes)
                AS prior_7d_avg_minutes_per_session
        FROM eligible_days e
        LEFT JOIN sessions s
            ON s.user_id = e.user_id
           AND s.session_date >= e.activity_date - INTERVAL 7 DAY
           AND s.session_date < e.activity_date
        GROUP BY e.user_id, e.activity_date
    ),

    same_day_activity AS (
        SELECT
            e.user_id,
            e.activity_date,
            COUNT(s.session_id) AS sessions_t
        FROM eligible_days e
        LEFT JOIN sessions s
            ON s.user_id = e.user_id
           AND s.session_date = e.activity_date
        GROUP BY e.user_id, e.activity_date
    ),

    future_activity AS (
        SELECT
            e.user_id,
            e.activity_date,
            COUNT(s.session_id) AS future_7d_sessions
        FROM eligible_days e
        LEFT JOIN sessions s
            ON s.user_id = e.user_id
           AND s.session_date > e.activity_date
           AND s.session_date <= e.activity_date + INTERVAL 7 DAY
        GROUP BY e.user_id, e.activity_date
    ),

    surface_counts AS (
        SELECT
            user_id,
            CAST(
                strptime(CAST(date AS VARCHAR), '%Y%m%d')
                AS DATE
            ) AS activity_date,
            tab,
            COUNT(*) AS interactions
        FROM standard_all
        WHERE tab IN (0, 1, 2, 4, 6)
        GROUP BY user_id, activity_date, tab
    ),

    ranked_surfaces AS (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY user_id, activity_date
                ORDER BY interactions DESC, tab
            ) AS surface_rank
        FROM surface_counts
    ),

    dominant_surface AS (
        SELECT
            user_id,
            activity_date,
            tab AS dominant_tab
        FROM ranked_surfaces
        WHERE surface_rank = 1
    )

    SELECT
        e.user_id,
        e.activity_date,
        e.long_view_rate_t,

        d.dominant_tab,

        p.prior_7d_sessions_per_day,
        p.prior_7d_avg_minutes_per_session,

        s.sessions_t,
        f.future_7d_sessions

    FROM eligible_days e

    INNER JOIN dominant_surface d
        USING (user_id, activity_date)

    INNER JOIN prior_activity p
        USING (user_id, activity_date)

    INNER JOIN same_day_activity s
        USING (user_id, activity_date)

    INNER JOIN future_activity f
        USING (user_id, activity_date)

    WHERE p.prior_7d_avg_minutes_per_session IS NOT NULL

    ORDER BY e.user_id, e.activity_date
)
TO 'outputs/tables/surface_heterogeneity_features.csv'
(HEADER, DELIMITER ',');