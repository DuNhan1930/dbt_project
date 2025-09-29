-- Quantity should be a positive whole number
SELECT
	sales_id
	,order_id
	,product_id
	,amount
FROM `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales`
WHERE amount IS NULL
    OR amount <= 0
	OR amount != SAFE_CAST(amount AS INT64)