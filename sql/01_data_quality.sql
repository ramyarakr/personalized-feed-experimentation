-- Personalized Feed Experimentation Phase 1: initial data-quality checks.

-- Row counts
SELECT 'standard_prior' AS table_name, COUNT(*) AS rows FROM standard_prior
UNION ALL
SELECT 'standard_current', COUNT(*) FROM standard_current
UNION ALL
SELECT 'random_current', COUNT(*) FROM random_current
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'videos', COUNT(*) FROM videos;

-- Date coverage
SELECT
    MIN(date) AS min_date,
    MAX(date) AS max_date,
    COUNT(DISTINCT date) AS active_dates,
    COUNT(DISTINCT user_id) AS users,
    COUNT(DISTINCT video_id) AS videos
FROM standard_all;

-- Basic engagement rates
SELECT
    AVG(is_click) AS click_or_valid_play_rate,
    AVG(long_view) AS long_view_rate,
    AVG(is_like) AS like_rate,
    AVG(is_follow) AS follow_rate,
    AVG(is_comment) AS comment_rate,
    AVG(is_forward) AS forward_rate,
    AVG(is_hate) AS hate_rate,
    AVG(is_profile_enter) AS profile_enter_rate
FROM standard_all;

-- Duplicate interaction candidates.
-- We do not assume duplicates are invalid until timestamp semantics are inspected.
SELECT
    user_id,
    video_id,
    time_ms,
    COUNT(*) AS n
FROM standard_all
GROUP BY ALL
HAVING COUNT(*) > 1
ORDER BY n DESC
LIMIT 100;
