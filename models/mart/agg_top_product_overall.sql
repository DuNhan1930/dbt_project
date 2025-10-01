WITH ranked AS (
    SELECT
        p.product_id
        ,p.product_name
        ,SUM(f.amount) AS total_qty
        ,RANK() OVER (ORDER BY SUM(f.amount) DESC) AS rnk
    FROM {{ ref('fact_sales') }} f
    JOIN {{ ref('dim_product') }} p USING (product_id)
    GROUP BY p.product_id, p.product_name
)
SELECT
    product_id
    ,product_name
    ,total_qty
FROM ranked
WHERE rnk <= 5
ORDER BY rnk
