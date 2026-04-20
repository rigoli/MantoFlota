"""Modelo Usuario (acceso API)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import RolUsuario


class Usuario(Base):
    """Usuario del sistema con rol y credenciales."""

    __tablename__ = "usuarios"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[str] = mapped_column(String(128))
    rol: Mapped[RolUsuario] = mapped_column(
        SAEnum(
            RolUsuario,
            values_callable=lambda e: [m.value for m in e],
            native_enum=False,
            length=32,
        ),
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
