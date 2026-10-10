SELECT
    d AS day_id,
    DATE(date) AS calendar_date,
    wm_yr_wk AS week_id,
    month AS month_number,
    year AS calendar_year,
    event_name_1,
    event_type_1,
    event_name_2,
    event_type_2,
    snap_CA,
    snap_TX,
    snap_WI
FROM `sincere-quasar-511010-v3.retail_demand_raw.calendar`
