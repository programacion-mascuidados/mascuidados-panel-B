from datetime import date, datetime, time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class LogsServicioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_registro: datetime | None = None
    codigo: str | None = None
    un: str | None = None
    fec_ini: date | None = None
    entra: time | None = None
    sale: time | None = None
    hs_total: Decimal | None = None
    dia: str | None = None
    nombre_beneficiario: str | None = None
    nombre_prestador: str | None = None
    perfil_prestador: str | None = None
    telefono_prestador_1: str | None = None
    asiste: str | None = None
    id_telefono: str | None = None
    telefono_prestador_2: str | None = None


class LogsServicioListResponse(BaseModel):
    items: list[LogsServicioRead]
    limit: int = Field(description="Cantidad máxima de filas solicitadas")
    count: int = Field(description="Cantidad de filas devueltas en esta respuesta")
