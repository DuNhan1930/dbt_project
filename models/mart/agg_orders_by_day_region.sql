{{ config(materialized='table') }}

SELECT
    d.full_date
    ,l.country_long_name
    ,l.region_name
    ,COUNT(DISTINCT f.order_id) AS orders
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_date') }} d USING (date_id)
JOIN {{ ref('dim_location') }} l USING (location_id)
GROUP BY d.full_date, l.country_long_name, l.region_name
ORDER BY d.full_date, l.country_long_name, l.region_name
