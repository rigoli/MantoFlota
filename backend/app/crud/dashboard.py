"""Agregados para panel de inicio (heurísticas documentadas en schemas)."""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import mantenimiento as crud_mant
from app.crud import unidad as crud_uni
from app.models.enums import EstadoUnidad
from app.schemas.dashboard import (
    DashboardInicio,
    ProximoMantenimientoRow,
    UnidadEnTallerRow,
)

INTERVALO_DIAS_PREVENTIVO = 90
INTERVALO_KM_PREVENTIVO = 10_000


async def resumen_inicio(session: AsyncSession, *, limite_proximos: int = 20) -> DashboardInicio:
    """Construye sugerencias de próximos servicios y unidades en taller."""
    unidades = await crud_uni.listar_unidades(session)
    proximos: list[ProximoMantenimientoRow] = []
    en_taller: list[UnidadEnTallerRow] = []

    for u in unidades:
        if u.estado == EstadoUnidad.taller:
            en_taller.append(
                UnidadEnTallerRow(
                    unidad_id=u.id,
                    numero_economico=u.numero_economico,
                    placas=u.placas,
                    marca=u.marca,
                    modelo=u.modelo,
                    kilometraje_actual=u.kilometraje_actual,
                    actualizado_en=u.actualizado_en,
                )
            )
            continue

        if u.estado != EstadoUnidad.activa:
            continue

        hist = await crud_mant.listar_mantenimientos_por_unidad(session, u.id)
        if hist:
            last = hist[0]
            ult_f = last.fecha_servicio
            ult_km = last.kilometraje
            prox_f = ult_f + timedelta(days=INTERVALO_DIAS_PREVENTIVO)
            prox_km = ult_km + INTERVALO_KM_PREVENTIVO
        else:
            ult_f = None
            ult_km = None
            base = u.creado_en.date() if u.creado_en else date.today()
            prox_f = base + timedelta(days=INTERVALO_DIAS_PREVENTIVO)
            prox_km = u.kilometraje_actual + INTERVALO_KM_PREVENTIVO

        proximos.append(
            ProximoMantenimientoRow(
                unidad_id=u.id,
                numero_economico=u.numero_economico,
                placas=u.placas,
                marca=u.marca,
                modelo=u.modelo,
                ultima_fecha_servicio=ult_f,
                ultimo_kilometraje_en_servicio=ult_km,
                kilometraje_actual=u.kilometraje_actual,
                proxima_fecha_estimada=prox_f,
                proximo_kilometraje_estimado=prox_km,
            )
        )

    proximos.sort(key=lambda r: r.proxima_fecha_estimada)
    proximos = proximos[: max(1, limite_proximos)]

    en_taller.sort(key=lambda r: r.actualizado_en, reverse=True)

    return DashboardInicio(
        proximos_mantenimientos=proximos,
        unidades_en_taller=en_taller,
    )
