import pandas as pd
import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent.joinpath("data")
JSON_PATH = DATA_PATH.joinpath("medicamentos_raw.json")
EXPORT_PATH = DATA_PATH.joinpath("medicamentos.xlsx")

def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        medicamentos_columnas_todas = json.load(f)

    medicamentos_clean = []
    for medicamento in medicamentos_columnas_todas:
        medicamento_clean = {
            "nregistro": medicamento.get("nregistro"),
            "nombre": medicamento.get("nombre"),
            "pactivos": medicamento.get("pactivos"),
            "labtitular": medicamento.get("labtitular"),
            "labcomercializador": medicamento.get("labcomercializador"),
            "cn": medicamento.get("presentaciones")[0].get("cn"),
            "forma_farmaceutica_simplificada": medicamento.get("formaFarmaceuticaSimplificada").get("nombre"),

            "estado_aut": pd.to_datetime(medicamento.get("estado").get("aut"), unit='ms', errors='coerce'),
            "estado_rev": pd.to_datetime(medicamento.get("estado").get("rev"), unit='ms', errors='coerce'),

            "vias_administracion": " ,".join(via.get("nombre") for via in medicamento.get("viasAdministracion")),

            # False en caso de que no exista para prevenir errores de conversion
            "comercializado": int(medicamento.get("comerc", False)),
            "requiere_receta": int(medicamento.get("receta", False)),
            "generico": int(medicamento.get("generico", False)),
            "afecta_conduccion": int(medicamento.get("conduc", False)),
            "triangulo_negro": int(medicamento.get("triangulo", False)),
            "medicamento_huerfano": int(medicamento.get("huerfano", False)),
            "biosimilar": int(medicamento.get("biosimilar", False)),

            "url_html_ficha_tecnica": next(
                (
                    doc.get("urlHtml")
                    for doc in medicamento.get("docs", [])
                    if doc.get("tipo") == 1
                ),
                None
            ),
            "url_foto_materiales": next(
                (
                    foto.get("url")
                    for foto in medicamento.get("fotos", [])
                    if foto.get("tipo") == "materialas"
                ),
                None
            ),

            "num_registros_atc": len(medicamento.get("atcs", [])),
            "num_principios_activos": len(medicamento.get("principiosActivos", [])),
            "num_excipientes": len(medicamento.get("excipientes", []))
        }
        medicamentos_clean.append(medicamento_clean)

    df_medicamentos = pd.DataFrame(medicamentos_clean)
    pd.DataFrame.to_excel(df_medicamentos, EXPORT_PATH, index=False)

if __name__ == "__main__":
    main()