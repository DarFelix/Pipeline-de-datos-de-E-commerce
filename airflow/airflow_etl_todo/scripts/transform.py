import sqlite3

# Pistas 
# 1. Conectarse a la base de datos donde están las tablas Silver 
# 2. Guarda los queries realizados en el trabajo pasado como un string => Gold

def transform_data():
    db_path = '/opt/airflow/dags/data/ecommerce.db'
    #TODO conexión
    try: 
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        #TODO Query 1: Top 10 Estados con mayor ingreso (str)
        query1 = """
        CREATE TABLE gold_top_states AS
        SELECT
            A.customer_state,
            A.customer_city,
            sum(C.payment_value) as Revenue
        FROM silver_olist_customers AS A
        left join silver_olist_orders AS B
        ON A.customer_id = B.customer_id
        left join silver_olist_order_payments AS C
        ON B.order_id = C.order_id
        WHERE 
        B.order_status = 'delivered' AND B.order_delivered_customer_date IS NOT NULL
        GROUP BY 
            A.customer_state 
        ORDER BY
            Revenue desc 
        LIMIT 10;
        """
        
        #TODO Query 2: Comparación de tiempos reales vs estimados por mes y año (str)
        query2 = """
        CREATE TABLE gold_delivery_comparison AS
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
                silver_olist_orders
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
        """
        
        #TODO ELiminar la tabla si existe gold_top_states, gold_delivery_comparison
        query_drops = """
        DROP TABLE IF EXISTS gold_top_states;
        DROP TABLE IF EXISTS gold_delivery_comparison;
        """
        cursor.executescript(query_drops)

        print("🚀 Ejecutando queries para crear tablas Gold...")
        cursor.executescript(query1)
        cursor.executescript(query2)
        print("✅ Tablas Gold creadas en ecommerce.db: 'gold_top_states' y 'gold_delivery_comparison'")

    except Exception as err:
        print(f"❌ Error en etapa de transformación: {err}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("🔒 Conexión cerrada.")