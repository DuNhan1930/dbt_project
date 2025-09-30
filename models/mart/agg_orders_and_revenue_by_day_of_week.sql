{{ config(materialized='table') }}

SELECT
    d.day_of_week
    ,COUNT(DISTINCT f.order_id) AS num_orders
    ,ROUND(SUM(f.line_total), 2) AS revenue
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_date') }} d USING (date_id)
GROUP BY d.day_of_week
ORDER BY CASE d.day_of_week
    WHEN 'Monday'    THEN 1
    WHEN 'Tuesday'   THEN 2
    WHEN 'Wednesday' THEN 3
    WHEN 'Thursday'  THEN 4
    WHEN 'Friday'    THEN 5
    WHEN 'Saturday'  THEN 6
    WHEN 'Sunday'    THEN 7
  END

