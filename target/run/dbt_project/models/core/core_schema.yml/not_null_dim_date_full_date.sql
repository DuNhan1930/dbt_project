
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select full_date
from `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_date`
where full_date is null



  
  
      
    ) dbt_internal_test