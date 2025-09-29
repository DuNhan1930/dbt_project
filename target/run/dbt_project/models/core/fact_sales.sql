
  
    

    create or replace table `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales`
      
    
    

    
    OPTIONS()
    as (
      

WITH src AS (
	SELECT *
	FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_sales`
)

,sales AS (
	SELECT 
		src.sales_id
		,src.order_id
		,src.customer_id

		,CAST(FORMAT_DATE('%Y%m%d', DATE(TIMESTAMP_SECONDS(src.time_stamp))) AS INT64) AS date_id
		,DATE(TIMESTAMP_SECONDS(src.time_stamp)) AS time_stamp
		,src.local_time
		
		,l.location_id
		,src.ip_address

		,src.store_id
		,src.product_id
		,src.amount

		,CASE
		WHEN src.currency_code IS NULL OR TRIM(src.currency_code) = "" 
			THEN "USD $"
		WHEN TRIM(src.currency_code) = " din." 
			THEN "din."
		WHEN TRIM(src.currency_code) = "د.ك.‏" 
			THEN "د.ك."
		ELSE 
			TRIM(src.currency_code)
		END AS currency_code
		
		,CASE
		WHEN src.price LIKE '%,%' AND src.price LIKE '%.%' 
			THEN SAFE_CAST(REPLACE(REPLACE(src.price, '.', ''), ',', '.') AS FLOAT64)
		WHEN src.price LIKE '%,%' 
			THEN SAFE_CAST(REPLACE(src.price, ',', '.') AS FLOAT64)
		ELSE
			SAFE_CAST(src.price AS FLOAT64)
		END AS price
	FROM src
	LEFT JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_location` l
		ON src.ip_address = l.ip_address
),

with_rates AS (
	SELECT
		s.*
		,COALESCE(c.exchange_rate, 1.0) AS exchange_rate
		,s.price * COALESCE(c.exchange_rate, 1.0) AS price_in_usd
	FROM sales s
	LEFT JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`dim_currency` c
		ON s.currency_code = c.code OR s.currency_code = c.symbol
)

SELECT
	sales_id
	,order_id
	,customer_id
	,date_id
	,time_stamp
	,local_time
	,location_id
	,ip_address
	,store_id
	,product_id
	,amount
	,currency_code
	,ROUND(price_in_usd, 3) 			AS price_in_usd
	,ROUND(price_in_usd * amount, 3) 	AS line_total
FROM with_rates
    );
  