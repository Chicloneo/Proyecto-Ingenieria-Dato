CREATE OR REPLACE VIEW Densidad_ficha AS
SELECT volumen_informativo / complejidad_desglose AS resultado_division 
FROM medicamentos;