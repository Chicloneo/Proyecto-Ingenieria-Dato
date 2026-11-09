-- Vamos a estudiar los medicamentos genéricos frente a los no genéricos
-- Vamos a agrupar los medicamentos los mismos principios activos. 
-- En cada grupo, separamos entre si son genéricos o no.
-- Calculamos la diferencia de medias entre subgrupos. (Tasa de ahorro)
-- Añadimos una tasa de fiabilidad, para no comparar un grupo de 1 medicamento con otro de 20.

CREATE OR REPLACE VIEW tasa_ahorro AS
WITH calculo_medias AS (
SELECT principios_activos, COUNT(CASE WHEN generico THEN principios_activos END) AS num_generico, 
    COUNT(CASE WHEN NOT generico THEN principios_activos END) AS num_no_generico, 
    AVG(CASE WHEN generico THEN precio_venta_publico_iva END) AS media_precios_genericos,
    AVG(CASE WHEN NOT generico THEN precio_venta_publico_iva END) AS media_precios_no_genericos
FROM medicamentos_clusterizados
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
            0), 
            2) AS tasa_ahorro,
       ROUND(
        IFNULL
        (LEAST(num_generico,num_no_generico)/GREATEST(num_generico,num_no_generico), 
        0),
        2) AS tasa_fiabilidad
FROM calculo_medias;