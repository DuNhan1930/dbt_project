
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select sales_id
from `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_sales`
where sales_id is null



  
  
      
    ) dbt_internal_test