{{ config(materialized='table') }}

SELECT
    d.year_month
    ,COUNT(DISTINCT f.order_id) AS orders
    ,SUM(f.line_total) AS revenue
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_date') }} d USING (date_id)
GROUP BY d.year_month
ORDER BY d.year_month
