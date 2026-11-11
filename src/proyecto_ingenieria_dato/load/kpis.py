import os
import mysql.connector
import numpy as np
import pandas as pd
from mysql.connector.abstracts import MySQLCursorAbstract
from pathlib import Path
from dotenv import load_dotenv

KPIS_PATH = Path(__file__).parent.resolve() / "KPIs"

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

def get_kpis_paths(path: Path) -> list[Path]:
    '''Returns the absolute path of each kpi query'''

    filenames = os.listdir(path)
    # Add absolute path and return
    return list(map(lambda x: path / x, filenames))

def get_query(path: Path) -> str:
    '''Returns the whole query in a single string'''

    file = open(path, "r")
    query = file.read()
    file.close()
    return query

def execute_kpi(kpi_name: str, query: str) -> None:
    ''' Executes the given query'''

    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**CONN_CONFIG)
        cursor = conn.cursor()

        cursor.execute(query)
        conn.commit()

        print(f"Executed: {kpi_name}")

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
    kpis_files = get_kpis_paths(KPIS_PATH)
    print(f"|----- Executing queries in: {KPIS_PATH} -----|")
    for kpi_path in kpis_files:
        query = get_query(kpi_path)
        execute_kpi(kpi_path, query)

if __name__ == "__main__":
    main()