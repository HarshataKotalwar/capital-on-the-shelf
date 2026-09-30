
import duckdb
from pathlib import Path

Path("reports/exports").mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

query = """
WITH base AS (
    SELECT
        item_id,
        store_id,
        cat_id,
        total_units,
        avg_daily_units,
        std_daily_units,
        CASE
            WHEN avg_daily_units > 0
            THEN std_daily_units / avg_daily_units
            ELSE NULL
        END AS coefficient_of_variation,
        100.0 * zero_sales_days / NULLIF(total_days, 0)
            AS zero_sales_pct
    FROM read_parquet(
        'data/processed/product_store_demand.parquet'
    )
),
ranked AS (
    SELECT
        *,
        SUM(total_units) OVER (
            ORDER BY total_units DESC, item_id, store_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_units,
        SUM(total_units) OVER () AS grand_total_units
    FROM base
),
classified AS (
    SELECT *,
        100.0 * cumulative_units /
            NULLIF(grand_total_units, 0) AS cumulative_share_pct,
        CASE
            WHEN 100.0 * cumulative_units /
                NULLIF(grand_total_units, 0) <= 80 THEN 'A'
            WHEN 100.0 * cumulative_units /
                NULLIF(grand_total_units, 0) <= 95 THEN 'B'
            ELSE 'C'
        END AS abc_class,
        CASE
            WHEN coefficient_of_variation IS NULL
                THEN 'Undefined'
            WHEN coefficient_of_variation < 0.5
                THEN 'Stable'
            WHEN coefficient_of_variation < 1.0
                THEN 'Moderate'
            ELSE 'High'
        END AS variability_class
    FROM ranked
)
SELECT *
FROM classified
ORDER BY total_units DESC
"""

df = con.execute(query).fetchdf()

df.to_csv(
    "reports/exports/demand_classification.csv",
    index=False
)

print("\n--- ABC CLASSIFICATION ---")
print(
    df.groupby("abc_class")
      .agg(
          product_store_count=("item_id", "size"),
          total_units=("total_units", "sum")
      )
      .assign(
          unit_share_pct=lambda x:
              100 * x["total_units"] / df["total_units"].sum()
      )
      .round(2)
      .to_string()
)

print("\n--- ABC AND VARIABILITY ---")
print(
    df.groupby(["abc_class", "variability_class"])
      .size()
      .unstack(fill_value=0)
      .to_string()
)

con.close()