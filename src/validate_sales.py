
import duckdb

con = duckdb.connect()

sales = "read_csv_auto('data/raw/sales_train_validation.csv', header=true)"
prices = "read_csv_auto('data/raw/sell_prices.csv', header=true)"

# Get the unique product-store combinations from sales.
con.execute(f"""
    CREATE TEMP TABLE sales_products AS
    SELECT DISTINCT item_id, store_id
    FROM {sales}
""")

# Find which combinations have at least one price record.
con.execute(f"""
    CREATE TEMP TABLE covered_products AS
    SELECT DISTINCT s.item_id, s.store_id
    FROM sales_products s
    SEMI JOIN {prices} p
    USING (item_id, store_id)
""")

total = con.execute(
    "SELECT COUNT(*) FROM sales_products"
).fetchone()[0]

covered = con.execute(
    "SELECT COUNT(*) FROM covered_products"
).fetchone()[0]

print("\n--- PRODUCT-STORE PRICE COVERAGE ---")
print("Total combinations:", f"{total:,}")
print("With price records:", f"{covered:,}")
print("Without price records:", f"{total - covered:,}")

con.close()