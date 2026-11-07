-- IVA por producto: 
-- Calcular la diferencia entre el PVP sin IVA y el PVP con IVA para conocer el importe correspondiente al IVA
CREATE OR REPLACE VIEW Importe_IVA AS
select nombre, precio_venta_publico_iva - precio_venta_publico_iva/1.21 as diferencia_neta
from medicamentos;