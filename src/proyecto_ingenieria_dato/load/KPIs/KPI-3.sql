-- Total de componentes
select nombre, num_principios_activos+num_excipientes as total_componentes
from medicamentos;