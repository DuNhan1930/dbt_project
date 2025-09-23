

WITH ranked AS (
    SELECT
        d.year_month
        ,p.product_id
        ,p.product_name
        ,SUM(f.amount) AS total_qty
        ,RANK() OVER (PARTITION BY d.year_month ORDER BY SUM(f.amount) DESC) AS rnk
    FROM `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales` f
    JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_date` d USING (date_id)
    JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_product` p USING (product_id)
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