El archivo principal de HU-2 es `web_scrapping.py`, pero requiere un archivo
`.xlsx` que se obtiene de `extraer_medicamentos.py` y
`preparar_dataset_medicamentos.py`.

## HU-3:

1. Tener `medicamentos_web_scrapping.xlsx`, generado por HU-2, en la raíz del proyecto.
2. Tener conexión a internet: el script descarga automáticamente el listado del
   [nomenclátor del Ministerio de Sanidad](https://www.sanidad.gob.es/profesionales/nomenclator.do?metodo=buscarProductos)
   y lo lee en memoria. No hace falta descargar ni guardar `nomenclator.csv`.
3. Desde la raíz, ejecutar:

```bash
uv sync
uv run python src/proyecto_ingenieria_dato/hu-3.py
```

El script crea `medicamentos_hu3.xlsx` con todas las filas y columnas de HU-2
y cinco columnas nuevas: Estado, Precio venta al público con IVA, Precio de
referencia, Tratamiento de larga duración y Especial control médico.
Código Nacional se usa para cruzar los datos con `cn`, que ya existe en HU-2.
Los datos sin coincidencia quedan vacíos. El archivo de HU-2 no se sobrescribe.

Si no encuentra el Excel de HU-2, utiliza `medicamentos.xlsx` como alternativa;
en ese caso la salida no incluirá los indicadores de HU-2.
