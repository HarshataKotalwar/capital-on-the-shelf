
import duckdb
from pathlib import Path

Path("reports/exports").mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

query = """
WITH training_week AS (
    SELECT wm_yr_wk
    FROM read_csv_auto('data/raw/calendar.csv', header=true)
    WHERE d = 'd_1885'
),
latest_prices AS (
    SELECT
        p.item_id,
        p.store_id,
        p.wm_yr_wk,
        p.sell_price,
        ROW_NUMBER() OVER (
            PARTITION BY p.item_id, p.store_id
            ORDER BY p.wm_yr_wk DESC
        ) AS rn
    FROM read_csv_auto(
        'data/raw/sell_prices.csv',
        header=true
    ) AS p
    CROSS JOIN training_week AS w
    WHERE p.wm_yr_wk <= w.wm_yr_wk
)
SELECT
    item_id,
    store_id,
    wm_yr_wk,
    sell_price
FROM latest_prices
WHERE rn = 1
"""

df = con.execute(query).fetchdf()

df.to_csv(
    "reports/exports/latest_available_prices.csv",
    index=False
)

print("\n--- AVAILABLE SELLING PRICES ---")
print("Product-store combinations with prices:", f"{len(df):,}")
print("Average selling price:", round(df["sell_price"].mean(), 2))
print("Median selling price:", round(df["sell_price"].median(), 2))
print("Minimum selling price:", round(df["sell_price"].min(), 2))
print("Maximum selling price:", round(df["sell_price"].max(), 2))

print("\nPrice distribution by category:")
sales = con.execute("""
    SELECT item_id, store_id, cat_id
    FROM read_csv_auto(
        'data/raw/sales_train_validation.csv',
        header=true
    )
""").fetchdf()

df = df.merge(
    sales[["item_id", "store_id", "cat_id"]],
    on=["item_id", "store_id"],
    how="left",
    validate="one_to_one"
)

print(
    df.groupby("cat_id")["sell_price"]
      .agg(["count", "mean", "median", "min", "max"])
      .round(2)
      .to_string()
)

con.close()