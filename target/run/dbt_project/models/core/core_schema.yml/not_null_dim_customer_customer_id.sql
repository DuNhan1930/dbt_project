
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select customer_id
from `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_customer`
where customer_id is null



  
  
      
    ) dbt_internal_test