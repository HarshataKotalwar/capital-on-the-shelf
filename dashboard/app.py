
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Capital on the Shelf | Business Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. THEME AND STYLING
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background-color: #f5f7fa;
        color: #172033;
    }

    [data-testid="stHeader"] {
        background-color: #f5f7fa;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5eaf1;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        color: #172033 !important;
        letter-spacing: -0.5px;
    }

    h1 {
        font-size: 2.3rem !important;
        font-weight: 800 !important;
    }

    h2 {
        font-size: 1.5rem !important;
        font-weight: 750 !important;
    }

    h3 {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }

    p, label {
        color: #445066;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    .hero {
        background: linear-gradient(115deg, #122b45, #1d4669);
        padding: 30px 34px;
        border-radius: 18px;
        margin: 8px 0 26px 0;
        color: white;
    }

    .hero h1 {
        color: #ffffff !important;
        margin: 0 0 8px 0;
    }

    .hero p {
        color: #d7e5f3 !important;
        font-size: 1rem;
        margin: 0;
        line-height: 1.7;
    }

    .eyebrow {
        color: #9cc9f0;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 1.7px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .section-label {
        color: #64748b;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5eaf1;
        border-radius: 13px;
        padding: 17px 19px;
        box-shadow: 0 2px 8px rgba(20, 40, 70, 0.035);
        min-height: 112px;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 0.84rem !important;
    }

    div[data-testid="stMetricValue"] {
        color: #172033 !important;
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
        font-size: 1.55rem !important;
    }

    .insight {
        background: #eaf4ff;
        border: 1px solid #c8e0fa;
        border-left: 5px solid #2474bc;
        border-radius: 11px;
        padding: 17px 20px;
        margin: 10px 0 20px 0;
    }

    .insight-title {
        color: #174c7c;
        font-weight: 800;
        font-size: 0.95rem;
        margin-bottom: 5px;
    }

    .insight p {
        color: #34516e;
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.65;
    }

    .note {
        background: #ffffff;
        border: 1px solid #e5eaf1;
        border-radius: 11px;
        padding: 14px 17px;
        color: #64748b;
        font-size: 0.83rem;
        line-height: 1.65;
        margin: 10px 0;
    }

    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
        border: 1px solid #e5eaf1;
        border-radius: 13px;
        padding: 8px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #e5eaf1;
        border-radius: 11px;
        overflow: hidden;
    }

    .footer {
        color: #94a3b8;
        font-size: 0.78rem;
        text-align: center;
        padding: 24px 0 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. PROJECT PATHS AND DATA
# ============================================================

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "reports" / "exports"

SCENARIO_FILE = EXPORTS / "allocation_scenario_comparison.csv"
ABC_FILE = EXPORTS / "allocation_by_abc_class.csv"


@st.cache_data
def load_data():
    scenarios = pd.read_csv(SCENARIO_FILE)
    abc = pd.read_csv(ABC_FILE)
    return scenarios, abc


try:
    scenarios, abc = load_data()

except FileNotFoundError as exc:
    st.error(
        f"Required file not found: {exc.filename}\n\n"
        "Ensure the allocation analysis has been run and "
        "the CSV files are in reports/exports/."
    )
    st.stop()

except Exception as exc:
    st.error(f"Unable to load the dashboard data: {exc}")
    st.stop()


# ============================================================
# 4. VALIDATE DATA
# ============================================================

scenario_required = {
    "budget_share",
    "budget",
    "strategy",
    "spend",
    "unused_budget",
    "budget_utilisation_pct",
    "purchased_units",
    "forecast_units_covered_pct",
    "excess_units",
    "excess_inventory_cost",
    "estimated_revenue",
    "estimated_gross_margin",
}

abc_required = {
    "budget_share",
    "strategy",
    "abc_class",
    "forecast_units",
    "allocated_units",
    "fulfilled_units",
    "excess_units",
    "procurement_spend",
    "estimated_revenue",
    "coverage_pct",
}

missing_scenario = scenario_required - set(scenarios.columns)
missing_abc = abc_required - set(abc.columns)

if missing_scenario or missing_abc:
    st.error(
        "The exported CSV files are missing required columns.\n\n"
        f"Scenario file: {sorted(missing_scenario)}\n\n"
        f"ABC file: {sorted(missing_abc)}"
    )
    st.stop()

if scenarios.empty or abc.empty:
    st.error("One or both exported CSV files are empty.")
    st.stop()

numeric_scenario = [
    "budget_share",
    "budget",
    "spend",
    "unused_budget",
    "budget_utilisation_pct",
    "purchased_units",
    "forecast_units_covered_pct",
    "excess_units",
    "excess_inventory_cost",
    "estimated_revenue",
    "estimated_gross_margin",
]

numeric_abc = [
    "budget_share",
    "forecast_units",
    "allocated_units",
    "fulfilled_units",
    "excess_units",
    "procurement_spend",
    "estimated_revenue",
    "coverage_pct",
]

for col in numeric_scenario:
    scenarios[col] = pd.to_numeric(scenarios[col], errors="coerce")

for col in numeric_abc:
    abc[col] = pd.to_numeric(abc[col], errors="coerce")

if scenarios[numeric_scenario].isna().any().any():
    st.error("Invalid or missing numeric values found in the scenario CSV.")
    st.stop()

if abc[numeric_abc].isna().any().any():
    st.error("Invalid or missing numeric values found in the ABC CSV.")
    st.stop()

# Accept budget shares stored as fractions or percentages.
def normalise_budget(value):
    value = float(value)
    return value / 100 if value > 1 else value


scenarios["budget_share"] = scenarios["budget_share"].apply(
    normalise_budget
)
abc["budget_share"] = abc["budget_share"].apply(
    normalise_budget
)

scenarios["budget_label"] = scenarios["budget_share"].map(
    lambda x: f"{x:.0%}"
)
abc["budget_label"] = abc["budget_share"].map(
    lambda x: f"{x:.0%}"
)

budgets = sorted(scenarios["budget_share"].unique())
strategies = scenarios["strategy"].dropna().unique().tolist()
classes = sorted(abc["abc_class"].dropna().unique().tolist())

if not budgets or not strategies:
    st.error("No valid budget or allocation strategy was found.")
    st.stop()


# ============================================================
# 5. FORMATTING HELPERS
# ============================================================

def money(value):
    return f"${value:,.2f}"


def money_short(value):
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"


def pct(value):
    return f"{value:.2f}%"


def selected_scenario(budget, strategy):
    result = scenarios[
        (scenarios["budget_share"] == budget)
        & (scenarios["strategy"] == strategy)
    ]
    return result.iloc[0] if not result.empty else None


# ============================================================
# 6. SIDEBAR
# ============================================================

st.sidebar.markdown("## Dashboard controls")
st.sidebar.caption("Explore inventory allocation scenarios.")

budget_options = [f"{b:.0%} budget" for b in budgets]
budget_mapping = {
    f"{b:.0%} budget": b for b in budgets
}

default_budget = (
    "70% budget" if "70% budget" in budget_options
    else budget_options[0]
)

budget_choice = st.sidebar.selectbox(
    "Available budget",
    budget_options,
    index=budget_options.index(default_budget),
)

budget = budget_mapping[budget_choice]

default_strategy = (
    strategies.index("Proportional")
    if "Proportional" in strategies
    else 0
)

strategy = st.sidebar.selectbox(
    "Allocation strategy",
    strategies,
    index=default_strategy,
)

abc_class = st.sidebar.selectbox(
    "ABC class",
    ["All"] + classes,
)

st.sidebar.divider()

st.sidebar.markdown("### About this model")
st.sidebar.caption(
    "A forecast-based inventory allocation simulation "
    "using historical Walmart M5 data."
)

st.sidebar.caption(
    "Procurement cost is assumed to be 60% of retail price."
)


# ============================================================
# 7. SELECTED SCENARIO
# ============================================================

current = selected_scenario(budget, strategy)

if current is None:
    st.error("No data available for the selected scenario.")
    st.stop()

budget_scenarios = scenarios[
    scenarios["budget_share"] == budget
].copy()

current_abc = abc[
    (abc["budget_share"] == budget)
    & (abc["strategy"] == strategy)
].copy()

if abc_class != "All":
    current_abc = current_abc[
        current_abc["abc_class"] == abc_class
    ]


# ============================================================
# 8. HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Business & Decision Analytics</div>
        <h1>Capital on the Shelf</h1>
        <p>
            Inventory Allocation & Working Capital Optimisation
            <br>
            Exploring how limited purchasing budgets can be
            distributed across products.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 9. EXECUTIVE OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-label">01 / Executive overview</div>',
    unsafe_allow_html=True,
)

