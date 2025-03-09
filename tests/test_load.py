import pytest
import pandas as pd
from unittest.mock import Mock, patch
from sqlalchemy.exc import SQLAlchemyError
from pandas import DataFrame
from sqlalchemy.engine import Engine
from src.load import load

#se hace una imitación de la interfaz de la clase Engine
@pytest.fixture
def mock_engine():
    return Mock(spec=Engine)

#se crean 2 dataframes de pruebas con información
@pytest.fixture
def valid_data_frames():
    df1 = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
    df2 = pd.DataFrame({'col3': [4, 5, 6], 'col4': ['d', 'e', 'f']})
    return {
        'table1': df1,
        'table2': df2
    }

#se crean 2 dataframes de pruebas, uno vacío
@pytest.fixture
def data_frames_with_empty():
    df1 = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
    empty_df = pd.DataFrame()
    return {
        'table1': df1,
        'empty_table': empty_df
    }

#se crean 1 dataframe para pruebas y un valor de tipo string para probar si el tipo de dato
#no es un dataframe
@pytest.fixture
def invalid_data_frames():
    df1 = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
    return {
        'table1': df1,
        'not_a_df': "esto no es un dataframe"
    }

#prueba para simular carga exitosa en la bd
@patch('logging.info')
@patch('logging.warning')
@patch('logging.error')
def test_successful_load(mock_error, mock_warning, mock_info, valid_data_frames, mock_engine):
    # Test para el caso exitoso
    with patch.object(DataFrame, 'to_sql') as mock_to_sql:
        results = load(valid_data_frames, mock_engine)
        
        # se verifica que to_sql fue llamado dos veces (una por cada DataFrame)
        assert mock_to_sql.call_count == 2
        
        # se validan los resultados
        assert results['table1'] == "éxito"
        assert results['table2'] == "éxito"
        
        # se verifica que se registraron mensajes de éxito
        assert mock_info.call_count == 2
        assert mock_warning.call_count == 0
        assert mock_error.call_count == 0

#prueba para caso de carga de dataframe vacío
@patch('logging.info')
@patch('logging.warning')
@patch('logging.error')
def test_empty_dataframe(mock_error, mock_warning, mock_info, data_frames_with_empty, mock_engine):
    # Test para el caso de DataFrame vacío
    with patch.object(DataFrame, 'to_sql') as mock_to_sql:
        results = load(data_frames_with_empty, mock_engine)
        
        # se verifica que to_sql fue llamado dos veces
        assert mock_to_sql.call_count == 2
        
        # se verifica los resultados
        assert results['table1'] == "éxito"
        assert results['empty_table'] == "éxito"
        
        # se verifica que se registró una advertencia para el DataFrame vacío
        assert mock_warning.call_count == 1
        assert mock_info.call_count == 2
        assert mock_error.call_count == 0

#prueba para caso de error de SQLAlchemy
@patch('logging.info')
@patch('logging.warning')
@patch('logging.error')
def test_sqlalchemy_error(mock_error, mock_warning, mock_info, valid_data_frames, mock_engine):
    with patch.object(DataFrame, 'to_sql') as mock_to_sql:
        # se configura to_sql para que lance una excepción SQLAlchemyError
        mock_to_sql.side_effect = SQLAlchemyError("Error de conexión")
        
        results = load(valid_data_frames, mock_engine)
        
        # se verifica los resultados
        assert results['table1'].startswith("error: ")
        assert results['table2'].startswith("error: ")
        
        # se verifica mensajes de log
        assert mock_info.call_count == 0
        assert mock_error.call_count == 2

#prueba de lanzamiento de excepción general
@patch('logging.info')
@patch('logging.warning')
@patch('logging.error')
def test_general_exception(mock_error, mock_warning, mock_info, valid_data_frames, mock_engine):
    # Test para el caso de una excepción general
    with patch.object(DataFrame, 'to_sql') as mock_to_sql:
        # se configura to_sql para que lance una excepción general
        mock_to_sql.side_effect = Exception("Error inesperado")
        
        results = load(valid_data_frames, mock_engine)
        
        # se verifica los resultados
        assert results['table1'].startswith("error: ")
        assert results['table2'].startswith("error: ")
        
        # se verifica mensajes de log
        assert mock_info.call_count == 0
        assert mock_error.call_count == 2