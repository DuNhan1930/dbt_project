
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select full_date
from `symmetric-fin-469415-q9`.`glamira_data_2025_mart`.`agg_orders_by_day_region`
where full_date is null



  
  
      
    ) dbt_internal_test