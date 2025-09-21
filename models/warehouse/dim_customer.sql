{{ config(materialized='table') }}

WITH src AS (
    SELECT *
    FROM {{ ref('stag_customer') }}
),

customer AS (
    SELECT
        customer_id,
        email_address,
        resolution,
        user_agent
    FROM src 
)

SELECT * FROM customer

