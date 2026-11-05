use MUIAAp_2026;

-- Total de componentes
-- select nombre, num_principios_activos+num_excipientes as total_componentes
-- from medicamentos;

-- IVA por producto: 
-- Calcular la diferencia entre el PVP sin IVA y el PVP con IVA para conocer el importe correspondiente al IVA
select nombre, precio_venta_publico_iva - precio_venta_publico_iva/1.21 as diferencia_neta
from medicamentos;