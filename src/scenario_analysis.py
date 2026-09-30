
from pathlib import Path
import math

import duckdb
import numpy as np
import pandas as pd


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
COST_RATIO = 0.60
BUDGET_SHARES = [0.50, 0.70, 0.90]


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

forecast = duckdb.query(f"""
    SELECT *
    FROM read_parquet(
        '{(ROOT / "data/processed/demand_forecast_evaluation.parquet").as_posix()}'
    )
""").to_df()

prices = pd.read_csv(
    ROOT / "reports/exports/latest_available_prices.csv"
)

classes = pd.read_csv(
    ROOT / "reports/exports/training_demand_classification.csv"
)


# --------------------------------------------------
# 3. VALIDATE INPUT COLUMNS
# --------------------------------------------------

required = {
    "forecast": {"item_id", "store_id", "forecast_units"},
    "prices": {"item_id", "store_id", "sell_price"},
    "classes": {"item_id", "store_id", "abc_class"},
}

for name, data in [
    ("forecast", forecast),
    ("prices", prices),
    ("classes", classes),
]:
    missing = required[name] - set(data.columns)
    if missing:
        raise ValueError(
            f"{name} is missing columns: {sorted(missing)}"
        )


# --------------------------------------------------
# 4. MERGE INPUT DATA
# --------------------------------------------------

df = (
    forecast[["item_id", "store_id", "forecast_units"]]
    .merge(
        prices[["item_id", "store_id", "sell_price"]],
        on=["item_id", "store_id"],
        validate="one_to_one",
    )
    .merge(
        classes[["item_id", "store_id", "abc_class"]],
        on=["item_id", "store_id"],
        validate="one_to_one",
    )
)

if df.isna().any().any():
    raise ValueError("Missing values found after merging inputs.")

if (df["sell_price"] <= 0).any():
    raise ValueError("Selling prices must be positive.")

if (df["forecast_units"] < 0).any():
    raise ValueError("Forecast demand cannot be negative.")

if not df["abc_class"].isin(["A", "B", "C"]).all():
    raise ValueError("Unexpected ABC classification found.")

df = df.reset_index(drop=True)


# --------------------------------------------------
# 5. WHOLE-UNIT INVENTORY REQUIREMENT
# --------------------------------------------------

# Round forecast requirements up to whole units.
df["max_units"] = np.ceil(
    df["forecast_units"]
).astype(int)

# Hypothetical procurement cost: 60% of selling price.
df["unit_cost"] = df["sell_price"] * COST_RATIO

df["full_requirement"] = (
    df["max_units"] * df["unit_cost"]
)

full_requirement = float(df["full_requirement"].sum())

if full_requirement <= 0:
    raise ValueError(
        "Full purchasing requirement must be positive."
    )

print(
    f"Full estimated purchasing requirement: "
    f"${full_requirement:,.2f}"
)


# --------------------------------------------------
# 6. PROPORTIONAL ALLOCATION
# --------------------------------------------------

def proportional_allocation(data, budget):
    """
    Allocate budget to achieve approximately equal
    forecast coverage across product-store combinations.
    """
    result = np.zeros(len(data), dtype=int)

    costs = data["unit_cost"].to_numpy()
    capacities = data["max_units"].to_numpy()
    forecasts = data["forecast_units"].to_numpy()

    share = min(1.0, budget / full_requirement)
    targets = forecasts * share

    result = np.minimum(
        np.floor(targets).astype(int),
        capacities,
    )

    remaining = budget - float(np.dot(result, costs))

    # Use remaining funds for affordable additional units,
    # favouring products closest to their proportional target.
    fractions = targets - np.floor(targets)
    order = np.argsort(-fractions, kind="stable")

    for i in order:
        if (
            result[i] < capacities[i]
            and costs[i] <= remaining + 1e-9
        ):
            result[i] += 1
            remaining -= costs[i]

    return result


# --------------------------------------------------
# 7. ABC-PRIORITISED ALLOCATION
# --------------------------------------------------

def abc_allocation(data, budget):
    """
    Allocate to A, then B, then C.
    Within each class, prioritise higher forecast demand.

    This is a policy heuristic, not a profit-optimal solution.
    """
    result = np.zeros(len(data), dtype=int)
    remaining = budget

    ordered = data.assign(
        abc_order=data["abc_class"].map(
            {"A": 0, "B": 1, "C": 2}
        )
    ).sort_values(
        ["abc_order", "forecast_units"],
        ascending=[True, False],
        kind="stable",
    )

    for idx, row in ordered.iterrows():
        affordable = math.floor(
            (remaining + 1e-9) / row["unit_cost"]
        )

        quantity = min(
            int(row["max_units"]),
            affordable,
        )

        position = data.index.get_loc(idx)
        result[position] = quantity

        remaining -= quantity * row["unit_cost"]

    return result


# --------------------------------------------------
# 8. EVALUATE AN ALLOCATION
# --------------------------------------------------

