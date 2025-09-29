-- Fails if computed or stored line_total is negative
WITH src AS (
    SELECT
        line_total
        ,price_in_usd
        ,amount
    FROM `symmetric-fin-469415-q9`.`glamira_data_2025_core`.`fact_sales`
),
calc AS (
    SELECT
        COALESCE(line_total, price_in_usd * amount) AS effective_line_total
        ,*
    FROM src
)
SELECT *
FROM calc
WHERE SAFE_CAST(effective_line_total AS NUMERIC) < 0