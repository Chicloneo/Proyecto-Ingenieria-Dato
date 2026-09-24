import unittest
from unittest.mock import Mock

import pandas as pd
import requests

from proyecto_ingenieria_dato.enriquecer_fichas_tecnicas import (
    INDICADORES, calcular_indicadores, enriquecer_dataset,
)


class IndicadoresTest(unittest.TestCase):
    def test_limites_subsecciones_y_palabras_completas(self):
        html = '''<script>grave</script><h2 id="4.3">4.3. Contraindicaciones</h2>
        <p>grave</p><h2 id="4.4">4.4. Advertencias</h2>
        <p>Riesgo <b>GRAVE</b> y reacciones graves.</p>
        <h3>Pacientes especiales</h3><table><tr><td>Precaución</td></tr></table>
        <h2 id="4.5">4.5. Interacciones</h2><p>gravemente agravado</p><table></table>'''
        self.assertEqual(list(calcular_indicadores(html).values()), [8, 2, 3])

    def test_seccion_ausente_o_sin_limite(self):
        for html in ("<p>grave</p>", "<h2>4.4. Advertencias</h2><p>grave</p>"):
            self.assertIsNone(calcular_indicadores(html)[INDICADORES[0]])

    def test_seccion_vacia(self):
        resultado = calcular_indicadores('<h2>4.4. Advertencias</h2><h2>4.5. Otra</h2>')
        self.assertEqual(list(resultado.values()), [0, 0, 0])

    def test_conserva_filas_cache_y_errores(self):
        datos = pd.DataFrame({"cn": ["001", "002", "003", "004"],
                              "url_html_ficha_tecnica": ["https://ejemplo/a"] * 2 + [None, "https://ejemplo/b"]})
        respuesta = Mock(content=b'<h2 id="4.4">4.4</h2><p>grave</p><h2>4.5</h2>',
                         headers={"Content-Type": "text/html"})
        session = Mock()
        session.get.side_effect = [respuesta, requests.Timeout("Tiempo agotado")]
        salida = enriquecer_dataset(datos, session)
        pd.testing.assert_frame_equal(salida[datos.columns], datos)
        self.assertEqual(session.get.call_count, 2)
        self.assertEqual(salida[INDICADORES[0]].tolist()[:2], [1, 1])
        self.assertTrue(salida.loc[2:, list(INDICADORES)].isna().all().all())
        self.assertTrue(salida.loc[2:, "error_scraping"].ne("").all())


if __name__ == "__main__":
    unittest.main()