st.header("Allocation at a glance")

st.caption(f"Selected scenario: {budget:.0%} budget · {strategy}")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Available budget",
    money(current["budget"]),
)

k2.metric(
    "Budget utilised",
    pct(current["budget_utilisation_pct"]),
)

k3.metric(
    "Forecast coverage",
    pct(current["forecast_units_covered_pct"]),
)

k4.metric(
    "Estimated gross margin",
    money_short(current["estimated_gross_margin"]),
)

k5, k6, k7, k8 = st.columns(4)

k5.metric(
    "Purchasing spend",
    money(current["spend"]),
)

k6.metric(
    "Unused budget",
    money(current["unused_budget"]),
)

k7.metric(
    "Excess units",
    f'{current["excess_units"]:,.0f}',
)

k8.metric(
    "Excess inventory cost",
    money(current["excess_inventory_cost"]),
)

st.markdown(
    """
    <div class="note">
        Financial estimates are illustrative. The model assumes
        procurement costs equal to 60% of retail selling prices.
        Forecast coverage represents the share of forecast units
        covered by the allocation; it is not verified customer
        demand fulfilment.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 10. BUSINESS INSIGHT
# ============================================================

st.markdown(
    '<div class="section-label">02 / Business insight</div>',
    unsafe_allow_html=True,
)

st.header("What does this scenario tell us?")

proportional = selected_scenario(budget, "Proportional")
abc_priority = selected_scenario(budget, "ABC-prioritised")

if proportional is not None and abc_priority is not None:

    coverage_diff = (
        abc_priority["forecast_units_covered_pct"]
        - proportional["forecast_units_covered_pct"]
    )

    if coverage_diff > 0:
        insight_text = (
            f"At a {budget:.0%} budget, ABC prioritisation covers "
            f"{abc_priority['forecast_units_covered_pct']:.2f}% "
            f"of forecast units, compared with "
            f"{proportional['forecast_units_covered_pct']:.2f}% "
            f"under proportional allocation. This is a difference "
            f"of {coverage_diff:.2f} percentage points. "
            "ABC prioritisation concentrates the available budget "
            "on higher-priority products."
        )

    elif coverage_diff < 0:
        insight_text = (
            f"At a {budget:.0%} budget, proportional allocation "
            f"covers more forecast units than ABC prioritisation "
            f"by {abs(coverage_diff):.2f} percentage points. "
            "This illustrates the trade-off between broader "
            "coverage and class prioritisation."
        )

    else:
        insight_text = (
            f"At a {budget:.0%} budget, both strategies achieve "
            "the same forecast-unit coverage in this scenario."
        )

    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-title">Key finding</div>
            <p>{insight_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 11. STRATEGY COMPARISON
# ============================================================

st.markdown(
    '<div class="section-label">03 / Strategy comparison</div>',
    unsafe_allow_html=True,
)

st.header("Compare allocation strategies")

left, right = st.columns(2)

with left:
    st.subheader("Forecast coverage")

    coverage_chart = px.bar(
        budget_scenarios,
        x="strategy",
        y="forecast_units_covered_pct",
        color="strategy",
        text="forecast_units_covered_pct",
        color_discrete_map={
            "Proportional": "#7ab8e8",
            "ABC-prioritised": "#1769aa",
        },
        labels={
            "strategy": "Allocation strategy",
            "forecast_units_covered_pct": "Coverage (%)",
        },
        template="plotly_white",
    )

    coverage_chart.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        textfont=dict(color="#1f2937", size=12),
        cliponaxis=False,
    )

    coverage_chart.update_layout(
        showlegend=False,
        height=370,
        margin=dict(l=20, r=20, t=30, b=25),
        yaxis=dict(
            range=[0, 108],
            title="Forecast coverage (%)",
            gridcolor="#e5e7eb",
        ),
        xaxis_title="",
        font=dict(family="DM Sans", color="#334155"),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )

    st.plotly_chart(
        coverage_chart,
        use_container_width=True,
    )


with right:
    st.subheader("Estimated gross margin")

    margin_chart = px.bar(
        budget_scenarios,
        x="strategy",
        y="estimated_gross_margin",
        color="strategy",
        text="estimated_gross_margin",
        color_discrete_map={
            "Proportional": "#7ab8e8",
            "ABC-prioritised": "#1769aa",
        },
        labels={
            "strategy": "Allocation strategy",
            "estimated_gross_margin": "Estimated gross margin ($)",
        },
        template="plotly_white",
    )

    margin_chart.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        textfont=dict(color="#1f2937", size=11),
        cliponaxis=False,
    )

    max_margin = budget_scenarios[
        "estimated_gross_margin"
    ].max()

    margin_chart.update_layout(
        showlegend=False,
        height=370,
        margin=dict(l=20, r=20, t=30, b=25),
        yaxis=dict(
            title="Estimated gross margin ($)",
            range=[
                0,
                max_margin * 1.2 if max_margin > 0 else 1,
            ],
            gridcolor="#e5e7eb",
            tickformat="~s",
        ),
        xaxis_title="",
        font=dict(family="DM Sans", color="#334155"),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )

    st.plotly_chart(
        margin_chart,
        use_container_width=True,
    )

st.markdown(
    """
    <div class="note">
        Estimated gross margins are calculated using the same
        assumed procurement-cost ratio for both strategies.
        Consequently, the margins can be almost identical.
        Forecast coverage is more useful for understanding the
        allocation trade-off in this model.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 12. BUDGET SENSITIVITY
# ============================================================

st.markdown(
    '<div class="section-label">04 / Sensitivity analysis</div>',
    unsafe_allow_html=True,
)

st.header("How does the budget change the outcome?")

sensitivity_metric = st.radio(
    "Metric",
    ["Forecast coverage", "Estimated gross margin"],
    horizontal=True,
)

if sensitivity_metric == "Forecast coverage":
    metric_column = "forecast_units_covered_pct"
    y_title = "Forecast coverage (%)"
    y_format = ".2f"
else:
    metric_column = "estimated_gross_margin"
    y_title = "Estimated gross margin ($)"
    y_format = ",.0f"

sensitivity = scenarios.sort_values("budget_share").copy()

sensitivity_chart = px.line(
    sensitivity,
    x="budget_share",
    y=metric_column,
    color="strategy",
    markers=True,
    color_discrete_map={
        "Proportional": "#7ab8e8",
        "ABC-prioritised": "#1769aa",
    },
    labels={
        "budget_share": "Available budget",
        metric_column: y_title,
        "strategy": "Strategy",
    },
    template="plotly_white",
)

sensitivity_chart.update_traces(
    line=dict(width=3),
    marker=dict(size=8),
)

sensitivity_chart.update_layout(
    height=430,
    margin=dict(l=25, r=20, t=30, b=30),
    xaxis=dict(
        title="Available budget",
        tickformat=".0%",
        showgrid=False,
    ),
    yaxis=dict(
        title=y_title,
        gridcolor="#e5e7eb",
        tickformat=y_format,
    ),
    font=dict(family="DM Sans", color="#334155"),
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
)

st.plotly_chart(
    sensitivity_chart,
    use_container_width=True,
)


# ============================================================
# 13. ABC CLASS ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-label">05 / Product prioritisation</div>',
    unsafe_allow_html=True,
)

