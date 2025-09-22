{{ config(materialized='table') }}

WITH src AS (
  SELECT *
  FROM {{ ref('stag_product') }}
)

,product AS (
  SELECT
    product_id
    ,product_name
    ,sku
    ,gender
    ,max_price_format AS max_price
    ,min_price_format AS min_price
    ,type_id
    ,store_code
  FROM src
)

SELECT * FROM product