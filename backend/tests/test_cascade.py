"""Eliminación en cascada unidad → mantenimientos."""

import pytest

from app.models.enums import EstadoUnidad


@pytest.mark.asyncio
async def test_eliminar_unidad_borra_mantenimientos(client):
    body = {
        "numero_economico": "CAS-01",
        "placas": "CAS-111",
        "marca": "Nissan",
        "modelo": "NP300",
        "anio": 2017,
        "tipo_vehiculo": "Pickup",
        "kilometraje_actual": 80000,
        "estado": EstadoUnidad.activa.value,
    }
    uid = (await client.post("/api/v1/unidades", json=body)).json()["id"]
    mp = {
        "tipo": "Servicio",
        "fecha_servicio": "2026-05-01",
        "kilometraje": 80500,
        "costo": 300,
        "proveedor": "Z",
        "observaciones": None,
        "responsable": "Q",
    }
    mid = (await client.post(f"/api/v1/unidades/{uid}/mantenimientos", json=mp)).json()[
        "id"
    ]

    r_del = await client.delete(f"/api/v1/unidades/{uid}")
    assert r_del.status_code == 204

    r_m = await client.get(f"/api/v1/mantenimientos/{mid}")
    assert r_m.status_code == 404
