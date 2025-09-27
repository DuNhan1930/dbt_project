{{ config(materialized='table') }}

WITH src AS (
	SELECT *
	FROM {{ source("glamira_data", "product_name") }}
)

,casted AS (
	SELECT
		src.product_id AS product_id
		,src.name AS product_name
		,src.sku AS sku
		,src.gender AS gender
		,src.max_price_format AS max_price_format
		,src.min_price_format AS min_price_format
		,src.type_id AS type_id
		,src.store_code AS store_code
	FROM src
)

SELECT * FROM casted