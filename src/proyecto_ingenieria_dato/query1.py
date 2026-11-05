from getpass import getpass

import pandas as pd
from sqlalchemy import URL, create_engine


# Solicita la contraseña de MySQL al ejecutar el script
contrasena = getpass("Contraseña de MySQL: ")

# Prepara la conexión
url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=contrasena,
    host="localhost",
    port=3306,
    database="medicamentos_db",
    query={"charset": "utf8mb4"},
)

engine = create_engine(url)

try:
    # Lee la tabla de MySQL y la guarda en un DataFrame
    df_medicamentos = pd.read_sql(
        "SELECT * FROM medicamentos",
        con=engine,
    )

    print("Número de filas:", len(df_medicamentos))
    print("\nPrimeras filas:")
    print(df_medicamentos.head())

    Desviacion_

finally:
    # Cierra los recursos de conexión
    engine.dispose()