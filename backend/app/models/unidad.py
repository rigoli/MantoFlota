"""Modelo Unidad (vehículo de flotilla)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, Numeric, String, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import EstadoUnidad

if TYPE_CHECKING:
    from app.models.mantenimiento import Mantenimiento


class Unidad(Base):
    """Unidad vehicular con kilometraje y estado."""

    __tablename__ = "unidades"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero_economico: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    placas: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    marca: Mapped[str] = mapped_column(String(128))
    modelo: Mapped[str] = mapped_column(String(128))
    anio: Mapped[int] = mapped_column(Integer)
    tipo_vehiculo: Mapped[str] = mapped_column(String(64))
    kilometraje_actual: Mapped[int] = mapped_column(Integer, default=0)
    estado: Mapped[EstadoUnidad] = mapped_column(
        SAEnum(
            EstadoUnidad,
            values_callable=lambda e: [m.value for m in e],
            native_enum=False,
            length=20,
        ),
        default=EstadoUnidad.activa,
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    mantenimientos: Mapped[list[Mantenimiento]] = relationship(
        "Mantenimiento",
        back_populates="unidad",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
