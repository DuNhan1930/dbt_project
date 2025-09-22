

WITH src AS (
    SELECT *
    FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_location`
)

,location_data AS (
    SELECT DISTINCT
        location_id
        ,city_name
        ,country_short_name
        ,country_long_name
        ,latitude
        ,longitude
        ,region_name
        ,time_zone
        ,zip_code
    FROM src
)

SELECT * FROM location_data