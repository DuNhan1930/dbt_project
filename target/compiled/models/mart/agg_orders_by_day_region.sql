

SELECT
    d.full_date
    ,l.country_long_name
    ,l.region_name
    ,COUNT(DISTINCT f.order_id) AS orders
FROM `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales` f
JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_date` d USING (date_id)
JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_location` l USING (location_id)
GROUP BY d.full_date, l.country_long_name, l.region_name
ORDER BY d.full_date, l.country_long_name, l.region_name