import pandas as pd
import requests
from io import BytesIO
from pathlib import Path

# Primero leemos el Excel. Si no está el de HU-2, usamos el de HU-1.
ruta = "medicamentos_web_scrapping.xlsx"
if not Path(ruta).is_file():
    ruta = "medicamentos.xlsx"

medicamentos = pd.read_excel(ruta, dtype={"cn": "string"})

# Este enlace descarga el listado completo del Ministerio en CSV.
url = "https://www.sanidad.gob.es/profesionales/nomenclator.do"
parametros = {
    "metodo": "buscarProductos",
    "especialidad": "%%%",
    "6578706f7274": "1 \u00a0",
    "d-4015021-e": "1",
}

print("Descargando los datos del Ministerio...")
respuesta = requests.get(url, params=parametros, timeout=60)
respuesta.raise_for_status()  # Si falla la descarga, se detiene aquí.

# BytesIO permite leer lo descargado sin guardar nomenclator.csv.
nomenclator = pd.read_csv(BytesIO(respuesta.content), dtype="string", encoding="utf-8-sig")

# Nos quedamos con las columnas que pide el enunciado.
columnas = [
    "Código Nacional",
    "Estado",
    "Precio venta al público con IVA",
    "Precio de referencia",
    "Tratamiento de larga duración",
    "Especial control médico",
]
nomenclator = nomenclator[columnas].copy()
nomenclator = nomenclator.rename(columns={"Código Nacional": "cn"})

# Ponemos los códigos igual en las dos tablas para que coincidan.
# Quitamos espacios y el .0 que a veces aparece al leer números de Excel.
for tabla in [medicamentos, nomenclator]:
    tabla["cn"] = tabla["cn"].str.strip().str.replace(r"\.0$", "", regex=True)
    tabla["cn"] = tabla["cn"].replace("", pd.NA).str.zfill(6)

# Un código vacío no sirve para buscar un medicamento.
nomenclator = nomenclator.dropna(subset=["cn"])

# Los precios se guardan como números para poder hacer cálculos con ellos.
for columna in ["Precio venta al público con IVA", "Precio de referencia"]:
    nomenclator[columna] = pd.to_numeric(nomenclator[columna])

# left mantiene todos nuestros medicamentos aunque no haya coincidencia.
# La comprobación evita duplicar filas si el Ministerio repite algún código.
resultado = medicamentos.merge(nomenclator, on="cn", how="left", validate="many_to_one")

resultado.to_excel("medicamentos_hu3.xlsx", index=False)
print("Guardado medicamentos_hu3.xlsx")
print("Los datos que no se han encontrado quedan vacíos.")
