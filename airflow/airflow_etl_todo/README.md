# ✈️ ETL con Apache Airflow, SQLite y Streamlit

Proyecto educativo para aprender a construir pipelines ETL usando Apache Airflow, almacenar datos en SQLite y visualizarlos en un dashboard interactivo con Streamlit.

En este caso trabajaremos con los datos de. E-commerce Olist

---

Objetivo: Completar las tareas faltantes en el DAG y desarrollar los módulos correspondientes a la etapa de limpieza (Silver) y transformación (Gold) para consolidar un pipeline ETL en Airflow.

---

🧩 Parte 1: Completa el DAG.

En esta primera parte, debes completar la definición del DAG importando las funciones cleaning_data y transform_data desde sus respectivos scripts. Luego, agrega dos tareas al flujo: una para la limpieza de datos correspondiente al stage Silver (task_id='cleaning_data') y otra para la transformación de datos en el stage Gold (task_id='transform_data'), asignando en cada caso la función correspondiente como python_callable. A continuación, define la secuencia completa del pipeline utilizando operadores de dependencia para que las tareas se ejecuten en el orden correcto: extract >> load >> [...]. Finalmente, configura una periodicidad de ejecución adecuada; si estás en modo de prueba, puedes usar '@once' para que el DAG se ejecute una sola vez al activarlo.

---

🧪 Parte 2: Crea los módulos cleaning.py y transform.py.

En la segunda parte, tu objetivo es construir los módulos cleaning.py y transform.py que se encargan de las etapas Silver y Gold del pipeline. 

En cleaning.py, debes conectarte a la base de datos ecommerce.db ubicada en /opt/airflow/dags/data, y crear tres tablas silver_* como copias exactas de las tablas bronze_* utilizando sentencias SQL del tipo CREATE TABLE AS SELECT. Aunque normalmente este paso incluiría limpieza de datos (duplicados, nulos, formatos), en este caso solo simularás la limpieza realizando una copia espejo. No olvides cerrar la conexión y utilizar print() para mostrar mensajes informativos sobre el estado del proceso. 

En transform.py, trabajarás sobre las tablas Silver y ejecutarás dos consultas SQL que ya formulaste previamente: una para calcular el top 10 de estados con mayor ingreso (gold_top_states), y otra para comparar los tiempos de entrega reales vs. estimados por mes y año (gold_delivery_comparison). Ambas consultas deben ser definidas como cadenas de texto y ejecutadas con cursor.executescript(...). Finalmente, confirma la ejecución exitosa con mensajes por consola y cierra la conexión correctamente.

---

🎬 Parte 3: Presentación en video + Análisis del dashboard

En esta etapa final, deberás realizar una presentación en video donde expliques el flujo completo de tu pipeline ETL construido con Airflow. En el video, describe brevemente qué hace cada etapa del código (extract, load, clean, transform) y cómo se conectan entre sí dentro del DAG. Además, incluye una navegación por el dashboard desarrollado en Streamlit. Explica cómo se visualizan los resultados generados a partir de las tablas gold_top_states y gold_delivery_comparison.

A continuación, realiza un análisis crítico del dashboard. Responde: ¿Qué datos relevantes se pueden obtener? ¿Qué patrones o hallazgos llaman la atención? ¿Qué decisiones podría tomar la compañía a partir de esta información? Por ejemplo, ¿hay estados que claramente deberían recibir más atención? ¿Existen diferencias estacionales en los tiempos de entrega que afecten la experiencia del cliente?

Por último, propón al menos dos recomendaciones de negocio basadas en los datos analizados, y una posible mejora al pipeline o al dashboard que podrías implementar en una futura iteración.

## 📄 Licencia
Este proyecto está bajo la licencia MIT.
Puedes usarlo, modificarlo y compartirlo libremente con atribución.

## ✨ Autor
Desarrollado por @SharonCamacho para enseñar y aprender pipelines y visualización.

