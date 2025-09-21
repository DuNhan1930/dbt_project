

WITH src AS (
    SELECT *
    FROM `symmetric-fin-469415-q9`.`glamira_data_2025`.`location`
),

casted AS (
    SELECT
        CONCAT(src.city, src.country_short, src.region) AS location_id,
        src.ip AS ip_address,
        src.city AS city_name, 
        src.country_short AS country_short_name,
        src.country_long AS country_long_name,  
        ROUND(SAFE_CAST(src.latitude AS NUMERIC), 6) AS latitude,
        ROUND(SAFE_CAST(src.longitude AS NUMERIC), 6) AS longitude,
        src.region AS region_name, 
        src.time_zone AS time_zone, 
        src.zip_code AS zip_code
    FROM src
)

SELECT * FROM casted