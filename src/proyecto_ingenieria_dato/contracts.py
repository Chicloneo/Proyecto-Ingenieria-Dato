from pydantic import Field, ConfigDict, BaseModel, field_validator
from typing import Literal
from datetime import datetime

class Medicamento(BaseModel):

    model_config = ConfigDict(extra='forbid')


    nombre: str = Field(min_length=1, description="Nombre del medicamento.")

    pactivos: str = Field(min_length=1, description="Principios activos.")

    labtitular: str = Field(min_length=1, description="Laboratorio titular.")

    labcomercializador: str = Field(min_length=1, description="Laboratorio comercializador.")

    dosis: float = Field(gt=0, alias="dosis (mg)", description="Dosis en miligramos.")

    forma_farmaceutica_simplificada: Literal["COMPRIMIDO", "SOLUCIÓN", "PRODUCTO USO NASAL", "COMPRIMIDO BUCODISPERSABLE", \
                                             "COMPRIMIDO LIBERACION MODIFICADA", "CAPSULA", "INYECTABLE"] = Field(
        description="Forma farmacéutica simplificada."
    )

    estado_aut: datetime = Field(description="Fecha de autorización.")

    estado_rev: datetime = Field(description="Fecha de revisión.")

    vias_administracion: Literal["VÍA ORAL", "VÍA NASAL", "VÍA INTRAMUSCULAR"] = Field(
        description="Vía de administración."
    )

    comercializado: int = Field(ge=0, le=1, description="Indica si está comercializado (0/1).")

    generico: int = Field(ge=0, le=1, description="Indica si es genérico (0/1).")

    afecta_conduccion: int = Field(ge=0, le=1, description="Indica si afecta a la conducción (0/1).")

    num_principios_activos: int = Field(ge=1, le=2, description="Número de principios activos.")

    volumen_informativo: int = Field(ge=0, description="Volumen informativo asociado. "
                                     "Número de palabras en la sección 4.4 de su ficha técnica.",
                                     alias="Volumen_Informativo")

    complejidad_desglose: int = Field(ge=0, description="Complejidad del desglose. "
                                      "Número de tablas en su ficha técnica",
                                      alias="Complejidad_Desglose")

    indicador_riesgo: int = Field(ge=0, description="Indicador de riesgo. "
                                  "Número de veces que aparece la palabra 'grave' o 'graves' en su ficha técnica",
                                  alias="Indicador_Riesgo")

    estado: Literal["ALTA", "BAJA POR NO COMERCIALIZAR", "BAJA GENERAL", "SUSPENSION TEMPORAL GENERAL"] = Field(
        description="Estado administrativo del medicamento.",
        alias="Estado"
    )

    precio_venta_al_público_con_iva: float = Field(
        gt=0, alias="Precio venta al público con IVA", description="Precio de venta al público con IVA."
    )

    tratamiento_de_larga_duración: int = Field(
        ge=0,
        le=1,
        alias="Tratamiento de larga duración", description="Indica si es de larga duración."
        )