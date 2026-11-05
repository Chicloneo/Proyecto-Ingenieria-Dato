from getpass import getpass
from pathlib import Path

import pandas as pd
from sqlalchemy import URL, create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError


# Ruta del CSV
RUTA_CSV = Path(
    "/Users/macbookpro/Desktop/Proyecto-Ingenieria-Dato/"
    "src/data/HU4_EDA.csv"
)

# Datos de conexión a MySQL
HOST = "localhost"
PUERTO = 3306
USUARIO = "root"
BASE_DATOS = "medicamentos_db"
TABLA = "medicamentos"


def main():
    if not RUTA_CSV.is_file():
        print(f"No se encuentra el archivo: {RUTA_CSV}")
        return

    # Solicita la contraseña sin escribirla en el código.
    contrasena = getpass("Contraseña de MySQL: ")

    # URL.create gestiona caracteres especiales de la contraseña.
    url = URL.create(
        drivername="mysql+pymysql",
        username=USUARIO,
        password= "Zunzun-1964",
        host=HOST,
        port=PUERTO,
        database=BASE_DATOS,
        query={"charset": "utf8mb4"},
    )

    engine = create_engine(url)

    try:
        # Lee los encabezados y los datos del CSV.
        datos = pd.read_csv(RUTA_CSV, encoding="utf-8-sig")

        print(f"Filas leídas: {len(datos)}")
        print("Columnas encontradas:")
        for columna in datos.columns:
            print(f"  - {columna}")
            

        # Crea la tabla e inserta los datos.
        datos.to_sql(
            name=TABLA,
            con=engine,
            if_exists="fail",
            index=False,
            chunksize=1000,
        )

        print(
            f"\nImportación terminada: {len(datos)} filas "
            f"en {BASE_DATOS}.{TABLA}."
        )

    except (SQLAlchemyError, OSError, ValueError) as error:
        print(f"\nNo se pudo completar la importación:\n{error}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()