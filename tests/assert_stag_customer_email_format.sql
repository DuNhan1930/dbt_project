-- Fails if email_address is non-null but malformed
WITH src AS (
  SELECT email_address
  FROM {{ ref('stag_customer') }}
)
SELECT *
FROM src
WHERE email_address IS NOT NULL
  AND NOT REGEXP_CONTAINS(
        email_address
        ,r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
      )
