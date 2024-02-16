



-- SELECT *
-- FROM dim_card_details;
-- SELECT *
-- FROM dim_date_times;
-- SELECT *
-- FROM dim_products;
-- SELECT *
-- FROM dim_store_details;
-- SELECT *
-- FROM dim_users;
-- SELECT *
-- FROM orders_table;

-- Task 1. How many stores does the business have and in which countries?
SELECT 
	country_code as country, 
	COUNT(country_code) as total_no_stores
FROM 
	dim_store_details
WHERE store_type != 'Web Portal'
GROUP BY 
	country_code
ORDER BY 
	total_no_stores DESC;

-- Task 2. Which locations currently have the most stores?
SELECT 
	locality, 
	COUNT(locality) as total_no_stores
FROM 
	dim_store_details
WHERE 
	store_type != 'Web Portal'
GROUP BY 
	locality
ORDER BY 
	total_no_stores DESC
LIMIT 7;

-- Task 3. Which months produced the largest amount of sales
SELECT 
	ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales, ddt.month
FROM 
	dim_products AS dp
JOIN 
	orders_table AS ot
ON 
	dp.product_code = ot.product_code
JOIN 
	dim_date_times AS ddt 
ON 
	ot.date_uuid = ddt.date_uuid
GROUP BY 
	ddt.month
ORDER BY 
	total_sales DESC
LIMIT 
	6;

-- Task 4. How many sales are coming from online? 
SELECT
	COUNT(dsd.store_type) AS number_of_sales,
	SUM(ot.product_quantity) AS product_quantity_count,
    CASE 
        WHEN dsd.store_type = 'Web Portal' THEN 'Web' 
        ELSE 'Offline' 
    END AS location
FROM 
    dim_store_details AS dsd
JOIN orders_table as ot
ON dsd.store_code = ot.store_code
GROUP BY 
    location
ORDER BY number_of_sales ASC;

-- Task 5. What percentage of sales come through each type of store?
WITH sum_of_sales AS (
    SELECT dsd.store_type, 
           ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales
    FROM dim_products AS dp
    JOIN orders_table AS ot ON dp.product_code = ot.product_code
    JOIN dim_store_details AS dsd ON ot.store_code = dsd.store_code
    GROUP BY dsd.store_type
),
total_sales_all AS (
    SELECT ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales
    FROM dim_products AS dp
    JOIN orders_table AS ot ON dp.product_code = ot.product_code
)
SELECT sum_of_sales.store_type, 
       ROUND(sum_of_sales.total_sales, 2) AS average_sum_of_payments, 
       ROUND((sum_of_sales.total_sales / total_sales_all.total_sales) * 100, 2) AS "percentage_total(%)"
FROM sum_of_sales
CROSS JOIN total_sales_all
ORDER BY average_sum_of_payments DESC;

-- Task 6b. Which months in each year produced the highest cost of sales?
SELECT
	ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales,
	ddt.year,
	ddt.month
FROM dim_date_times AS ddt
JOIN orders_table AS ot
ON ddt.date_uuid = ot.date_uuid
JOIN dim_products AS dp
ON ot.product_code = dp.product_code
GROUP BY 
	ddt.year,
	ddt.month
ORDER BY total_sales DESC
LIMIT 10;

-- Otherwise if we were to target the month alone that has the most sales from each year alone then see below.

-- Task 6a. Which month in each year produced the highest cost of sales?
WITH monthly_sales AS (
	SELECT
		ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales,
		ddt.year,
		ddt.month,
		ROW_NUMBER() OVER (PARTITION BY ddt.year ORDER BY SUM(ot.product_quantity * dp."product_price_(gbp)") DESC) AS month_rank
	FROM dim_date_times AS ddt
	JOIN orders_table AS ot ON ddt.date_uuid = ot.date_uuid
	JOIN dim_products AS dp ON ot.product_code = dp.product_code
	GROUP BY 
		ddt.year,
		ddt.month
)
SELECT
	ms.total_sales,
	ms.year,
	ms.month
FROM
	monthly_sales AS ms
WHERE
	month_rank = 1
ORDER BY
	total_sales DESC
LIMIT 10;

-- Task 7. What is our staff headcount?
SELECT 
	SUM(staff_numbers) AS total_staff_numbers,
	country_code
FROM 
	dim_store_details
GROUP BY
	country_code
ORDER BY 
	total_staff_numbers DESC;

-- Task 8. Which German store type is selling the most?
SELECT
	ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales,
	dsd.store_type,
	dsd.country_code
FROM 
	dim_store_details AS dsd
JOIN
	orders_table AS ot
ON
	dsd.store_code =  ot.store_code
JOIN 
	dim_products AS dp
ON
	ot.product_code = dp.product_code
WHERE
	dsd.country_code = 'DE'
GROUP BY
	dsd.store_type, dsd.country_code
ORDER BY
	total_sales 
LIMIT 10;


-- Task 9: How quickly is the company making sales?
-- work in progress
SELECT ddt.year, ROUND(8760/COUNT(ddt.year)::numeric, 4) AS average_time_between_sales_in_a_year
FROM orders_table AS ot
JOIN dim_date_times AS ddt
ON ot.date_uuid = ddt.date_uuid
GROUP BY ddt.year
ORDER BY average_time_between_sales_in_a_year DESC;

