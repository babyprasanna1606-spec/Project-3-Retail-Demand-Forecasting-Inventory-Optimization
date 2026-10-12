SELECT
    id AS product_store_id,
    item_id,
    dept_id,
    cat_id,
    store_id,
    state_id,
    * EXCEPT(id, item_id, dept_id, cat_id, store_id, state_id)
FROM `sincere-quasar-511010-v3.retail_demand_raw.sales_train_validation`
