from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "processed" / "personalized-feed-experimentation.duckdb"
SQL_PATH = ROOT / "sql" / "00_create_views.sql"


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    try:
        sql = SQL_PATH.read_text(encoding="utf-8")
        # DuckDB read_csv paths are resolved from the current working directory.
        # Execute from repository root so relative paths in SQL stay portable.
        import os
        os.chdir(ROOT)
        con.execute(sql)
        print(f"Created local warehouse: {DB_PATH}")
        print("Views:")
        for row in con.execute("SHOW TABLES").fetchall():
            print(f"  - {row[0]}")
    finally:
        con.close()


if __name__ == "__main__":
    main()
