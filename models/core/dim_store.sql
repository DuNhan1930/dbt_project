WITH src AS (
    SELECT *
    FROM {{ ref('stag_sales') }}
)

,store AS (
    SELECT
        DISTINCT store_id
        ,CONCAT("Store ", CAST(store_id AS STRING)) AS store_name
    FROM src
)

SELECT * FROM store