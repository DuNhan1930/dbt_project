
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select amount
from `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales`
where amount is null



  
  
      
    ) dbt_internal_test