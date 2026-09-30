
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("reports/figures").mkdir(parents=True, exist_ok=True)
Path("reports/exports").mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

data = "data/processed/daily_demand_by_store_category.parquet"

# Calculate sales for complete months only
monthly = con.execute(f"""
    WITH daily AS (
        SELECT
            CAST(date AS DATE) AS sales_date,
            SUM(units_sold) AS daily_units
        FROM read_parquet('{data}')
        GROUP BY CAST(date AS DATE)
    ),
    monthly AS (
        SELECT
            DATE_TRUNC('month', sales_date)::DATE AS month,
            SUM(daily_units) AS total_units,
            COUNT(*) AS observed_days,
            DAY(LAST_DAY(sales_date)) AS days_in_month
        FROM daily
        GROUP BY
            DATE_TRUNC('month', sales_date),
            LAST_DAY(sales_date)
    )
    SELECT *
    FROM monthly
    WHERE observed_days = days_in_month
    ORDER BY month
""").fetchdf()

con.close()

monthly["month"] = pd.to_datetime(monthly["month"])
monthly["month_name"] = monthly["month"].dt.month_name()
monthly["month_number"] = monthly["month"].dt.month

# Calculate average sales by calendar month
seasonality = (
    monthly.groupby(["month_number", "month_name"], as_index=False)
    ["total_units"].mean()
    .sort_values("month_number")
)

overall_average = monthly["total_units"].mean()
seasonality["index"] = (
    seasonality["total_units"] / overall_average * 100
)

seasonality.to_csv(
    "reports/exports/monthly_seasonality.csv",
    index=False
)

print("\n--- MONTHLY SEASONALITY ---")
print(seasonality[
    ["month_name", "total_units", "index"]
].round(2).to_string(index=False))

# Plot average sales by calendar month
plt.figure(figsize=(12, 6))
plt.bar(seasonality["month_name"], seasonality["total_units"])
plt.title("Average Sales by Calendar Month")
plt.xlabel("Month")
plt.ylabel("Average Units Sold")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "reports/figures/monthly_seasonality.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

print("\nSeasonality chart saved.")
print("Seasonality CSV saved.")