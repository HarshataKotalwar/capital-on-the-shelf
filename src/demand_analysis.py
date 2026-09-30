
import duckdb
from pathlib import Path

Path("data/processed").mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

sales = "read_csv_auto('data/raw/sales_train_validation.csv', header=true)"
calendar = "read_csv_auto('data/raw/calendar.csv', header=true)"

output = "data/processed/daily_demand_by_store_category.parquet"


query = f"""
COPY (
    SELECT
        c.date,
        c.d,
        u.state_id,
        u.store_id,
        u.cat_id,
        SUM(u.units) AS units_sold
    FROM (
        SELECT *
        FROM {sales}
        UNPIVOT (
            units FOR day_id IN (
                COLUMNS(* EXCLUDE (
                    id, item_id, dept_id,
                    cat_id, store_id, state_id
                ))
            )
        )
    ) AS u
    JOIN {calendar} AS c
        ON c.d = u.day_id
    GROUP BY
        c.date, c.d, u.state_id, u.store_id, u.cat_id
    ORDER BY
        c.date, u.store_id, u.cat_id
)
TO 'data/processed/daily_demand_by_store_category.parquet'
(FORMAT PARQUET, COMPRESSION ZSTD)
"""
con.execute(query)

result = con.execute(f"""
    SELECT
        COUNT(*) AS rows,
        MIN(date) AS first_date,
        MAX(date) AS last_date,
        SUM(units_sold) AS total_units
    FROM read_parquet('{output}')
""").fetchone()

print("DAILY DEMAND DATASET")
print("Rows:", f"{result[0]:,}")
print("First date:", result[1])
print("Last date:", result[2])
print("Total units sold:", f"{result[3]:,}")

con.close()