st.header("ABC inventory insights")

st.caption(
    f"Class-level allocation details for the {budget:.0%} "
    f"budget and {strategy} strategy."
)

if not current_abc.empty:

    abc_chart = px.bar(
        current_abc.sort_values("abc_class"),
        x="abc_class",
        y="coverage_pct",
        color="abc_class",
        text="coverage_pct",
        color_discrete_map={
            "A": "#7ab8e8",
            "B": "#1769aa",
            "C": "#f3a6ad",
        },
        labels={
            "abc_class": "ABC class",
            "coverage_pct": "Coverage (%)",
        },
        template="plotly_white",
    )

    abc_chart.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        textfont=dict(color="#1f2937", size=12),
        cliponaxis=False,
    )

    abc_chart.update_layout(
        showlegend=False,
        height=350,
        margin=dict(l=20, r=20, t=30, b=25),
        yaxis=dict(
            range=[0, 108],
            title="Forecast coverage (%)",
            gridcolor="#e5e7eb",
        ),
        xaxis_title="ABC class",
        font=dict(family="DM Sans", color="#334155"),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
    )

    st.plotly_chart(
        abc_chart,
        use_container_width=True,
    )

    st.subheader("ABC class allocation details")

    display_abc = current_abc[
        [
            "abc_class",
            "forecast_units",
            "allocated_units",
            "fulfilled_units",
            "excess_units",
            "procurement_spend",
            "estimated_revenue",
            "coverage_pct",
        ]
    ].copy()

    display_abc = display_abc.rename(
        columns={
            "abc_class": "ABC class",
            "forecast_units": "Forecast units",
            "allocated_units": "Allocated units",
            "fulfilled_units": "Covered units",
            "excess_units": "Excess units",
            "procurement_spend": "Purchasing spend ($)",
            "estimated_revenue": "Estimated revenue ($)",
            "coverage_pct": "Coverage (%)",
        }
    )

    st.dataframe(
        display_abc,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Forecast units": st.column_config.NumberColumn(
                format="localized"
            ),
            "Allocated units": st.column_config.NumberColumn(
                format="localized"
            ),
            "Covered units": st.column_config.NumberColumn(
                format="localized"
            ),
            "Excess units": st.column_config.NumberColumn(
                format="localized"
            ),
            "Purchasing spend ($)": st.column_config.NumberColumn(
                format="$%.2f"
            ),
            "Estimated revenue ($)": st.column_config.NumberColumn(
                format="$%.2f"
            ),
            "Coverage (%)": st.column_config.NumberColumn(
                format="%.2f%%"
            ),
        },
    )

