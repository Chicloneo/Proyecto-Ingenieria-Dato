import os
import mysql.connector
import numpy as np
import pandas as pd
from mysql.connector.abstracts import MySQLCursorAbstract
from pathlib import Path
from dotenv import load_dotenv

DATA_PATH = Path(__file__).parents[3].resolve() / "data/datos_clusterizados.csv"

TABLE_NAME = "medicamentos"

load_dotenv()
CONN_CONFIG = {
    "host": "db",
    "port": 3306,
    "user": os.getenv("SQL_USER"),
    "password": os.getenv("SQL_PASSWORD"),
    "database": "MUIAAp_2026",
    "charset": "utf8mb4",
    "connection_timeout": 10,
    "autocommit": False,
}

def read_data(path: Path) -> pd.DataFrame:
    '''Creates a dataframe from the path of a CSV containing ";" as separator'''

    if not path.is_file():
        raise FileNotFoundError(f"No se encontró el CSV: {path.resolve()}")

    df = pd.read_csv(path, sep=";", encoding="utf-8")
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    '''Returns a copy dataframe with column names adapted to sql standards'''

    column_mapping = {
        "nombre": "nombre",
        "pactivos": "principios_activos",
        "labtitular": "laboratorio_titular",
        "labcomercializador": "laboratorio_comercializador",
        "dosis (mg)": "dosis_mg",
        "forma_farmaceutica_simplificada": "forma_farmaceutica",
        "estado_aut": "estado_autorizacion",
        "estado_rev": "estado_revision",
        "vias_administracion": "via_administracion",
        "comercializado": "comercializado",
        "generico": "generico",
        "afecta_conduccion": "afecta_conduccion",
        "num_principios_activos": "num_principios_activos",
        "num_excipientes": "num_excipientes",
        "Volumen_Informativo": "volumen_informativo",
        "Complejidad_Desglose": "complejidad_desglose",
        "Indicador_Riesgo": "indicador_riesgo",
        "Estado": "estado",
        "Precio venta al público con IVA": "precio_venta_publico_iva",
        "Tratamiento de larga duración": "tratamiento_larga_duracion",
        "cluster": "cluster",
    }

    df_load = df.rename(columns=column_mapping).copy()
    return df_load

def get_create_table_query() -> str:
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(512) NOT NULL,
        principios_activos VARCHAR(255) NOT NULL,
        laboratorio_titular VARCHAR(255) NOT NULL,
        laboratorio_comercializador VARCHAR(255) NOT NULL,
        dosis_mg DECIMAL(10, 2) NOT NULL,
        forma_farmaceutica VARCHAR(150) NOT NULL,
        estado_autorizacion SMALLINT NOT NULL,
        estado_revision SMALLINT NOT NULL,
        via_administracion VARCHAR(150) NOT NULL,
        comercializado TINYINT NOT NULL,
        generico TINYINT NOT NULL,
        afecta_conduccion TINYINT NOT NULL,
        num_principios_activos SMALLINT NOT NULL,
        num_excipientes SMALLINT NOT NULL,
        volumen_informativo INT NOT NULL,
        complejidad_desglose SMALLINT NOT NULL,
        indicador_riesgo SMALLINT NOT NULL,
        estado VARCHAR(100) NOT NULL,
        precio_venta_publico_iva DECIMAL(10, 2) NOT NULL,
        tratamiento_larga_duracion TINYINT NOT NULL,
        cluster INT NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
    return create_table_sql

def get_insert_query(df: pd.DataFrame) -> str:
    columns = list(df.columns)
    quoted_columns = ", ".join(f"`{column}`" for column in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    insert_sql = f"INSERT INTO {TABLE_NAME} ({quoted_columns}) VALUES ({placeholders})"

    return insert_sql

def get_rows(df: pd.DataFrame) -> list[tuple]:
    '''Returns the rows of the dataframe in format to be used with cursor.executemany()'''

    rows = list(df.itertuples(index=False, name=None))
    return rows

def load_to_mysql(df: pd.DataFrame, create: str, insert: str, rows: list[tuple]) -> None:
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**CONN_CONFIG)
        cursor = conn.cursor()
        cursor.execute(create)
        cursor.execute(f"DELETE FROM {TABLE_NAME}")
        cursor.executemany(insert, rows)

        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        sql_count = cursor.fetchone()[0]
        if sql_count != len(df):
            raise ValueError(f"El recuento no coincide: SQL={sql_count}, CSV={len(df)}")

        conn.commit()
        print(f"Carga confirmada: {sql_count} filas en {CONN_CONFIG['database']}.{TABLE_NAME}")
    except Exception:
        if conn is not None and conn.is_connected():
            conn.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()

def main():
    df = read_data(DATA_PATH)
    df = rename_columns(df)

    create_query = get_create_table_query()
    insert_query = get_insert_query(df)
    rows = get_rows(df)

    load_to_mysql(df, create_query, insert_query, rows)


if __name__ == "__main__":
    main()