import pandas as pd
from pandas import DataFrame
from pathlib import Path
import numpy as np

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

RUTA_INPUT = "../data/catalogo_enriquecido.xlsx"

RUTA_FECHAS = "../data/medicamentos_web_scrapping.xlsx"

RUTA_EXPORT = "../data/HU4_EDA.csv"

def leer_excel(ruta=RUTA_INPUT) -> DataFrame:
    ruta_input = Path(ruta)
    if not ruta_input.exists():
        raise FileNotFoundError(f"No se encontró la ruta '{ruta}'")
    
    df = pd.read_excel(ruta_input, index_col = False)
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
    df["vias_administracion"] = df["vias_administracion"].replace("VÍA INTRAMUSCULAR ,VÍA INTRAVENOSA", "VÍA INTRAVENOSA")

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

    df_fechas = pd.read_excel(RUTA_FECHAS)

    df["estado_aut"] = df_fechas["estado_aut"].copy()
    df["estado_rev"] = df_fechas["estado_rev"].copy()
    df["estado_rev"] = df["estado_rev"].fillna(df["estado_aut"])

    return df

def exportar_df(df:DataFrame, ruta = RUTA_EXPORT):
    ruta_export = Path(ruta)
    df.to_csv(ruta, index=False)

def main(ruta=RUTA_INPUT):
    df = leer_excel(ruta)
    df = eliminar_columnas(df)
    df = df.drop(df.columns[0], axis = 1)
    df = normalizar_strings(df)
    df = gestionar_nulos(df)
    df = gestionar_fechas(df)
    exportar_df(df)


if __name__ == "__main__":
    main()