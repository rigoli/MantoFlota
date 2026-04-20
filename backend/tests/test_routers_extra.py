"""Rutas adicionales (404 y listas vacías)."""

import pytest

from app.models.enums import EstadoUnidad


@pytest.mark.asyncio
async def test_get_unidad_404(client):
    r = await client.get("/api/v1/unidades/999999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_lista_unidades_vacia_inicial(client):
    r = await client.get("/api/v1/unidades")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_get_mantenimiento_404(client):
    r = await client.get("/api/v1/mantenimientos/999999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_patch_delete_mantenimiento_404(client):
    assert (
        await client.patch("/api/v1/mantenimientos/999999", json={"tipo": "X"})
    ).status_code == 404
    assert (
        await client.delete("/api/v1/mantenimientos/999999")
    ).status_code == 404


@pytest.mark.asyncio
async def test_historial_unidad_inexistente(client):
    r = await client.get("/api/v1/unidades/999999/mantenimientos")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_patch_kilometraje_ok(client):
    body = {
        "numero_economico": "KM-OK",
        "placas": "KM-OK-1",
        "marca": "M",
        "modelo": "M",
        "anio": 2020,
        "tipo_vehiculo": "T",
        "kilometraje_actual": 1000,
        "estado": EstadoUnidad.activa.value,
    }
    uid = (await client.post("/api/v1/unidades", json=body)).json()["id"]
    r = await client.patch(
        f"/api/v1/unidades/{uid}/kilometraje",
        json={"kilometraje_actual": 5000},
    )
    assert r.status_code == 200
    assert r.json()["kilometraje_actual"] == 5000


@pytest.mark.asyncio
async def test_duplicado_placas(client):
    base = {
        "numero_economico": "U1",
        "placas": "SAME",
        "marca": "M",
        "modelo": "M",
        "anio": 2020,
        "tipo_vehiculo": "T",
        "kilometraje_actual": 0,
        "estado": EstadoUnidad.activa.value,
    }
    await client.post("/api/v1/unidades", json=base)
    dup = dict(base)
    dup["numero_economico"] = "U2"
    r = await client.post("/api/v1/unidades", json=dup)
    assert r.status_code == 409
