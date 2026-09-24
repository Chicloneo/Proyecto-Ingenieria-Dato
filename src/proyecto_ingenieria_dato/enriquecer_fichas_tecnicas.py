"""HU-2: añade información de las fichas técnicas al Excel de medicamentos.

RECORRIDO DEL PROGRAMA
1. Lee medicamentos.xlsx, generado por preparar_dataset_medicamentos.py (HU-1).
2. Visita el enlace de la ficha técnica de cada medicamento.
3. Calcula los tres indicadores que pide el enunciado:
   - Palabras de la sección 4.4: Advertencias y precauciones especiales de empleo.
   - Número de tablas en todo el documento HTML.
   - Apariciones de las palabras completas «grave» o «graves» en todo el texto.
4. Guarda los datos originales y los indicadores en medicamentos_hu2.xlsx.

HTML es el formato de las páginas web. Contiene etiquetas como <h2> (título),
<p> (párrafo) o <table> (tabla). Hacer web scraping consiste aquí en descargar
ese HTML y extraer información de él automáticamente.

Para ejecutarlo desde la raíz del proyecto:
    uv run python -m proyecto_ingenieria_dato.enriquecer_fichas_tecnicas

También se pueden añadir --entrada ruta/origen.xlsx y --salida ruta/destino.xlsx.
Las rutas relativas se interpretan desde la carpeta donde ejecutas el comando.
"""

# Las importaciones ponen a nuestra disposición herramientas ya programadas.
# argparse interpreta opciones de terminal, como --entrada medicamentos.xlsx.
# re busca patrones de texto; Path permite trabajar con rutas de archivos.
import argparse
import re
from pathlib import Path

# pandas representa el Excel como una tabla en memoria, llamada DataFrame.
# El alias «pd» es una abreviatura para utilizar pandas en el resto del archivo.
import pandas as pd
# requests descarga páginas; BeautifulSoup permite examinar su HTML.
# Tag representa una etiqueta, NavigableString un texto y Comment un comentario
# interno del HTML, que no forma parte del texto que ve el lector de la ficha.
import requests
from bs4 import BeautifulSoup, Comment, NavigableString, Tag
# Estas dos herramientas permiten reintentar algunas descargas que fallen.
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Nombres de las columnas nuevas. Se escriben una sola vez para reutilizarlos.
# Su orden será: palabras de 4.4, tablas del documento, menciones de riesgo.
INDICADORES = (
    "volumen_informativo_seguridad",
    "complejidad_desglose_clinico",
    "indicador_riesgo_severo",
)
# En HTML, h1 es el título de mayor nivel; h2, h3, etc. son niveles inferiores.
ENCABEZADOS = ["h1", "h2", "h3", "h4", "h5", "h6"]


