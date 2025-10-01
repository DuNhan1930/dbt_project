{{ config(materialized='table') }}

WITH src AS (
	SELECT *
	FROM {{ ref('stag_sales') }}
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
		-- US/UK thousands with comma + dot decimal: 1,000.50
		WHEN src.price LIKE '%,%' AND src.price LIKE '%.%'
			THEN SAFE_CAST(REPLACE(src.price, ',', '') AS FLOAT64)

		-- EU both separators: 1.077,00
		WHEN src.price LIKE '%.%' AND src.price LIKE '%,%'
			THEN SAFE_CAST(
				REPLACE(REPLACE(src.price, '.', ''), ',', '.') AS FLOAT64)

		-- EU only comma: 54,00
		WHEN src.price LIKE '%,%'
			THEN SAFE_CAST(REPLACE(src.price, ',', '.') AS FLOAT64)

		-- Swiss apostrophe + dot decimal: 1'018.00
		WHEN src.price LIKE "%'%" AND src.price LIKE '%.%'
			THEN SAFE_CAST(REPLACE(src.price, "'", '') AS FLOAT64)

		-- Arabic decimal separator: 61٫00 
		WHEN src.price LIKE '%٫%'
			THEN SAFE_CAST(REPLACE(src.price, '٫', '.') AS FLOAT64)

		-- US / plain numeric: 560.00, 5000
		ELSE
			SAFE_CAST(src.price AS FLOAT64)
		END AS price

	FROM src
	LEFT JOIN {{ ref('stag_location') }} l
		ON src.ip_address = l.ip_address
),

with_rates AS (
	SELECT
		s.*
		,COALESCE(c.exchange_rate, 1.0) AS exchange_rate
		,s.price * COALESCE(c.exchange_rate, 1.0) AS price_in_usd
	FROM sales s
	LEFT JOIN {{ ref('dim_currency') }} c
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
	,ROUND(price_in_usd, 2) 			AS price_in_usd
	,ROUND(price_in_usd * amount, 2) 	AS line_total
FROM with_rates
