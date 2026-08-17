COPY (
    WITH user_tab_days AS (
        SELECT
            user_id,
            tab,
            date,
            COUNT(*) AS daily_interactions,
            AVG(long_view) AS daily_long_view_rate
        FROM standard_all
        WHERE tab IN (0,1,2,4)
        GROUP BY user_id, tab, date
    ),

    user_tab_summary AS (
        SELECT
            tab,
            AVG(daily_interactions) AS avg_daily_interactions_per_user,
            MEDIAN(daily_interactions) AS median_daily_interactions_per_user,
            AVG(daily_long_view_rate) AS avg_user_day_long_view_rate
        FROM user_tab_days
        GROUP BY tab
    ),

    surface_summary AS (
        SELECT
            tab,

            COUNT(*) AS interactions,
            COUNT(DISTINCT user_id) AS users,
            COUNT(DISTINCT video_id) AS videos,

            AVG(long_view) AS long_view_rate,
            AVG(is_click) AS click_or_valid_play_rate,

            AVG(is_like) AS like_rate,
            AVG(is_follow) AS follow_rate,
            AVG(is_comment) AS comment_rate,
            AVG(is_forward) AS forward_rate,
            AVG(is_profile_enter) AS profile_enter_rate,
            AVG(is_hate) AS hate_rate,

            AVG(play_time_ms) / 1000.0 AS avg_play_seconds,

            AVG(
                CASE
                    WHEN duration_ms > 0
                    THEN duration_ms / 1000.0
                END
            ) AS avg_video_duration_seconds,

            MEDIAN(play_time_ms) / 1000.0 AS median_play_seconds

        FROM standard_all
        WHERE tab IN (0,1,2,4)

        GROUP BY tab
    )

    SELECT
        s.*,
        u.avg_daily_interactions_per_user,
        u.median_daily_interactions_per_user,
        u.avg_user_day_long_view_rate

    FROM surface_summary s
    JOIN user_tab_summary u USING(tab)

    ORDER BY tab
)
TO 'outputs/tables/surface_profiles.csv'
(HEADER, DELIMITER ',');