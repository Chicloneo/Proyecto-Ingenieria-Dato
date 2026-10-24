import pandas as pd
from pandas import DataFrame
from pathlib import Path
import numpy as np
import sys
from .contracts import Medicamento

COLUMNAS_A_ELIMINAR = columnas_a_eliminar = [
    "nregistro", 
    "cn",
    "Código Nacional",
    "url_html_ficha_tecnica",
    "url_foto_materiales",
    "Precio de referencia",
    "requiere_receta",
    "triangulo_negro", 
    "medicamento_huerfano", 
    "biosimilar", 
    "num_registros_atc", 
    "num_excipientes",
    "Especial control médico"
]

MAIN_DIR = Path(__file__).resolve().parent

RUTA_INPUT = Path(MAIN_DIR).parent / "data" / "HU-3.csv"
#RUTA_INPUT = Path(MAIN_DIR).parent / "data" / "catalogo_enriquecido.xlsx"

RUTA_FECHAS = Path(MAIN_DIR).parent / "data" / "medicamentos_web_scrapping.xlsx"

RUTA_EXPORT = Path(MAIN_DIR).parent / "data" / "HU4_EDA.csv"

def leer_excel(ruta=RUTA_INPUT) -> DataFrame:
    ruta_input = Path(ruta)
    if not ruta_input.exists():
        raise FileNotFoundError(f"No se encontró la ruta '{ruta}'")
    
    df = pd.read_csv(ruta_input, index_col = False)
    return df

def eliminar_columnas(df:DataFrame) -> DataFrame:
    df = df.drop(COLUMNAS_A_ELIMINAR, axis=1)
    return df

def normalizar_strings(df:DataFrame) -> DataFrame:

    for nombre_columna in df.columns:
        if df[nombre_columna].dtype == "object":
            df[nombre_columna] = df[nombre_columna].str.strip()

    df["forma_farmaceutica_simplificada"] = df["forma_farmaceutica_simplificada"].replace("SOLUCIÓN/SUSPENSIÓN ORAL", "SOLUCIÓN")
    df["forma_farmaceutica_simplificada"] = df["forma_farmaceutica_simplificada"].replace("COMPRIMIDO BUCODISPERSABLE/LIOTAB", "COMPRIMIDO BUCODISPERSABLE")
    df["vias_administracion"] = df["vias_administracion"].replace("VÍA INTRAMUSCULAR ,VÍA INTRAVENOSA", "VÍA INTRAMUSCULAR")

    return df

def gestionar_nulos_duracion(df:DataFrame) -> DataFrame:
    df["Tratamiento de larga duración"] = df["Tratamiento de larga duración"].replace(pd.NA, 'NO')
    return df

def gestionar_nulos_estado(df:DataFrame) -> DataFrame:
    moda = list(df["Estado"].mode())[0]
    df["Estado"] = df["Estado"].replace(pd.NA, moda)
    return df

def gestionar_nulos_precios(df:DataFrame) -> DataFrame:
    min_precio = float(df["Precio venta al público con IVA"].min())
    cuantil_90 = 40

    df_random_cuantil_90 = df.copy()
    columna = "Precio venta al público con IVA"
    es_na = df_random_cuantil_90[columna].isna()
    df_random_cuantil_90[columna] = np.where(
        es_na,
        np.random.uniform(low=min_precio, high=cuantil_90, size=len(df_random_cuantil_90)),
        df_random_cuantil_90[columna],
    )

    df["Precio venta al público con IVA"] = df_random_cuantil_90["Precio venta al público con IVA"].copy()

    return df

def gestionar_nulos(df:DataFrame) -> DataFrame:

    df = gestionar_nulos_duracion(df)
    df = gestionar_nulos_estado(df)
    df = gestionar_nulos_precios(df)

    return df

def gestionar_fechas(df:DataFrame) -> DataFrame:

    df["estado_aut"] = pd.to_datetime(df["estado_aut"], unit="ms")
    df["estado_rev"] = pd.to_datetime(df["estado_rev"], unit="ms")

    df["estado_rev"] = df["estado_rev"].fillna(df["estado_aut"])

    return df

def gestionar_dosis(df:DataFrame) -> DataFrame:

    df["dosis"] = df["dosis"].str.strip().str.split().str[0].str.replace(",", ".").astype(float)
    df = df.rename(columns={"dosis": "dosis (mg)"})

    return df

def gestionar_generico(df:DataFrame) -> DataFrame:

    df["generico"] = df["generico"].astype(int)

    return df

def validar_filas(df:DataFrame) -> DataFrame:
    for index, row in df.iterrows():
        try:
            Medicamento(**row.to_dict())
        except Exception as e:
            raise ValueError(f" Error al validar el lote. Error en el medicamento {df.get("nombre")[index]} \n \n {row}. \n \n Error: \n {e}")
    return df 

def exportar_df(df:DataFrame, ruta = RUTA_EXPORT):
    ruta_export = Path(ruta)
    ruta_export.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta_export, index=False)
    print("Se ha realizado el EDA de medicamentos en data/HU4_EDA")



def main(ruta=RUTA_INPUT):
    df = leer_excel(ruta)
    df = eliminar_columnas(df)
    #df = df.drop(df.columns[0], axis = 1) 
    # esto era por si había que eliminar el unnamed:0, pero creo que ya no hace falta
    # poner un if
    df = normalizar_strings(df)
    df = gestionar_nulos(df)
    df = gestionar_fechas(df)
    df = gestionar_dosis(df)
    df = gestionar_generico(df)

    try:
        df = validar_filas(df)
    except ValueError as e: #porque hemos raiseado un ValueError
        print(e, file=sys.stderr) 
        return 2

    exportar_df(df)
    
    
    


if __name__ == "__main__":
    main()