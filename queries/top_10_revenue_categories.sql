-- TODO: Esta consulta devolverá una tabla con las 10 categorías con mayores ingresos
-- (en inglés), el número de pedidos y sus ingresos totales. La primera columna será
-- Category, que contendrá las 10 categorías con mayores ingresos; la segunda será
-- Num_order, con el total de pedidos de cada categoría; y la última será Revenue,
-- con el ingreso total de cada categoría.
-- PISTA: Todos los pedidos deben tener un estado 'delivered' y tanto la categoría
-- como la fecha real de entrega no deben ser nulas.

---posible respuesta correcta que no tiene los mismo resultados del test

select C.product_category_name_english as Category, 
count(*) as Num_order,
sum(D.price) as Revenue
from olist_order_items as A 
left join olist_products as B 
on A.product_id  = B.product_id 
left join product_category_name_translation as C
on B.product_category_name = C.product_category_name 
left join olist_order_items as D
on A.order_id = D.order_id 
LEFT JOIN olist_orders as E
on A.order_id = E.order_id 
WHERE Category IS NOT NULL  AND 
E.order_status = 'delivered' AND E.order_delivered_customer_date IS NOT NULL
GROUP BY 
    B.product_category_name
ORDER BY 
    Revenue DESC 
LIMIT 10;