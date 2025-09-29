

WITH src AS (
    SELECT *
    FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_sales`
)

,date_ AS (
    SELECT DISTINCT
        CAST(FORMAT_DATE('%Y%m%d', DATE(TIMESTAMP_SECONDS(src.time_stamp))) AS INT64) AS date_id
        ,DATE(TIMESTAMP_SECONDS(src.time_stamp)) AS full_date
    FROM src
)

SELECT
    date_id
    ,full_date
    ,FORMAT_DATE('%A', full_date) AS day_of_week

    ,CASE 
        WHEN EXTRACT(DAYOFWEEK FROM full_date) IN (1,7) 
            THEN TRUE 
        ELSE 
            FALSE 
    END AS is_weekend
    
    ,EXTRACT(DAY FROM full_date)        AS day_of_month
    ,FORMAT_DATE('%Y-%m', full_date)    AS year_month
    ,EXTRACT(MONTH FROM full_date)      AS month
    ,EXTRACT(ISOWEEK FROM full_date)    AS week_of_year
    ,CONCAT('Q', CAST(EXTRACT(QUARTER FROM full_date) AS STRING)) AS quarter_number
    ,CAST(EXTRACT(YEAR FROM full_date) AS STRING) AS year
    ,EXTRACT(YEAR FROM full_date) AS year_number
FROM date_
ORDER BY full_date