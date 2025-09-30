

SELECT
    d.week_of_year
    ,COUNT(DISTINCT f.order_id) AS orders
    ,ROUND(SUM(f.line_total), 2) AS revenue
FROM `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales` f
JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_date` d USING (date_id)
GROUP BY d.week_of_year
ORDER BY d.week_of_year