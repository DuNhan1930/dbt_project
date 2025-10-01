WITH src AS (
    SELECT *
    FROM {{ source("glamira_data", "location") }}
)

,casted AS (
    SELECT
        CAST(
        FARM_FINGERPRINT(
            CONCAT(
            COALESCE(src.city, ''), 
            COALESCE(src.country_short, ''), 
            COALESCE(src.region, '')
            )
        ) AS STRING
        ) AS location_id

        ,src.ip                 AS ip_address
        ,src.city               AS city_name
        ,src.country_short      AS country_short_name
        ,src.country_long       AS country_long_name

        ,ROUND(SAFE_CAST(src.latitude AS NUMERIC), 6)   AS latitude
        ,ROUND(SAFE_CAST(src.longitude AS NUMERIC), 6)  AS longitude

        ,src.region             AS region_name
        ,src.time_zone          AS time_zone
    FROM src
    WHERE REGEXP_CONTAINS(
        src.ip,
        r'^(25[0-5]|2[0-4]\d|[01]?\d?\d)(\.(25[0-5]|2[0-4]\d|[01]?\d?\d)){3}$'
    )
)

SELECT * FROM casted