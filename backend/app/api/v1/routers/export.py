"""Exportación de datos para respaldo (JSON y CSV)."""

import csv
from io import StringIO
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response

from app.api.v1.deps import DbSession
from app.api.v1.deps_auth import get_current_active_user
from app.crud import mantenimiento as crud_mant
from app.crud import unidad as crud_uni
from app.models.usuario import Usuario
from app.schemas.mantenimiento import MantenimientoListItem, MantenimientoRead
from app.schemas.unidad import UnidadRead

AnyUser = Annotated[Usuario, Depends(get_current_active_user)]

router = APIRouter(prefix="/export", tags=["export"])

_UNIDAD_CSV_COLUMNS: tuple[str, ...] = (
    "id",
    "numero_economico",
    "placas",
    "marca",
    "modelo",
    "anio",
    "tipo_vehiculo",
    "kilometraje_actual",
    "estado",
    "creado_en",
    "actualizado_en",
)

_MANT_CSV_COLUMNS: tuple[str, ...] = (
    "id",
    "unidad_id",
    "numero_economico",
    "placas",
    "tipo",
    "fecha_servicio",
    "kilometraje",
    "costo",
    "proveedor",
    "observaciones",
    "responsable",
    "creado_en",
    "actualizado_en",
)


def _csv_utf8_bom(rows: list[list[str]]) -> bytes:
    buf = StringIO()
    writer = csv.writer(buf)
    for row in rows:
        writer.writerow(row)
    return ("\ufeff" + buf.getvalue()).encode("utf-8")


async def _mantenimiento_list_items(
    session: DbSession, *, limit: int
) -> list[MantenimientoListItem]:
    raw = await crud_mant.listar_mantenimientos_global(session, limit=limit)
    out: list[MantenimientoListItem] = []
    for m, u in raw:
        base = MantenimientoRead.model_validate(m)
        out.append(
            MantenimientoListItem(
                **base.model_dump(),
                numero_economico=u.numero_economico,
                placas=u.placas,
            )
        )
    return out


@router.get("/unidades", response_model=list[UnidadRead])
async def exportar_unidades_json(
    session: DbSession,
    _: AnyUser,
) -> list[UnidadRead]:
    """Lista completa de unidades en JSON (respaldo)."""
    lista = await crud_uni.listar_unidades(session)
    return [UnidadRead.model_validate(u) for u in lista]


@router.get("/unidades/csv")
async def exportar_unidades_csv(session: DbSession, _: AnyUser) -> Response:
    """Exportación CSV de todas las unidades (UTF-8 con BOM para Excel)."""
    lista = await crud_uni.listar_unidades(session)
    reads = [UnidadRead.model_validate(u) for u in lista]
    body_rows: list[list[str]] = [list(_UNIDAD_CSV_COLUMNS)]
    for ent in reads:
        d = ent.model_dump(mode="json")
        body_rows.append(["" if d[k] is None else str(d[k]) for k in _UNIDAD_CSV_COLUMNS])
    content = _csv_utf8_bom(body_rows)
    return Response(
        content=content,
        media_type="text/csv; charset=utf-8",
    )


@router.get("/mantenimientos", response_model=list[MantenimientoListItem])
async def exportar_mantenimientos_json(
    session: DbSession,
    _: AnyUser,
    limit: int = Query(500, ge=1, le=500),
) -> list[MantenimientoListItem]:
    """Historial global en JSON (más recientes primero; hasta ``limit`` filas)."""
    return await _mantenimiento_list_items(session, limit=limit)


@router.get("/mantenimientos/csv")
async def exportar_mantenimientos_csv(
    session: DbSession,
    _: AnyUser,
    limit: int = Query(500, ge=1, le=500),
) -> Response:
    """Exportación CSV del historial global de mantenimientos."""
    items = await _mantenimiento_list_items(session, limit=limit)
    body_rows: list[list[str]] = [list(_MANT_CSV_COLUMNS)]
    for it in items:
        d = it.model_dump(mode="json")
        body_rows.append(["" if d[k] is None else str(d[k]) for k in _MANT_CSV_COLUMNS])
    content = _csv_utf8_bom(body_rows)
    return Response(
        content=content,
        media_type="text/csv; charset=utf-8",
    )
