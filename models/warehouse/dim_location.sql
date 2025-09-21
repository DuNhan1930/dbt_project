{{ config(materialized='table') }}

WITH src AS (
    SELECT *
    FROM {{ ref('stag_location') }}
),

location_data AS (
    SELECT DISTINCT
        location_id,
        city_name, 
        country_short_name,
        country_long_name,  
        latitude,
        longitude,
        region_name, 
        time_zone, 
        zip_code
    FROM src
)

SELECT * FROM location_data
