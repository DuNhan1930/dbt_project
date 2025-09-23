
  
    

    create or replace table `symmetric-fin-469415-q9`.`glamira_data_2025_mart`.`agg_revenue_by_month`
      
    
    

    
    OPTIONS()
    as (
      

SELECT
    d.year_month
    ,SUM(f.line_total) AS revenue
FROM `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales` f
JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_date` d USING (date_id)
GROUP BY d.year_month
ORDER BY d.year_month
    );
  