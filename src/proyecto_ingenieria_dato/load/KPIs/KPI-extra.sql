-- Vamos a estudiar los medicamentos genéricos frente a los no genéricos
-- Vamos a agrupar los medicamentos según su principio activo. 
-- En cada grupo, separamos entre si son genéricos o no.
-- Calculamos la diferencia de medias entre subgrupos. (Tasa de ahorro)
-- Añadimos una tasa de fiabilidad, para no comparar un grupo de 1 medicamento con otro de 20.

-- ¿Qué nos devuelve este KPI? Nos da una métrica de cuánto ahorramos si compramos el medicamento genérico
-- frente a un no genérico. Si el resultado es negativo, pagamos de más al comprar un genérico.
-- ¿Por qué añadimos la tasa de fiabilidad? Para saber cuántos elementos estamos comparando:
-- será muy baja si comparamos una media de un medicamento frente a una media de 20 medicamentos
-- Es 1 si comparamos el mismo número de medicamentos (tasa de fiabilidad máxima)
-- Es 0 si no podemos comparar los subgrupos porque o bien no hay genéricos o bien
-- no hay No Genéricos (tasa de fiabilidad mínima)

CREATE OR REPLACE VIEW tasa_ahorro AS
-- Creamos una subquery para poder trabajar con las nuevas columnas calculadas 
-- CASE WHEN calcula COUNT(principios_activos) solo cuando es generico.
-- Lo mismo para cuando no es genérico y para average, creando 4 columnas
WITH calculo_medias AS (
SELECT principios_activos, COUNT(CASE WHEN generico THEN principios_activos END) AS num_generico, 
    COUNT(CASE WHEN NOT generico THEN principios_activos END) AS num_no_generico, 
    AVG(CASE WHEN generico THEN precio_venta_publico_iva END) AS media_precios_genericos,
    AVG(CASE WHEN NOT generico THEN precio_venta_publico_iva END) AS media_precios_no_genericos
FROM medicamentos
GROUP BY principios_activos
) 


SELECT principios_activos, 
       num_generico, 
       num_no_generico, 
       media_precios_no_genericos, 
       media_precios_genericos,
       ROUND(
        IFNULL(
            media_precios_no_genericos - media_precios_genericos, 
            0), -- Si es nulo, ponemos un 0 (ahorramos 0€ si solo hay genérico)
            2) AS tasa_ahorro, -- dejamos el resultado en 2 decimales
       ROUND(
        IFNULL(
            -- Queremos un número entre 0 y 1.
            LEAST(num_generico,num_no_generico)/GREATEST(num_generico,num_no_generico), 
        0),
        2) AS tasa_fiabilidad
FROM calculo_medias;