

WITH src AS (
    SELECT *
    FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_customer`
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
