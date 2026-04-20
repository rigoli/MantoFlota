"""Rutas de mantenimiento por id global."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.v1.deps import DbSession
from app.api.v1.deps_auth import get_current_active_user, require_roles
from app.crud import mantenimiento as crud_mant
from app.models.enums import RolUsuario
from app.models.usuario import Usuario
from app.schemas.mantenimiento import (
    MantenimientoListItem,
    MantenimientoRead,
    MantenimientoUpdate,
)

AnyUser = Annotated[Usuario, Depends(get_current_active_user)]
WriteUser = Annotated[
    Usuario,
    Depends(require_roles(RolUsuario.administrador, RolUsuario.operador)),
]

router = APIRouter(prefix="/mantenimientos", tags=["mantenimientos"])


@router.get("", response_model=list[MantenimientoListItem])
async def listar_mantenimientos_globales(
    session: DbSession,
    _: AnyUser,
    limit: int = Query(100, ge=1, le=500),
) -> list[MantenimientoListItem]:
    """Lista mantenimientos de toda la flota (más recientes primero)."""
    rows = await crud_mant.listar_mantenimientos_global(session, limit=limit)
    out: list[MantenimientoListItem] = []
    for m, u in rows:
        base = MantenimientoRead.model_validate(m)
        out.append(
            MantenimientoListItem(
                **base.model_dump(),
                numero_economico=u.numero_economico,
                placas=u.placas,
            )
        )
    return out


@router.get("/{mantenimiento_id}", response_model=MantenimientoRead)
async def obtener_mantenimiento(
    session: DbSession,
    _: AnyUser,
    mantenimiento_id: int,
) -> MantenimientoRead:
    ent = await crud_mant.obtener_mantenimiento(session, mantenimiento_id)
    if ent is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Mantenimiento no encontrado",
        )
    return MantenimientoRead.model_validate(ent)


@router.patch("/{mantenimiento_id}", response_model=MantenimientoRead)
async def modificar_mantenimiento(
    session: DbSession,
    _: WriteUser,
    mantenimiento_id: int,
    body: MantenimientoUpdate,
) -> MantenimientoRead:
    ent = await crud_mant.actualizar_mantenimiento(session, mantenimiento_id, body)
    if ent is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Mantenimiento no encontrado",
        )
    await session.refresh(ent)
    return MantenimientoRead.model_validate(ent)


@router.delete("/{mantenimiento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_mantenimiento(
    session: DbSession,
    _: WriteUser,
    mantenimiento_id: int,
) -> None:
    ok = await crud_mant.eliminar_mantenimiento(session, mantenimiento_id)
    if not ok:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Mantenimiento no encontrado",
        )
