import sqlite3
import pandas as pd
import os

def load_data():
    db_path = '/opt/airflow/dags/data/ecommerce.db'
    conn = sqlite3.connect(db_path)

    # Diccionario: nombre de tabla → nombre de archivo CSV
    files = {
        'bronze_olist_orders': 'olist_orders.csv',
        'bronze_olist_order_payments': 'olist_order_payments.csv',
        'bronze_olist_customers': 'olist_customers.csv'
    }

    bronze_dir = '/opt/airflow/dags/data'

    for table_name, file_name in files.items():
        file_path = os.path.join(bronze_dir, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ No se encontró el archivo: {file_path}")

        df = pd.read_csv(file_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"✅ Cargado {file_name} como tabla '{table_name}' en SQLite.")

    conn.close()
    print("✅ Todos los archivos han sido cargados correctamente en ecommerce.db.")
