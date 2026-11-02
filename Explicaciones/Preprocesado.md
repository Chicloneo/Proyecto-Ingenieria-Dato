# Preprocesado

#### Gonzalo Carrasco, Santiago Lillo, Rafael Sánchez

Datos originales: `src/data/HU-3.csv`. Datos preprocesados: `src/data/HU4_EDA.xlsx`. 70 medicamentos contra la migraña.

---
Este documento explica todo el pipeline de preprocesado de los datos: tratamiento de nulos, fechas, normalizar strings, ...

## Columnas eliminadas

Inicialmente, el dataset presenta 32 columnas. Eliminamos:

- `url_html_ficha_tecnica`: una vez que obtenemos la información necesaria de la ficha técnica (en historias de usuarios anteriores), no aporta información útil. Lo mismo para `url_foto_materiales`, que podría ser útil si quisiéramos entrenar un modelo con estas imágenes.

- `nregistro`, `cn`, y `Código Nacional` son identificadores. Los eliminamos porque utilizamos `nombre` como columna identificadora.

- `Precio de referencia`: todos los valores no nulos de estas columnas son los mismos que en `Precio venta al público con IVA`. Además, existe un valor no nulo de `Precio venta al público con IVA` no presente en `Precio de referencia`. Por tanto, eliminamos al columna `Precio de referencia` y mantenemos `Precio venta al público con IVA`.

- `requiere_receta`: todos los medicamentos requieren receta. Es una columna con un valor constante; el modelo no aprende nada de ella.

- `triangulo_negro`: ningún medicamento está marcado con el triángulo negro invertido, símbolo que identifica medicamentos sujetos a seguimiento adicional de seguridad. 

- `medicamento_huerfano`: ninguno lo es. Los medicamento huérfanos tratan una enfermedades raras. Se llaman así porque están _huérfanos_ de inversión.

- `biosimilar`: ninguno es biosimilar. La mayoría de los medicamentos biosimilares son de uso exclusivo en hospitales. Por tanto, estamos ante medicamentos distribuibles en farmacias tradicionales.

- `num_registros_atc`: todos los medicamentos analizados tienen valor  constante 3.

- `num_excipientes`, aunque variaba, se dejó fuera del conjunto final de variables elegido para el análisis y del contrato de datos. 

- `Especial control médico`, solo aparecían NO y valores nulos; no había medicamentos marcados con SI. Desconocemos cual seria el signo real de los valores nulos en caso de tener datos.
