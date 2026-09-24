import argparse
import re
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

INDICADORES = (
    "volumen_informativo_seguridad",
    "complejidad_desglose_clinico",
    "indicador_riesgo_severo",
)
ENCABEZADOS = ["h1", "h2", "h3", "h4", "h5", "h6"]

def calcular_indicadores(html):
    sopa = BeautifulSoup(html, "html.parser")

    # Cuenta las tablas de toda la ficha.
    numero_tablas = len(sopa.find_all("table"))

    # Elimina contenido que no forma parte del texto de la ficha.
    for elemento in sopa(["script", "style", "noscript", "template", "head"]):
        elemento.decompose()

    # Cuenta "grave" y "graves" como palabras completas.
    texto_completo = sopa.get_text(" ", strip=True)
    menciones_grave = len(
        re.findall(r"\bgraves?\b", texto_completo, flags=re.IGNORECASE)
    )

    # Busca el encabezado de la sección 4.4.
    inicio = next(
        (
            encabezado
            for encabezado in sopa.find_all(ENCABEZADOS)
            if encabezado.get("id") == "4.4"
            or re.match(
                r"^4\.4(?:\.(?!\d)|\s|$)",
                encabezado.get_text(" ", strip=True)
            )
        ),
        None,
    )

    palabras_seccion_44 = 0

    if inicio is not None:
        nivel = int(inicio.name[1])
        fragmentos = []
        encontro_siguiente_seccion = False

        # Recorre el contenido que aparece después del título 4.4.
        for elemento in inicio.next_elements:
            if isinstance(elemento, Tag) and elemento.name in ENCABEZADOS:
                # Un encabezado del mismo nivel o superior cierra la sección.
                if int(elemento.name[1]) <= nivel:
                    encontro_siguiente_seccion = True
                    break

            if (
                isinstance(elemento, NavigableString)
                and not isinstance(elemento, Comment)
                and inicio not in elemento.parents
            ):
                fragmentos.append(str(elemento))

        # Solo calcula el total si encontró el siguiente encabezado.
        if encontro_siguiente_seccion:
            texto_seccion = " ".join(fragmentos)
            palabras_seccion_44 = len(re.findall(r"\b\w+\b", texto_seccion))

    return {
        "volumen_informativo_seguridad": palabras_seccion_44,
        "complejidad_desglose_clinico": numero_tablas,
        "indicador_riesgo_severo": menciones_grave,
    }


def main():
    parser = argparse.ArgumentParser(description="Calcula indicadores de una ficha técnica HTML.")
    parser.add_argument(
        "html",
        nargs="?",
        type=Path,
        help="Ruta a un archivo HTML. Si no se indica, usa un ejemplo de prueba.",
    )
    args = parser.parse_args()

    if args.html is not None:
        html = args.html.read_text(encoding="utf-8")
    else:
        html = '''<script>grave</script><h2 id="4.3">4.3. Contraindicaciones</h2>
        <p>grave</p><h2 id="4.4">4.4. Advertencias</h2>
        <p>Riesgo <b>GRAVE</b> y reacciones graves.</p>
        <h3>Pacientes especiales</h3><table><tr><td>Precaución</td></tr></table>
        <h2 id="4.5">4.5. Interacciones</h2><p>gravemente agravado</p><table></table>'''

    resultado = calcular_indicadores(html)
    print(resultado)


if __name__ == "__main__":
    main()

