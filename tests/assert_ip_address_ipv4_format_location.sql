-- Fails if any location.ip_address is NOT a valid IPv4
WITH src AS (
  SELECT ip_address
  FROM {{ ref('stag_location') }}
)
SELECT *
FROM src
WHERE ip_address IS NULL
   OR NOT REGEXP_CONTAINS(
         ip_address,
         r'^((25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(25[0-5]|2[0-4]\d|1?\d?\d)$'
       )
