# Capital on the Shelf

### Inventory Allocation & Working Capital Optimisation

**Capital on the Shelf** is a business and decision analytics project that explores how retailers can allocate limited purchasing budgets across products using historical demand, demand forecasts and ABC classification.

The project uses Walmart's M5 Forecasting dataset to examine how different inventory allocation strategies affect forecast demand coverage and the utilisation of available purchasing budgets.

## Business Problem

Retailers often operate with limited purchasing budgets and must decide how to distribute capital across products. Insufficient inventory can lead to potential lost sales, while excessive purchasing can tie up working capital.

This project investigates the following question:

**How should a retailer allocate a constrained inventory budget across products to maximise forecast demand coverage while making effective use of available capital?**

## Objectives

* Analyse historical product and store-level demand.
* Identify demand patterns, trends and seasonality.
* Develop a short-term demand forecasting baseline.
* Classify products using ABC analysis.
* Estimate hypothetical inventory purchasing requirements.
* Compare proportional and ABC-prioritised allocation strategies under different budget constraints.
* Translate analytical findings into business recommendations.

## Dataset

The analysis uses the **M5 Forecasting dataset**, which contains Walmart historical sales, calendar and selling-price information.

| File                         | Description                                       |
| ---------------------------- | ------------------------------------------------- |
| `sales_train_validation.csv` | Historical daily sales at product and store level |
| `calendar.csv`               | Calendar dates, events and related information    |
| `sell_prices.csv`            | Weekly selling prices by product and store        |

The original datasets are not included in this repository because of their size. Download the M5 Forecasting data from Kaggle and place the three files in `data/raw/` before reproducing the analysis.

## Analytical Approach

1. **Data validation and profiling:** Examine data quality, missing values, duplicates, date coverage and sales consistency.
2. **Exploratory data analysis:** Study category performance, store-level demand, monthly trends and seasonality.
3. **Demand analysis:** Aggregate historical sales and calculate product-store demand metrics.
4. **ABC classification:** Segment products based on their historical contribution to demand, using training-period information.
5. **Demand forecasting:** Establish a 28-day baseline forecast using recent historical demand and evaluate it against a holdout period.
6. **Inventory economics:** Estimate hypothetical purchasing requirements using an assumed procurement cost equal to 60% of the selling price.
7. **Scenario analysis:** Compare proportional and ABC-prioritised allocation at 50%, 70% and 90% of the estimated purchasing requirement.

## Key Findings

* Food products account for approximately **68.63%** of historical unit sales, followed by Household at 22.04% and Hobbies at 9.32%.
* August recorded the highest complete-month seasonal index (107.01), while February recorded the lowest (94.27).
* The 28-day demand forecasting baseline achieved a **28.54% WAPE** on the holdout period.
* The estimated full purchasing requirement under the assumed cost model was approximately **$2.20 million**.

### Inventory Allocation Scenarios

The project compares proportional allocation with an ABC-prioritised policy that allocates available capital to A-class products first, followed by B and C.

| Budget | Proportional coverage | ABC-prioritised coverage |
| ------ | --------------------: | -----------------------: |
| 50%    |                50.00% |                   63.43% |
| 70%    |                69.99% |                   80.58% |
| 90%    |                89.98% |                   94.39% |

At the 70% budget level, ABC prioritisation covers 80.58% of forecast demand, compared with 69.99% under proportional allocation. This illustrates how prioritising products by historical demand contribution changes the distribution of limited capital.

These figures represent modelled forecast coverage, not verified customer demand fulfilment.

## Dashboard

The project includes an interactive Streamlit dashboard for exploring the demand analysis and inventory allocation scenarios.

To run it locally:

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## Technology Stack

* **Python:** Data processing, analysis and scenario modelling
* **Pandas & NumPy:** Data manipulation and numerical analysis
* **DuckDB:** Analytical data processing
* **Matplotlib, Seaborn & Plotly:** Data visualisation
* **Streamlit:** Interactive dashboard
* **SQL:** Data quality and demand analysis

## Project Structure

```text
capital-on-the-shelf/
├── dashboard/
│   ├── app.py
│   └── README.md
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── docs/
│   ├── Business_Recommendations.md
│   ├── Data_Dictionary.md
│   ├── Data_Quality_Report.md
│   ├── Methodology.md
│   └── Project_Charter.md
├── notebooks/
│   ├── 01_data_profiling.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   └── 03_demand_analysis.ipynb
├── reports/
│   ├── exports/
│   └── figures/
├── sql/
├── src/
├── tests/
├── .gitignore
└── requirements.txt
```

## Assumptions and Limitations

* Procurement cost is assumed to be 60% of the selling price; actual supplier costs are not available.
* Historical demand is used as a proxy for future requirements.
* The ABC-prioritised approach is a policy heuristic, not a mathematically proven optimal solution.
* The analysis does not incorporate verified opening inventory, supplier lead times, replenishment constraints, holding costs or actual stockout records.
* Estimated revenue and gross margin are scenario-based figures, not observed financial outcomes.

Consequently, the results should be interpreted as an exploratory decision-support analysis rather than a validated operational inventory optimisation system.

## Author

**Harshata Kotalwar**

Business Analytics | Data Analytics | AI/ML
## 🚀 Live Demo

Explore the interactive dashboard:

**[Open Capital on the Shelf Dashboard](https://harshatakotalwar-capital-on-the-shelf-dashboardapp-bnaanb.streamlit.app/)**