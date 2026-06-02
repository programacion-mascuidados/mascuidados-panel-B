from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LogsServicio(Base):
    __tablename__ = "logs_servicios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_registro: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    codigo: Mapped[str | None] = mapped_column(String, nullable=True)
    un: Mapped[str | None] = mapped_column(String, nullable=True)
    fec_ini: Mapped[date | None] = mapped_column(Date, nullable=True)
    entra: Mapped[time | None] = mapped_column(Time, nullable=True)
    sale: Mapped[time | None] = mapped_column(Time, nullable=True)
    hs_total: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    dia: Mapped[str | None] = mapped_column(String, nullable=True)
    nombre_beneficiario: Mapped[str | None] = mapped_column(String, nullable=True)
    nombre_prestador: Mapped[str | None] = mapped_column(String, nullable=True)
    perfil_prestador: Mapped[str | None] = mapped_column(String, nullable=True)
    telefono_prestador_1: Mapped[str | None] = mapped_column(String, nullable=True)
    asiste: Mapped[str | None] = mapped_column(String, nullable=True)
    id_telefono: Mapped[str | None] = mapped_column(String, nullable=True)
    telefono_prestador_2: Mapped[str | None] = mapped_column(String, nullable=True)
