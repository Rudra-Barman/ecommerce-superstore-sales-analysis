
-- ============================================================
-- PostgreSQL: Create Table for Superstore Sales Dataset
-- ============================================================

DROP TABLE IF EXISTS superstore_sales;

CREATE TABLE superstore_sales (
    order_id            VARCHAR(20),
    customer_id         VARCHAR(20),
    product_id          VARCHAR(30),
    order_date          DATE,
    ship_date           DATE,
    customer_name       VARCHAR(100),
    segment             VARCHAR(20),
    city                VARCHAR(50),
    state               VARCHAR(50),
    postal_code         VARCHAR(10),
    region              VARCHAR(20),
    product_name        VARCHAR(255),
    category            VARCHAR(30),
    sub_category        VARCHAR(30),
    ship_mode           VARCHAR(30),
    shipping_duration   INTEGER,
    sales               NUMERIC(12,4),
    quantity            INTEGER,
    discount            NUMERIC(5,4),
    profit              NUMERIC(12,4),
    profit_margin_pct   NUMERIC(10,4),
    revenue_per_unit    NUMERIC(12,4),
    profit_category     VARCHAR(20),
    discount_tier       VARCHAR(20),
    is_high_discount    SMALLINT,
    order_year          SMALLINT,
    order_month         SMALLINT,
    order_quarter       SMALLINT,
    order_month_name    VARCHAR(15),
    order_day_name      VARCHAR(15),
    year_month          VARCHAR(10)
);

-- ============================================================
-- Import CSV (update path to your local file)
-- ============================================================
COPY superstore_sales
FROM '/your/path/superstore_clean.csv'
DELIMITER ','
CSV HEADER;

-- ============================================================
-- Verify Import
-- ============================================================
SELECT COUNT(*) AS total_rows FROM superstore_sales;
SELECT * FROM superstore_sales LIMIT 5;

-- ============================================================
-- Category wise sales
-- ============================================================
SELECT category, 
       ROUND(SUM(sales)::numeric, 2) AS total_sales,
       ROUND(SUM(profit)::numeric, 2) AS total_profit
FROM superstore_sales
GROUP BY category
ORDER BY total_sales DESC;
