

SELECT
    d.full_date
    ,COUNT(DISTINCT f.order_id) AS orders
    ,SUM(f.line_total) AS revenue
FROM `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales` f
JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_date` d USING (date_id)
GROUP BY d.full_date
ORDER BY d.full_date