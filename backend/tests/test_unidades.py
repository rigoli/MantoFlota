"""Pruebas CRUD unidades."""

import pytest

from app.models.enums import EstadoUnidad


@pytest.mark.asyncio
async def test_create_and_list_unidad(client):
    body = {
        "numero_economico": "ECO-001",
        "placas": "ABC-123",
        "marca": "Toyota",
        "modelo": "Hiace",
        "anio": 2020,
        "tipo_vehiculo": "Van",
        "kilometraje_actual": 10000,
        "estado": EstadoUnidad.activa.value,
    }
    r = await client.post("/api/v1/unidades", json=body)
    assert r.status_code == 201
    uid = r.json()["id"]

    r2 = await client.get("/api/v1/unidades")
    assert r2.status_code == 200
    assert len(r2.json()) == 1
    assert r2.json()[0]["id"] == uid


@pytest.mark.asyncio
async def test_negativo_kilometraje_422(client):
    body = {
        "numero_economico": "ECO-NEG",
        "placas": "NEG-111",
        "marca": "X",
        "modelo": "Y",
        "anio": 2021,
        "tipo_vehiculo": "Camión",
        "kilometraje_actual": -1,
        "estado": EstadoUnidad.activa.value,
    }
    r = await client.post("/api/v1/unidades", json=body)
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_duplicado_numero_economico_409(client):
    base = {
        "numero_economico": "DUP-01",
        "placas": "AAA-111",
        "marca": "M",
        "modelo": "Mo",
        "anio": 2022,
        "tipo_vehiculo": "Pickup",
        "kilometraje_actual": 0,
        "estado": EstadoUnidad.activa.value,
    }
    assert (await client.post("/api/v1/unidades", json=base)).status_code == 201
    dup = base.copy()
    dup["placas"] = "BBB-222"
    r = await client.post("/api/v1/unidades", json=dup)
    assert r.status_code == 409


@pytest.mark.asyncio
async def test_patch_unidad(client):
    body = {
        "numero_economico": "P-01",
        "placas": "CCC-333",
        "marca": "Ford",
        "modelo": "Ranger",
        "anio": 2019,
        "tipo_vehiculo": "Pickup",
        "kilometraje_actual": 5000,
        "estado": EstadoUnidad.activa.value,
    }
    uid = (await client.post("/api/v1/unidades", json=body)).json()["id"]
    r = await client.patch(
        f"/api/v1/unidades/{uid}",
        json={"placas": "CCC-999", "kilometraje_actual": 6000},
    )
    assert r.status_code == 200
    assert r.json()["placas"] == "CCC-999"
    assert r.json()["kilometraje_actual"] == 6000


@pytest.mark.asyncio
async def test_patch_kilometraje_invalido(client):
    body = {
        "numero_economico": "K-01",
        "placas": "DDD-444",
        "marca": "VW",
        "modelo": "Crafter",
        "anio": 2021,
        "tipo_vehiculo": "Van",
        "kilometraje_actual": 10000,
        "estado": EstadoUnidad.activa.value,
    }
    uid = (await client.post("/api/v1/unidades", json=body)).json()["id"]
    r = await client.patch(
        f"/api/v1/unidades/{uid}/kilometraje",
        json={"kilometraje_actual": 5000},
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_delete_unidad_404(client):
    r = await client.delete("/api/v1/unidades/99999")
    assert r.status_code == 404

