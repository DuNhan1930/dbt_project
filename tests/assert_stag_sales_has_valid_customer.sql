-- Every sales row should reference an existing customer/session
SELECT 
	s.sales_id
	,s.order_id
	,s.customer_id
FROM {{ ref('stag_sales') }} s
LEFT JOIN {{ ref('stag_customer') }} c
	ON s.customer_id = c.customer_id
WHERE s.customer_id IS NOT NULL
	AND c.customer_id IS NULL
