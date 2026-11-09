-- Densidad de la ficha técnica
-- Número de palabras en la sección 4.4 por tabla

CREATE OR REPLACE VIEW Densidad_ficha AS
SELECT nombre, 
volumen_informativo as numero_de_palabras_4_4,
complejidad_desglose as numero_de_tablas,
IFNULL(
    ROUND(
        volumen_informativo / complejidad_desglose, 
        2), 
        "No hay tablas en la ficha técnica") 
        AS densidad_ficha_tecnica 
FROM medicamentos;