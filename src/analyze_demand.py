
import duckdb
from pathlib import Path

Path("reports/exports").mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

sales = "read_csv_auto('data/raw/sales_train_validation.csv', header=true)"

query = f"""
COPY (
    SELECT
        u.item_id,
        u.store_id,
        u.cat_id,
        SUM(u.units) AS total_units,
        AVG(u.units) AS avg_daily_units,
        STDDEV_POP(u.units) AS std_daily_units,
        COUNT(*) FILTER (WHERE u.units = 0) AS zero_sales_days,
        COUNT(*) FILTER (WHERE u.units > 0) AS selling_days,
        COUNT(*) AS total_days
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
    GROUP BY u.item_id, u.store_id, u.cat_id
)
TO 'data/processed/product_store_demand.parquet'
(FORMAT PARQUET, COMPRESSION ZSTD)
"""

con.execute(query)

# Calculate CV and zero-sales percentage from the summary.
summary = con.execute("""
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
        zero_sales_days,
        selling_days,
        total_days,
        100.0 * zero_sales_days / total_days
            AS zero_sales_pct
    FROM read_parquet(
        'data/processed/product_store_demand.parquet'
    )
    ORDER BY total_units DESC
""").fetchdf()

summary.to_csv(
    "reports/exports/product_store_demand.csv",
    index=False
)

print("\n--- PRODUCT-STORE DEMAND SUMMARY ---")
print("Product-store records:", f"{len(summary):,}")
print("Total units:", f"{summary['total_units'].sum():,.0f}")
print(
    "Average zero-sales percentage:",
    round(summary["zero_sales_pct"].mean(), 2)
)
print("\nTop 10 product-store combinations:")
print(
    summary[
        ["item_id", "store_id", "total_units",
         "avg_daily_units", "coefficient_of_variation",
         "zero_sales_pct"]
    ].head(10).round(3).to_string(index=False)
)

con.close()