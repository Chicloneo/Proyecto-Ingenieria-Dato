# Exploratory Data Analysis (EDA)

#### Gonzalo Carrasco, Santiago Lillo, Rafael Sánchez

Datos: `src/data/HU4_EDA.xlsx`. 70 medicamentos contra la migraña.

## Principio Activo

El principio activo de un medicamento es la sustancia química que produce el efecto curativo en el organismo.

![Medicamentos por principio activo](graficas/medicamentos-por-principio-activo.png)
Topiramato e Ibuprofeno son los principios más comunes entre los datos.

## Frecuencia de las dosis

La dosis está expresada en miligramos (mg), que indica la cantidad de principio activo que contiene el fármaco.

![Frecuencia de las dosis](graficas/frecuencia-de-las-dosis.png)

A priori no se observa un patrón en las dosis de los medicamentos.

## Forma farmacéutica simplificada y Vía de Administración

![Medicamentos por forma farmacéutica simplificada](graficas/medicamentos-por-forma-farmaceutica-simplificada.png)

Las principales características son `COMPRIMIDO` y `SOLUCION`. Los comprimidos son prácticos de almacenar y administrar, sin asegurar que esa sea la causa de su predominio. Esto concuerda con que la vía oral sea la más representada. 

![Medicamentos por vía de administración](graficas/medicamentos-por-via-de-administracion.png)

La escasez en las vías nasales e intramusculares podría deberse a que estas requieren material sanitario. No obstante, estas pueden ser útiles en circunstancias particulares.

## Año de autorización y revisión

![Medicamentos por año: autorización y revisión](graficas/medicamentos-por-ano-autorizacion-y-revision.png)

En este conjunto de datos no hay fechas de autorización posteriores a 2016. Además, solo 19 registros tienen una fecha de revisión original (todas entre 2021 y 2026), y el resto son valores nulos sustituidos por so fecha de autorización. 

Se observa que los datos consideran principalmente ,medicamentos autorizados a partir de 1996.

No se informa del resultado de cada revisión: si el medicamento se mantuvo, se retiró o cambió de estado.

## Comercialización

![Medicamentos según comercialización](graficas/medicamentos-segun-comercializacion.png)

La no comercialización de 26 medicamentos podría deberse a diferentes causas: retirada, falta de lanzamiento, o de disponibilidad.

## Genéricos

Un medicamento genérico es aquel que tiene el mismo componente activo, seguridad y eficacia que el original de marca. Se puede fabricar y vender a menor precio una vez que caduca la patente del medicamento original.

![Medicamentos según si son genéricos](graficas/medicamentos-segun-si-son-genericos.png)

![Precio según si el medicamento es genérico](graficas/correlacion-precio-generico.png)

En este caso, no se observa ninguna relación entre los medicamentos genéricos y un precio menor. Los medicamentos no genéricos podrían seguir una distribución en el precio similar (o incluso menor) a los genéricos.

## Efecto en la conducción

![Medicamentos según efecto sobre la conducción](graficas/medicamentos-segun-efecto-sobre-la-conduccion.png)

Estas advertencias suelen relacionarse con posibles efectos que alteren la atención, la visión o el estado de alerta. No se deduce que, para todas las personas que los tomen, se vaya a ver afectada su capacidad de conducción.

![Precio según efecto sobre la conducción](graficas/correlacion-precio-conduccion.png)

En este caso sí se observa una correlación con el precio, siendo más baratos aquellos medicamentos que no afectan a la conducción.

## Número de principios activos

![Medicamentos por número de principios activos](graficas/medicamentos-por-numero-de-principios-activos.png)

