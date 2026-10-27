# Explicación de las columnas eliminadas

Durante el EDA de HU-4 se retiraron columnas que eran identificadores o enlaces, que duplicaban información o que no aportaban variación útil en los datos analizados.
- 1 - `url_html_ficha_tecnica` y `url_foto_materiales` son urls y no aportan informacion que no este presente ya en las demas variables.
- 2 - `nregistro`, es un identificador, no una característica del medicamento para el análisis. Se podía usar para distinguir registros si había medicamentos con el mismo nombre; una vez resuelta esa comprobación, no hacía falta conservarlo.
- 3 - `cn`, es un código identificador. Se retiró junto con `Código Nacional`, porque los códigos no describen características analíticas del medicamento.
- 4 - `Precio de referencia`, era equivalente a Precio venta al público con IVA. Se conservó esta última porque tenía algún valor disponible más.
- 5 - `requiere_receta`, en los datos revisados todos los medicamentos tenían el mismo valor, sí requieren receta. 
- 6 - `triangulo_negro`, todos los registros tenían el valor 0: no estaban marcados con el triángulo negro invertido, símbolo que identifica medicamentos sujetos a seguimiento adicional de seguridad. 
- 7 - `medicamento_huerfano`, ninguno lo era. Un medicamento huérfano está destinado a diagnosticar, prevenir o tratar una enfermedad rara.
- 8 - `biosimilar`, todos los registros tenían valor False; ninguno era un medicamento biológico muy similar a otro medicamento biológico de referencia, sin diferencias clínicamente relevantes en calidad, seguridad o eficacia.
- 9 - `num_registros_atc`, cuenta cuántas entradas de la clasificación ATC devuelve CIMA para cada medicamento. En el ejemplo de almotriptán aparecen tres entradas jerárquicas: nivel 3 (subgrupo farmacológico), nivel 4 (subgrupo químico) y nivel 5 (sustancia química). Por tanto, el valor 3 no significa que haya una entrada anatómica, otra terapéutica y otra química: cuenta esas tres entradas de los niveles 3, 4 y 5. Como todos los medicamentos analizados tenían tres entradas, la columna era constante y no permitía distinguirlos.
- 10 - `num_excipientes`, aunque variaba, se dejó fuera del conjunto final de variables elegido para el análisis y del contrato de datos. El notebook no documenta una razón más específica para descartarla.
- 11 - `Especial control médico`, solo aparecían NO y valores nulos; no había medicamentos marcados con SI. Desconocemos cual seria el signo real de los valores nulos en caso de tener datos.

