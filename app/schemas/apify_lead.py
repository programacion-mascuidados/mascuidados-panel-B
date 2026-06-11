from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ApifyLeadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str | None = None
    telefono: str | None = None
    ciudad: str | None = None
    ciudad_responsable: str | None = None
    nombre_responsable: str | None = None
    estado: str | None = None
    creado_en: datetime | None = None


class ApifyLeadListResponse(BaseModel):
    items: list[ApifyLeadRead]
    limit: int = Field(description="Cantidad máxima de filas solicitadas")
    count: int = Field(description="Cantidad de filas devueltas en esta respuesta")
