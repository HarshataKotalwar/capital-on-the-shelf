# Data Dictionary

## 1. Overview

This document describes the source datasets, important fields and analytical outputs used in **Capital on the Shelf — Inventory Allocation & Working Capital Optimisation**.

The project uses the Walmart M5 Forecasting dataset and produces processed datasets, demand metrics, forecast evaluations and inventory allocation scenario results.

## 2. Source Datasets

### 2.1 `sales_train_validation.csv`

Contains historical daily unit sales for individual products at individual Walmart stores.

| Field             | Description                                                               |
| ----------------- | ------------------------------------------------------------------------- |
| `id`              | Unique identifier for a product-store series.                             |
| `item_id`         | Product identifier.                                                       |
| `dept_id`         | Department identifier.                                                    |
| `cat_id`          | Product category identifier.                                              |
| `store_id`        | Store identifier.                                                         |
| `state_id`        | State identifier associated with the store.                               |
| `d_1` to `d_1913` | Daily unit sales observations, represented by sequential day identifiers. |

**Grain:** One row per product-store combination.

**Use in the project:** Historical demand analysis, aggregation, ABC classification and demand forecasting.

### 2.2 `calendar.csv`

Provides calendar information corresponding to the sequential daily identifiers in the sales dataset.

| Field          | Description                                                                 |
| -------------- | --------------------------------------------------------------------------- |
| `date`         | Calendar date corresponding to the daily observation.                       |
| `wm_yr_wk`     | Walmart year-week identifier.                                               |
| `weekday`      | Name of the day of the week.                                                |
| `wday`         | Numeric weekday identifier.                                                 |
| `month`        | Calendar month number.                                                      |
| `year`         | Calendar year.                                                              |
| `event_name_1` | First event name, when available.                                           |
| `event_type_1` | Event category for the first event.                                         |
| `event_name_2` | Second event name, when available.                                          |
| `event_type_2` | Event category for the second event.                                        |
| `snap_CA`      | SNAP indicator for California.                                              |
| `snap_TX`      | SNAP indicator for Texas.                                                   |
| `snap_WI`      | SNAP indicator for Wisconsin.                                               |
| `d`            | Sequential day identifier used to map sales observations to calendar dates. |

**Grain:** One row per calendar day.

**Use in the project:** Date mapping, monthly aggregation, trend analysis and seasonality analysis.

### 2.3 `sell_prices.csv`

Contains weekly selling prices for products at individual stores.

| Field        | Description                                                    |
| ------------ | -------------------------------------------------------------- |
| `store_id`   | Store identifier.                                              |
| `item_id`    | Product identifier.                                            |
| `wm_yr_wk`   | Walmart year-week identifier.                                  |
| `sell_price` | Selling price of the product for the specified store and week. |

**Grain:** One row per product-store-week combination.

**Use in the project:** Price analysis, latest available price selection and hypothetical inventory economics.

## 3. Processed Datasets

The following processed Parquet files are generated during the analytical workflow.

### 3.1 `product_store_demand.parquet`

Contains demand metrics aggregated at the product-store level.

| Logical field      | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| Product identifier | Identifies the product being analysed.                       |
| Store identifier   | Identifies the store associated with the product.            |
| Historical demand  | Aggregated historical sales used for product-store analysis. |
| Demand metrics     | Derived measures describing product-store demand behaviour.  |

**Grain:** One record per product-store combination.

**Use:** Product demand analysis, classification and inventory planning.

### 3.2 `daily_demand_by_store_category.parquet`

Contains daily sales aggregated at the store-category level.

| Logical field | Description                                                       |
| ------------- | ----------------------------------------------------------------- |
| Date          | Calendar date of the observation.                                 |
| Store         | Store associated with the demand observation.                     |
| Category      | Product category being analysed.                                  |
| Daily demand  | Total units sold for the store-category combination on that date. |

**Grain:** One record per date-store-category combination.

**Use:** Category-level demand trends and time-series analysis.

### 3.3 `demand_forecast_evaluation.parquet`

Contains product-store-level forecast estimates and holdout-period evaluation information.

| Logical field            | Description                                                                         |
| ------------------------ | ----------------------------------------------------------------------------------- |
| Product-store identifier | Identifies the series being forecast.                                               |
| Actual demand            | Observed demand during the holdout period.                                          |
| Forecast demand          | Estimated demand over the forecast horizon.                                         |
| Forecast error           | Difference between forecast and actual demand, based on the evaluation calculation. |
| Forecast metrics         | Measures used to assess forecast performance.                                       |

**Grain:** One record per evaluated product-store combination.

**Use:** Forecast evaluation and inventory requirement estimation.

The exact physical column names should be read from the Parquet schema when using the file programmatically.

## 4. Classification and Forecasting Concepts

| Term               | Description                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------- |
| ABC classification | Segmentation of products based on cumulative historical unit-demand contribution.                 |
| A-class            | Products with the highest cumulative contribution to historical unit demand.                      |
| B-class            | Products with an intermediate cumulative contribution.                                            |
| C-class            | Products with the remaining cumulative contribution.                                              |
| Training period    | Historical observations used to develop the baseline forecast and training-based classification.  |
| Holdout period     | A reserved period used to evaluate forecast accuracy.                                             |
| Forecast horizon   | The future period for which demand is estimated; 28 days in this project.                         |
| MAE                | Mean Absolute Error; average absolute difference between actual and forecast demand.              |
| WAPE               | Weighted Absolute Percentage Error; total absolute forecast error divided by total actual demand. |
| Forecast bias      | Difference between total forecast demand and total actual demand.                                 |

