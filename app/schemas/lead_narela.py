from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class LeadNarelaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str | None = None
    ciudad: str | None = None
    fecha_ingreso: date | None = None
    porcentaje_cierre: Decimal | None = None
    prestacion: str | None = None
    telefono: str | None = None
    email: str | None = None
    situacion: str | None = None
    estado: str | None = None
    mensaje_basura: str | None = None
    creado_en: datetime | None = None


class LeadNarelaListResponse(BaseModel):
    items: list[LeadNarelaRead]
    limit: int = Field(description="Cantidad máxima de filas solicitadas")
    count: int = Field(description="Cantidad de filas devueltas en esta respuesta")


class DismissMensajeBasuraRequest(BaseModel):
    message_index: int = Field(
        ge=0,
        description="Índice del mensaje dentro de mensaje_basura (0-based)",
    )
