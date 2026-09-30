
import csv
from pathlib import Path

DATA_DIR = Path("data/raw")

files = [
    "calendar.csv",
    "sales_train_validation.csv",
    "sell_prices.csv",
]

for filename in files:
    path = DATA_DIR / filename

    print(f"\n{'=' * 60}")
    print(f"FILE: {filename}")
    print(f"SIZE: {path.stat().st_size / (1024 * 1024):.2f} MB")

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        row_count = sum(1 for _ in reader)

    print(f"ROWS: {row_count:,}")
    print(f"COLUMNS: {len(header):,}")
    print("FIRST 15 COLUMN NAMES:")
    print(header[:15])