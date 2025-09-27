-- Fails if any sales.ip_address is NOT a valid IPv4
-- Accepts 0–255 for each octet; rejects blanks/nulls and malformed strings.
WITH src AS (
    SELECT ip_address
    FROM {{ ref('stag_sales') }}
)
SELECT *
FROM src
WHERE ip_address IS NULL
    OR NOT REGEXP_CONTAINS(
        ip_address
        ,r'^((25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(25[0-5]|2[0-4]\d|1?\d?\d)$'
        )
