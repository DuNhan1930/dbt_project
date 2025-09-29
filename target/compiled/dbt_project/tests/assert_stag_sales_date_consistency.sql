-- Expect DATE(date_id) == time_stamp (UTC date)
SELECT
  sales_id
  ,order_id
  ,date_id
  ,time_stamp
FROM `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales`
WHERE date_id IS NULL
   OR time_stamp IS NULL
   OR date_id != CAST(FORMAT_DATE('%Y%m%d', time_stamp) AS INT64)