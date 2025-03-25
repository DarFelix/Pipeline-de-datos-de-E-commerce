
SELECT 
  c.customer_id ,
  c.customer_city ,
  c.customer_state ,
  o.order_id ,
  o.order_status,
  o.order_delivered_carrier_date ,
  o.order_delivered_customer_date ,
  o.order_estimated_delivery_date ,
  op.payment_type ,
  op.payment_value ,
  OOR.review_score ,
  ooi.price ,
  ooi.freight_value ,
  op2.product_id ,
  op2.product_category_name ,
  op2.product_weight_g ,
  op2.product_length_cm ,
  op2.product_height_cm ,
  op2.product_width_cm 
FROM olist_customers c
JOIN olist_orders o ON c.customer_id = o.customer_id
JOIN olist_order_payments op ON o.order_id = op.order_id
JOIN olist_order_reviews OOR ON o.order_id = OOR.order_id
LEFT JOIN olist_order_items ooi on ooi.order_id = op.order_id 
LEFT JOIN olist_products op2 on op2.product_id = ooi.product_id 