def calcular_indicadores(html):
    """Recibe el HTML de UNA ficha y devuelve sus tres recuentos.

    Una función agrupa instrucciones para poder utilizarlas varias veces.
    Esta función analiza el contenido recibido; no descarga ni escribe archivos.
    Devuelve un diccionario: cada nombre de indicador está asociado a su valor.
    El título de 4.4 queda excluido; los subtítulos interiores quedan incluidos.
    None significa «no se ha podido calcular» y se guardará como celda vacía.
    Es distinto de 0, que significa «se ha calculado y no hay ninguna aparición».
    """
    # Convertimos el HTML en una estructura que podemos recorrer y consultar.
    soup = BeautifulSoup(html, "html.parser")
    # find_all devuelve todas las etiquetas indicadas; len cuenta cuántas hay.
    # Contamos las tablas antes de eliminar otras partes del documento.
    tablas = len(soup.find_all("table"))
    # Quitamos código, estilos y metadatos para que no sumen palabras.
    # decompose elimina el elemento completo, incluido su contenido.
    for elemento in soup(["script", "style", "noscript", "template", "head"]):
        elemento.decompose()
    # Extraemos texto sin etiquetas. El espacio separa fragmentos y strip=True
    # elimina espacios sobrantes al principio y al final de cada fragmento.
    texto = soup.get_text(" ", strip=True)
    # Una expresión regular es una regla de búsqueda de texto:
    # \b marca un límite de palabra; s? significa «una s opcional».
    # Así contamos «grave» y «graves», pero no «gravemente» ni «agravado».
    # IGNORECASE permite contar también «GRAVE», «Graves», etc.
    # El prefijo r conserva las barras de la expresión tal como se escriben.
    graves = len(re.findall(r"\bgraves?\b", texto, flags=re.IGNORECASE))
    # Localizamos el título de 4.4, la sección exigida por HU-2.
    # Primero comprobamos su identificador HTML: por ejemplo, <h2 id="4.4">.
    # También aceptamos que el texto del título empiece por «4.4».
    # La regla evita confundirlo con 4.40 o con el subtítulo 4.4.1:
    # ^ indica inicio; \. un punto literal; \s un espacio; $ el final.
    # (?!\d) exige que después del punto no haya inmediatamente un número.
    # next(..., None) toma el primer título que cumple la condición, o None
    # si no encuentra ninguno. La h representa cada encabezado examinado.
    inicio = next(
        (h for h in soup.find_all(ENCABEZADOS)
         if h.get("id") == "4.4"
         or re.match(r"^4\.4(?:\.(?!\d)|\s|$)", h.get_text(" ", strip=True))),
        None,
    )
    # Partimos de «no calculado» hasta confirmar ambos límites de la sección.
    palabras = None
    if inicio is not None:
        # Una lista acumula los trozos de texto que después contaremos juntos.
        fragmentos = []
        # Si el título es h2, name[1] obtiene «2» e int lo convierte al número 2.
        nivel = int(inicio.name[1])
        limite_encontrado = False
        # Recorremos los elementos siguientes en el orden del documento.
        # isinstance comprueba qué tipo de elemento estamos leyendo.
        for elemento in inicio.next_elements:
            if isinstance(elemento, Tag) and elemento.name in ENCABEZADOS:
                # Un título del mismo nivel o superior cierra la sección.
                # Por ejemplo, después de un h2 paramos ante h2 o h1.
                # Un h3 es un subtítulo interno y se incluye en el recuento.
                if int(elemento.name[1]) <= nivel:
                    limite_encontrado = True
                    break  # Dejamos de recorrer: ya llegamos a otra sección.
            # Guardamos solo texto, excluyendo comentarios y el propio título
            # de 4.4. parents contiene las etiquetas que envuelven ese texto.
            if (isinstance(elemento, NavigableString)
                    and not isinstance(elemento, Comment)
                    and inicio not in elemento.parents):
                fragmentos.append(str(elemento))  # append añade a la lista.
        # Sin límite no podemos asegurar que el texto pertenezca solo a 4.4.
        if limite_encontrado:
            # join une los fragmentos con espacios; findall busca las palabras.
            # \w+ es una secuencia de letras Unicode (incluidas tildes), números
            # o guiones bajos. Puntuación y guiones separan palabras.
            # Ejemplo: «Precaución: riesgo grave.» cuenta como 3 palabras.
            palabras = len(re.findall(r"\b\w+\b", " ".join(fragmentos)))
    # zip empareja cada nombre con su recuento; dict crea el diccionario.
    # return entrega el resultado a la parte del programa que llamó la función.
    return dict(zip(INDICADORES, (palabras, tablas, graves)))


def enriquecer_dataset(datos, session):
    """Recibe la tabla de HU-1 y una sesión para descargar páginas.

    Procesa una fila por medicamento y devuelve una copia de la tabla con los
    indicadores. Una descarga fallida queda registrada y no detiene las demás.
    «Dataset» significa aquí simplemente el conjunto de datos del Excel.
    """
    # Sin la columna de enlaces no se puede realizar el trabajo. raise genera
    # un error explicativo que main mostrará a quien ejecute el programa.
    if "url_html_ficha_tecnica" not in datos.columns:
        raise ValueError("Falta la columna url_html_ficha_tecnica del Excel de HU-1")
    resultados = []  # Un resultado por fila, respetando el orden del Excel.
    cache = {}  # Guarda resultados por URL para no descargar fichas repetidas.
    for url in datos["url_html_ficha_tecnica"]:
        # Creamos los tres indicadores con valor None hasta poder calcularlos.
        resultado = dict.fromkeys(INDICADORES)
        # pd.isna detecta celdas vacías. strip también detecta celdas que solo
        # contienen espacios; str convierte el contenido en texto.
        if pd.isna(url) or not str(url).strip():
            resultado["error_scraping"] = "Sin URL de ficha técnica"
        else:
            url = str(url).strip()
            if url not in cache:
                # try intenta descargar y calcular; except recoge los errores
                # previstos para poder continuar con el siguiente medicamento.
                try:
                    # GET solicita la página. Damos hasta 10 segundos para
                    # conectar y 60 de espera de lectura; no es un límite
                    # global de duración de todo el proceso.
                    respuesta = session.get(url, timeout=(10, 60))
                    # Convierte respuestas como 404 (no encontrado) en errores.
                    respuesta.raise_for_status()
                    # El servidor indica el formato en Content-Type. Exigimos
                    # HTML para no intentar analizar como página, por ejemplo,
                    # un PDF recibido accidentalmente.
                    tipo = respuesta.headers.get("Content-Type", "").lower()
                    if "html" not in tipo:
                        raise ValueError("La respuesta no es HTML")
                    # content contiene los bytes descargados de la ficha.
                    resultado = calcular_indicadores(respuesta.content)
                    # Una cadena vacía indica que no hubo incidencias.
                    # INDICADORES[0] es el nombre del recuento de palabras 4.4.
                    resultado["error_scraping"] = (
                        "" if resultado[INDICADORES[0]] is not None
                        else "No se pudo delimitar la sección 4.4"
                    )
                except (requests.RequestException, ValueError) as exc:
                    # Conservamos el motivo del fallo en vez de inventar ceros.
                    resultado["error_scraping"] = str(exc)
                # La caché dura solo esta ejecución y también conserva errores.
                cache[url] = resultado
            resultado = cache[url]
        resultados.append(resultado)
    # Hacemos una copia para conservar la tabla de entrada sin modificarla.
    salida = datos.copy()
    for columna in INDICADORES:
        # [r[columna] for r in resultados] reúne los valores de una columna.
        # Int64, con I mayúscula, admite enteros y valores ausentes a la vez.
        salida[columna] = pd.array([r[columna] for r in resultados], dtype="Int64")
    salida["error_scraping"] = [r["error_scraping"] for r in resultados]
    return salida


