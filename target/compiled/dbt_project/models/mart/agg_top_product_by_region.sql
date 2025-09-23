

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
    FROM `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales` f
    JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_location` l USING (location_id)
    JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_product` p USING (product_id)
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