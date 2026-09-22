import requests
import pandas as pd

# TODO paginación (no es necesario pero suma)

url = "https://cima.aemps.es/cima/rest/buscarEnFichaTecnica?pagina=1"

#Este es el body del POST request. Estamos preguntando "dime todos los medicamentos para tratar la migraña".
payload = [
    {
        "seccion": "4.1",
        "texto": "migraña",
        "contiene": 1
    }
]

r = requests.post(url, json=payload)

url_medicamentos = "https://cima.aemps.es/cima/rest/medicamento"
medicamentos = []
for resultado in r.json()["resultados"]:
    response_medicamento = requests.get(url_medicamentos, params={"nregistro": resultado["nregistro"]})
    #Este es un GET request, que no tiene body. Necesita un parámetro (nregistro).
    #Aquí estamos diciendo "para cada medicamento, dame todos sus datos".

    if response_medicamento.status_code == 200:
        medicamentos.append(response_medicamento.json())

df_medicamentos = pd.DataFrame(medicamentos)
print(df_medicamentos.columns)