
import duckdb

con = duckdb.connect()

sales = "read_csv_auto('data/raw/sales_train_validation.csv', header=true)"
processed = "read_parquet('data/processed/daily_demand_by_store_category.parquet')"

# Calculate the original total sales.
original_total = con.execute(f"""
    SELECT SUM(units) 
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
    )
""").fetchone()[0]

# Calculate the aggregated total sales.
aggregated_total = con.execute(f"""
    SELECT SUM(units_sold)
    FROM {processed}
""").fetchone()[0]

print("ORIGINAL TOTAL:", f"{original_total:,.0f}")
print("AGGREGATED TOTAL:", f"{aggregated_total:,.0f}")
print("DIFFERENCE:", f"{original_total - aggregated_total:,.0f}")

if original_total == aggregated_total:
    print("VALIDATION: PASSED")
else:
    print("VALIDATION: FAILED")

con.close()