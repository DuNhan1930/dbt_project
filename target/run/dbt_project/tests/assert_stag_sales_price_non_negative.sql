
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  -- Unit price should never be negative
SELECT
    sales_id
    ,order_id
    ,product_id
    ,price
FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_sales`
WHERE price < 0
  
  
      
    ) dbt_internal_test