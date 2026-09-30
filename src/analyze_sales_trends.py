
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Create output directories
Path("reports/figures").mkdir(parents=True, exist_ok=True)
Path("reports/exports").mkdir(parents=True, exist_ok=True)

# Connect to DuckDB
con = duckdb.connect()

data = "data/processed/daily_demand_by_store_category.parquet"

# Analyse only complete calendar months

monthly = con.execute(f"""
    WITH daily AS (
        SELECT
            CAST(date AS DATE) AS sales_date,
            SUM(units_sold) AS daily_units
        FROM read_parquet('{data}')
        GROUP BY CAST(date AS DATE)
    )
    SELECT
        DATE_TRUNC('month', sales_date)::DATE AS month,
        SUM(daily_units) AS total_units,
        COUNT(*) AS observed_days,
        DAY(LAST_DAY(sales_date)) AS days_in_month
    FROM daily
    GROUP BY
        DATE_TRUNC('month', sales_date),
        LAST_DAY(sales_date)
    HAVING COUNT(*) = DAY(LAST_DAY(sales_date))
    ORDER BY month
""").fetchdf()

con.close()

monthly["month"] = pd.to_datetime(monthly["month"])

# Save monthly data
monthly.to_csv(
    "reports/exports/monthly_sales_trend_complete.csv",
    index=False
)

# Print summary
print("\n--- COMPLETE MONTHLY SALES SUMMARY ---")
print("Complete months:", len(monthly))
print(
    "Average monthly sales:",
    round(monthly["total_units"].mean(), 2)
)

highest = monthly.loc[monthly["total_units"].idxmax()]
lowest = monthly.loc[monthly["total_units"].idxmin()]

print(
    "Highest sales month:",
    highest["month"].strftime("%B %Y")
)
print("Highest sales:", f"{highest['total_units']:,.0f}")

print(
    "Lowest sales month:",
    lowest["month"].strftime("%B %Y")
)
print("Lowest sales:", f"{lowest['total_units']:,.0f}")

# Plot monthly sales
plt.figure(figsize=(14, 6))
plt.plot(
    monthly["month"],
    monthly["total_units"],
    linewidth=1.5
)

plt.title("Monthly Recorded Sales (Complete Months Only)")
plt.xlabel("Month")
plt.ylabel("Units Sold")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "reports/figures/monthly_sales_trend_complete.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

print("\nChart saved successfully.")
print("CSV saved successfully.")