

WITH src AS (
	SELECT *
	FROM `symmetric-fin-469415-q9`.`glamira_data_2025`.`product_name`
)

,casted AS (
	SELECT
		src.product_id 			AS product_id
		,src.name 				AS product_name
		,src.sku 				AS sku
		,src.gender 			AS gender
		,src.max_price_format 	AS max_price_format
		,src.min_price_format 	AS min_price_format
		,src.type_id 			AS type_id
		,src.store_code 		AS store_code
	FROM src
)

,missing_from_sales AS (
    -- find product_ids used in sales but missing in product_name
    SELECT DISTINCT
        s.product_id
		,'Unknown Product' 	AS product_name
		,'Unknown'         	AS sku
		,'Unknown'         	AS gender
		,'Unknown'         	AS max_price_format
		,'Unknown'         	AS min_price_format
		,'Unknown'         	AS type_id
		,'Unknown'         	AS store_code
    FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_sales` s
    LEFT JOIN casted p
      	ON s.product_id = p.product_id
    WHERE s.product_id IS NOT NULL
      	AND p.product_id IS NULL
)

SELECT * FROM casted
UNION ALL
SELECT * FROM missing_from_sales