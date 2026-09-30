
import csv
from datetime import datetime
from pathlib import Path

import duckdb

DATA = Path("data/raw")

# 1. Validate the calendar
with (DATA / "calendar.csv").open(
    encoding="utf-8", newline=""
) as f:
    calendar = list(csv.DictReader(f))

calendar_dates = [r["date"] for r in calendar]
calendar_days = [r["d"] for r in calendar]

print("\n--- CALENDAR VALIDATION ---")
print("Date range:", min(calendar_dates), "to", max(calendar_dates))
print("Unique dates:", len(set(calendar_dates)))
print("Unique day IDs:", len(set(calendar_days)))
print("Duplicate dates:", len(calendar_dates) - len(set(calendar_dates)))
print("Duplicate day IDs:", len(calendar_days) - len(set(calendar_days)))

# 2. Validate sales structure and IDs
with (DATA / "sales_train_validation.csv").open(
    encoding="utf-8", newline=""
) as f:
    reader = csv.reader(f)
    header = next(reader)
    metadata_cols = header[:6]
    day_cols = header[6:]

    ids = set()
    duplicates = 0
    row_count = 0
    bad_width = 0

    for row in reader:
        row_count += 1
        if len(row) != len(header):
            bad_width += 1
        if row[0] in ids:
            duplicates += 1
        ids.add(row[0])

print("\n--- SALES VALIDATION ---")
print("Metadata columns:", metadata_cols)
print("Daily columns:", len(day_cols))
print("First daily column:", day_cols[0])
print("Last daily column:", day_cols[-1])
print("Sales rows:", row_count)
print("Unique IDs:", len(ids))
print("Duplicate IDs:", duplicates)
print("Rows with unexpected width:", bad_width)

# 3. Check calendar coverage of sales days
calendar_day_set = set(calendar_days)
missing_days = [
    day for day in day_cols if day not in calendar_day_set
]
print("\n--- DATE COVERAGE ---")
print("Sales days missing from calendar:", len(missing_days))
print("Missing day examples:", missing_days[:10])

# 4. Validate price records with DuckDB
con = duckdb.connect()

price_file = str(DATA / "sell_prices.csv").replace("'", "''")
price_table = f"read_csv_auto('{price_file}', header=true)"

summary = con.execute(f"""
    SELECT
        COUNT(*) AS rows,
        COUNT(*) FILTER (
            WHERE store_id IS NULL
               OR item_id IS NULL
               OR wm_yr_wk IS NULL
               OR sell_price IS NULL
        ) AS missing_rows,
        MIN(sell_price) AS min_price,
        MAX(sell_price) AS max_price
    FROM {price_table}
""").fetchone()

duplicates = con.execute(f"""
    SELECT COUNT(*)
    FROM (
        SELECT store_id, item_id, wm_yr_wk
        FROM {price_table}
        GROUP BY store_id, item_id, wm_yr_wk
        HAVING COUNT(*) > 1
    ) t
""").fetchone()[0]

print("\n--- PRICE VALIDATION ---")
print("Rows:", f"{summary[0]:,}")
print("Rows with missing key/price:", f"{summary[1]:,}")
print("Minimum price:", summary[2])
print("Maximum price:", summary[3])
print("Duplicate store-item-week keys:", f"{duplicates:,}")

con.close()