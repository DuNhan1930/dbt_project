

WITH src AS (
	SELECT *
 	FROM `symmetric-fin-469415-q9`.`glamira_data_2025`.`summary`
)

,flattened AS (
	SELECT
		GENERATE_UUID() 				AS sales_id
		,CAST(src.order_id AS INT64) 	AS order_id
		,src._id 						AS customer_id
		
		,src.time_stamp 				AS date_id
		,src.time_stamp 				AS time_stamp
		,src.local_time 				AS local_time

		,src.ip 						AS ip_address

		,CAST(src.store_id AS INT64) 	AS store_id
		
		,cp.product_id 					AS product_id
		,cp.amount 						AS amount
		,cp.currency 					AS currency_code
		,cp.price 						AS price
  	FROM src
  	,UNNEST(src.cart_products) AS cp
  	WHERE collection = 'checkout_success' 
	AND REGEXP_CONTAINS(
        src.ip,
        r'^(25[0-5]|2[0-4]\d|[01]?\d?\d)(\.(25[0-5]|2[0-4]\d|[01]?\d?\d)){3}$'
    )
)

SELECT * FROM flattened