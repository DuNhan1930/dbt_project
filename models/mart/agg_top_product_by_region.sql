{{ config(materialized='table') }}

WITH ranked AS (
    SELECT
        l.country_long_name
        ,l.region_name
        ,p.product_id
        ,p.product_name
        ,SUM(f.amount) AS total_qty
        ,RANK() OVER (
            PARTITION BY l.country_long_name, l.region_name
            ORDER BY SUM(f.amount) DESC
        ) AS rnk
    FROM {{ ref('fact_sales') }} f
    JOIN {{ ref('dim_location') }} l USING (location_id)
    JOIN {{ ref('dim_product') }} p USING (product_id)
    GROUP BY l.country_long_name, l.region_name, p.product_id, p.product_name
)

SELECT 
    country_long_name
    ,region_name
    ,product_id
    ,product_name
    ,total_qty
FROM ranked
WHERE rnk = 1
ORDER BY country_long_name, region_name
