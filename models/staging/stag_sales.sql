{{ config(materialized='table') }}


WITH src AS (
 SELECT *
 FROM {{ source("glamira_data", "summary") }}
),


flattened AS (
 SELECT
   GENERATE_UUID() as sales_id,
   CAST(src.order_id AS INT64) AS order_id,
   src._id AS customer_id,
   src.time_stamp AS date_id,
   src.ip AS ip_address,
   src.time_stamp AS time_stamp,
   src.local_time AS local_time,
   CAST(src.store_id AS INT64) AS store_id,
   cp.product_id AS product_id,
   cp.amount AS amount,
   cp.currency AS currency_code,
   cp.price AS price
 FROM src,
 UNNEST(src.cart_products) AS cp
 WHERE collection = 'checkout_success'
)


SELECT * FROM flattened