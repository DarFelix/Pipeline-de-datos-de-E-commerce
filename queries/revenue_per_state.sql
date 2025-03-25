-- TODO: Esta consulta devolverá una tabla con dos columnas; customer_state y Revenue.
-- La primera contendrá las abreviaturas que identifican a los 10 estados con mayores ingresos,
-- y la segunda mostrará el ingreso total de cada uno.
-- PISTA: Todos los pedidos deben tener un estado "delivered" y la fecha real de entrega no debe ser nula.
select C.customer_state AS customer_state, ROUND(SUM(B.payment_value),10) AS Revenue
FROM olist_orders AS A
LEFT JOIN olist_order_payments AS B
ON A.order_id = B.order_id 
LEFT JOIN olist_customers AS C ON A.customer_id  = C.customer_id
where A.order_status = 'delivered' AND A.order_delivered_customer_date IS NOT NULL
GROUP BY customer_state ORDER BY Revenue DESC LIMIT 10;