
from pathlib import Path

import duckdb
import pandas as pd

Path("reports/exports").mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

# Illustrative assumption, not an observed M5 cost.
PROCUREMENT_COST_RATIO = 0.60

query = f"""
WITH forecast AS (
    SELECT *
    FROM read_parquet(
        'data/processed/demand_forecast_evaluation.parquet'
    )
),
prices AS (
    SELECT
        item_id,
        store_id,
        sell_price
    FROM read_csv_auto(
        'reports/exports/latest_available_prices.csv',
        header=true
    )
)
SELECT
    f.item_id,
    f.store_id,
    f.cat_id,
    f.forecast_units,
    f.actual_units,
    p.sell_price,
    p.sell_price * {PROCUREMENT_COST_RATIO}
        AS unit_cost_assumption,
    f.forecast_units * p.sell_price
        AS estimated_revenue,
    f.forecast_units * p.sell_price * {PROCUREMENT_COST_RATIO}
        AS estimated_procurement_cost,
    f.forecast_units * p.sell_price * (1 - {PROCUREMENT_COST_RATIO})
        AS estimated_gross_margin
FROM forecast AS f
LEFT JOIN prices AS p
    USING (item_id, store_id)
"""

df = con.execute(query).fetchdf()

if df["sell_price"].isna().any():
    raise ValueError("Some product-store combinations have no price.")

df.to_csv(
    "reports/exports/inventory_economics.csv",
    index=False
)

print("\n--- 28-DAY INVENTORY ECONOMICS ---")
print("Product-store combinations:", f"{len(df):,}")
print(
    "Estimated sales revenue:",
    f"${df['estimated_revenue'].sum():,.2f}"
)
print(
    "Estimated procurement requirement:",
    f"${df['estimated_procurement_cost'].sum():,.2f}"
)
print(
    "Estimated gross margin:",
    f"${df['estimated_gross_margin'].sum():,.2f}"
)
print(
    "Assumed procurement cost ratio:",
    f"{PROCUREMENT_COST_RATIO:.0%}"
)

print("\n--- ECONOMICS BY CATEGORY ---")
category = (
    df.groupby("cat_id")
    .agg(
        forecast_units=("forecast_units", "sum"),
        revenue=("estimated_revenue", "sum"),
        procurement_cost=("estimated_procurement_cost", "sum"),
        gross_margin=("estimated_gross_margin", "sum")
    )
)

print(category.round(2).to_string())

print("\nNote: These are hypothetical economics, not actual profits.")

con.close()