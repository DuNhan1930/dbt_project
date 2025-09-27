

WITH src AS (
	SELECT *
	FROM `symmetric-fin-469415-q9`.`glamira_data_2025`.`product_name`
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