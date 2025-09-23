{{ config(materialized='table') }}

SELECT
    l.country_long_name
    ,l.region_name
    ,SUM(f.line_total) AS revenue
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_location') }} l USING (location_id)
GROUP BY l.country_long_name, l.region_name
ORDER BY revenue DESC
