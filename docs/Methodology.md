# Methodology

## 1. Overview

This document describes the analytical methodology used in **Capital on the Shelf — Inventory Allocation & Working Capital Optimisation**.

The project uses historical Walmart sales data from the M5 Forecasting dataset to analyse demand, develop a short-term forecasting baseline, classify products and compare inventory allocation strategies under budget constraints.

The methodology consists of the following stages:

1. Data collection and validation
2. Data preparation and aggregation
3. Exploratory demand analysis
4. ABC demand classification
5. Demand forecasting and evaluation
6. Inventory purchasing requirement estimation
7. Budget-constrained allocation scenarios
8. Business interpretation

## 2. Data Sources

The analysis uses three files from the M5 Forecasting dataset.

| Dataset                      | Purpose                                       |
| ---------------------------- | --------------------------------------------- |
| `sales_train_validation.csv` | Historical daily product-store sales          |
| `calendar.csv`               | Date mapping, calendar information and events |
| `sell_prices.csv`            | Weekly product-store selling prices           |

The sales dataset contains 30,490 product-store combinations and 1,913 daily observations per combination, covering the period from January 29, 2011, to April 24, 2016.

The calendar extends to June 19, 2016. The price dataset provides weekly selling prices for the relevant product-store combinations.

## 3. Data Validation and Preparation

The initial stage involved inspecting the structure, completeness and consistency of the source datasets.

The following checks were performed:

* Dataset dimensions and column types
* Missing values and duplicate records
* Date coverage and alignment
* Negative and non-integer sales values
* Product and store coverage in the price dataset
* Uniqueness of store-item-week price records

Sales data was reshaped and aggregated for demand analysis. The daily sales records were mapped to calendar dates and combined with relevant product, store and price information where required.

Daily demand was aggregated at the store-category level to examine broad demand patterns. Product-store-level demand metrics were also generated for forecasting and inventory analysis.

## 4. Exploratory Data Analysis

Exploratory analysis was conducted to understand demand behaviour across products, categories, stores and time.

The analysis included:

* Category-level sales contribution
* Store-level sales performance
* Monthly sales trends
* Monthly demand seasonality
* Product-store demand distributions
* Recent demand patterns

Monthly seasonality was examined using a seasonal index calculated from complete calendar months. The overall monthly average serves as the reference level of 100. Values above 100 indicate demand above that reference, while values below 100 indicate demand below it.

Incomplete months were excluded from the complete-month seasonality comparison to avoid partial-period distortion.

## 5. ABC Demand Classification

ABC analysis was used to segment product-store combinations according to their contribution to historical unit demand.

Products were ranked by their historical demand contribution and grouped into A, B and C classes.

The classification is intended to distinguish products with different levels of demand importance:

* **A:** Products contributing the largest share of cumulative demand.
* **B:** Products contributing an intermediate share.
* **C:** Products contributing the remaining share.

The classification used for forecasting and allocation scenarios is based on training-period demand information to reduce the risk of information leakage from the holdout period.

ABC classification in this project is based on unit demand contribution, not profitability, strategic importance or supplier risk.

## 6. Demand Forecasting

A simple recent-demand baseline was developed to estimate demand over a 28-day forecast horizon.

### Training and holdout periods

The forecasting evaluation used:

* Training period: 1,885 days
* Holdout period: 28 days

The final 28 days were reserved for evaluation. Forecast estimates were generated using information from the training period only.

### Baseline forecasting method

For each product-store combination, average daily demand was calculated over the final 28 days of the training period.

The daily average was multiplied by the 28-day forecast horizon to estimate total demand over the holdout period.

The forecast was evaluated against actual sales in the holdout period.

### Evaluation metrics

The following metrics were used:

**Mean Absolute Error (MAE)**

MAE measures the average absolute difference between forecast and actual demand.

**Weighted Absolute Percentage Error (WAPE)**

WAPE measures the total absolute forecast error relative to total actual demand. It provides an aggregate measure of forecast accuracy.

**Forecast bias**

Forecast bias measures the difference between total forecast demand and total actual demand. Negative bias indicates aggregate underforecasting.

