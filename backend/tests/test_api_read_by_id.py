"""GET individual 200."""

import pytest

from app.models.enums import EstadoUnidad


@pytest.mark.asyncio
async def test_get_unidad_y_mantenimiento_200(client):
    ubody = {
        "numero_economico": "GID-1",
        "placas": "GID-PL",
        "marca": "M",
        "modelo": "M",
        "anio": 2024,
        "tipo_vehiculo": "T",
        "kilometraje_actual": 100,
        "estado": EstadoUnidad.activa.value,
    }
    uid = (await client.post("/api/v1/unidades", json=ubody)).json()["id"]
    gu = await client.get(f"/api/v1/unidades/{uid}")
    assert gu.status_code == 200
    assert gu.json()["placas"] == "GID-PL"

    mbody = {
        "tipo": "Rev",
        "fecha_servicio": "2026-06-01",
        "kilometraje": 150,
        "costo": 99.99,
        "proveedor": "Prov",
        "observaciones": None,
        "responsable": "R",
    }
    mid = (
        await client.post(f"/api/v1/unidades/{uid}/mantenimientos", json=mbody)
    ).json()["id"]
    gm = await client.get(f"/api/v1/mantenimientos/{mid}")
    assert gm.status_code == 200
    assert gm.json()["unidad_id"] == uid
