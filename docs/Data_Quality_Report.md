# Data Quality Report

## Project: Capital on the Shelf

### 1. Dataset Overview

The project uses the M5 Forecasting dataset, consisting of three primary files:

| File                       |   Records | Columns |
| -------------------------- | --------: | ------: |
| calendar.csv               |     1,969 |      14 |
| sales_train_validation.csv |    30,490 |   1,919 |
| sell_prices.csv            | 6,841,121 |       4 |

### 2. Structural Validation

* Calendar dates and day identifiers are unique, with no duplicates.
* All 1,913 daily sales columns are present.
* All 30,490 sales records have unique IDs and the expected structure.
* All sales day identifiers have corresponding entries in the calendar.
* No duplicate store-item-week price keys were found.
* No missing price keys or price values were found.

### 3. Sales Value Validation

A total of 58,327,370 daily sales observations were checked.

| Check                    |     Result |
| ------------------------ | ---------: |
| Missing sales values     |          0 |
| Negative sales values    |          0 |
| Non-integer sales values |          0 |
| Minimum daily sales      |          0 |
| Maximum daily sales      |        763 |
| Zero-sales observations  | 39,777,094 |

The sales data contains no missing, negative or fractional daily values. Zero sales are common and should not automatically be interpreted as stockouts.

### 4. Price Coverage

All 30,490 unique product-store combinations have at least one corresponding price record.

| Metric                             | Result |
| ---------------------------------- | -----: |
| Total product-store combinations   | 30,490 |
| Combinations with price records    | 30,490 |
| Combinations without price records |      0 |
| Overall product-store coverage     |   100% |

This check establishes the existence of price history for each product-store combination. It does not establish complete price availability for every week.

### 5. Data Quality Assessment

The initial structural and value-level checks have passed. No missing sales observations, invalid negative sales values or duplicate price keys were detected.

However, further checks are required for weekly price coverage, the selected analysis period and the suitability of sales data as a proxy for demand.

### 6. Limitations

* The dataset contains historical sales, not actual inventory-on-hand records.
* Observed zero sales do not establish that a product was out of stock.
* Selling prices are available, but procurement costs and inventory holding costs are not directly provided.
* Inventory allocation outcomes will therefore require clearly documented assumptions and scenario-based evaluation.

### 7. Conclusion

The dataset has passed the initial structural and sales-value validation checks. It is suitable for proceeding to exploratory demand analysis, subject to further assessment of price availability and the limitations identified above.
