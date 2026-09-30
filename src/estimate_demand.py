
import re
from pathlib import Path

import duckdb
import pandas as pd

Path("data/processed").mkdir(parents=True, exist_ok=True)
Path("reports/exports").mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

sales_file = "data/raw/sales_train_validation.csv"
sales = f"read_csv_auto('{sales_file}', header=true)"

# Identify and numerically sort the daily sales columns.
columns = con.execute(
    f"DESCRIBE SELECT * FROM {sales}"
).fetchdf()["column_name"].tolist()

day_columns = sorted(
    [c for c in columns if re.fullmatch(r"d_\d+", c)],
    key=lambda c: int(c.split("_")[1])
)

if len(day_columns) != 1913:
    raise ValueError(
        f"Expected 1913 daily columns, found {len(day_columns)}"
    )

# Reserve the last 28 days for evaluation.
holdout_days = day_columns[-28:]
training_days = day_columns[:-28]

# Use the 28 days immediately before the holdout
# to estimate average daily demand.
baseline_days = training_days[-28:]

def quote_columns(names):
    return ", ".join(f'"{name}"' for name in names)

metadata = """
    id, item_id, dept_id, cat_id, store_id, state_id
"""

baseline_sql = f"""
    SELECT
        item_id,
        store_id,
        cat_id,
        AVG(units) AS avg_daily_demand,
        SUM(units) AS baseline_units
    FROM (
        SELECT *
        FROM {sales}
        UNPIVOT (
            units FOR day_id IN ({quote_columns(baseline_days)})
        )
    ) AS b
    GROUP BY item_id, store_id, cat_id
"""

actual_sql = f"""
    SELECT
        item_id,
        store_id,
        cat_id,
        SUM(units) AS actual_units
    FROM (
        SELECT *
        FROM {sales}
        UNPIVOT (
            units FOR day_id IN ({quote_columns(holdout_days)})
        )
    ) AS h
    GROUP BY item_id, store_id, cat_id
"""

query = f"""
COPY (
    SELECT
        a.item_id,
        a.store_id,
        a.cat_id,
        b.avg_daily_demand,
        b.avg_daily_demand * 28 AS forecast_units,
        a.actual_units,
        ABS(b.avg_daily_demand * 28 - a.actual_units)
            AS absolute_error,
        b.avg_daily_demand * 28 - a.actual_units
            AS forecast_bias
    FROM ({actual_sql}) AS a
    JOIN ({baseline_sql}) AS b
        USING (item_id, store_id, cat_id)
)
TO 'data/processed/demand_forecast_evaluation.parquet'
(FORMAT PARQUET, COMPRESSION ZSTD)
"""

print("Estimating demand and evaluating holdout period...")
con.execute(query)

df = con.execute("""
    SELECT *
    FROM read_parquet(
        'data/processed/demand_forecast_evaluation.parquet'
    )
""").fetchdf()

df.to_csv(
    "reports/exports/demand_forecast_evaluation.csv",
    index=False
)

total_actual = df["actual_units"].sum()
total_forecast = df["forecast_units"].sum()
total_abs_error = df["absolute_error"].sum()

mae = df["absolute_error"].mean()
wape = (
    100 * total_abs_error / total_actual
    if total_actual else float("nan")
)
bias = df["forecast_bias"].sum()

print("\n--- 28-DAY DEMAND FORECAST EVALUATION ---")
print("Product-store combinations:", f"{len(df):,}")
print("Baseline days:", baseline_days[0], "to", baseline_days[-1])
print("Holdout days:", holdout_days[0], "to", holdout_days[-1])
print("Actual units:", f"{total_actual:,.0f}")
print("Forecast units:", f"{total_forecast:,.0f}")
print("MAE (units per combination):", f"{mae:,.2f}")
print("WAPE:", f"{wape:.2f}%")
print("Forecast bias (units):", f"{bias:,.0f}")

con.close()