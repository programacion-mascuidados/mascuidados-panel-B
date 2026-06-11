from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ApifyLead(Base):
    __tablename__ = "apify_leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str | None] = mapped_column(String, nullable=True)
    telefono: Mapped[str | None] = mapped_column(String, nullable=True)
    ciudad: Mapped[str | None] = mapped_column(String, nullable=True)
    ciudad_responsable: Mapped[str | None] = mapped_column(String, nullable=True)
    nombre_responsable: Mapped[str | None] = mapped_column(String, nullable=True)
    estado: Mapped[str | None] = mapped_column(String, nullable=True)
    creado_en: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    flujo: Mapped[str | None] = mapped_column(String, nullable=True)
