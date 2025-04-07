import pandas as pd
import os

def extract_data():
    urls = {
        'olist_orders': '17F6q-lhV7HOFDsxyWIy_UTZlw5g-Wauw',
        'olist_order_payments': '1iW5c438VGlzsh4yyqoikBX0hHsZZGXL2',
        'olist_customers': '1YOuXnoJrUDo20b6NBmn1ZwDy-GZ9PdYG'
    }

    bronze_dir = '/opt/airflow/dags/data/bronze'
    os.makedirs(bronze_dir, exist_ok=True)

    for name, url in urls.items():
        print(f"⬇️ Descargando {name} desde {url}")
        path = 'https://drive.google.com/uc?export=download&id='+url
        df = pd.read_csv(path)

        os.makedirs('/opt/airflow/dags/data', exist_ok=True)
        df.to_csv(f'/opt/airflow/dags/data/{name}.csv', index=False)
        print(f"✅ {name} CSV descargado y guardado.")
