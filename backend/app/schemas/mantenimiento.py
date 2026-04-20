"""Schemas Pydantic para Mantenimiento."""

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.validators import parse_fecha_dd_mm_yyyy


class MantenimientoBase(BaseModel):
    """Campos de un mantenimiento."""

    tipo: str = Field(min_length=1, max_length=128)
    fecha_servicio: date
    kilometraje: int = Field(ge=0)
    costo: float = Field(ge=0)
    proveedor: str = Field(min_length=1, max_length=256)
    observaciones: str | None = Field(None, max_length=4000)
    responsable: str = Field(min_length=1, max_length=128)

    @field_validator("fecha_servicio", mode="before")
    @classmethod
    def _fecha_flexible(cls, v: Any) -> date:
        """Acepta ``date``, ISO string o ``dd/mm/aaaa``."""
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            s = v.strip()
            # ISO rápido
            if len(s) >= 10 and s[4] == "-":
                return date.fromisoformat(s[:10])
            return parse_fecha_dd_mm_yyyy(s)
        raise TypeError("fecha_servicio inválida")


class MantenimientoCreate(MantenimientoBase):
    """Alta de mantenimiento ligada a unidad en ruta."""

    pass


class MantenimientoUpdate(BaseModel):
    """Actualización parcial."""

    tipo: str | None = Field(None, min_length=1, max_length=128)
    fecha_servicio: date | None = None
    kilometraje: int | None = Field(None, ge=0)
    costo: float | None = Field(None, ge=0)
    proveedor: str | None = Field(None, min_length=1, max_length=256)
    observaciones: str | None = Field(None, max_length=4000)
    responsable: str | None = Field(None, min_length=1, max_length=128)

    @field_validator("fecha_servicio", mode="before")
    @classmethod
    def _fecha_opcional(cls, v: Any) -> date | None:
        if v is None or v == "":
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            s = v.strip()
            if len(s) >= 10 and s[4] == "-":
                return date.fromisoformat(s[:10])
            return parse_fecha_dd_mm_yyyy(s)
        raise TypeError("fecha_servicio inválida")


class MantenimientoRead(MantenimientoBase):
    """Respuesta completa."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    unidad_id: int
    creado_en: datetime
    actualizado_en: datetime


class MantenimientoListItem(MantenimientoRead):
    """Listado global con datos mínimos de la unidad."""

    numero_economico: str
    placas: str
