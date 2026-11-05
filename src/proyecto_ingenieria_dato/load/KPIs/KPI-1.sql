use MUIAAp_2026;

-- Desviación de Precio (%): Calcular el porcentaje de diferencia entre el PVP-IVA
-- y el precio sin IVA mediante la fórmula: (PVP-IVA - PR) / PR * 100 (da el IVA)
select nombre, ((precio_venta_publico_iva - precio_venta_publico_iva/1.21) / (precio_venta_publico_iva / 1.21))*100 as desviacion_precio
from medicamentos;