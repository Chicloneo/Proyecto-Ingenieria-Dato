# Proyecto de ingeniería del dato

## HU-2: indicadores de las fichas técnicas

Instalar las dependencias con `uv sync`. Desde la raíz del proyecto, usar el
Excel obtenido en HU-1:

Si todavía no se han generado los datos de HU-1, ejecutar primero, en este orden:

```bash
uv run python src/proyecto_ingenieria_dato/extraer_medicamentos.py
uv run python src/proyecto_ingenieria_dato/preparar_dataset_medicamentos.py
```

El primer script genera `medicamentos_raw.json` y el segundo, `medicamentos.xlsx`.
A continuación, ejecutar HU-2:

```bash
uv run python -m proyecto_ingenieria_dato.enriquecer_fichas_tecnicas
```

Por defecto lee `medicamentos.xlsx` y genera `medicamentos_hu2.xlsx`.
Para utilizar otras rutas:

```bash
uv run python -m proyecto_ingenieria_dato.enriquecer_fichas_tecnicas --entrada datos/medicamentos.xlsx --salida datos/medicamentos_hu2.xlsx
```

Conserva las filas y columnas de entrada y añade:

| Columna | Cálculo |
| --- | --- |
| `volumen_informativo_seguridad` | Palabras del contenido de 4.4, sin su título y hasta el siguiente encabezado del mismo nivel o superior. Incluye los subtítulos internos. |
| `complejidad_desglose_clinico` | Número de etiquetas `<table>` del HTML completo. |
| `indicador_riesgo_severo` | Apariciones completas de «grave» y «graves» en el texto del documento, sin distinguir mayúsculas. |
| `error_scraping` | Incidencia de descarga o sección ausente; vacío cuando los tres indicadores se han calculado. |

Se cuentan como palabras las secuencias Unicode de letras, números o guiones
bajos (`\b\w+\b`); la puntuación y los guiones separan palabras. Se excluyen
scripts, estilos, plantillas y metadatos. Los indicadores que no puedan calcularse
quedan vacíos, para distinguirlos de un recuento real de cero. Las URL repetidas
se descargan una sola vez por ejecución. Hay tiempo límite y reintentos para
errores temporales. El fichero de HU-1 no se sobrescribe.

Pruebas locales, sin acceso a internet:

```bash
uv run python -m unittest discover -s tests
```
