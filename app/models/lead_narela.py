from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LeadNarela(Base):
    __tablename__ = "leads_narela"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str | None] = mapped_column(String, nullable=True)
    ciudad: Mapped[str | None] = mapped_column(String, nullable=True)
    fecha_ingreso: Mapped[date | None] = mapped_column(Date, nullable=True)
    porcentaje_cierre: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    prestacion: Mapped[str | None] = mapped_column(String, nullable=True)
    telefono: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    situacion: Mapped[str | None] = mapped_column(String, nullable=True)
    estado: Mapped[str | None] = mapped_column(String, nullable=True)
    mensaje_basura: Mapped[str | None] = mapped_column(String, nullable=True)
    creado_en: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
