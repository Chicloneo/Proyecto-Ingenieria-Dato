"""
Objetivo: hacer un web-scrapping de las fichas técnicas de cada medicamento


Workflow (flujo de trabajo):

1. Leer el json/xlsx
2. Recorrer las filas (medicamentos)
3. Obtener la columna ficha_tecnica correspondiente
4. Acceder a dicha url
5. Contar cuántas palabras hay en la sección 4.4
6. Contar cuántas tablas hay en toda la url
7. Contar cuántas veces aparece la palabra "grave" o "graves"
"""

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent.joinpath('data')
ruta_excel = DATA_PATH.joinpath("medicamentos.xlsx")

df = pd.read_excel(ruta_excel) 

#En estas variables vamos guardando los datos
longitudes_4_4 = []
numero_de_tablas = []
contador_grave = []

for index, row in df.iterrows():
    url = row["url_html_ficha_tecnica"] #obtenemos la url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    seccion_4_4 = soup.find('h2', id='4.4') #buscamos la sección 4.4 (esto es solo el título, no el contenido)
    contenido = seccion_4_4.find_next_sibling() #esto encuentra el contenido de la sección 4.4
    texto = contenido.text
    longitudes_4_4.append(len(texto.split())) #split devuelve una lista de todas las palabras, así que las contamos calculando la longitud de dicha lista

    lista_tablas = soup.find_all('table') #'table' busca una sección de tipo <table> en el html (predeterminado de find_all)
    #devuelve una lista con todas las tablas del html. 
    numero_de_tablas.append(len(lista_tablas))

    texto = texto.lower()
    #Esto ha sido con ayuda de la IA:
    # s? indica que la s es opcional (buscamos tanto "grave" como "graves")
    # \b: Asegura que sea la palabra completa (no queremos palabras como "agravamiento")
    coincidencias = re.findall(r"\bgraves?\b", texto)

    # Coincidencias devuelve una lista con las palabras "grave" o "graves" repetidas, según su orden de aparición.
    contador_grave.append(len(coincidencias))

# Los nombres de las columnas vienen indicados en el enunciado
df["Volumen_Informativo"] = longitudes_4_4 #Añadimos una columna al dataframe. Como no existe ninguna que se llame Volumen_Informativo, la crea.
df["Complejidad_Desglose"] = numero_de_tablas
df["Indicador_Riesgo"] = contador_grave

export_path = DATA_PATH.joinpath("medicamentos_web_scrapping.xlsx")
df.to_excel(export_path, index=False)