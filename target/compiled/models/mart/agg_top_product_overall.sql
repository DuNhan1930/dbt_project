

WITH ranked AS (
    SELECT
        p.product_id
        ,p.product_name
        ,SUM(f.amount) AS total_qty
        ,RANK() OVER (ORDER BY SUM(f.amount) DESC) AS rnk
    FROM `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales` f
    JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_product` p USING (product_id)
    GROUP BY p.product_id, p.product_name
)
SELECT
    product_id
    ,product_name
    ,total_qty
FROM ranked
WHERE rnk = 1