"""Rutas de unidades y mantenimientos anidados."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.deps import DbSession
from app.api.v1.deps_auth import get_current_active_user, require_roles
from app.crud import mantenimiento as crud_mant
from app.crud import unidad as crud_uni
from app.models.enums import RolUsuario
from app.models.usuario import Usuario
from app.schemas.mantenimiento import (
    MantenimientoCreate,
    MantenimientoRead,
    MantenimientoUpdate,
)
from app.schemas.unidad import KilometrajeUpdate, UnidadCreate, UnidadRead, UnidadUpdate

AnyUser = Annotated[Usuario, Depends(get_current_active_user)]
WriteUser = Annotated[
    Usuario,
    Depends(require_roles(RolUsuario.administrador, RolUsuario.operador)),
]
AdminOnly = Annotated[Usuario, Depends(require_roles(RolUsuario.administrador))]

router = APIRouter(prefix="/unidades", tags=["unidades"])


@router.post("", response_model=UnidadRead, status_code=status.HTTP_201_CREATED)
async def crear_unidad(
    session: DbSession,
    _: WriteUser,
    body: UnidadCreate,
) -> UnidadRead:
    try:
        ent = await crud_uni.crear_unidad(session, body)
    except ValueError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    await session.refresh(ent)
    return UnidadRead.model_validate(ent)


@router.get("", response_model=list[UnidadRead])
async def listar_unidades(
    session: DbSession,
    _: AnyUser,
) -> list[UnidadRead]:
    lista = await crud_uni.listar_unidades(session)
    return [UnidadRead.model_validate(u) for u in lista]


@router.get("/{unidad_id}", response_model=UnidadRead)
async def obtener_unidad(
    session: DbSession,
    _: AnyUser,
    unidad_id: int,
) -> UnidadRead:
    ent = await crud_uni.obtener_unidad_por_id(session, unidad_id)
    if ent is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unidad no encontrada")
    return UnidadRead.model_validate(ent)


@router.patch("/{unidad_id}", response_model=UnidadRead)
async def modificar_unidad(
    session: DbSession,
    _: WriteUser,
    unidad_id: int,
    body: UnidadUpdate,
) -> UnidadRead:
    try:
        ent = await crud_uni.actualizar_unidad(session, unidad_id, body)
    except ValueError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    if ent is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unidad no encontrada")
    await session.refresh(ent)
    return UnidadRead.model_validate(ent)


@router.delete("/{unidad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_unidad(
    session: DbSession,
    _: AdminOnly,
    unidad_id: int,
) -> None:
    ok = await crud_uni.eliminar_unidad(session, unidad_id)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unidad no encontrada")


@router.patch("/{unidad_id}/kilometraje", response_model=UnidadRead)
async def patch_kilometraje(
    session: DbSession,
    _: WriteUser,
    unidad_id: int,
    body: KilometrajeUpdate,
) -> UnidadRead:
    try:
        ent = await crud_uni.actualizar_kilometraje(
            session, unidad_id, body.kilometraje_actual
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if ent is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unidad no encontrada")
    await session.refresh(ent)
    return UnidadRead.model_validate(ent)


@router.post(
    "/{unidad_id}/mantenimientos",
    response_model=MantenimientoRead,
    status_code=status.HTTP_201_CREATED,
)
async def crear_mantenimiento_en_unidad(
    session: DbSession,
    _: WriteUser,
    unidad_id: int,
    body: MantenimientoCreate,
) -> MantenimientoRead:
    try:
        ent = await crud_mant.crear_mantenimiento(session, unidad_id, body)
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    await session.refresh(ent)
    return MantenimientoRead.model_validate(ent)


@router.get(
    "/{unidad_id}/mantenimientos",
    response_model=list[MantenimientoRead],
)
async def historial_mantenimientos(
    session: DbSession,
    _: AnyUser,
    unidad_id: int,
) -> list[MantenimientoRead]:
    uni = await crud_uni.obtener_unidad_por_id(session, unidad_id)
    if uni is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unidad no encontrada")
    lista = await crud_mant.listar_mantenimientos_por_unidad(session, unidad_id)
    return [MantenimientoRead.model_validate(m) for m in lista]
