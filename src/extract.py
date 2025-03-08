from typing import Dict, List

import requests
from pandas import DataFrame, read_csv, read_json, to_datetime, concat

def temp() -> DataFrame:
    """Get the temperature data.
    Returns:
        DataFrame: A dataframe with the temperature data.
    """
    return read_csv("data/temperature.csv")

def get_public_holidays(public_holidays_url: str, year: str, code_country: str) -> DataFrame:
    """Get the public holidays for the given year for Brazil.
    Args:
        public_holidays_url (str): url to the public holidays.
        year (str): The year to get the public holidays for.
    Raises:
        SystemExit: If the request fails.
    Returns:
        DataFrame: A dataframe with the public holidays.
    """
    # TODO: Implementa esta función.
    # Debes usar la biblioteca requests para obtener los días festivos públicos del año dado.
    # La URL es public_holidays_url/{year}/BR.
    # Debes eliminar las columnas "types" y "counties" del DataFrame.
    # Debes convertir la columna "date" a datetime.
    # Debes lanzar SystemExit si la solicitud falla. Investiga el método raise_for_status
    # de la biblioteca requests.

    response = requests.get(f"{public_holidays_url}/{year}/{code_country}")
    try:
        #se verifica si la solicitud fue exitosa con el método raise_for_status()
        #si se obtiene un código de error, el flujo salta al except.
        response.raise_for_status()
        #se convierte el json de la respuesta en un dataframe
        df = read_json(response.text)
        #se convierte la columna date a tipo fecha
        df["date"] = to_datetime(df["date"])
        #se eliminan las columnas no necesarias
        df = df.drop(columns=["types", "counties"])
        #se devuelve el dataframe
        return df
    except requests.exceptions.HTTPError as err:
        #si ocurre un error en raise_for_status() se captura y se imprime el 
        #error, terminando la ejecución
        raise SystemExit(err)


def extract(
    csv_folder: str, 
    csv_table_mapping: Dict[str, str], 
    public_holidays_url: str,
    years: List[str],
    code_country: str
) -> Dict[str, DataFrame]:
    """Extract the data from the csv files and load them into the dataframes.
    Args:
        csv_folder (str): The path to the csv's folder.
        csv_table_mapping (Dict[str, str]): The mapping of the csv file names to the
        table names.
        public_holidays_url (str): The url to the public holidays.
    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the table names and values as
        the dataframes.
    """
    dataframes = {
        table_name: read_csv(f"{csv_folder}/{csv_file}")
        for csv_file, table_name in csv_table_mapping.items()
    }
    df_holidays = DataFrame()

    for year in years:
        holidays = get_public_holidays(public_holidays_url, year, code_country)
        df_holidays = concat([df_holidays, holidays], ignore_index=True)
   
    dataframes["public_holidays"] = df_holidays

    return dataframes
