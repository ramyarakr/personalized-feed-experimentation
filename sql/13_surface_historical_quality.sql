COPY (
    SELECT
        s.tab,

        AVG(vs.show_cnt) AS avg_historical_shows,
        AVG(vs.play_cnt) AS avg_historical_plays,

        AVG(
            vs.valid_play_cnt
            / NULLIF(vs.show_cnt, 0)
        ) AS avg_historical_valid_play_rate,

        AVG(
            vs.long_time_play_cnt
            / NULLIF(vs.show_cnt, 0)
        ) AS avg_historical_long_play_rate,

        AVG(
            vs.like_cnt
            / NULLIF(vs.show_cnt, 0)
        ) AS avg_historical_like_rate,

        AVG(
            vs.comment_cnt
            / NULLIF(vs.show_cnt, 0)
        ) AS avg_historical_comment_rate,

        AVG(
            vs.follow_cnt
            / NULLIF(vs.show_cnt, 0)
        ) AS avg_historical_follow_rate,

        AVG(
            vs.share_cnt
            / NULLIF(vs.show_cnt, 0)
        ) AS avg_historical_share_rate,

        AVG(vs.play_progress)
            AS avg_historical_play_progress

    FROM standard_all s

    INNER JOIN video_stats vs
        ON s.video_id = vs.video_id

    WHERE s.tab IN (0,1,2,4)

    GROUP BY s.tab
    ORDER BY s.tab
)
TO 'outputs/tables/surface_historical_quality.csv'
(HEADER, DELIMITER ',');