-- Expect DATE(date_id) == time_stamp (UTC date)
SELECT
  sales_id
  ,order_id
  ,date_id
  ,time_stamp
FROM {{ ref('stag_sales') }}
WHERE date_id IS NULL
   OR time_stamp IS NULL
   OR DATE(date_id) != time_stamp
