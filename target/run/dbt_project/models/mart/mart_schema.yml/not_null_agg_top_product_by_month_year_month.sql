
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select year_month
from `symmetric-fin-469415-q9`.`glamira_data_2025_mart`.`agg_top_product_by_month`
where year_month is null



  
  
      
    ) dbt_internal_test