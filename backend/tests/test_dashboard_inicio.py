"""Panel /dashboard/inicio."""

from datetime import date

import pytest

from app.crud import dashboard as crud_dash
from app.crud import mantenimiento as crud_mant
from app.crud import unidad as crud_uni
from app.crud.dashboard import resumen_inicio
from app.models.enums import EstadoUnidad
from app.schemas.mantenimiento import MantenimientoCreate
from app.schemas.unidad import UnidadCreate


@pytest.mark.asyncio
async def test_resumen_dashboard_vacio(session):
    """Sin unidades activas ni taller: listas vacías."""
    dash = await resumen_inicio(session)
    assert dash.proximos_mantenimientos == []
    assert dash.unidades_en_taller == []


@pytest.mark.asyncio
async def test_dashboard_inicio_http(client):
    uid_act = (
        await client.post(
            "/api/v1/unidades",
            json={
                "numero_economico": "DSH-ACT",
                "placas": "DSA-01",
                "marca": "VW",
                "modelo": "Caddy",
                "anio": 2021,
                "tipo_vehiculo": "Van",
                "kilometraje_actual": 50000,
                "estado": EstadoUnidad.activa.value,
            },
        )
    ).json()["id"]
    await client.post(
        f"/api/v1/unidades/{uid_act}/mantenimientos",
        json={
            "tipo": "Preventivo",
            "fecha_servicio": "2026-01-15",
            "kilometraje": 49500,
            "costo": 3000,
            "proveedor": "T",
            "responsable": "R",
        },
    )

    uid_taller = (
        await client.post(
            "/api/v1/unidades",
            json={
                "numero_economico": "DSH-TALL",
                "placas": "DST-02",
                "marca": "Ford",
                "modelo": "Transit",
                "anio": 2020,
                "tipo_vehiculo": "Van",
                "kilometraje_actual": 120000,
                "estado": EstadoUnidad.taller.value,
            },
        )
    ).json()["id"]

    r = await client.get("/api/v1/dashboard/inicio")
    assert r.status_code == 200
    data = r.json()
    assert len(data["proximos_mantenimientos"]) >= 1
    eco = {x["numero_economico"] for x in data["proximos_mantenimientos"]}
    assert "DSH-ACT" in eco

    taller = data["unidades_en_taller"]
    assert len(taller) >= 1
    ids_t = {x["unidad_id"] for x in taller}
    assert uid_taller in ids_t


@pytest.mark.asyncio
async def test_resumen_inicio_directo_taller_y_activa_sin_historial(session):
    """Ejecuta el CRUD del dashboard vía sesión (trazado de cobertura en crud/dashboard)."""
    u_taller = await crud_uni.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="DIR-T",
            placas="DIR-01",
            marca="M",
            modelo="Mo",
            anio=2022,
            tipo_vehiculo="Van",
            kilometraje_actual=1000,
            estado=EstadoUnidad.taller,
        ),
    )
    u_act = await crud_uni.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="DIR-A",
            placas="DIR-02",
            marca="M",
            modelo="Mo",
            anio=2023,
            tipo_vehiculo="Van",
            kilometraje_actual=5000,
            estado=EstadoUnidad.activa,
        ),
    )
    await crud_uni.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="DIR-B",
            placas="DIR-03",
            marca="M",
            modelo="Mo",
            anio=2021,
            tipo_vehiculo="Van",
            kilometraje_actual=100,
            estado=EstadoUnidad.baja,
        ),
    )
    await session.commit()

    dash = await resumen_inicio(session)
    assert len(dash.unidades_en_taller) >= 1
    ids_t = {r.unidad_id for r in dash.unidades_en_taller}
    assert u_taller.id in ids_t
    prox_eco = {r.numero_economico for r in dash.proximos_mantenimientos}
    assert "DIR-A" in prox_eco
    assert "DIR-B" not in prox_eco

    row = next(r for r in dash.proximos_mantenimientos if r.unidad_id == u_act.id)
    assert row.ultima_fecha_servicio is None
    assert row.ultimo_kilometraje_en_servicio is None


@pytest.mark.asyncio
async def test_resumen_inicio_directo_activa_con_historial(session):
    u = await crud_uni.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="DIR-H",
            placas="DIR-04",
            marca="M",
            modelo="Mo",
            anio=2024,
            tipo_vehiculo="Van",
            kilometraje_actual=8000,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    await crud_mant.crear_mantenimiento(
        session,
        u.id,
        MantenimientoCreate(
            tipo="P",
            fecha_servicio=date(2025, 6, 1),
            kilometraje=7500,
            costo=100.0,
            proveedor="X",
            observaciones=None,
            responsable="Y",
        ),
    )
    await session.commit()

    dash = await resumen_inicio(session)
    row = next(r for r in dash.proximos_mantenimientos if r.unidad_id == u.id)
    assert row.ultima_fecha_servicio is not None
    assert row.ultimo_kilometraje_en_servicio == 7500


@pytest.mark.asyncio
async def test_resumen_inicio_limite_proximos(session):
    for i in range(3):
        await crud_uni.crear_unidad(
            session,
            UnidadCreate(
                numero_economico=f"LIM-{i}",
                placas=f"LM-{i:02d}",
                marca="M",
                modelo="Mo",
                anio=2020,
                tipo_vehiculo="Van",
                kilometraje_actual=i * 100,
                estado=EstadoUnidad.activa,
            ),
        )
    await session.commit()
    dash = await crud_dash.resumen_inicio(session, limite_proximos=2)
    assert len(dash.proximos_mantenimientos) == 2
