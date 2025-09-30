{{ config(materialized='table') }}

SELECT
    d.week_of_year
    ,COUNT(DISTINCT f.order_id) AS num_orders
    ,ROUND(SUM(f.line_total), 2) AS revenue
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_date') }} d USING (date_id)
GROUP BY d.week_of_year
ORDER BY d.week_of_year