### Baseline evaluation results

| Metric                            |          Result |
| --------------------------------- | --------------: |
| Forecast horizon                  |         28 days |
| Actual holdout demand             | 1,183,626 units |
| Forecast demand                   | 1,176,067 units |
| MAE per product-store combination |     11.08 units |
| WAPE                              |          28.54% |
| Aggregate forecast bias           |    -7,559 units |

The baseline provides a reference forecast for the allocation scenarios. It is not a production-grade forecasting system.

## 7. Inventory Economics

The forecast demand estimates were translated into hypothetical inventory purchasing requirements.

The latest available selling price for each product-store combination, using information available by the end of the training period, was used as the price reference.

Because actual procurement costs were unavailable, procurement cost was assumed to be 60% of the selling price.

The estimated unit procurement cost was therefore:

`Unit procurement cost = Selling price × 0.60`

The full estimated purchasing requirement was calculated using the forecast units required for each product-store combination, rounded up to whole units.

The resulting estimated purchasing requirement was approximately **$2,200,609.41**.

This amount is a scenario assumption based on forecast demand and estimated procurement costs, rather than an observed retailer expenditure.

## 8. Budget-Constrained Allocation

Two allocation strategies were compared under three budget levels: 50%, 70% and 90% of the estimated full purchasing requirement.

### Strategy 1: Proportional allocation

The available purchasing budget is distributed proportionally across product requirements, based on their estimated purchasing costs.

This approach spreads the budget across the product portfolio instead of explicitly prioritising ABC classes.

### Strategy 2: ABC-prioritised allocation

The available budget is allocated in the following order:

1. A-class products
2. B-class products
3. C-class products

Within each class, products are prioritised by higher forecast demand.

Purchases are capped at the estimated forecast requirement for each product-store combination. The model does not intentionally purchase quantities beyond those requirements.

### Budget scenarios

| Scenario      | Budget share | Approximate budget |
| ------------- | -----------: | -----------------: |
| Low budget    |          50% |         $1,100,305 |
| Medium budget |          70% |         $1,540,427 |
| High budget   |          90% |         $1,980,548 |

### Evaluation measures

The strategies were compared using:

* Budget utilisation
* Purchased units
* Forecast demand coverage
* Coverage by ABC class
* Estimated revenue
* Estimated gross margin
* Unused budget
* Excess inventory

Forecast demand coverage is calculated as the proportion of forecast units covered by the allocated purchase quantities.

The scenario model caps purchases at forecast requirements, so excess inventory is zero by construction. This should not be interpreted as evidence that actual inventory would never become excessive.

## 9. Interpretation

The scenarios illustrate how different allocation policies distribute limited purchasing capital.

Proportional allocation spreads coverage more evenly across product requirements. ABC prioritisation concentrates available capital on products with higher historical demand contribution.

At a 70% budget, proportional allocation covers approximately 69.99% of forecast demand, while ABC prioritisation covers approximately 80.58%.

Because the same procurement-cost assumption is applied to both strategies, their estimated financial returns are nearly identical at comparable spending levels. The main difference is the distribution of forecast coverage, rather than demonstrated profitability.

## 10. Limitations

The methodology has several limitations:

* Historical sales may not represent unconstrained customer demand, particularly where stockouts occurred.
* The forecast is a simple recent-demand baseline and may not capture complex seasonal or promotional patterns.
* The 60% procurement-cost ratio is hypothetical.
* Actual opening inventory, supplier lead times, order minimums and replenishment constraints are not modelled.
* Holding costs, spoilage, markdowns and actual stockout costs are unavailable.
* ABC classes are based on unit contribution rather than profit or business criticality.
* Scenario coverage represents forecast demand coverage, not confirmed customer fulfilment.
* The allocation strategy is a heuristic and is not mathematically proven to be globally optimal.

## 11. Conclusion

The methodology provides a structured framework for examining the relationship between demand forecasting, inventory prioritisation and limited purchasing budgets.

By combining demand analysis, ABC classification and scenario modelling, the project demonstrates how analytical methods can support inventory allocation decisions. The results are exploratory and should be validated against real inventory and cost data before operational implementation.
