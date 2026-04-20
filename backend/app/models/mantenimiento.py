"""Modelo Mantenimiento asociado a una unidad."""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.unidad import Unidad


class Mantenimiento(Base):
    """Registro de mantenimiento preventivo o correctivo."""

    __tablename__ = "mantenimientos"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unidad_id: Mapped[int] = mapped_column(
        ForeignKey("unidades.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tipo: Mapped[str] = mapped_column(String(128))
    fecha_servicio: Mapped[date] = mapped_column(Date)
    kilometraje: Mapped[int] = mapped_column(Integer)
    costo: Mapped[float] = mapped_column(Numeric(12, 2))
    proveedor: Mapped[str] = mapped_column(String(256))
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsable: Mapped[str] = mapped_column(String(128))
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    unidad: Mapped[Unidad] = relationship("Unidad", back_populates="mantenimientos")