else:
    st.info("No ABC class records match the selected filters.")


# ============================================================
# 14. FULL SCENARIO TABLE
# ============================================================

st.markdown(
    '<div class="section-label">06 / Scenario details</div>',
    unsafe_allow_html=True,
)

st.header("All budget scenarios")

scenario_display = scenarios[
    [
        "budget_label",
        "strategy",
        "budget",
        "spend",
        "forecast_units_covered_pct",
        "estimated_revenue",
        "estimated_gross_margin",
        "excess_inventory_cost",
    ]
].copy()

scenario_display = scenario_display.rename(
    columns={
        "budget_label": "Budget",
        "strategy": "Strategy",
        "budget": "Available budget ($)",
        "spend": "Purchasing spend ($)",
        "forecast_units_covered_pct": "Forecast coverage (%)",
        "estimated_revenue": "Estimated revenue ($)",
        "estimated_gross_margin": "Estimated gross margin ($)",
        "excess_inventory_cost": "Excess inventory cost ($)",
    }
)

# Important: no arithmetic scaling or rounding is applied
# to the original currency values here.

st.dataframe(
    scenario_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Available budget ($)": st.column_config.NumberColumn(
            format="$%.2f"
        ),
        "Purchasing spend ($)": st.column_config.NumberColumn(
            format="$%.2f"
        ),
        "Forecast coverage (%)": st.column_config.NumberColumn(
            format="%.2f%%"
        ),
        "Estimated revenue ($)": st.column_config.NumberColumn(
            format="$%.2f"
        ),
        "Estimated gross margin ($)": st.column_config.NumberColumn(
            format="$%.2f"
        ),
        "Excess inventory cost ($)": st.column_config.NumberColumn(
            format="$%.2f"
        ),
    },
)


