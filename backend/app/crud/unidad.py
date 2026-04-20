"""Operaciones CRUD para unidades.

Se usan condicionales para validar reglas de negocio y bucles para recorrer
resultados al exponer listas (requisitos de documentación Etapa 2).
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.unidad import Unidad
from app.schemas.unidad import UnidadCreate, UnidadUpdate


async def crear_unidad(session: AsyncSession, data: UnidadCreate) -> Unidad:
    """Registra una nueva unidad vehicular."""
    entidad = Unidad(
        numero_economico=data.numero_economico.strip(),
        placas=data.placas.strip(),
        marca=data.marca.strip(),
        modelo=data.modelo.strip(),
        anio=data.anio,
        tipo_vehiculo=data.tipo_vehiculo.strip(),
        kilometraje_actual=data.kilometraje_actual,
        estado=data.estado,
    )
    session.add(entidad)
    try:
        await session.flush()
    except IntegrityError as exc:
        raise ValueError("Número económico o placas duplicados") from exc
    return entidad


async def obtener_unidad_por_id(session: AsyncSession, unidad_id: int) -> Unidad | None:
    """Consulta una unidad por identificador."""
    res = await session.execute(select(Unidad).where(Unidad.id == unidad_id))
    return res.scalar_one_or_none()


async def listar_unidades(session: AsyncSession) -> list[Unidad]:
    """Lista todas las unidades registradas."""
    res = await session.execute(select(Unidad).order_by(Unidad.id.asc()))
    filas = res.scalars().all()
    resultado: list[Unidad] = []
    for unidad in filas:
        resultado.append(unidad)
    return resultado


async def actualizar_unidad(
    session: AsyncSession, unidad_id: int, data: UnidadUpdate
) -> Unidad | None:
    """Modifica campos no nulos de una unidad existente."""
    entidad = await obtener_unidad_por_id(session, unidad_id)
    if entidad is None:
        return None
    campos = data.model_dump(exclude_unset=True)
    for nombre, valor in campos.items():
        if valor is None:
            continue
        if nombre == "numero_economico" and isinstance(valor, str):
            setattr(entidad, nombre, valor.strip())
        elif nombre == "placas" and isinstance(valor, str):
            setattr(entidad, nombre, valor.strip())
        elif nombre in {"marca", "modelo", "tipo_vehiculo"} and isinstance(valor, str):
            setattr(entidad, nombre, valor.strip())
        else:
            setattr(entidad, nombre, valor)
    try:
        await session.flush()
    except IntegrityError as exc:
        raise ValueError("Número económico o placas duplicados") from exc
    return entidad


async def eliminar_unidad(session: AsyncSession, unidad_id: int) -> bool:
    """Elimina una unidad; los mantenimientos se borran en cascada (FK)."""
    entidad = await obtener_unidad_por_id(session, unidad_id)
    if entidad is None:
        return False
    await session.delete(entidad)
    await session.flush()
    return True


async def actualizar_kilometraje(
    session: AsyncSession, unidad_id: int, nuevo_km: int
) -> Unidad | None:
    """Actualiza kilometraje si el nuevo valor no es menor al registrado."""
    entidad = await obtener_unidad_por_id(session, unidad_id)
    if entidad is None:
        return None
    if nuevo_km < entidad.kilometraje_actual:
        raise ValueError(
            "El kilometraje nuevo no puede ser menor al kilometraje actual"
        )
    entidad.kilometraje_actual = nuevo_km
    await session.flush()
    return entidad
