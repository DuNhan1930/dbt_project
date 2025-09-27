-- Unit price should never be negative
SELECT
    sales_id
    ,order_id
    ,product_id
    ,price
FROM {{ ref('stag_sales') }}
WHERE price < 0