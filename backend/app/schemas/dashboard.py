"""Schemas para panel de inicio (resumen operativo)."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class ProximoMantenimientoRow(BaseModel):
    """Sugerencia de próximo preventivo (heurística: último servicio + 90 d / +10 000 km)."""

    unidad_id: int
    numero_economico: str
    placas: str
    marca: str
    modelo: str
    ultima_fecha_servicio: date | None = Field(
        description="Fecha del último mantenimiento registrado, si existe.",
    )
    ultimo_kilometraje_en_servicio: int | None = Field(
        description="Kilometraje en el último mantenimiento, si existe.",
    )
    kilometraje_actual: int
    proxima_fecha_estimada: date = Field(
        description="Estimación: última fecha + 90 días (sin historial: alta unidad + 90 d).",
    )
    proximo_kilometraje_estimado: int = Field(
        description="Estimación: km del último servicio + 10 000 (sin historial: km actual + 10 000).",
    )


class UnidadEnTallerRow(BaseModel):
    """Unidad en taller (pendiente de reincorporación a operación)."""

    unidad_id: int
    numero_economico: str
    placas: str
    marca: str
    modelo: str
    kilometraje_actual: int
    actualizado_en: datetime


class DashboardInicio(BaseModel):
    """Datos para la pantalla principal."""

    proximos_mantenimientos: list[ProximoMantenimientoRow]
    unidades_en_taller: list[UnidadEnTallerRow]
