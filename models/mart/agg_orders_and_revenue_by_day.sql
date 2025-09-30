{{ config(materialized='table') }}

SELECT
    d.full_date
    ,COUNT(DISTINCT f.order_id) AS num_orders
    ,ROUND(SUM(f.line_total), 2) AS revenue
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_date') }} d USING (date_id)
GROUP BY d.full_date
ORDER BY d.full_date
