{{ config(materialized='table') }}

WITH src AS (
  SELECT *
  FROM {{ source('glamira_data', 'summary') }}
),


checkout_success AS (
  SELECT
    _id AS customer_id,
    device_id AS device_id,
    email_address AS email_address,
    resolution AS resolution,
    user_id_db AS user_id_db,
    user_agent AS user_agent 
  FROM src
  WHERE collection = 'checkout_success'
)

SELECT * FROM checkout_success