## 5. Inventory Economics Fields

| Field or concept                | Description                                                                                                                                   |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Selling price                   | Latest available selling price used as the scenario's price reference.                                                                        |
| Procurement cost ratio          | Assumed proportion of selling price used to estimate procurement cost; 60% in this project.                                                   |
| Estimated unit procurement cost | Selling price multiplied by the assumed procurement cost ratio.                                                                               |
| Forecast units required         | Forecast demand rounded up to whole units for the purchasing scenario.                                                                        |
| Full purchasing requirement     | Estimated cost of purchasing all forecast units required across the analysed product-store combinations.                                      |
| Budget share                    | Fraction of the full purchasing requirement available to an allocation scenario.                                                              |
| Budget                          | Amount of purchasing capital available in a scenario.                                                                                         |
| Purchased units                 | Total whole units allocated under a scenario.                                                                                                 |
| Spend                           | Estimated procurement expenditure for allocated units.                                                                                        |
| Unused budget                   | Available budget remaining after allocation.                                                                                                  |
| Budget utilisation              | Proportion of the available budget spent.                                                                                                     |
| Forecast demand coverage        | Proportion of forecast unit requirements covered by allocated units.                                                                          |
| Excess units                    | Allocated units beyond forecast requirements, if permitted by the model. In the current model, purchases are capped at forecast requirements. |
| Excess inventory cost           | Estimated procurement cost of excess units, if any.                                                                                           |
| Estimated revenue               | Hypothetical selling revenue based on allocated forecast units and the relevant selling prices.                                               |
| Estimated gross margin          | Estimated revenue less assumed procurement cost. It excludes other operating expenses.                                                        |

## 6. Allocation Scenario Outputs

### 6.1 `allocation_scenario_comparison.csv`

Contains the aggregate results of the proportional and ABC-prioritised allocation scenarios.

| Field                        | Description                                                         |
| ---------------------------- | ------------------------------------------------------------------- |
| `budget_share`               | Budget available as a proportion of the estimated full requirement. |
| `budget`                     | Estimated amount of capital available.                              |
| `strategy`                   | Allocation policy used in the scenario.                             |
| `spend`                      | Estimated purchasing expenditure.                                   |
| `unused_budget`              | Amount of the budget not spent.                                     |
| `budget_utilisation_pct`     | Percentage of the budget utilised.                                  |
| `purchased_units`            | Total allocated units.                                              |
| `forecast_units_covered_pct` | Percentage of forecast demand covered.                              |
| `excess_units`               | Units allocated beyond the forecast requirement.                    |
| `excess_inventory_cost`      | Estimated cost of excess units.                                     |
| `estimated_revenue`          | Scenario-based revenue estimate.                                    |
| `estimated_gross_margin`     | Scenario-based gross margin estimate.                               |

### 6.2 `allocation_by_abc_class.csv`

Contains the allocation results broken down by ABC class.

| Concept             | Description                                                 |
| ------------------- | ----------------------------------------------------------- |
| Budget scenario     | The available purchasing budget level.                      |
| Allocation strategy | Proportional or ABC-prioritised allocation.                 |
| ABC class           | A, B or C.                                                  |
| Class coverage      | Forecast demand coverage for the specified class.           |
| Allocated quantity  | Quantity allocated to the class.                            |
| Class expenditure   | Estimated purchasing expenditure associated with the class. |

The class-level outputs help explain how the two allocation strategies distribute capital across demand segments.

## 7. Other Analytical Exports

| File                                             | Description                                                                    |
| ------------------------------------------------ | ------------------------------------------------------------------------------ |
| `category_performance.csv`                       | Historical sales performance summarised by product category.                   |
| `store_performance.csv`                          | Historical sales performance summarised by store.                              |
| `monthly_sales_trend.csv`                        | Monthly sales trend results.                                                   |
| `monthly_sales_trend_complete.csv`               | Monthly trend results restricted to complete months.                           |
| `monthly_seasonality.csv`                        | Monthly seasonal indices and related summaries.                                |
| `forecast_segment_performance.csv`               | Forecast evaluation summarised across demand segments.                         |
| `forecast_segment_performance_training_only.csv` | Forecast evaluation by segments defined using training-period information.     |
| `latest_available_prices.csv`                    | Latest available price reference for each relevant product-store combination.  |
| `training_demand_classification.csv`             | Product-store demand classifications derived from training-period information. |

## 8. Units and Conventions

| Measure            | Unit or convention                        |
| ------------------ | ----------------------------------------- |
| Sales              | Whole units                               |
| Forecast demand    | Units over the specified forecast horizon |
| Selling price      | Dataset currency                          |
| Procurement cost   | Estimated currency amount                 |
| Budget             | Estimated currency amount                 |
| WAPE               | Percentage                                |
| Budget utilisation | Percentage                                |
| Forecast coverage  | Percentage                                |
| Seasonal index     | Reference average of 100                  |

The original M5 dataset uses Walmart's historical selling-price data. Financial amounts in the scenario outputs are expressed in the same currency as the source prices.

## 9. Important Interpretation Notes

* Historical sales represent recorded sales, not necessarily unconstrained customer demand.
* Forecast demand is an estimate and is subject to forecasting error.
* ABC classification is based on unit-demand contribution rather than revenue or profit.
* Procurement cost is hypothetical because actual supplier costs are not provided.
* Forecast demand coverage is a modelled quantity measure, not verified customer service or fulfilment.
* Estimated revenue and gross margin are scenario estimates and exclude other operating expenses.
* Allocation results should be interpreted alongside the assumptions and limitations documented in the methodology.
