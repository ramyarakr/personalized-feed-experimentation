COPY (
    WITH source AS (
        SELECT *
        FROM read_csv_auto(
            'outputs/tables/surface_heterogeneity_features.csv'
        )
    ),

    surface_usage AS (
        SELECT
            user_id,

            SUM(CASE WHEN dominant_tab = 1 THEN 1 ELSE 0 END)
                AS tab1_days,

            SUM(CASE WHEN dominant_tab = 2 THEN 1 ELSE 0 END)
                AS tab2_days

        FROM source
        GROUP BY user_id
    ),

    overlap_users AS (
        SELECT user_id
        FROM surface_usage
        WHERE tab1_days > 0
          AND tab2_days > 0
    )

    SELECT
        f.user_id,
        f.activity_date,
        f.dominant_tab,
        f.long_view_rate_t,
        f.prior_7d_sessions_per_day,
        f.prior_7d_avg_minutes_per_session,
        f.sessions_t,
        f.future_7d_sessions

    FROM source f

    INNER JOIN overlap_users u
        USING (user_id)

    WHERE f.dominant_tab IN (1,2)

    ORDER BY
        f.user_id,
        f.activity_date
)
TO 'outputs/tables/within_user_surface_features.csv'
(HEADER, DELIMITER ',');