def main():
    """Coordina el proceso: opciones, lectura, descargas y escritura del Excel."""
    # Esta es la función de entrada. Las funciones anteriores definen tareas;
    # main decide en qué orden se ejecutan y qué archivos utilizan.
    # __doc__ contiene la explicación escrita al principio de este archivo.
    # argparse permite consultar la ayuda ejecutando el programa con --help.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", type=Path, default=Path("medicamentos.xlsx"))
    parser.add_argument("--salida", type=Path, default=Path("medicamentos_hu2.xlsx"))
    # Si no damos opciones, se usan los nombres indicados en default.
    args = parser.parse_args()
    # Comprobamos los archivos antes de descargar nada. parser.error muestra
    # un mensaje y termina el programa cuando no se puede continuar.
    if not args.entrada.is_file():
        parser.error(f"No existe {args.entrada}. Indica el Excel de HU-1 con --entrada.")
    # resolve convierte las rutas a su ubicación completa para compararlas.
    if args.entrada.resolve() == args.salida.resolve():
        parser.error("El fichero de salida debe ser diferente al de entrada.")
    # Leemos los identificadores como texto: son códigos, no cantidades para
    # hacer cuentas. Esto conserva ceros iniciales si están guardados como texto
    # en el Excel; no recupera ceros que ya se hubieran perdido en el origen.
    datos = pd.read_excel(args.entrada, dtype={"nregistro": "string", "cn": "string"})
    # La sesión reutiliza conexiones entre descargas. with la cierra al salir
    # de este bloque, incluso si se produce un error.
    with requests.Session() as session:
        # Aplicamos reintentos a las peticiones HTTPS:
        # total=3: hasta tres reintentos adicionales de una petición fallida.
        # backoff_factor=1: introduce esperas crecientes entre reintentos.
        # 429 indica demasiadas peticiones; los 5xx listados, fallos del servidor.
        # Solo reintentamos GET, el método usado para leer estas páginas.
        session.mount("https://", HTTPAdapter(max_retries=Retry(
            total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )))
        try:
            salida = enriquecer_dataset(datos, session)
        except ValueError as exc:
            parser.error(str(exc))
    # Creamos la carpeta de destino si falta. parents=True permite crear las
    # carpetas intermedias y exist_ok=True acepta que la carpeta ya exista.
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    # index=False evita añadir al Excel la numeración interna de filas de pandas.
    # Si ya existe el archivo de salida, se reemplaza con este nuevo resultado.
    salida.to_excel(args.salida, index=False)
    # ne("") comprueba qué mensajes no están vacíos. sum cuenta esos casos
    # porque True equivale a 1 y False a 0 al sumar valores booleanos.
    errores = salida["error_scraping"].ne("").sum()
    print(f"Guardado {args.salida}: {len(salida)} medicamentos, {errores} con incidencias.")


# Ejecutamos main solo cuando lanzamos este archivo como programa.
# Si otro archivo lo importa (por ejemplo, las pruebas), sus funciones estarán
# disponibles sin descargar fichas ni generar un Excel automáticamente.
if __name__ == "__main__":
    main()
