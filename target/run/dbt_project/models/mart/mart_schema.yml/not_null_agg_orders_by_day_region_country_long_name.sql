
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select country_long_name
from `symmetric-fin-469415-q9`.`glamira_data_2025_mart`.`agg_orders_by_day_region`
where country_long_name is null



  
  
      
    ) dbt_internal_test