
  
    

    create or replace table `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_product`
      
    
    

    
    OPTIONS()
    as (
      

WITH src AS (
	SELECT *
	FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_product`
)

,product AS (
	SELECT
		product_id
		,product_name
		,sku
		,gender
		,max_price_format AS max_price
		,min_price_format AS min_price
		,type_id
		,store_code
	FROM src
)

SELECT * FROM product
    );
  