Solamente hay un medicamento que combina dos principios activos. Este medicamento es `CAFERGOT 1 mg/100 mg COMPRIMIDOS`. Cada comprimido tiene 1mg de `ERGOTAMINA TARTRATO` y 100 mg de `CAFEINA`. Se usa para ataques de migraña agudos. [Fuente](https://www.e-lactancia.org/media/papers/ErgotaminaCafergot-FT-AEMPS-Amdipharm2009.pdf)

## Volumen informativo e indicador de riesgo

El volumen informativo corresponde al número de palabras de la sección 4.4 de la ficha técnica. 

![Densidad del volumen informativo](graficas/densidad-del-volumen-informativo.png)

![Distribución del indicador de riesgo](graficas/distribucion-del-indicador-de-riesgo.png)

El indicador de riesgo se refiere al número de apariciones de las palabras «grave» o «graves» en la ficha técnica; no es medida clínica de riesgo.

![Correlación entre volumen informativo e indicador de riesgo](graficas/correlacion-volumen-riesgo.png)

Cuantas más palabras y más extensa sea la sección 4.4, más veces aparece potencialmente la palabra «grave».

## Complejidad de desglose

La complejidad del desglose se refiere al número de tablas de la ficha técnica correspondiente. En la muestra, 26 registros no tienen ninguna tabla.

![Medicamentos por complejidad de desglose](graficas/medicamentos-por-complejidad-de-desglose.png)

## Estado

![Medicamentos por estado](graficas/medicamentos-por-estado.png)

![Comercialización según estado](graficas/comercializacion-segun-estado.png)

- `ALTA`: Se puede recetar y comprar en las farmacias.

- `BAJA POR NO COMERCIALIZAR`: El laboratorio titular ha decidido dejar de venderlo. Sigue teniendo permiso legal para comercializarse, pero deja de ser rentable o es sustituido por por otra versión.

- `BAJA GENERAL`: La Agencia Española de Medicamentos (AEMPS) ha retirado de forma definitiva el medicamento. Ya no existe administrativamente en el sistema de facturación o bien se le ha retirado la autorización de comercialización.

- `SUSPENSION TEMPORAL GENERAL`: Hay una pausa temporal en la venta, debido a problemas puntuales en la fábrica, problemas de seguridas, o desabastecimientos, entre otros.

## Precio de venta

![Frecuencia de los precios](graficas/frecuencia-de-los-precios.png)

![Distribución del precio de venta al público](graficas/distribucion-del-precio-de-venta-al-publico.png)

Se observa una notable diferencia entre la mediana (línea naranja) y la media (triángulo verde) debido al _outlier_ con valor de 73€. 

Este es un valor atípico debido a la ausencia de medicamentos con precio entre 40€ y 70€.

## Tratamiento de larga duración

![Tratamiento de larga duración](graficas/tratamiento-de-larga-duracion.png)


## Matriz de correlación

![Matriz de correlación de variables numéricas](graficas/matriz-correlacion-ml.png)

A continuación se estudia la correlación entre la dosis y si afecta o no a la conducción, cuyo coeficiente de correlación de Pearson es de -0.67.

### Conducción y dosis

![Dosis según efecto sobre la conducción](graficas/correlacion-conduccion-dosis.png)


Que el valor del coeficiente sea negativo indicaría una relación inversa. Es decir, cuanto más afecta a la conducción, menos dosis tiene el medicamento. Sin embargo, como la variable de la conducción es categórica (Sí/No), la posible correlación debe interpretarse de la siguiente forma: los medicamentos que sí afectan a la conducción requieren una menor dosis. Una posible explicación sería que mayores dosis en dichos medicamentos afectarían gravemente a la percepción, los sentidos o la capacidad de reacción, imposibilitando totalmente la conducción.

### Precio y año de autorización

![Correlación entre precio y año de autorización](graficas/correlacion-precio-autorizacion.png)

Pese a que el coeficiente de correlación de estas variables sea de 0.66, no se observa ninguna correlación evidente entre ambas. El bajo coste de los medicamentos autorizados en los años 60, así como la gran cantidad de medicamentos autorizados en los 2000, explican que este coeficiente tenga un valor elevado.