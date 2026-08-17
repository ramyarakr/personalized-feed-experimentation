-- ============================================================
-- 15 — Randomized Ranking Evaluation Dataset
--
-- Goal:
-- Build an unbiased evaluation dataset for comparing
-- recommendation policies.
--
-- Features come only from the PRIOR observation window.
-- Outcomes come from the later randomized exposure sample.
-- ============================================================

COPY (
    WITH user_history AS (
        SELECT
            user_id,

            COUNT(*) AS prior_user_interactions,

            AVG(long_view)
                AS prior_user_long_view_rate,

            AVG(is_like)
                AS prior_user_like_rate,

            AVG(is_follow)
                AS prior_user_follow_rate,

            AVG(play_time_ms)
                AS prior_user_avg_play_time_ms

        FROM standard_prior

        GROUP BY user_id
    ),

    video_history AS (
        SELECT
            video_id,

            COUNT(*) AS prior_video_interactions,

            AVG(long_view)
                AS prior_video_long_view_rate,

            AVG(is_like)
                AS prior_video_like_rate,

            AVG(is_follow)
                AS prior_video_follow_rate,

            AVG(play_time_ms)
                AS prior_video_avg_play_time_ms

        FROM standard_prior

        GROUP BY video_id
    )

    SELECT
        r.user_id,
        r.video_id,
        r.date,
        r.hourmin,
        r.tab,

        -- Outcome
        r.long_view,

        -- Supporting outcomes / guardrails
        r.is_like,
        r.is_follow,
        r.is_comment,
        r.is_forward,
        r.is_hate,
        r.is_profile_enter,
        r.play_time_ms,

        -- User history available before evaluation period
        COALESCE(u.prior_user_interactions, 0)
            AS prior_user_interactions,

        COALESCE(u.prior_user_long_view_rate, 0)
            AS prior_user_long_view_rate,

        COALESCE(u.prior_user_like_rate, 0)
            AS prior_user_like_rate,

        COALESCE(u.prior_user_follow_rate, 0)
            AS prior_user_follow_rate,

        COALESCE(u.prior_user_avg_play_time_ms, 0)
            AS prior_user_avg_play_time_ms,

        -- Video history available before evaluation period
        COALESCE(vh.prior_video_interactions, 0)
            AS prior_video_interactions,

        COALESCE(vh.prior_video_long_view_rate, 0)
            AS prior_video_long_view_rate,

        COALESCE(vh.prior_video_like_rate, 0)
            AS prior_video_like_rate,

        COALESCE(vh.prior_video_follow_rate, 0)
            AS prior_video_follow_rate,

        COALESCE(vh.prior_video_avg_play_time_ms, 0)
            AS prior_video_avg_play_time_ms,

        -- Static video metadata
        vb.video_duration,
        vb.video_type,
        vb.upload_type

    FROM random_current r

    LEFT JOIN user_history u
        ON r.user_id = u.user_id

    LEFT JOIN video_history vh
        ON r.video_id = vh.video_id

    LEFT JOIN videos vb
        ON r.video_id = vb.video_id

)
TO 'outputs/tables/randomized_ranking_dataset.csv'
(HEADER, DELIMITER ',');