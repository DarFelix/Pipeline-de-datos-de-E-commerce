-- TODO: Esta consulta devolverá una tabla con las diferencias entre los tiempos 
-- reales y estimados de entrega por mes y año. Tendrá varias columnas: 
-- month_no, con los números de mes del 01 al 12; month, con las primeras 3 letras 
-- de cada mes (ej. Ene, Feb); Year2016_real_time, con el tiempo promedio de 
-- entrega real por mes de 2016 (NaN si no existe); Year2017_real_time, con el 
-- tiempo promedio de entrega real por mes de 2017 (NaN si no existe); 
-- Year2018_real_time, con el tiempo promedio de entrega real por mes de 2018 
-- (NaN si no existe); Year2016_estimated_time, con el tiempo promedio estimado 
-- de entrega por mes de 2016 (NaN si no existe); Year2017_estimated_time, con 
-- el tiempo promedio estimado de entrega por mes de 2017 (NaN si no existe); y 
-- Year2018_estimated_time, con el tiempo promedio estimado de entrega por mes 
-- de 2018 (NaN si no existe).
-- PISTAS:
-- 1. Puedes usar la función julianday para convertir una fecha a un número.
-- 2. order_status == 'delivered' AND order_delivered_customer_date IS NOT NULL
-- 3. Considera tomar order_id distintos.

WITH delivery_times AS (
    SELECT 
        strftime('%m', order_purchase_timestamp) AS month_no,
        CASE 
            WHEN strftime('%m', order_purchase_timestamp) = '01' THEN 'Jan'
            WHEN strftime('%m', order_purchase_timestamp) = '02' THEN 'Feb'
            WHEN strftime('%m', order_purchase_timestamp) = '03' THEN 'Mar'
            WHEN strftime('%m', order_purchase_timestamp) = '04' THEN 'Apr'
            WHEN strftime('%m', order_purchase_timestamp) = '05' THEN 'May'
            WHEN strftime('%m', order_purchase_timestamp) = '06' THEN 'Jun'
            WHEN strftime('%m', order_purchase_timestamp) = '07' THEN 'Jul'
            WHEN strftime('%m', order_purchase_timestamp) = '08' THEN 'Aug'
            WHEN strftime('%m', order_purchase_timestamp) = '09' THEN 'Sep'
            WHEN strftime('%m', order_purchase_timestamp) = '10' THEN 'Oct'
            WHEN strftime('%m', order_purchase_timestamp) = '11' THEN 'Nov'
            WHEN strftime('%m', order_purchase_timestamp) = '12' THEN 'Dec'
        END AS month,
        strftime('%Y', order_purchase_timestamp) AS year,
        ROUND(AVG(JULIANDAY(order_delivered_customer_date) - JULIANDAY(order_purchase_timestamp)), 2) AS real_delivery_time,
        ROUND(AVG(JULIANDAY(order_estimated_delivery_date) - JULIANDAY(order_purchase_timestamp)), 2) AS estimated_delivery_time
    FROM 
        olist_orders
    WHERE 
        order_status = 'delivered' AND 
        order_delivered_customer_date IS NOT NULL
    GROUP BY 
        month_no, month, year
    ORDER BY
        year, month_no
)

SELECT 
    d.month_no,
    d.month,
    MAX(CASE WHEN d.year = '2016' THEN d.real_delivery_time END) AS Year2016_real_time,
    MAX(CASE WHEN d.year = '2017' THEN d.real_delivery_time END) AS Year2017_real_time,
    MAX(CASE WHEN d.year = '2018' THEN d.real_delivery_time END) AS Year2018_real_time,
    MAX(CASE WHEN d.year = '2016' THEN d.estimated_delivery_time END) AS Year2016_estimated_time,
    MAX(CASE WHEN d.year = '2017' THEN d.estimated_delivery_time END) AS Year2017_estimated_time,
    MAX(CASE WHEN d.year = '2018' THEN d.estimated_delivery_time END) AS Year2018_estimated_time
FROM 
    delivery_times d
GROUP BY 
    d.month_no, d.month
ORDER BY 
    d.month_no;