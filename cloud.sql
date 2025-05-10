SELECT
  date,
  actual_state,
  close,
  forecast
FROM (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY FORMAT_DATE('%Y-%m', date) ORDER BY date DESC) AS rn
  FROM `projeto-case-459220.Case.ism_pmi_eua`
)
WHERE rn = 1
ORDER BY date
LIMIT 1000