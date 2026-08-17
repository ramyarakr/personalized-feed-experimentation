-- ============================================================
-- 12 — Surface Content Analysis
-- Question:
-- Is Tab 2 serving structurally different content?
-- ============================================================


-- ------------------------------------------------------------
-- A. Content profile by surface
-- ------------------------------------------------------------

COPY (
    WITH enriched AS (
        SELECT
            s.tab,
            s.user_id,
            s.video_id,
            s.duration_ms,
            v.author_id,
            v.video_type,
            v.upload_type,
            v.tag,
            v.upload_dt,

            CAST(
                strptime(CAST(s.date AS VARCHAR), '%Y%m%d')
                AS DATE
            ) AS event_date

        FROM standard_all s

        LEFT JOIN videos v
            ON s.video_id = v.video_id

        WHERE s.tab IN (0,1,2,4)
    ),

    author_counts AS (
        SELECT
            tab,
            author_id,
            COUNT(*) AS interactions
        FROM enriched
        WHERE author_id IS NOT NULL
        GROUP BY tab, author_id
    ),

    top_author AS (
        SELECT
            tab,
            MAX(interactions) AS top_author_interactions
        FROM author_counts
        GROUP BY tab
    ),

    totals AS (
        SELECT
            tab,
            COUNT(*) AS total_interactions
        FROM enriched
        GROUP BY tab
    )

    SELECT
        e.tab,

        COUNT(*) AS interactions,
        COUNT(DISTINCT e.video_id) AS unique_videos,
        COUNT(DISTINCT e.author_id) AS unique_authors,
        COUNT(DISTINCT e.tag) AS unique_tag_values,

        AVG(
            CASE WHEN e.duration_ms > 0
                 THEN e.duration_ms / 1000.0
            END
        ) AS avg_video_duration_seconds,

        MEDIAN(
            CASE WHEN e.duration_ms > 0
                 THEN e.duration_ms / 1000.0
            END
        ) AS median_video_duration_seconds,

        AVG(
            CASE
                WHEN e.upload_dt IS NOT NULL
                THEN date_diff(
                    'day',
                    e.upload_dt,
                    e.event_date
                )
            END
        ) AS avg_content_age_days,

        ta.top_author_interactions * 1.0
            / t.total_interactions
            AS top_author_interaction_share

    FROM enriched e

    JOIN totals t USING(tab)
    JOIN top_author ta USING(tab)

    GROUP BY
        e.tab,
        ta.top_author_interactions,
        t.total_interactions

    ORDER BY e.tab
)
TO 'outputs/tables/surface_content_profiles.csv'
(HEADER, DELIMITER ',');


-- ------------------------------------------------------------
-- B. Video-type distribution
-- ------------------------------------------------------------

COPY (
    SELECT
        s.tab,
        v.video_type,
        COUNT(*) AS interactions,

        COUNT(*) * 1.0
        / SUM(COUNT(*)) OVER (
            PARTITION BY s.tab
        ) AS interaction_share

    FROM standard_all s

    LEFT JOIN videos v
        ON s.video_id = v.video_id

    WHERE s.tab IN (0,1,2,4)

    GROUP BY
        s.tab,
        v.video_type

    ORDER BY
        s.tab,
        interactions DESC
)
TO 'outputs/tables/surface_video_type_distribution.csv'
(HEADER, DELIMITER ',');


-- ------------------------------------------------------------
-- C. Upload-type distribution
-- ------------------------------------------------------------

COPY (
    SELECT
        s.tab,
        v.upload_type,
        COUNT(*) AS interactions,

        COUNT(*) * 1.0
        / SUM(COUNT(*)) OVER (
            PARTITION BY s.tab
        ) AS interaction_share

    FROM standard_all s

    LEFT JOIN videos v
        ON s.video_id = v.video_id

    WHERE s.tab IN (0,1,2,4)

    GROUP BY
        s.tab,
        v.upload_type

    ORDER BY
        s.tab,
        interactions DESC
)
TO 'outputs/tables/surface_upload_type_distribution.csv'
(HEADER, DELIMITER ',');


-- ------------------------------------------------------------
-- D. Top tag values by surface
-- ------------------------------------------------------------

COPY (
    WITH tag_counts AS (
        SELECT
            s.tab,
            v.tag,
            COUNT(*) AS interactions

        FROM standard_all s

        LEFT JOIN videos v
            ON s.video_id = v.video_id

        WHERE s.tab IN (0,1,2,4)
          AND v.tag IS NOT NULL

        GROUP BY
            s.tab,
            v.tag
    ),

    ranked AS (
        SELECT
            *,

            ROW_NUMBER() OVER (
                PARTITION BY tab
                ORDER BY interactions DESC
            ) AS tag_rank,

            interactions * 1.0
            / SUM(interactions) OVER (
                PARTITION BY tab
            ) AS interaction_share

        FROM tag_counts
    )

    SELECT
        tab,
        tag_rank,
        tag,
        interactions,
        interaction_share

    FROM ranked

    WHERE tag_rank <= 10

    ORDER BY
        tab,
        tag_rank
)
TO 'outputs/tables/surface_top_tags.csv'
(HEADER, DELIMITER ',');