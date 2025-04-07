import sqlite3
import pandas as pd
import os

#Pistas
# En este paso la idea sería quitar duplicados, manejar nulos, pero como no es el objetivo, 
# Vamos a hacer una copia espejo de los datos, simulando que los datos ya están limpios.
# 1.Conectarse a la base de datos ecommerce.db ubicada en /opt/airflow/dags/data
# 2: Elimine la tabla Silver si ya existe, cree una tabla nueva Silver copiando 
#    todo el contenido de su tabla Bronze correspondiente
#    Cada bloque debe hacer una copia de la tabla Bronze a una nueva tabla Silver
# 3: Guardar los cambios y cerrar la conexión
# 4: Usa print() para mostrar el estado del proceso

def cleaning_data():
    db_path = '/opt/airflow/dags/data/ecommerce.db'
    #TODO
    names_datasets = ['olist_customers', 'olist_order_payments', 'olist_orders']
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("🔗 Conexión establecida con la base de datos.")

        for name in names_datasets:
            try:
                query = f"""
                DROP TABLE IF EXISTS silver_{name};

                CREATE TABLE silver_{name} AS
                SELECT * FROM bronze_{name};
                """
                cursor.executescript(query)
                print(f"✅ Tabla creada: silver_{name}")

            except Exception as e:
                print(f"❌ Error procesando '{name}': {e}")

    except Exception as conn_err:
        print(f"❌ Error al conectar con la base de datos: {conn_err}")

    finally:
        if 'conn' in locals():
            conn.commit()
            conn.close()
            print("🔒 Conexión cerrada.")
