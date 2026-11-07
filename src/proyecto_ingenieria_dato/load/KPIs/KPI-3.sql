-- Total de componentes
CREATE OR REPLACE VIEW Total_componentes AS
select nombre, num_principios_activos+num_excipientes as total_componentes
from medicamentos;