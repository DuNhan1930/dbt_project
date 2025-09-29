-- Every sales row should reference an existing product
SELECT 
  	s.sales_id
  	,s.order_id
  	,s.product_id
FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_sales` s
LEFT JOIN `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_product` p
	ON s.product_id = p.product_id
WHERE s.product_id IS NOT NULL 
  	AND p.product_id IS NULL