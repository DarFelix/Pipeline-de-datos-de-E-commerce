import logging
from typing import Dict
from pandas import DataFrame
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import SQLAlchemyError


def load(data_frames: Dict[str, DataFrame], database: Engine):
    """Load the dataframes into the sqlite database.

    Args:
        data_frames (Dict[str, DataFrame]): A dictionary with keys as the table names
        and values as the dataframes.
        database Engine: Conexión a la base de datos SQLAlchemy

    Returns:
        dict: Resultados de la operación con estado de éxito/error para cada tabla
    """
    # TODO: Implementa esta función. Por cada DataFrame en el diccionario, debes
    # usar pandas.DataFrame.to_sql() para cargar el DataFrame en la base de datos
    # como una tabla.
    # Para el nombre de la tabla, utiliza las claves del diccionario `data_frames`.

    results = {}
    
    for table_name, df in data_frames.items():
        try:
            # Se verifica que df sea realmente un DataFrame
            if not isinstance(df, DataFrame):
                raise TypeError(f"El objeto para {table_name} no es un DataFrame")
            
            # Se verifica que el DataFrame no esté vacío
            if df.empty:
                logging.warning(f"DataFrame vacío para la tabla {table_name}")
            
            # Se intentan cargar los datos
            df.to_sql(table_name, con=database, if_exists="replace")
            results[table_name] = "éxito"
            logging.info(f"Tabla {table_name} cargada exitosamente")
            
        except SQLAlchemyError as e:
            # Se capturan errores específicos de SQLAlchemy
            error_msg = str(e)
            results[table_name] = f"error: {error_msg}"
            logging.error(f"Error al cargar la tabla {table_name}: {error_msg}")
            
        except Exception as e:
            # Se captura cualquier otro error
            error_msg = str(e)
            results[table_name] = f"error: {error_msg}"
            logging.error(f"Error inesperado al cargar la tabla {table_name}: {error_msg}")
    
    return results
