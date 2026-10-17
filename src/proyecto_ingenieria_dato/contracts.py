from pydantic import Field, ConfigDict, BaseModel
from typing import Literal
from datetime import datetime

class Medicamento(BaseModel):

    model_config = ConfigDict(extra='forbid')

    nombre: str = Field(min_length=1)

    pactivos: str = Field(min_length=1)

    labtitular: str = Field(min_length=1)
    labcomercializador: str = Field(min_length=1)

    forma_farmaceutica_simplificada: Literal["COMPRIMIDO", "SOLUCIÓN", "PRODUCTO USO NASAL", "COMPRIMIDO BUCODISPERSABLE", \
                                             "COMPRIMIDO LIBERACION MODIFICADA", "CAPSULA", "INYECTABLE"]
    
    estado_aut: datetime

    estado_rev: datetime

    vias_administracion: Literal["VÍA ORAL", "VÍA NASAL", "VÍA INTRAVENOSA"]

    comercializado: int = Field(ge=0, le=1)

    generico: int = Field(ge=0, le=1)

    afecta_conduccion: int = Field(ge=0, le=1)

    num_principios_activos: int = Field(ge=1, le=2)

    Volumen_Informativo: int = Field(ge=0)

    Complejidad_Desglose: int = Field(ge=0)

    Indicador_Riesgo: int = Field(ge=0)

    Estado: Literal["ALTA", "BAJA POR NO COMERCIALIZAR", "BAJA GENERAL", "SUSPENSION TEMPORAL GENERAL"]

    Precio_venta_al_público_con_IVA: float = Field(gt=0, alias="Precio venta al público con IVA")

    Tratamiento_de_larga_duración: Literal["NO", "SI"] = Field(alias="Tratamiento de larga duración")