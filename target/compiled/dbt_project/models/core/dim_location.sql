

WITH src AS (
    SELECT *
    FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_location`
)

,location_data AS (
    SELECT
        location_id,
        ANY_VALUE(city_name)            AS city_name,
        ANY_VALUE(country_short_name)   AS country_short_name,
        ANY_VALUE(country_long_name)    AS country_long_name,
        AVG(latitude)                   AS latitude,         
        AVG(longitude)                  AS longitude,
        ANY_VALUE(region_name)          AS region_name,
        ANY_VALUE(time_zone)            AS time_zone
    FROM src
    GROUP BY location_id
)

SELECT * FROM location_data