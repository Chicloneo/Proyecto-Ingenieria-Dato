import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent.joinpath('data')

# Este url te descarga el csv directamente de la página del ministerio.
url = "https://www.sanidad.gob.es/profesionales/nomenclator.do?metodo=buscarProductos&especialidad=%25%25%25&d-4015021-e=1&6578706f7274=1%20%C2%A"

def main():
    df_medicamentos = pd.read_excel(DATA_PATH.joinpath("medicamentos_web_scrapping.xlsx"))
    df_ministerio = pd.read_csv(url)

    columnas_anadir = [
        "Código Nacional",
        "Estado",
        "Precio venta al público con IVA",
        "Precio de referencia",
        "Tratamiento de larga duración",
        "Especial control médico",
    ]

    df_final = pd.merge(
        df_medicamentos,
        df_ministerio[columnas_anadir],
        left_on="cn", 
        right_on="Código Nacional",
        how="left",  # Conservar filas del dataframe original de medicamentos
    )

    df_final.to_excel(DATA_PATH.joinpath("catalogo_enriquecido.xlsx"))

if __name__== "__main__":
    main()