# ============================================================
# 15. DATA VALIDATION
# ============================================================

with st.expander("Data validation and source values"):

    st.markdown(
        """
        The values below are read directly from the exported
        scenario CSV. They are not recalculated for display.
        """
    )

    validation_budget = st.selectbox(
        "Budget to validate",
        budgets,
        index=budgets.index(budget),
        format_func=lambda x: f"{x:.0%}",
        key="validation_budget",
    )

    validation_strategy = st.selectbox(
        "Strategy to validate",
        strategies,
        index=(
            strategies.index(strategy)
            if strategy in strategies else 0
        ),
        key="validation_strategy",
    )

    validation_row = selected_scenario(
        validation_budget,
        validation_strategy,
    )

    if validation_row is not None:
        validation_data = pd.DataFrame(
            [
                {
                    "Metric": "Available budget",
                    "CSV value": validation_row["budget"],
                },
                {
                    "Metric": "Purchasing spend",
                    "CSV value": validation_row["spend"],
                },
                {
                    "Metric": "Estimated revenue",
                    "CSV value": validation_row["estimated_revenue"],
                },
                {
                    "Metric": "Estimated gross margin",
                    "CSV value": validation_row["estimated_gross_margin"],
                },
            ]
        )

        st.dataframe(
            validation_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "CSV value": st.column_config.NumberColumn(
                    format="$%.2f"
                ),
            },
        )

    # Check duplicate budget-strategy rows.
    duplicate_scenarios = scenarios.duplicated(
        subset=["budget_share", "strategy"],
        keep=False,
    )

    if duplicate_scenarios.any():
        st.error(
            "Duplicate budget and strategy combinations "
            "were found in the scenario CSV."
        )
    else:
        st.success(
            "No duplicate budget and strategy combinations found."
        )

    # Check basic budget consistency.
    budget_errors = (
        scenarios["spend"] > scenarios["budget"] + 0.02
    )

    if budget_errors.any():
        st.warning(
            "Some scenarios have purchasing spend greater "
            "than the available budget. Review the source results."
        )
    else:
        st.success(
            "Purchasing spend does not exceed the budget "
            "in the exported scenarios."
        )


