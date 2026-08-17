-- ============================================================
-- Personalized Feed Experimentation
-- 02 — Instrumentation & Data Quality Audit
--
-- Purpose:
-- Validate event coverage, feedback signals, product surfaces,
-- and logging assumptions before defining product metrics.
-- ============================================================


-- ------------------------------------------------------------
-- 1. Standard recommendation log coverage
-- for every observation window from earliest date to latest, use standard all to see interaction records, users, videos, etc
-- ------------------------------------------------------------
COPY (
    SELECT 
        observation_window,
        COUNT(*) AS interaction_records,
        COUNT(DISTINCT user_id) AS unique_users,
        COUNT(DISTINCT video_id) AS unique_videos,
        MIN(date) AS first_date,
        MAX(date) AS last_date,
    FROM 
        standard_all,
    GROUP BY 
        observation_window
    ORDER BY
        first_date ASC
)
TO 'outputs/tables/audit_standard_coverage.csv'
(HEADER, DELIMITER ',');

-- ------------------------------------------------------------
-- 2. Random-intervention log coverage
-- 
-- ------------------------------------------------------------
COPY (
    SELECT 
        COUNT(*) AS interaction_records,
        COUNT(DISTINCT user_id) AS unique_users,
        COUNT(DISTINCT video_id) AS unique_videos,
        MIN(date) AS first_date,
        MAX(date) AS last_date,
        AVG(is_rand) AS random_flag_rate
    FROM 
        random_current
)
TO 'outputs/tables/audit_random_coverage.csv'
(HEADER, DELIMITER ',');

-- ------------------------------------------------------------
-- 3. Feedback rates by product surface / tab
--
-- IMPORTANT:
-- is_click does not mean exactly the same thing across every UI,
-- so we examine it by tab rather than treating it as universal CTR.
-- ------------------------------------------------------------

COPY (
    SELECT
        tab,
        COUNT(*) AS interactions,
        COUNT(DISTINCT user_id) AS users,
        AVG(is_click) AS click_or_valid_play_rate,
        AVG(long_view) AS long_view_rate,
        AVG(is_like) AS like_rate,
        AVG(is_follow) AS follow_rate,
        AVG(is_comment) AS comment_rate,
        AVG(is_forward) AS forward_rate,
        AVG(is_hate) AS hate_rate,
        AVG(is_profile_enter) AS profile_enter_rate,
        AVG(play_time_ms) AS avg_play_time_ms,
        AVG(duration_ms) AS avg_video_duration_ms
    FROM standard_all
    GROUP BY tab
    ORDER BY interactions DESC
)
TO 'outputs/tables/audit_feedback_rates_by_tab.csv'
(HEADER, DELIMITER ',');

-- ------------------------------------------------------------
-- 4. Relationship between is_click and long_view
--
-- This helps determine whether long_view captures behavior
-- materially different from the overloaded is_click signal.
-- table with is click, long view, number of interactions, and pct of itneractions from each group
-- group by is click and long view
-- ------------------------------------------------------------
COPY (
    SELECT
        is_click,
        long_view,
        COUNT(*) AS interactions,
        ROUND(
            100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
            3
        ) AS pct_interactions
    FROM standard_all
    GROUP BY is_click, long_view
    ORDER BY is_click, long_view
)
TO 'outputs/tables/audit_click_long_view_matrix.csv'
(HEADER, DELIMITER ',');
-- ------------------------------------------------------------
-- 5. Core logging quality checks
-- ------------------------------------------------------------
COPY (
    SELECT
        COUNT(*) AS total_rows,

        SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END)
            AS missing_user_id,

        SUM(CASE WHEN video_id IS NULL THEN 1 ELSE 0 END)
            AS missing_video_id,

        SUM(CASE WHEN time_ms IS NULL THEN 1 ELSE 0 END)
            AS missing_timestamp,

        SUM(CASE WHEN play_time_ms IS NULL THEN 1 ELSE 0 END)
            AS missing_play_time,

        SUM(CASE WHEN duration_ms IS NULL THEN 1 ELSE 0 END)
            AS missing_duration,

        SUM(CASE WHEN play_time_ms < 0 THEN 1 ELSE 0 END)
            AS negative_play_time,

        SUM(CASE WHEN duration_ms <= 0 THEN 1 ELSE 0 END)
            AS nonpositive_duration,

        SUM(
            CASE
                WHEN is_click IS NULL OR is_click NOT IN (0,1)
                THEN 1 ELSE 0
            END
        ) AS invalid_click_flag,

        SUM(
            CASE
                WHEN long_view IS NULL OR long_view NOT IN (0,1)
                THEN 1 ELSE 0
            END
        ) AS invalid_long_view_flag,

        SUM(
            CASE
                WHEN is_like IS NULL OR is_like NOT IN (0,1)
                THEN 1 ELSE 0
            END
        ) AS invalid_like_flag,

        SUM(
            CASE
                WHEN is_hate IS NULL OR is_hate NOT IN (0,1)
                THEN 1 ELSE 0
            END
        ) AS invalid_hate_flag

    FROM standard_all
)
TO 'outputs/tables/audit_data_quality.csv'
(HEADER, DELIMITER ',');

-- ------------------------------------------------------------
-- 6. Basic distribution of recommendation scenarios
-- ------------------------------------------------------------

COPY (
    SELECT
        tab,
        COUNT(*) AS interactions,
        COUNT(DISTINCT user_id) AS users,
        COUNT(DISTINCT video_id) AS videos,
        ROUND(
            100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
            3
        ) AS pct_interactions
    FROM standard_all
    GROUP BY tab
    ORDER BY interactions DESC
)
TO 'outputs/tables/audit_tab_distribution.csv'
(HEADER, DELIMITER ',');