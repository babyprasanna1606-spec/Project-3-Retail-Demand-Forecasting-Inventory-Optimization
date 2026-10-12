
import streamlit as st
import pandas as pd
import plotly.express as px
from google.cloud import bigquery

PROJECT_ID = "sincere-quasar-511010-v3"
DATASET = "retail_demand_raw"

st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📊",
    layout="wide"
)

st.title("Retail Demand Forecasting & Inventory Optimization")
st.caption("M5 dataset | BigQuery | Prophet | LightGBM")

@st.cache_resource
def get_client():
    return bigquery.Client(project=PROJECT_ID)

@st.cache_data(ttl=300)
def load_forecasts():
    client = get_client()

    lgb_query = f"""
        SELECT item_id, store_id, forecast_date,
               actual_units, predicted_units, mae
        FROM `{PROJECT_ID}.{DATASET}.forecast_results`
        WHERE model_name = 'LightGBM'
    """

    prophet_query = f"""
        SELECT forecast_date, predicted_units,
               lower_bound, upper_bound
        FROM `{PROJECT_ID}.{DATASET}.prophet_forecast_results`
    """

    lgb = client.query(lgb_query).to_dataframe()
    prophet = client.query(prophet_query).to_dataframe()

    lgb["forecast_date"] = pd.to_datetime(lgb["forecast_date"])
    prophet["forecast_date"] = pd.to_datetime(prophet["forecast_date"])
    lgb["category_group"] = lgb["item_id"].str.split("_").str[0]

    return lgb, prophet

try:
    lgb, prophet = load_forecasts()
except Exception as exc:
    st.error("Could not load forecast data from BigQuery.")
    st.exception(exc)
    st.stop()

if lgb.empty or prophet.empty:
    st.warning("One or both forecast tables contain no data.")
    st.stop()

st.sidebar.header("Dashboard Filters")

stores = sorted(lgb["store_id"].dropna().unique().tolist())
selected_store = st.sidebar.selectbox("Select store", stores)

categories = sorted(lgb["category_group"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select product group", categories)

filtered = lgb[
    (lgb["store_id"] == selected_store)
    & (lgb["category_group"] == selected_category)
].copy()

col1, col2, col3 = st.columns(3)

col1.metric("Stores in dataset", lgb["store_id"].nunique())
col2.metric("Filtered prediction rows", f"{len(filtered):,}")

recorded_mae = filtered["mae"].dropna()
if not recorded_mae.empty:
    col3.metric("Recorded LightGBM MAE", f"{recorded_mae.iloc[0]:.2f}")
else:
    col3.metric("Recorded LightGBM MAE", "N/A")

st.subheader("LightGBM: Actual vs Predicted Units")

if filtered.empty:
    st.info("No LightGBM rows match these filters.")
else:
    daily = (
        filtered.groupby("forecast_date", as_index=False)
        .agg(
            Actual=("actual_units", "sum"),
            Predicted=("predicted_units", "sum")
        )
        .sort_values("forecast_date")
    )

    chart_data = daily.melt(
        id_vars="forecast_date",
        value_vars=["Actual", "Predicted"],
        var_name="Series",
        value_name="Units"
    )

    fig = px.line(
        chart_data,
        x="forecast_date",
        y="Units",
        color="Series",
        markers=True,
        title="Actual vs Predicted Demand"
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Prophet Model — Historical Forecast Series")
st.caption(
    "This series covers historical M5 dataset dates and ends on 12 June 2016. "
    "It should not be interpreted as a forecast beyond the dataset period."
)

prophet_chart = prophet.sort_values("forecast_date").tail(30)

fig_prophet = px.line(
    prophet_chart,
    x="forecast_date",
    y="predicted_units",
    title="Prophet Predictions — Latest 30 Available Dates"
)
fig_prophet.add_scatter(
    x=prophet_chart["forecast_date"],
    y=prophet_chart["upper_bound"],
    mode="lines",
    line=dict(width=0),
    showlegend=False,
    name="Upper bound"
)
fig_prophet.add_scatter(
    x=prophet_chart["forecast_date"],
    y=prophet_chart["lower_bound"],
    mode="lines",
    fill="tonexty",
    line=dict(width=0),
    name="Prediction interval"
)
st.plotly_chart(fig_prophet, use_container_width=True)

st.subheader("What-if Demand Scenario")

st.caption(
    "Illustrative scenario only; this does not establish a causal price effect."
)

price_change = st.slider(
    "Assumed price reduction (%)",
    min_value=0,
    max_value=30,
    value=10,
    step=5
)

elasticity = st.slider(
    "Assumed price elasticity",
    min_value=-3.0,
    max_value=0.0,
    value=-1.0,
    step=0.5
)

baseline = filtered["predicted_units"].sum()

if price_change == 0:
    demand_change = 0.0
else:
    demand_change = ((1 - price_change / 100) ** elasticity - 1) * 100

scenario_demand = baseline * (1 + demand_change / 100)

c1, c2, c3 = st.columns(3)
c1.metric("Baseline predicted units", f"{baseline:,.2f}")
c2.metric("Scenario demand change", f"{demand_change:+.2f}%")
c3.metric("Illustrative scenario units", f"{scenario_demand:,.2f}")

st.download_button(
    "Download filtered LightGBM data (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="lightgbm_filtered_forecasts.csv",
    mime="text/csv"
)

st.caption(
    "Note: LightGBM records are the uploaded test predictions. "
    "The Prophet series uses historical dataset dates, not future dates."
)
