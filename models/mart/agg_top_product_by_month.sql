{{ config(materialized='table') }}

WITH ranked AS (
    SELECT
        d.year_month
        ,p.product_id
        ,p.product_name
        ,SUM(f.amount) AS total_qty
        ,RANK() OVER (PARTITION BY d.year_month ORDER BY SUM(f.amount) DESC) AS rnk
    FROM {{ ref('fact_sales') }} f
    JOIN {{ ref('dim_date') }} d USING (date_id)
    JOIN {{ ref('dim_product') }} p USING (product_id)
    GROUP BY d.year_month, p.product_id, p.product_name
)
SELECT 
    year_month
    ,product_id
    ,product_name
    ,total_qty
FROM ranked
WHERE rnk = 1
ORDER BY year_month
