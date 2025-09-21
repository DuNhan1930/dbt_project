

WITH src AS (
    SELECT *
    FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_sales`
),

store AS (
    SELECT
        DISTINCT store_id,
        CONCAT("Store ", CAST(store_id AS STRING)) AS store_name
    FROM src
)

SELECT * FROM store