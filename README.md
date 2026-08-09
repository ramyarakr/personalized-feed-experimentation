# Personalized Feed Experimentation

> Product analytics, experimentation, causal inference, and personalization on large-scale behavioral data.

**Product Data Science for Personalized Feed Experimentation, Retention, and Recommendation Quality**

Personalized Feed Experimentation is a portfolio-grade Product Data Science project built around a realistic short-video recommendation feed. The goal is not merely to train a recommender. The goal is to answer a product decision:

> **Should a feed ranking strategy optimize short-term clicks or meaningful engagement if the product team cares about long-term user value?**

The project uses the public **KuaiRand** dataset from Kuaishou and is designed to demonstrate the skills expected in Product Data Science roles at large consumer technology companies: product metrics, SQL analytics, cohort/retention analysis, experimentation, causal inference, recommendation modeling, heterogeneous treatment effects, and executive communication.

## Zero-cost constraint

This project is intentionally designed to cost **$0**:

- Public KuaiRand dataset
- Local DuckDB for analytical SQL
- Python + open-source statistical/ML libraries
- Jupyter for analysis
- Git + GitHub public repository
- GitHub Pages for the public portfolio site

No paid API, cloud warehouse, paid compute, paid database, or paid hosting is required.

## Product question

The fictional feed team currently optimizes primarily for click/valid-play behavior. We will investigate whether a ranking objective focused on **meaningful engagement** is more aligned with user value and retention, and determine which user segments should receive the new experience.

## Core deliverables

1. **Product brief** — decision, hypotheses, scope, users, and risks
2. **Metric tree** — North Star, input metrics, retention metrics, and guardrails
3. **SQL analytics layer** — reusable DuckDB views and product metrics
4. **Behavioral deep dive** — funnels, cohorts, segments, and root-cause analysis
5. **Experiment design** — hypothesis, power, MDE, SRM checks, and analysis plan
6. **Causal analysis** — compare naive observational estimates with debiased estimates using randomized exposure data
7. **Personalization model** — baseline vs challenger model for meaningful engagement
8. **Heterogeneous effects** — identify who benefits and who may be harmed
9. **Launch memo** — ship / do not ship / segmented rollout recommendation
10. **Portfolio website** — concise recruiter-facing case study hosted with GitHub Pages

## Repository structure

```text
personalized-feed-experimentation/
├── PRODUCT_BRIEF.md
├── METRIC_TREE.md
├── ROADMAP.md
├── data/
│   ├── README.md
│   ├── raw/              # gitignored
│   └── processed/        # gitignored
├── sql/
│   ├── 00_create_views.sql
│   └── 01_data_quality.sql
├── src/
│   └── build_warehouse.py
├── notebooks/
│   └── README.md
├── outputs/
│   ├── figures/
│   └── tables/
├── decision_memo/
├── docs/                 # GitHub Pages site
│   ├── index.html
│   └── styles.css
├── requirements.txt
└── .gitignore
```

## Dataset

We will use **KuaiRand-1K** as the primary working dataset because it contains sequential logs suitable for retention and session analysis while remaining feasible to process locally. Raw data must **not** be committed to GitHub.

Official project: https://github.com/chongminggao/KuaiRand

Official Zenodo record: https://zenodo.org/records/10439422

Expected extracted data folder:

```text
data/raw/KuaiRand-1K/data/
├── log_random_4_22_to_5_08_1k.csv
├── log_standard_4_08_to_4_21_1k.csv
├── log_standard_4_22_to_5_08_1k.csv
├── user_features_1k.csv
├── video_features_basic_1k.csv
└── video_features_statistic_1k.csv
```

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

After downloading and extracting KuaiRand-1K into `data/raw/`, run:

```bash
python src/build_warehouse.py
```

This creates a local DuckDB database at `data/processed/personalized-feed-experimentation.duckdb` and registers views over the CSV files without loading the full dataset into RAM.

## Portfolio principle

Every analysis must answer one of three questions:

1. **What is happening to the product?**
2. **Why is it happening?**
3. **What should the product team do next?**

Charts, models, and statistical tests that do not help answer one of those questions do not belong in the final case study.
