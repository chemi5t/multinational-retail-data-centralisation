"orders_table. Casting columns to the correct data_types"

SELECT * 
FROM dim_date_times;

-- Task 1
ALTER TABLE orders_table
    ALTER COLUMN date_uuid TYPE UUID USING (date_uuid::UUID),
    ALTER COLUMN user_uuid TYPE UUID USING (user_uuid::UUID),
    ALTER COLUMN card_number TYPE VARCHAR(255) USING (card_number::VARCHAR(255)), -- appropriate length
    ALTER COLUMN store_code TYPE VARCHAR(255) USING (store_code::VARCHAR(255)), -- appropriate length
    ALTER COLUMN product_code TYPE VARCHAR(255) USING (product_code::VARCHAR(255)), -- appropriate length
    ALTER COLUMN product_quantity TYPE SMALLINT USING (product_quantity::SMALLINT);

-- Task 2
ALTER TABLE dim_users
    ALTER COLUMN first_name TYPE VARCHAR(255) USING (first_name::VARCHAR(255)),
    ALTER COLUMN last_name TYPE VARCHAR(255) USING (last_name::VARCHAR(255)),
    ALTER COLUMN date_of_birth TYPE DATE USING (date_of_birth::DATE),
    ALTER COLUMN country_code TYPE VARCHAR(255) USING (country_code::VARCHAR(255)), -- appropriate length
    ALTER COLUMN user_uuid TYPE UUID USING (user_uuid::UUID),
    ALTER COLUMN join_date TYPE DATE USING (join_date::DATE);

-- Task 3
ALTER TABLE dim_store_details
    ALTER COLUMN longitude TYPE FLOAT USING (longitude::FLOAT),
    ALTER COLUMN locality TYPE VARCHAR(255) USING (locality::VARCHAR(255)),
    ALTER COLUMN store_code TYPE VARCHAR(255) USING (store_code::VARCHAR(255)),  -- appropriate length
    ALTER COLUMN staff_numbers TYPE SMALLINT USING (staff_numbers::SMALLINT),
    ALTER COLUMN opening_date TYPE DATE USING (opening_date::DATE),
    ALTER COLUMN store_type TYPE VARCHAR(255) USING (store_type::VARCHAR(255)),  -- and NULLABLE ?
    ALTER COLUMN latitude TYPE FLOAT USING (latitude::FLOAT),
    ALTER COLUMN country_code TYPE VARCHAR(255) USING (country_code::VARCHAR(255)),  -- appropriate length
    ALTER COLUMN continent TYPE VARCHAR(255) USING (continent::VARCHAR(255));

-- Task 4
-- Step 1: Remove £ character from product_price
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '') 
WHERE product_price LIKE '£%';
-- Step 2: Rename product_price to product_price_(gbp)
ALTER TABLE dim_products
RENAME COLUMN product_price TO "product_price_(gbp)";
-- Step 3: Add a new column weight_class
ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(50);
-- Step 4: Update weight_class based on weight ranges
UPDATE dim_products
SET weight_class = 
    CASE 
        WHEN "weight_(kg)" >= 0 AND "weight_(kg)" < 5 THEN 'Light'
        WHEN "weight_(kg)" >= 5 AND "weight_(kg)" < 10 THEN 'Medium'
        WHEN "weight_(kg)" >= 10 AND "weight_(kg)" < 20 THEN 'Heavy'
        ELSE 'Very Heavy'
    END;

-- Task 5
-- Step 1: Rename removed to still_available
ALTER TABLE dim_products
RENAME COLUMN removed TO still_available;
-- Step 2: Change data types of columns
ALTER TABLE dim_products
    ALTER COLUMN "product_price_(gbp)" TYPE FLOAT USING ("product_price_(gbp)"::FLOAT),
    ALTER COLUMN "weight_(kg)" TYPE FLOAT USING ("weight_(kg)"::FLOAT),
    ALTER COLUMN "EAN" TYPE VARCHAR(255) USING ("EAN"::VARCHAR(255)),
    ALTER COLUMN product_code TYPE VARCHAR(255) USING (product_code::VARCHAR(255)),
    ALTER COLUMN date_added TYPE DATE USING (date_added::DATE),
    ALTER COLUMN uuid TYPE UUID USING (uuid::UUID),
    --ALTER COLUMN still_available TYPE boolean USING (still_available = 'Still_available'::text::boolean),
    ALTER COLUMN weight_class TYPE VARCHAR(255) USING (weight_class::VARCHAR(255));

