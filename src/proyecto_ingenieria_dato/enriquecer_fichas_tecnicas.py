"""HU-2: incorpora al Excel de HU-1 indicadores de las fichas técnicas."""

import argparse
import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


INDICADORES = (
    "volumen_informativo_seguridad",
    "complejidad_desglose_clinico",
    "indicador_riesgo_severo",
)
ENCABEZADOS = ["h1", "h2", "h3", "h4", "h5", "h6"]


def calcular_indicadores(html):
    """Cuenta palabras Unicode y términos completos, sin distinguir mayúsculas.

    El título de 4.4 queda excluido; los subtítulos interiores quedan incluidos.
    Si no se encuentra la sección, su recuento es nulo, nunca un cero ficticio.
    """
    soup = BeautifulSoup(html, "html.parser")
    tablas = len(soup.find_all("table"))
    for elemento in soup(["script", "style", "noscript", "template", "head"]):
        elemento.decompose()
    texto = soup.get_text(" ", strip=True)
    graves = len(re.findall(r"\bgraves?\b", texto, flags=re.IGNORECASE))
    inicio = next(
        (h for h in soup.find_all(ENCABEZADOS)
         if h.get("id") == "4.4"
         or re.match(r"^4\.4(?:\.(?!\d)|\s|$)", h.get_text(" ", strip=True))),
        None,
    )
    palabras = None
    if inicio is not None:
        fragmentos = []
        nivel = int(inicio.name[1])
        limite_encontrado = False
        for elemento in inicio.next_elements:
            if isinstance(elemento, Tag) and elemento.name in ENCABEZADOS:
                if int(elemento.name[1]) <= nivel:
                    limite_encontrado = True
                    break
            if (isinstance(elemento, NavigableString)
                    and not isinstance(elemento, Comment)
                    and inicio not in elemento.parents):
                fragmentos.append(str(elemento))
        # Sin límite no podemos asegurar que el texto pertenezca solo a 4.4.
        if limite_encontrado:
            palabras = len(re.findall(r"\b\w+\b", " ".join(fragmentos)))
    return dict(zip(INDICADORES, (palabras, tablas, graves)))


def enriquecer_dataset(datos, session):
    if "url_html_ficha_tecnica" not in datos.columns:
        raise ValueError("Falta la columna url_html_ficha_tecnica del Excel de HU-1")
    resultados = []
    cache = {}
    for url in datos["url_html_ficha_tecnica"]:
        resultado = dict.fromkeys(INDICADORES)
        if pd.isna(url) or not str(url).strip():
            resultado["error_scraping"] = "Sin URL de ficha técnica"
        else:
            url = str(url).strip()
            if url not in cache:
                try:
                    respuesta = session.get(url, timeout=(10, 60))
                    respuesta.raise_for_status()
                    tipo = respuesta.headers.get("Content-Type", "").lower()
                    if "html" not in tipo:
                        raise ValueError("La respuesta no es HTML")
                    resultado = calcular_indicadores(respuesta.content)
                    resultado["error_scraping"] = (
                        "" if resultado[INDICADORES[0]] is not None
                        else "No se pudo delimitar la sección 4.4"
                    )
                except (requests.RequestException, ValueError) as exc:
                    resultado["error_scraping"] = str(exc)
                cache[url] = resultado
            resultado = cache[url]
        resultados.append(resultado)
    salida = datos.copy()
    for columna in INDICADORES:
        salida[columna] = pd.array([r[columna] for r in resultados], dtype="Int64")
    salida["error_scraping"] = [r["error_scraping"] for r in resultados]
    return salida


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", type=Path, default=Path("medicamentos.xlsx"))
    parser.add_argument("--salida", type=Path, default=Path("medicamentos_hu2.xlsx"))
    args = parser.parse_args()
    if not args.entrada.is_file():
        parser.error(f"No existe {args.entrada}. Indica el Excel de HU-1 con --entrada.")
    if args.entrada.resolve() == args.salida.resolve():
        parser.error("El fichero de salida debe ser diferente al de entrada.")
    datos = pd.read_excel(args.entrada, dtype={"nregistro": "string", "cn": "string"})
    with requests.Session() as session:
        session.mount("https://", HTTPAdapter(max_retries=Retry(
            total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )))
        try:
            salida = enriquecer_dataset(datos, session)
        except ValueError as exc:
            parser.error(str(exc))
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    salida.to_excel(args.salida, index=False)
    errores = salida["error_scraping"].ne("").sum()
    print(f"Guardado {args.salida}: {len(salida)} medicamentos, {errores} con incidencias.")


if __name__ == "__main__":
    main()
