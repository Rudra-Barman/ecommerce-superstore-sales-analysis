-- ── Q1: Yearly Revenue Growth ─────────────────────────────
SELECT 
    order_year,
    ROUND(SUM(sales)::numeric, 2) AS total_sales,
    ROUND(SUM(profit)::numeric, 2) AS total_profit,
    ROUND((SUM(profit)/SUM(sales)*100)::numeric, 2) AS profit_margin_pct
FROM superstore_sales
GROUP BY order_year
ORDER BY order_year;

-- ── Q2: Top 5 Most Profitable Products ────────────────────
SELECT 
    product_name,
    category,
    ROUND(SUM(profit)::numeric, 2) AS total_profit,
    COUNT(*) AS order_count
FROM superstore_sales
GROUP BY product_name, category
ORDER BY total_profit DESC
LIMIT 5;

-- ── Q3: Top 5 Loss-Making Products ────────────────────────
SELECT 
    product_name,
    category,
    ROUND(SUM(profit)::numeric, 2) AS total_profit,
    COUNT(*) AS order_count
FROM superstore_sales
GROUP BY product_name, category
ORDER BY total_profit ASC
LIMIT 5;

-- ── Q4: Region wise Performance ───────────────────────────
SELECT 
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales)::numeric, 2) AS total_sales,
    ROUND(SUM(profit)::numeric, 2) AS total_profit,
    ROUND(AVG(discount)::numeric*100, 2) AS avg_discount_pct
FROM superstore_sales
GROUP BY region
ORDER BY total_profit DESC;

-- ── Q5: Discount Impact on Profit ─────────────────────────
SELECT 
    discount_tier,
    COUNT(*) AS total_orders,
    ROUND(AVG(profit)::numeric, 2) AS avg_profit,
    ROUND(SUM(profit)::numeric, 2) AS total_profit
FROM superstore_sales
GROUP BY discount_tier
ORDER BY avg_profit DESC;

-- ── Q6: Monthly Sales Trend 2017 ──────────────────────────
SELECT 
    order_month_name,
    order_month,
    ROUND(SUM(sales)::numeric, 2) AS total_sales,
    ROUND(SUM(profit)::numeric, 2) AS total_profit
FROM superstore_sales
WHERE order_year = 2017
GROUP BY order_month_name, order_month
ORDER BY order_month;

-- ── Q7: Customer Segment Analysis ─────────────────────────
SELECT 
    segment,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales)::numeric, 2) AS total_sales,
    ROUND(AVG(sales)::numeric, 2) AS avg_order_value
FROM superstore_sales
GROUP BY segment
ORDER BY total_sales DESC;

-- ── Q8: Ship Mode Efficiency ───────────────────────────────
SELECT 
    ship_mode,
    COUNT(*) AS total_orders,
    ROUND(AVG(shipping_duration)::numeric, 1) AS avg_ship_days,
    ROUND(AVG(profit)::numeric, 2) AS avg_profit
FROM superstore_sales
GROUP BY ship_mode
ORDER BY avg_profit DESC;

-- ── Q9: States with Negative Profit ───────────────────────
SELECT 
    state,
    ROUND(SUM(sales)::numeric, 2) AS total_sales,
    ROUND(SUM(profit)::numeric, 2) AS total_profit,
    COUNT(*) AS total_orders
FROM superstore_sales
GROUP BY state
HAVING SUM(profit) < 0
ORDER BY total_profit ASC;

-- ── Q10: YoY Growth Rate ──────────────────────────────────
SELECT 
    order_year,
    ROUND(SUM(sales)::numeric, 2) AS total_sales,
    ROUND(
        (SUM(sales) - LAG(SUM(sales)) OVER (ORDER BY order_year)) 
        / LAG(SUM(sales)) OVER (ORDER BY order_year) * 100
    ::numeric, 2) AS yoy_growth_pct
FROM superstore_sales
GROUP BY order_year
ORDER BY order_year;