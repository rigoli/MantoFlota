"""Panel /dashboard/inicio."""

import pytest

from app.crud.dashboard import resumen_inicio
from app.models.enums import EstadoUnidad


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
