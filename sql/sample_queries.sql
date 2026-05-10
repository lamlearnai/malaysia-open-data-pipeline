-- 1. View latest fuel price
SELECT *
FROM gold_fuel_latest_price;


-- 2. View latest 10 monthly average fuel prices
SELECT month, ron95, ron97, diesel, diesel_eastmsia
FROM gold_fuel_monthly_average
ORDER BY month DESC
LIMIT 10;


-- 3. Find top 5 highest monthly average RON97 prices
SELECT month, ron97
FROM gold_fuel_monthly_average
ORDER BY ron97 DESC
LIMIT 5;


-- 4. Find top 5 lowest monthly average RON97 prices
SELECT month, ron97
FROM gold_fuel_monthly_average
ORDER BY ron97 ASC
LIMIT 5;


-- 5. Compare average fuel prices across all available months
SELECT 
    ROUND(AVG(ron95), 3) AS avg_ron95,
    ROUND(AVG(ron97), 3) AS avg_ron97,
    ROUND(AVG(diesel), 3) AS avg_diesel,
    ROUND(AVG(diesel_eastmsia), 3) AS avg_diesel_eastmsia
FROM gold_fuel_monthly_average;


-- 6. Find months where RON97 monthly average is above RM 4.00
SELECT month, ron97
FROM gold_fuel_monthly_average
WHERE ron97 > 4.00
ORDER BY ron97 DESC;


-- 7. View weekly changes for recent records
SELECT 
    date,
    ron95,
    ron95_change,
    ron97,
    ron97_change,
    diesel,
    diesel_change
FROM gold_fuel_weekly_change
ORDER BY date DESC
LIMIT 20;


-- 8. Find biggest weekly RON97 increase
SELECT date, ron97, ron97_change
FROM gold_fuel_weekly_change
ORDER BY ron97_change DESC
LIMIT 5;


-- 9. Find biggest weekly RON97 decrease
SELECT date, ron97, ron97_change
FROM gold_fuel_weekly_change
ORDER BY ron97_change ASC
LIMIT 5;


-- 10. Count records in each gold table
SELECT 'gold_fuel_monthly_average' AS table_name, COUNT(*) AS total_rows
FROM gold_fuel_monthly_average

UNION ALL

SELECT 'gold_fuel_latest_price' AS table_name, COUNT(*) AS total_rows
FROM gold_fuel_latest_price

UNION ALL

SELECT 'gold_fuel_weekly_change' AS table_name, COUNT(*) AS total_rows
FROM gold_fuel_weekly_change;