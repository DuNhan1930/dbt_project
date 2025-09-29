-- Fails if email_address is non-null but malformed
WITH src AS (
  SELECT email_address
  FROM `symmetric-fin-469415-q9`.`glamira_data_2025_staging`.`stag_customer`
)
SELECT *
FROM src
WHERE email_address IS NOT NULL
  AND NOT REGEXP_CONTAINS(
        email_address
        ,r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
      )