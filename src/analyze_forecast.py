
import re
from pathlib import Path

import duckdb

Path("reports/exports").mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

sales = "read_csv_auto('data/raw/sales_train_validation.csv', header=true)"

columns = con.execute(
    f"DESCRIBE SELECT * FROM {sales}"
).fetchdf()["column_name"].tolist()

training_days = sorted(
    [c for c in columns if re.fullmatch(r"d_\d+", c)
     and int(c.split("_")[1]) <= 1885],
    key=lambda c: int(c.split("_")[1])
)

if len(training_days) != 1885:
    raise ValueError(f"Expected 1885 training days, found {len(training_days)}")

day_list = ", ".join(f'"{d}"' for d in training_days)

query = f"""
WITH demand AS (
    SELECT
        item_id,
        store_id,
        cat_id,
        SUM(units) AS training_units,
        AVG(units) AS avg_daily_demand,
        STDDEV_POP(units) AS std_daily_demand
    FROM (
        SELECT *
        FROM {sales}
        UNPIVOT (
            units FOR day_id IN ({day_list})
        )
    ) AS u
    GROUP BY item_id, store_id, cat_id
),
ranked AS (
    SELECT *,
        SUM(training_units) OVER (
            ORDER BY training_units DESC, item_id, store_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_units,
        SUM(training_units) OVER () AS grand_total
    FROM demand
),
classified AS (
    SELECT *,
        100.0 * cumulative_units / NULLIF(grand_total, 0)
            AS cumulative_share_pct,
        CASE
            WHEN 100.0 * cumulative_units / NULLIF(grand_total, 0)
                <= 80 THEN 'A'
            WHEN 100.0 * cumulative_units / NULLIF(grand_total, 0)
                <= 95 THEN 'B'
            ELSE 'C'
        END AS abc_class,
        CASE
            WHEN avg_daily_demand <= 0 THEN 'Undefined'
            WHEN std_daily_demand / avg_daily_demand < 0.5
                THEN 'Stable'
            WHEN std_daily_demand / avg_daily_demand < 1.0
                THEN 'Moderate'
            ELSE 'High'
        END AS variability_class
    FROM ranked
)
SELECT *
FROM classified
"""

df = con.execute(query).fetchdf()

df.to_csv(
    "reports/exports/training_demand_classification.csv",
    index=False
)

print("\n--- TRAINING-ONLY ABC CLASSIFICATION ---")
print(
    df.groupby("abc_class")
      .agg(
          combinations=("item_id", "size"),
          units=("training_units", "sum")
      )
      .assign(
          share_pct=lambda x:
              100 * x["units"] / df["training_units"].sum()
      )
      .round(2)
      .to_string()
)

df_eval = con.execute("""
    SELECT *
    FROM read_parquet(
        'data/processed/demand_forecast_evaluation.parquet'
    )
""").fetchdf()

df_eval = df_eval.merge(
    df[[
        "item_id", "store_id", "cat_id",
        "abc_class", "variability_class"
    ]],
    on=["item_id", "store_id", "cat_id"],
    how="left",
    validate="one_to_one"
)

segments = (
    df_eval.groupby(["abc_class", "variability_class"])
    .agg(
        combinations=("item_id", "size"),
        actual_units=("actual_units", "sum"),
        forecast_units=("forecast_units", "sum"),
        mae=("absolute_error", "mean"),
        absolute_error=("absolute_error", "sum"),
        forecast_bias=("forecast_bias", "sum")
    )
    .reset_index()
)

segments["wape_pct"] = (
    100 * segments["absolute_error"] /
    segments["actual_units"].replace(0, float("nan"))
)

segments.to_csv(
    "reports/exports/forecast_segment_performance_training_only.csv",
    index=False
)

print("\n--- HOLDOUT PERFORMANCE BY TRAINING-ONLY SEGMENT ---")
print(
    segments.drop(columns="absolute_error")
    .round(2)
    .to_string(index=False)
)

con.close()