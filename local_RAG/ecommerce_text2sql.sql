-- Ecommerce dataset - https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
CREATE SCHEMA ecommerce;
CREATE TABLE ecommerce.customers (
    customer_id VARCHAR(32),
    customer_unique_id VARCHAR(32),
    customer_zip_code_prefix VARCHAR(10),
    customer_city VARCHAR(50),
    customer_state CHAR(2)
);
COPY ecommerce.customers FROM '/Users/blessy/Downloads/olist_customers_dataset.csv'
DELIMITER ',' CSV HEADER;

CREATE TABLE ecommerce.products (
    product_id VARCHAR(32),
    product_category_name VARCHAR(50),
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
);
COPY ecommerce.products FROM '/Users/blessy/Downloads/olist_products_dataset.csv'
DELIMITER ',' CSV HEADER;

CREATE TABLE ecommerce.orders (
    order_id VARCHAR(32),
    customer_id VARCHAR(32),
    order_status VARCHAR(20),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);
COPY ecommerce.orders FROM '/Users/blessy/Downloads/olist_orders_dataset.csv'
DELIMITER ',' CSV HEADER;
