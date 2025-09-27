-- Quantity should be a positive whole number
SELECT
	sales_id
	,order_id
	,product_id
	,amount
FROM {{ ref('stag_sales') }}
WHERE amount IS NULL
    OR amount <= 0
	OR amount != SAFE_CAST(amount AS INT64)