ALTER TABLE dim_products
    ALTER COLUMN still_available TYPE BOOLEAN USING
    CASE
        WHEN still_available ILIKE 'Still_available' THEN TRUE
        ELSE FALSE
    END;

-- Task 6
-- Step 1: Change data types of columns
ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE VARCHAR(255) USING (month::VARCHAR(255)),
    ALTER COLUMN year TYPE VARCHAR(255) USING (year::VARCHAR(255)),
    ALTER COLUMN day TYPE VARCHAR(255) USING (day::VARCHAR(255)),
    ALTER COLUMN time_period TYPE VARCHAR(255) USING (time_period::VARCHAR(255)),
    ALTER COLUMN date_uuid TYPE UUID USING (date_uuid::UUID);

-- Task 7
-- Step 1: Change data types of columns
-- Step 1: Change data types of columns in dim_card_details table
ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(255) USING (card_number::VARCHAR(255)),
    ALTER COLUMN expiry_date TYPE VARCHAR(255) USING (expiry_date::VARCHAR(255)),
    ALTER COLUMN date_payment_confirmed TYPE DATE USING (date_payment_confirmed::DATE);

-- Task 8
-- Add primary
-- 1: 
ALTER TABLE dim_date_times
    ADD PRIMARY KEY (date_uuid);

-- 2: 
ALTER TABLE dim_users
    ADD PRIMARY KEY (user_uuid);

-- 3: 
ALTER TABLE dim_store_details
    ADD PRIMARY KEY (store_code);

-- 4:
ALTER TABLE dim_products
    ADD PRIMARY KEY (product_code);

-- 5:
ALTER TABLE dim_card_details
    ADD PRIMARY KEY (card_number);

-- Task 9
-- Add foreign key constraint
-- 1:
ALTER TABLE orders_table
    ADD CONSTRAINT fk_orders_date FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid);

-- 2:
ALTER TABLE orders_table
    ADD CONSTRAINT fk_orders_user FOREIGN KEY (user_uuid)  REFERENCES dim_users(user_uuid);

-- -- 3: 
-- ALTER TABLE orders_table
--     ADD CONSTRAINT fk_orders_store FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code);

-- 4: 
ALTER TABLE orders_table
    ADD CONSTRAINT fk_orders_product FOREIGN KEY (product_code) REFERENCES dim_products(product_code);

-- 5: 
ALTER TABLE orders_table
    ADD CONSTRAINT fk_orders_card FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number);

SELECT DISTINCT store_code FROM dim_store_details;

SELECT *
FROM orders_table
WHERE store_code IS NOT NULL  -- Assuming store_code is the column you're checking
  AND store_code NOT IN (SELECT store_code FROM dim_store_details WHERE store_code IS NOT NULL);

SELECT *
FROM dim_store_details
WHERE store_code IS NOT NULL  -- Assuming store_code is the column you're checking
  AND store_code NOT IN (SELECT store_code FROM orders_table WHERE store_code IS NOT NULL);

SELECT DISTINCT(ord.store_code)
FROM orders_table ord
WHERE NOT EXISTS
(SELECT * FROM dim_store_details dsd
WHERE dsd.store_code = ord.store_code);

SELECT DISTINCT(ord.product_code)
FROM orders_table ord
WHERE NOT EXISTS
(SELECT * FROM dim_products prod
WHERE prod.product_code = ord.product_code);

-- You can query this row like
SELECT * FROM orders_table
WHERE store_code = 'WEB-1388012W';

--Ok, nice now try to run the same in
SELECT * FROM dim_store_details
WHERE store_code = 'WEB-1388012W';