
  
    

    create or replace table `symmetric-fin-469415-q9`.`glamira_data_2025_mart`.`agg_orders_by_region`
      
    
    

    
    OPTIONS()
    as (
      

SELECT
    l.country_long_name
    ,l.region_name
    ,COUNT(DISTINCT f.order_id) AS orders
FROM `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales` f
JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_location` l USING (location_id)
GROUP BY l.country_long_name, l.region_name
ORDER BY orders DESC
    );
  