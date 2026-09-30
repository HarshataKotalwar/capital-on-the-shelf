
import duckdb
import matplotlib.pyplot as plt
from pathlib import Path

Path("reports/figures").mkdir(parents=True, exist_ok=True)
Path("reports/exports").mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

data = "data/processed/daily_demand_by_store_category.parquet"

# Category performance
category = con.execute(f"""
    SELECT
        cat_id AS category,
        SUM(units_sold) AS total_units
    FROM read_parquet('{data}')
    GROUP BY cat_id
    ORDER BY total_units DESC
""").fetchdf()

category["share_pct"] = (
    category["total_units"] / category["total_units"].sum() * 100
)

# Store performance
store = con.execute(f"""
    SELECT
        store_id AS store,
        SUM(units_sold) AS total_units
    FROM read_parquet('{data}')
    GROUP BY store_id
    ORDER BY total_units DESC
""").fetchdf()

store["share_pct"] = (
    store["total_units"] / store["total_units"].sum() * 100
)

con.close()

# Save results
category.to_csv(
    "reports/exports/category_performance.csv",
    index=False
)
store.to_csv(
    "reports/exports/store_performance.csv",
    index=False
)

print("\n--- CATEGORY PERFORMANCE ---")
print(category.round(2).to_string(index=False))

print("\n--- STORE PERFORMANCE ---")
print(store.round(2).to_string(index=False))

# Category chart
plt.figure(figsize=(9, 5))
plt.bar(category["category"], category["total_units"])
plt.title("Total Recorded Sales by Category")
plt.xlabel("Category")
plt.ylabel("Units Sold")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(
    "reports/figures/category_performance.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# Store chart
plt.figure(figsize=(10, 5))
plt.bar(store["store"], store["total_units"])
plt.title("Total Recorded Sales by Store")
plt.xlabel("Store")
plt.ylabel("Units Sold")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(
    "reports/figures/store_performance.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

print("\nCharts and CSV files saved successfully.")