#!/usr/bin/env python3
"""Sembrado desarrollo: usuarios (un rol c/u), vehículos demo y mantenimientos."""

from __future__ import annotations

import asyncio
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import Settings
from app.core.security import get_password_hash
from app.crud import mantenimiento as crud_mant
from app.crud import unidad as crud_uni
from app.crud import usuario as crud_u
from app.models.enums import EstadoUnidad, RolUsuario
from app.models.unidad import Unidad
from app.schemas.mantenimiento import MantenimientoCreate
from app.schemas.unidad import UnidadCreate

SEED_USERS: list[tuple[str, str, str, RolUsuario]] = [
    ("admin@manto.local", "Admin123!", "Administrador demo", RolUsuario.administrador),
    ("operador@manto.local", "Operador123!", "Operador demo", RolUsuario.operador),
    ("consulta@manto.local", "Consulta123!", "Consulta demo", RolUsuario.consulta),
]

# Unidades demo (numero_economico único en DB)
SEED_UNIDADES: list[tuple[str, str, str, str, int, str, int, EstadoUnidad]] = [
    (
        "DEMO-ECO-01",
        "ABC-123-A",
        "Toyota",
        "Hiace",
        2020,
        "Van",
        98500,
        EstadoUnidad.activa,
    ),
    (
        "DEMO-ECO-02",
        "XYZ-456-B",
        "Ford",
        "Transit",
        2019,
        "Van",
        112400,
        EstadoUnidad.activa,
    ),
    (
        "DEMO-ECO-03",
        "MNT-789-C",
        "Mercedes-Benz",
        "Sprinter",
        2021,
        "Van",
        45200,
        EstadoUnidad.taller,
    ),
]

# Mantenimientos por numero_economico (solo si la unidad no tiene historial aún)
SEED_MANTOS: dict[
    str,
    list[tuple[str, date, int, float, str, str | None, str]],
] = {
    "DEMO-ECO-01": [
        (
            "Preventivo programado",
            date(2025, 11, 8),
            98200,
            4200.50,
            "Taller Central MTY",
            "Aceite y filtros",
            "Carlos Méndez",
        ),
        (
            "Correctivo frenos",
            date(2025, 8, 14),
            97500,
            8950.00,
            "Frenos del Norte",
            "Pastillas y discos delanteros",
            "Ana Ruiz",
        ),
    ],
    "DEMO-ECO-02": [
        (
            "Preventivo",
            date(2026, 1, 20),
            111800,
            5100.00,
            "Taller Central MTY",
            None,
            "Luis Ortega",
        ),
        (
            "Revisión general",
            date(2025, 6, 3),
            108000,
            2400.00,
            "Servicio Rápido",
            "Inspección 50k km",
            "María León",
        ),
    ],
    "DEMO-ECO-03": [
        (
            "Diagnóstico taller",
            date(2026, 3, 2),
            45200,
            1200.00,
            "Electro Diesel SA",
            "Chequeo electrónico",
            "Pedro Soto",
        ),
    ],
}


async def seed_users(session: AsyncSession) -> None:
    """Usuarios por rol; idempotente por email."""
    for email, password, nombre, rol in SEED_USERS:
        existing = await crud_u.obtener_usuario_por_email(session, email)
        hp = get_password_hash(password)
        if existing:
            existing.hashed_password = hp
            existing.nombre = nombre
            existing.rol = rol
            existing.activo = True
        else:
            await crud_u.crear_usuario(
                session,
                email=email,
                hashed_password=hp,
                nombre=nombre,
                rol=rol,
            )
    await session.commit()


async def _obtener_unidad_por_ne(
    session: AsyncSession, numero_economico: str
) -> Unidad | None:
    res = await session.execute(
        select(Unidad).where(Unidad.numero_economico == numero_economico)
    )
    return res.scalar_one_or_none()


async def seed_demo_flota(session: AsyncSession) -> None:
    """Vehículos y mantenimientos demo; idempotente por número económico."""
    ne_to_id: dict[str, int] = {}

    for (
        numero_economico,
        placas,
        marca,
        modelo,
        anio,
        tipo,
        km,
        estado,
    ) in SEED_UNIDADES:
        exist = await _obtener_unidad_por_ne(session, numero_economico)
        if exist is None:
            u = await crud_uni.crear_unidad(
                session,
                UnidadCreate(
                    numero_economico=numero_economico,
                    placas=placas,
                    marca=marca,
                    modelo=modelo,
                    anio=anio,
                    tipo_vehiculo=tipo,
                    kilometraje_actual=km,
                    estado=estado,
                ),
            )
            ne_to_id[numero_economico] = u.id
        else:
            ne_to_id[numero_economico] = exist.id

    await session.commit()

    for ne, lista_m in SEED_MANTOS.items():
        uid = ne_to_id.get(ne)
        if uid is None:
            continue
        hist = await crud_mant.listar_mantenimientos_por_unidad(session, uid)
        if hist:
            continue
        for (
            tipo,
            fecha_servicio,
            kilometraje,
            costo,
            proveedor,
            observaciones,
            responsable,
        ) in lista_m:
            await crud_mant.crear_mantenimiento(
                session,
                uid,
                MantenimientoCreate(
                    tipo=tipo,
                    fecha_servicio=fecha_servicio,
                    kilometraje=kilometraje,
                    costo=costo,
                    proveedor=proveedor,
                    observaciones=observaciones,
                    responsable=responsable,
                ),
            )
        await session.commit()


async def seed(session: AsyncSession) -> None:
    await seed_users(session)
    await seed_demo_flota(session)


async def main() -> None:
    settings = Settings()  # type: ignore[call-arg]
    engine = create_async_engine(settings.database_url_async, echo=False)
    factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    async with factory() as session:
        await seed(session)
    await engine.dispose()
    print("Usuarios (desarrollo):")
    for email, password, nombre, rol in SEED_USERS:
        print(f"  {email} / {password} — {nombre} ({rol.value})")
    print(f"Unidades demo: {len(SEED_UNIDADES)} · Mantenimientos insertados si historial vacío.")
    for ne in SEED_MANTOS:
        print(f"  · {ne}: hasta {len(SEED_MANTOS[ne])} registros")


if __name__ == "__main__":
    asyncio.run(main())
