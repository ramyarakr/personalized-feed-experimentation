-- Personalized Feed Experimentation: raw DuckDB views over KuaiRand-1K CSV files.
-- Paths are relative to the repository root when build_warehouse.py runs.

CREATE OR REPLACE VIEW standard_prior AS
SELECT *
FROM read_csv_auto('data/raw/KuaiRand-1K/data/log_standard_4_08_to_4_21_1k.csv', header=true);

CREATE OR REPLACE VIEW standard_current AS
SELECT *
FROM read_csv_auto('data/raw/KuaiRand-1K/data/log_standard_4_22_to_5_08_1k.csv', header=true);

CREATE OR REPLACE VIEW random_current AS
SELECT *
FROM read_csv_auto('data/raw/KuaiRand-1K/data/log_random_4_22_to_5_08_1k.csv', header=true);

CREATE OR REPLACE VIEW users AS
SELECT *
FROM read_csv_auto('data/raw/KuaiRand-1K/data/user_features_1k.csv', header=true);

CREATE OR REPLACE VIEW videos AS
SELECT *
FROM read_csv_auto('data/raw/KuaiRand-1K/data/video_features_basic_1k.csv', header=true);

CREATE OR REPLACE VIEW video_stats AS
SELECT *
FROM read_csv_auto('data/raw/KuaiRand-1K/data/video_features_statistic_1k.csv', header=true);

-- Unified standard recommendation log across the two periods.
CREATE OR REPLACE VIEW standard_all AS
SELECT *, 'prior' AS observation_window FROM standard_prior
UNION ALL BY NAME
SELECT *, 'current' AS observation_window FROM standard_current;
