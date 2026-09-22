import requests
import pandas as pd

# TODO paginación (no es necesario pero suma)

url = "https://cima.aemps.es/cima/rest/buscarEnFichaTecnica?pagina=1"

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

    if response_medicamento.status_code == 200:
        medicamentos.append(response_medicamento.json())

df_medicamentos = pd.DataFrame(medicamentos)
print(df_medicamentos.columns)