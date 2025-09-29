-- Unit price should never be negative
SELECT
    sales_id
    ,order_id
    ,product_id
    ,price
FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_sales`
WHERE price < 0