# Retail Demand Forecasting & Inventory Optimization

An end-to-end retail analytics and demand forecasting project using the M5 retail dataset, Google BigQuery, dbt, Prophet, LightGBM, and Streamlit. The project explores retail sales data, builds analytics-ready data models, evaluates forecasting models, and presents results through an interactive dashboard.

## Project Objectives

- Explore retail sales, calendar, and pricing data.
- Store and query large datasets in Google BigQuery.
- Transform raw data into analytics-ready models using dbt.
- Build and evaluate demand forecasting models.
- Visualize actual versus predicted demand.
- Explore an illustrative inventory and pricing scenario through an interactive dashboard.

## Technology Stack

| Area | Tools |
|---|---|
| Programming | Python, SQL |
| Data warehouse | Google BigQuery |
| Data transformation | dbt Core, dbt-bigquery |
| Forecasting | Prophet, LightGBM |
| Dashboard | Streamlit, Plotly |
| Data analysis | Pandas, Jupyter Notebook |
| Version control | Git, GitHub |

## Dataset

This project uses the M5 retail forecasting dataset, including:

- **Calendar data:** Dates, weekdays, and related calendar attributes.
- **Sales data:** Historical product sales by store.
- **Sell-price data:** Product prices across stores and dates.

The raw data is stored in BigQuery for analysis. Local raw data files and credentials should not be committed to the repository.

## Project Progress — Four Weeks

### Week 1: Data Exploration and BigQuery Setup

- Explored the M5 dataset and its structure.
- Loaded the calendar, sales, and sell-price data into Google BigQuery.
- Created the `retail_demand_raw` dataset.
- Started the retail demand forecasting workflow using Jupyter notebooks.

### Week 2: Data Transformation with dbt

- Configured dbt Core and the BigQuery adapter.
- Created staging models for calendar, sales, and sell-price data.
- Built weekly and monthly sales mart models.
- Generated dbt documentation.
- Ran dbt data-quality tests successfully, with 12 tests passing.

### Week 3: Demand Forecasting

- Developed a Prophet forecasting notebook.
- Developed a LightGBM forecasting notebook.
- Evaluated model predictions using MAE and RMSE.
- Uploaded forecast outputs to BigQuery for dashboard consumption.

**Recorded LightGBM evaluation metrics**
- MAE: 76.20
- RMSE: 120.67

These values reflect the current evaluation run and should be interpreted in the context of its test data and aggregation level.

The Prophet output currently contains historical dataset dates ending on **12 June 2016**. It should not be presented as a future forecast beyond that period.

### Week 4: Interactive Streamlit Dashboard

Created an interactive dashboard using Streamlit, Plotly, and BigQuery.

Dashboard features:
- Store and product-group filters.
- Key dataset and model metrics.
- Actual versus predicted LightGBM demand chart.
- Prophet historical prediction chart.
- An illustrative what-if demand scenario.
- CSV download for filtered forecast records.

The what-if scenario uses an assumed price elasticity. It is an illustration, not a validated causal estimate of how a real price change would affect demand.

## Repository Structure

```text
Project-3-Retail-Demand-Forecasting-Inventory-Optimization/
├── app/
│   └── streamlit_app.py
├── notebooks/
│   ├── 01_Retail_Demand_EDA.ipynb
│   ├── 02_M5_Data_Extraction.ipynb
│   ├── 03_BigQuery_Data_Loading.ipynb
│   ├── 04_Prophet_Forecasting.ipynb
│   ├── 05_LightGBM_Forecasting.ipynb
│   └── 06_Streamlit_Dashboard.ipynb
├── retail_demand_dbt/
├── scripts/
├── src/
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Run the Dashboard Locally

### 1. Clone the repository

```bash
git clone -b feature-baby https://github.com/babyprasanna1606-spec/Project-3-Retail-Demand-Forecasting-Inventory-Optimization.git
cd Project-3-Retail-Demand-Forecasting-Inventory-Optimization
```

### 2. Create and activate a virtual environment

Windows:

```bat
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Google Cloud authentication

Ensure you have access to the Google Cloud project and the required BigQuery tables. Configure Application Default Credentials using the Google Cloud CLI:

```bash
gcloud auth application-default login
```

The dashboard currently references these BigQuery tables:

- `sincere-quasar-511010-v3.retail_demand_raw.forecast_results`
- `sincere-quasar-511010-v3.retail_demand_raw.prophet_forecast_results`

Make sure these tables exist and your account has permission to query them.

### 5. Start Streamlit

```bash
python -m streamlit run app/streamlit_app.py
```

Streamlit will display a local URL, usually `http://localhost:8501`.

## Limitations

- Forecast results depend on the available historical data and current evaluation setup.
- The uploaded LightGBM results represent test predictions, not necessarily future production forecasts.
- The Prophet series currently covers historical M5 dates.
- The price-elasticity scenario is illustrative and requires real-world validation before business use.
- Inventory recommendations would benefit from additional constraints such as lead times, safety stock, stock-on-hand, and service-level targets.

## Future Improvements

- Perform time-based cross-validation and compare forecasting models.
- Improve forecasts with item-store-level features and seasonal variables.
- Add stock-on-hand, lead-time, and safety-stock calculations.
- Develop inventory reorder recommendations.
- Add forecast monitoring and model-performance tracking.
- Deploy the dashboard to a hosted environment.

## Author

**Baby Prasanna**

GitHub: [babyprasanna1606-spec](https://github.com/babyprasanna1606-spec)

---

*This project was developed incrementally across four weeks, from data exploration and warehouse modeling through forecasting and dashboard development.*
