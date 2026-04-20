"""CRUD de mantenimientos ligados a unidades."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mantenimiento import Mantenimiento
from app.models.unidad import Unidad
from app.schemas.mantenimiento import MantenimientoCreate, MantenimientoUpdate


async def crear_mantenimiento(
    session: AsyncSession, unidad_id: int, data: MantenimientoCreate
) -> Mantenimiento:
    """Registra un mantenimiento para una unidad existente."""
    unidad = await session.get(Unidad, unidad_id)
    if unidad is None:
        raise ValueError("La unidad no existe")
    entidad = Mantenimiento(
        unidad_id=unidad_id,
        tipo=data.tipo.strip(),
        fecha_servicio=data.fecha_servicio,
        kilometraje=data.kilometraje,
        costo=data.costo,
        proveedor=data.proveedor.strip(),
        observaciones=data.observaciones.strip() if data.observaciones else None,
        responsable=data.responsable.strip(),
    )
    session.add(entidad)
    try:
        await session.flush()
    except IntegrityError as exc:
        raise ValueError("No se pudo registrar el mantenimiento") from exc
    return entidad


async def obtener_mantenimiento(session: AsyncSession, mid: int) -> Mantenimiento | None:
    """Obtiene un mantenimiento por id."""
    return await session.get(Mantenimiento, mid)


async def listar_mantenimientos_global(
    session: AsyncSession, *, limit: int = 100
) -> list[tuple[Mantenimiento, Unidad]]:
    """Historial combinado ordenado por fecha de servicio (más reciente primero)."""
    lim = max(1, min(limit, 500))
    res = await session.execute(
        select(Mantenimiento, Unidad)
        .join(Unidad, Mantenimiento.unidad_id == Unidad.id)
        .order_by(Mantenimiento.fecha_servicio.desc(), Mantenimiento.id.desc())
        .limit(lim)
    )
    return list(res.all())


async def listar_mantenimientos_por_unidad(
    session: AsyncSession, unidad_id: int
) -> list[Mantenimiento]:
    """Historial de mantenimientos de una unidad (recorrido explícito con ciclo)."""
    res = await session.execute(
        select(Mantenimiento)
        .where(Mantenimiento.unidad_id == unidad_id)
        .order_by(Mantenimiento.fecha_servicio.desc())
    )
    filas = res.scalars().all()
    historial: list[Mantenimiento] = []
    for m in filas:
        historial.append(m)
    return historial


async def actualizar_mantenimiento(
    session: AsyncSession, mid: int, data: MantenimientoUpdate
) -> Mantenimiento | None:
    """Edita campos definidos del mantenimiento."""
    entidad = await obtener_mantenimiento(session, mid)
    if entidad is None:
        return None
    campos = data.model_dump(exclude_unset=True)
    for nombre, valor in campos.items():
        if valor is None:
            continue
        if nombre in {"tipo", "proveedor", "responsable"} and isinstance(valor, str):
            setattr(entidad, nombre, valor.strip())
        elif nombre == "observaciones" and valor is not None:
            if isinstance(valor, str):
                obs = valor.strip()
                setattr(entidad, nombre, obs or None)
            else:
                setattr(entidad, nombre, valor)
        else:
            setattr(entidad, nombre, valor)
    await session.flush()
    return entidad


async def eliminar_mantenimiento(session: AsyncSession, mid: int) -> bool:
    """Elimina un mantenimiento por id."""
    entidad = await obtener_mantenimiento(session, mid)
    if entidad is None:
        return False
    await session.delete(entidad)
    await session.flush()
    return True
