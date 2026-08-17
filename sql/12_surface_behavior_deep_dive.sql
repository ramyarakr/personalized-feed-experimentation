COPY (
    SELECT
        tab,

        COUNT(*) AS interactions,
        COUNT(DISTINCT user_id) AS users,
        COUNT(DISTINCT video_id) AS unique_videos,

        COUNT(DISTINCT video_id) * 1.0
            / COUNT(*) AS unique_video_ratio,

        AVG(long_view) AS long_view_rate,

        AVG(play_time_ms) / 1000.0
            AS avg_play_seconds,

        MEDIAN(play_time_ms) / 1000.0
            AS median_play_seconds,

        AVG(
            CASE
                WHEN duration_ms > 0
                THEN duration_ms / 1000.0
            END
        ) AS avg_video_duration_seconds,

        AVG(is_like) AS like_rate,
        AVG(is_follow) AS follow_rate,
        AVG(is_comment) AS comment_rate,
        AVG(is_forward) AS forward_rate,
        AVG(is_profile_enter) AS profile_enter_rate,
        AVG(is_hate) AS hate_rate,

        AVG(
            CASE
                WHEN is_like = 1
                  OR is_follow = 1
                  OR is_comment = 1
                  OR is_forward = 1
                  OR is_profile_enter = 1
                THEN 1.0
                ELSE 0.0
            END
        ) AS explicit_positive_rate

    FROM standard_all

    WHERE tab IN (0,1,2,4)

    GROUP BY tab
    ORDER BY tab
)
TO 'outputs/tables/surface_behavior_deep_dive.csv'
(HEADER, DELIMITER ',');