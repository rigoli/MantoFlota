"""Pruebas mantenimientos."""

import pytest

from app.models.enums import EstadoUnidad


async def _crear_unidad(client):
    body = {
        "numero_economico": "M-ECON",
        "placas": "MMM-999",
        "marca": "Isuzu",
        "modelo": "ELF",
        "anio": 2018,
        "tipo_vehiculo": "Camión",
        "kilometraje_actual": 20000,
        "estado": EstadoUnidad.activa.value,
    }
    r = await client.post("/api/v1/unidades", json=body)
    assert r.status_code == 201
    return r.json()["id"]


@pytest.mark.asyncio
async def test_registrar_y_consultar_mantenimiento(client):
    uid = await _crear_unidad(client)
    payload = {
        "tipo": "Preventivo",
        "fecha_servicio": "2026-04-01",
        "kilometraje": 20500,
        "costo": 1500.50,
        "proveedor": "Taller Central",
        "observaciones": "Cambio de aceite",
        "responsable": "Juan Pérez",
    }
    r = await client.post(f"/api/v1/unidades/{uid}/mantenimientos", json=payload)
    assert r.status_code == 201
    mid = r.json()["id"]

    hist = await client.get(f"/api/v1/unidades/{uid}/mantenimientos")
    assert hist.status_code == 200
    assert len(hist.json()) == 1
    assert hist.json()[0]["id"] == mid


@pytest.mark.asyncio
async def test_fecha_dd_mm_yyyy(client):
    uid = await _crear_unidad(client)
    payload = {
        "tipo": "Correctivo",
        "fecha_servicio": "15/03/2026",
        "kilometraje": 21000,
        "costo": 800,
        "proveedor": "X",
        "observaciones": None,
        "responsable": "María",
    }
    r = await client.post(f"/api/v1/unidades/{uid}/mantenimientos", json=payload)
    assert r.status_code == 201


@pytest.mark.asyncio
async def test_eliminar_mantenimiento(client):
    uid = await _crear_unidad(client)
    payload = {
        "tipo": "P",
        "fecha_servicio": "2026-01-01",
        "kilometraje": 20001,
        "costo": 100,
        "proveedor": "Y",
        "observaciones": "",
        "responsable": "Z",
    }
    mid = (
        await client.post(f"/api/v1/unidades/{uid}/mantenimientos", json=payload)
    ).json()["id"]
    r = await client.delete(f"/api/v1/mantenimientos/{mid}")
    assert r.status_code == 204
    hist = await client.get(f"/api/v1/unidades/{uid}/mantenimientos")
    assert hist.json() == []


@pytest.mark.asyncio
async def test_patch_mantenimiento(client):
    uid = await _crear_unidad(client)
    payload = {
        "tipo": "P",
        "fecha_servicio": "2026-02-02",
        "kilometraje": 20002,
        "costo": 200,
        "proveedor": "Prov",
        "observaciones": None,
        "responsable": "Resp",
    }
    mid = (
        await client.post(f"/api/v1/unidades/{uid}/mantenimientos", json=payload)
    ).json()["id"]
    r = await client.patch(
        f"/api/v1/mantenimientos/{mid}",
        json={"tipo": "Preventivo extendido"},
    )
    assert r.status_code == 200
    assert r.json()["tipo"] == "Preventivo extendido"


@pytest.mark.asyncio
async def test_list_mantenimientos_global(client):
    uid = await _crear_unidad(client)
    payload = {
        "tipo": "Lista global",
        "fecha_servicio": "2026-05-01",
        "kilometraje": 30000,
        "costo": 50,
        "proveedor": "T",
        "observaciones": None,
        "responsable": "R",
    }
    await client.post(f"/api/v1/unidades/{uid}/mantenimientos", json=payload)
    r = await client.get("/api/v1/mantenimientos?limit=50")
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 1
    row = next(x for x in data if x["tipo"] == "Lista global")
    assert row["numero_economico"] == "M-ECON"
    assert row["placas"] == "MMM-999"
    assert row["unidad_id"] == uid


@pytest.mark.asyncio
async def test_mantenimiento_sin_unidad(client):
    payload = {
        "tipo": "P",
        "fecha_servicio": "2026-02-02",
        "kilometraje": 1,
        "costo": 1,
        "proveedor": "P",
        "responsable": "R",
    }
    r = await client.post("/api/v1/unidades/99999/mantenimientos", json=payload)
    assert r.status_code == 400
