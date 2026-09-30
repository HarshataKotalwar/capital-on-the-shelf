# Business Recommendations

## 1. Executive Summary

**Capital on the Shelf** examines how retailers can distribute limited purchasing budgets across products using historical demand, a short-term forecast and ABC classification.

The analysis compares two inventory allocation strategies:

* Proportional allocation
* ABC-prioritised allocation

The strategies were evaluated at 50%, 70% and 90% of the estimated full purchasing requirement of approximately $2.20 million.

The results demonstrate that the choice of allocation policy changes how forecast demand is covered when purchasing capital is constrained. ABC prioritisation concentrates available funds on higher-demand products, while proportional allocation spreads coverage more evenly.

These findings can inform inventory planning, but actual operational decisions require additional information about inventory on hand, supplier costs and service-level requirements.

## 2. Key Business Findings

### 2.1 Demand is concentrated across categories

Historical unit sales are distributed unevenly across the three product categories.

| Category  | Share of historical units |
| --------- | ------------------------: |
| Foods     |                    68.63% |
| Household |                    22.04% |
| Hobbies   |                     9.32% |

Foods represents more than two-thirds of historical unit demand. This makes category-level demand composition an important consideration when planning purchasing budgets.

However, a high share of unit sales does not necessarily imply a proportionally high share of revenue or profit.

### 2.2 Demand shows monthly seasonality

The complete-month seasonal analysis identified the following results:

| Month    | Seasonal index |
| -------- | -------------: |
| August   |         107.01 |
| February |          94.27 |

An index above 100 indicates demand above the reference average, while an index below 100 indicates demand below it.

The observed monthly variation suggests that inventory planning should consider time-dependent demand patterns rather than relying exclusively on annual averages.

### 2.3 Forecast accuracy has room for improvement

The 28-day recent-demand baseline achieved a WAPE of 28.54% on the holdout period.

| Metric          |                                    Result |
| --------------- | ----------------------------------------: |
| Actual demand   |                           1,183,626 units |
| Forecast demand |                           1,176,067 units |
| MAE             | 11.08 units per product-store combination |
| WAPE            |                                    28.54% |
| Aggregate bias  |                              -7,559 units |

The baseline provides a useful benchmark, but the observed error indicates that forecasts should be treated as estimates rather than exact future requirements.

## 3. Inventory Allocation Scenario Results

The estimated full purchasing requirement was approximately $2,200,609.41.

The two allocation strategies were evaluated under three budget constraints.

| Budget | Proportional coverage | ABC-prioritised coverage |
| ------ | --------------------: | -----------------------: |
| 50%    |                50.00% |                   63.43% |
| 70%    |                69.99% |                   80.58% |
| 90%    |                89.98% |                   94.39% |

### 3.1 Low-budget scenario: 50%

With approximately $1.10 million available:

* Proportional allocation covers 50.00% of forecast demand.
* ABC prioritisation covers 63.43%.
* Under ABC prioritisation, A-class forecast demand coverage is 86.35%, while B- and C-class coverage is zero.

The scenario demonstrates how prioritisation can concentrate limited purchasing capital on A-class products. It also reveals the potential trade-off: lower-priority products may receive no allocation.

### 3.2 Medium-budget scenario: 70%

With approximately $1.54 million available:

* Proportional allocation covers 69.99% of forecast demand.
* ABC prioritisation covers 80.58%.
* ABC prioritisation covers 100% of A-class demand and 39.50% of B-class demand, while C-class coverage is approximately zero.

This scenario illustrates the difference between distributing purchasing capital broadly and prioritising it according to historical demand contribution.

### 3.3 High-budget scenario: 90%

With approximately $1.98 million available:

* Proportional allocation covers 89.98% of forecast demand.
* ABC prioritisation covers 94.39%.
* ABC prioritisation covers all A- and B-class forecast requirements and 34.12% of C-class requirements.

As the budget increases, the ABC-prioritised strategy extends coverage to lower-priority classes after meeting higher-priority requirements.

## 4. Business Recommendations

### Recommendation 1: Use ABC classification as a planning input

ABC classification can help planners distinguish products by historical demand contribution.

It can be used as an input to purchasing reviews, budget allocation discussions and inventory prioritisation.

However, ABC class should not be the only consideration. Products with low historical unit contribution may still be strategically important or have high margins.

### Recommendation 2: Evaluate allocation policies against service requirements

The allocation scenarios show that proportional and ABC-prioritised policies distribute forecast coverage differently.

Before applying either policy operationally, retailers should define service-level requirements for different products and categories.

For example, a retailer may wish to protect essential products from being excluded entirely, even when their historical unit contribution is low.

### Recommendation 3: Use forecast uncertainty in purchasing decisions

The baseline forecast achieved a WAPE of 28.54%. This level of forecast error makes it important to review uncertainty when determining purchase quantities.

A practical next step would be to evaluate alternative forecasting methods and compare their errors across product categories and ABC classes.

Purchase quantities should also be reviewed regularly as new sales information becomes available.

### Recommendation 4: Incorporate actual inventory before making purchase decisions

The current scenarios estimate purchasing requirements using forecast demand. They do not deduct verified opening inventory or account for goods already on order.

A production-oriented allocation model should incorporate:

* Current inventory on hand
* Confirmed purchase orders
* Supplier lead times
* Replenishment frequency
* Minimum order quantities
* Product shelf life, where relevant

This would make the purchasing recommendations more closely reflect actual requirements.

### Recommendation 5: Validate procurement costs and financial assumptions

The analysis assumes procurement costs equal 60% of selling prices.

This is a modelling assumption rather than a verified supplier cost. Consequently, the estimated purchasing requirements and financial outcomes should be treated as illustrative.

Before using the model for financial planning, replace the assumed cost ratio with actual procurement costs and incorporate relevant logistics, holding and markdown expenses.

### Recommendation 6: Monitor category-level demand patterns

The observed category contributions and monthly seasonality can help identify areas for further investigation.

Demand planning should consider changes in category composition, seasonal variation, events and promotional activity where reliable data is available.

Historical patterns should be re-evaluated periodically rather than treated as permanent relationships.

## 5. Financial Interpretation

The two allocation strategies produce nearly identical estimated revenue and gross margin at comparable spending levels under the current assumptions.

This is because the model uses the same selling-price and procurement-cost assumptions for both strategies, and the allocation changes which forecast units are covered rather than the assumed unit economics.

Therefore, the higher forecast coverage under ABC prioritisation should not be interpreted as demonstrated higher profitability.

A financial comparison would require additional evidence, including actual margins, stockout costs, holding costs and the economic value of demand served.

## 6. Suggested Future Improvements

The following improvements would extend the analysis:

1. Compare more advanced forecasting methods, including seasonal and machine-learning approaches.
2. Incorporate actual inventory on hand and incoming orders.
3. Introduce product-specific procurement costs and gross margins.
4. Model holding costs, markdowns and stockout penalties.
5. Add supplier lead-time and minimum-order constraints.
6. Compare allocation strategies using service-level and profit-based objectives.
7. Conduct sensitivity analysis on procurement costs and forecast uncertainty.
8. Validate the allocation model using historical inventory outcomes where available.

## 7. Conclusion

The scenario analysis illustrates how inventory allocation policies can change forecast demand coverage under purchasing-budget constraints.

Proportional allocation distributes coverage more broadly, whereas ABC prioritisation focuses capital on products with greater historical demand contribution.

Neither approach is universally suitable without considering the retailer's service objectives, inventory position and actual cost structure.

The findings provide a foundation for more detailed inventory planning and future optimisation work.
