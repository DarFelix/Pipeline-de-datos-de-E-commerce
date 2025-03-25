-- TODO: Esta consulta devolverá una tabla con los ingresos por mes y año.
-- Tendrá varias columnas: month_no, con los números de mes del 01 al 12;
-- month, con las primeras 3 letras de cada mes (ej. Ene, Feb);
-- Year2016, con los ingresos por mes de 2016 (0.00 si no existe);
-- Year2017, con los ingresos por mes de 2017 (0.00 si no existe); y
-- Year2018, con los ingresos por mes de 2018 (0.00 si no existe).

--posible respuesta correcta pero con resultados diferentes al test: 
---------query solitada-------------

WITH OrderRevenue AS (
    SELECT 
        strftime('%m', A.order_delivered_customer_date) AS month_no,
        CASE strftime('%m', A.order_delivered_customer_date)
            WHEN '01' THEN 'Jan'
            WHEN '02' THEN 'Feb'
            WHEN '03' THEN 'Mar'
            WHEN '04' THEN 'Apr'
            WHEN '05' THEN 'May'
            WHEN '06' THEN 'Jun'
            WHEN '07' THEN 'Jul'
            WHEN '08' THEN 'Aug'
            WHEN '09' THEN 'Sep'
            WHEN '10' THEN 'Oct'
            WHEN '11' THEN 'Nov'
            WHEN '12' THEN 'Dec'
        END AS month,
        strftime('%Y', A.order_delivered_customer_date) AS year,
        B.payment_value AS revenue
    FROM olist_orders AS A
    LEFT JOIN olist_order_payments AS B ON A.order_id = B.order_id
    WHERE A.order_status = 'delivered' 
      AND A.order_delivered_customer_date IS NOT NULL
)

SELECT 
    month_no,
    month,
    ROUND(SUM(CASE WHEN year = '2016' THEN revenue ELSE 0 END), 2) AS Year2016,
    ROUND(SUM(CASE WHEN year = '2017' THEN revenue ELSE 0 END), 2) AS Year2017,
    ROUND(SUM(CASE WHEN year = '2018' THEN revenue ELSE 0 END), 2) AS Year2018
FROM OrderRevenue
GROUP BY month_no, month
ORDER BY month_no

/*
-------prueba para enero de 2018---------

select sum(B.payment_value)
FROM olist_orders AS A
LEFT JOIN olist_order_payments AS B
ON A.order_id = B.order_id 
where A.order_status = 'delivered' AND A.order_delivered_customer_date IS NOT NULL and 
	strftime('%Y-%m-%d', A.order_delivered_customer_date) >= '2018-01-01' 
  AND strftime('%Y-%m-%d', A.order_delivered_customer_date) <= '2018-01-31'


(resultado: 993588.74, diferente a 969967.80)
*/


