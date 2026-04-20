"""Schemas Pydantic para Unidad."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import EstadoUnidad


class UnidadBase(BaseModel):
    """Campos base compartidos."""

    numero_economico: str = Field(min_length=1, max_length=64)
    placas: str = Field(min_length=1, max_length=32)
    marca: str = Field(min_length=1, max_length=128)
    modelo: str = Field(min_length=1, max_length=128)
    anio: int = Field(ge=1900, le=2100)
    tipo_vehiculo: str = Field(min_length=1, max_length=64)
    kilometraje_actual: int = Field(ge=0)
    estado: EstadoUnidad


class UnidadCreate(UnidadBase):
    """Payload para alta de unidad."""

    pass


class UnidadUpdate(BaseModel):
    """Actualización parcial; campos None omiten cambio."""

    numero_economico: str | None = Field(None, min_length=1, max_length=64)
    placas: str | None = Field(None, min_length=1, max_length=32)
    marca: str | None = Field(None, min_length=1, max_length=128)
    modelo: str | None = Field(None, min_length=1, max_length=128)
    anio: int | None = Field(None, ge=1900, le=2100)
    tipo_vehiculo: str | None = Field(None, min_length=1, max_length=64)
    kilometraje_actual: int | None = Field(None, ge=0)
    estado: EstadoUnidad | None = None


class UnidadRead(UnidadBase):
    """Respuesta con id y timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    creado_en: datetime
    actualizado_en: datetime


class KilometrajeUpdate(BaseModel):
    """Actualización exclusiva del kilometraje."""

    kilometraje_actual: int = Field(ge=0)