def evaluate(data, quantities, budget, strategy, share):
    units = np.asarray(quantities, dtype=int)

    # Use whole-unit requirements consistently.
    forecast_units = data["max_units"].to_numpy().astype(float)
    prices_array = data["sell_price"].to_numpy()
    costs = data["unit_cost"].to_numpy()

    # Units purchased that meet the rounded requirement.
    fulfilled = np.minimum(units, forecast_units)

    # Purchased units above the rounded requirement.
    excess_units = np.maximum(units - forecast_units, 0)

    spend = float(np.dot(units, costs))
    excess_cost = float(np.dot(excess_units, costs))
    revenue = float(np.dot(fulfilled, prices_array))

    # Procurement cost is already included in spend.
    gross_margin = revenue - spend

    total_forecast = float(forecast_units.sum())

    summary = {
        "budget_share": share,
        "budget": budget,
        "strategy": strategy,
        "spend": spend,
        "unused_budget": budget - spend,
        "budget_utilisation_pct": (
            100 * spend / budget if budget > 0 else 0
        ),
        "purchased_units": int(units.sum()),
        "forecast_units_covered_pct": (
            100 * fulfilled.sum() / total_forecast
            if total_forecast > 0 else 0
        ),
        "excess_units": float(excess_units.sum()),
        "excess_inventory_cost": excess_cost,
        "estimated_revenue": revenue,
        "estimated_gross_margin": gross_margin,
    }

    # Detailed ABC-class calculations.
    by_class = data[
        ["abc_class", "sell_price"]
    ].copy()

    by_class["forecast_units"] = forecast_units
    by_class["allocated_units"] = units
    by_class["fulfilled_units"] = fulfilled
    by_class["excess_units"] = excess_units

    by_class["procurement_spend"] = units * costs
    by_class["excess_inventory_cost"] = excess_units * costs
    by_class["estimated_revenue"] = fulfilled * prices_array

    by_class["strategy"] = strategy
    by_class["budget_share"] = share

    class_summary = (
        by_class.groupby(
            ["budget_share", "strategy", "abc_class"]
        )
        .agg(
            forecast_units=("forecast_units", "sum"),
            allocated_units=("allocated_units", "sum"),
            fulfilled_units=("fulfilled_units", "sum"),
            excess_units=("excess_units", "sum"),
            procurement_spend=("procurement_spend", "sum"),
            excess_inventory_cost=(
                "excess_inventory_cost", "sum"
            ),
            estimated_revenue=("estimated_revenue", "sum"),
        )
        .reset_index()
    )

    class_summary["coverage_pct"] = (
        100 * class_summary["fulfilled_units"]
        / class_summary["forecast_units"].replace(0, np.nan)
    )

    class_summary["coverage_pct"] = (
        class_summary["coverage_pct"].fillna(0)
    )

    return summary, class_summary


# --------------------------------------------------
# 9. RUN ALL BUDGET SCENARIOS
# --------------------------------------------------

summaries = []
class_summaries = []

for share in BUDGET_SHARES:
    budget = full_requirement * share

    for strategy, allocator in [
        ("Proportional", proportional_allocation),
        ("ABC-prioritised", abc_allocation),
    ]:
        quantities = allocator(df, budget)

        summary, class_summary = evaluate(
            df,
            quantities,
            budget,
            strategy,
            share,
        )

        summaries.append(summary)
        class_summaries.append(class_summary)


# --------------------------------------------------
# 10. CREATE RESULTS
# --------------------------------------------------

summary_df = pd.DataFrame(summaries)

class_df = pd.concat(
    class_summaries,
    ignore_index=True,
)


# --------------------------------------------------
# 11. VALIDATE RESULTS
# --------------------------------------------------

if len(summary_df) != len(BUDGET_SHARES) * 2:
    raise AssertionError(
        "Unexpected number of scenario results."
    )

if (
    summary_df["spend"] > summary_df["budget"] + 0.01
).any():
    raise AssertionError(
        "An allocation exceeded its budget."
    )

if (summary_df["excess_units"] < 0).any():
    raise AssertionError(
        "Negative excess inventory found."
    )

if not np.isfinite(
    summary_df.select_dtypes(include="number").to_numpy()
).all():
    raise AssertionError(
        "Non-finite scenario results found."
    )

if not np.allclose(
    summary_df["spend"] + summary_df["unused_budget"],
    summary_df["budget"],
    atol=0.01,
):
    raise AssertionError(
        "Budget reconciliation failed."
    )

if not np.allclose(
    summary_df["estimated_gross_margin"],
    summary_df["estimated_revenue"] - summary_df["spend"],
    atol=0.01,
):
    raise AssertionError(
        "Gross margin reconciliation failed."
    )


# --------------------------------------------------
# 12. EXPORT RESULTS
# --------------------------------------------------

out = ROOT / "reports/exports"
out.mkdir(parents=True, exist_ok=True)

summary_path = out / "allocation_scenario_comparison.csv"
class_path = out / "allocation_by_abc_class.csv"

summary_df.to_csv(summary_path, index=False)
class_df.to_csv(class_path, index=False)


# --------------------------------------------------
# 13. DISPLAY RESULTS
# --------------------------------------------------

print("\nALLOCATION SCENARIO COMPARISON")
print(summary_df.round(2).to_string(index=False))

print("\nALLOCATION BY ABC CLASS")
print(class_df.round(2).to_string(index=False))

print("\nSaved:")
print(summary_path)
print(class_path)

print("\nAll scenario validations passed.")