# ============================================================
# 16. DOWNLOADS
# ============================================================

st.markdown(
    '<div class="section-label">07 / Data exports</div>',
    unsafe_allow_html=True,
)

st.header("Download analysis")

d1, d2 = st.columns(2)

with d1:
    st.download_button(
        "Download scenario comparison CSV",
        data=scenarios.drop(
            columns=["budget_label"]
        ).to_csv(index=False).encode("utf-8"),
        file_name="allocation_scenario_comparison.csv",
        mime="text/csv",
        use_container_width=True,
    )

with d2:
    st.download_button(
        "Download ABC class analysis CSV",
        data=abc.drop(
            columns=["budget_label"]
        ).to_csv(index=False).encode("utf-8"),
        file_name="allocation_by_abc_class.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ============================================================
# 17. METHODOLOGY AND LIMITATIONS
# ============================================================

with st.expander("Model assumptions and limitations"):

    st.markdown(
        """
        ### Allocation methodology

        - Proportional allocation distributes the purchasing
          budget across forecast requirements.
        - ABC-prioritised allocation prioritises A-class products,
          followed by B and then C. Demand is used to order
          products within each class.
        - The model evaluates budgets at 50%, 70% and 90%
          of the estimated full purchasing requirement.

        ### Financial assumptions

        - Procurement cost is assumed to be 60% of retail
          selling price.
        - Revenue and gross margin are estimates based on
          forecast units covered and selling prices.
        - These are not realised sales or audited financial results.

        ### Limitations

        - The model does not incorporate actual on-hand inventory.
        - Holding costs, replenishment lead times and supplier
          constraints are not modelled.
        - Historical demand forecasts may not represent future demand.
        - Forecast coverage is not a direct measure of actual
          stockout prevention or customer satisfaction.
        - ABC prioritisation is a policy heuristic, not a
          proven globally optimal allocation.
        """
    )


# ============================================================
# 18. FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Capital on the Shelf · Business & Decision Analytics
        <br>
        Illustrative decision-support model · Based on M5 retail data
    </div>
    """,
    unsafe_allow_html=True,
)