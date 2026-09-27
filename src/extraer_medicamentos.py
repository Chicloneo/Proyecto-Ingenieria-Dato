import requests
import json
from pathlib import Path


def peticion_ficha_tecnica(num_pagina: int) -> requests.Response:
    '''Devuelve la respuesta de la petición de la ficha técnica dado el número de página'''

    url = f"https://cima.aemps.es/cima/rest/buscarEnFichaTecnica?pagina={str(num_pagina)}"
    payload = [
        {
            "seccion": "4.1",
            "texto": "migraña",
            "contiene": 1
        }
    ]

    respuesta_ficha = requests.post(url, json=payload)
    if respuesta_ficha.status_code == 200:
        return requests.post(url, json=payload)
    
    respuesta_ficha.raise_for_status()

def incluir_medicamentos(medicamentos, resultados) -> None:
    '''Añade a la lista de medicamentos los medicamentos que se encuentren en los resultados de la ficha técnica'''

    url_medicamentos = "https://cima.aemps.es/cima/rest/medicamento"

    for resultado in resultados:
        response_medicamento = requests.get(url_medicamentos, params={"nregistro": resultado["nregistro"]})

        if response_medicamento.status_code == 200:
            medicamentos.append(response_medicamento.json())
        else:
            raise response_medicamento.raise_for_status()

def export_to_json(filename: str, medicamentos: list[dict]) -> None:
    '''Exporta la lista de medicamentos a json en el directorio data'''

    path.parent.mkdir(parents=True, exist_ok=True)
    path = Path(__file__).resolve().parent.parent.joinpath('data', filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(medicamentos, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    pagina: int = 1
    medicamentos = []
    total_registros: int = 0

    # Bucle de peticiones con paginación
    while True:
        # Obtener ficha técnica y sus resultados
        ficha_tecnica = peticion_ficha_tecnica(pagina).json()
        resultados = ficha_tecnica["resultados"]

        # Valores para paginación
        tamano_pagina: int = ficha_tecnica["tamanioPagina"]
        total_medicamentos: int = ficha_tecnica["totalFilas"]
        total_registros += len(resultados)

        incluir_medicamentos(medicamentos, resultados)

        # Control de paginación
        if total_registros >= total_medicamentos:
            break
        pagina += 1

    # Exportar medicamentos con todas las columnas a json
    export_to_json("medicamentos_raw.json", medicamentos)