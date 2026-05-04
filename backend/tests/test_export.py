"""Exportaciones JSON y CSV (/api/v1/export/*)."""

import pytest

from app.models.enums import EstadoUnidad


@pytest.mark.asyncio
async def test_export_unidades_json_vacio(client):
    r = await client.get("/api/v1/export/unidades")
    assert r.status_code == 200
    assert "application/json" in r.headers.get("content-type", "")
    assert r.json() == []


@pytest.mark.asyncio
async def test_export_unidades_csv_vacio(client):
    r = await client.get("/api/v1/export/unidades/csv")
    assert r.status_code == 200
    ct = r.headers.get("content-type", "")
    assert "text/csv" in ct
    raw = r.content.decode("utf-8-sig")
    assert raw.strip().startswith("id")
    lines = raw.strip().splitlines()
    assert len(lines) == 1


@pytest.mark.asyncio
async def test_export_unidades_json_y_csv_con_datos(client):
    await client.post(
        "/api/v1/unidades",
        json={
            "numero_economico": "EXP-001",
            "placas": "EXP-AAA",
            "marca": "Toyota",
            "modelo": "Hilux",
            "anio": 2023,
            "tipo_vehiculo": "Pickup",
            "kilometraje_actual": 12000,
            "estado": EstadoUnidad.activa.value,
        },
    )
    rj = await client.get("/api/v1/export/unidades")
    data = rj.json()
    assert len(data) >= 1
    assert "EXP-001" in {x["numero_economico"] for x in data}

    rc = await client.get("/api/v1/export/unidades/csv")
    text = rc.content.decode("utf-8-sig")
    assert "numero_economico" in text
    assert "EXP-001" in text
    assert "EXP-AAA" in text


@pytest.mark.asyncio
async def test_export_mantenimientos_json_y_csv(client):
    uid = (
        await client.post(
            "/api/v1/unidades",
            json={
                "numero_economico": "EXM-U",
                "placas": "EXM-PL",
                "marca": "VW",
                "modelo": "Caddy",
                "anio": 2022,
                "tipo_vehiculo": "Van",
                "kilometraje_actual": 30000,
                "estado": EstadoUnidad.activa.value,
            },
        )
    ).json()["id"]
    await client.post(
        f"/api/v1/unidades/{uid}/mantenimientos",
        json={
            "tipo": "Aceite",
            "fecha_servicio": "2026-02-01",
            "kilometraje": 29500,
            "costo": 1500.5,
            "proveedor": "Taller X",
            "responsable": "Ana",
        },
    )

    rj = await client.get("/api/v1/export/mantenimientos?limit=50")
    assert rj.status_code == 200
    assert "application/json" in rj.headers.get("content-type", "")
    js = rj.json()
    assert isinstance(js, list)
    assert len(js) >= 1
    tipos = {x["tipo"] for x in js}
    assert "Aceite" in tipos
    eco = {x["numero_economico"] for x in js}
    assert "EXM-U" in eco

    rc = await client.get("/api/v1/export/mantenimientos/csv?limit=50")
    assert rc.status_code == 200
    assert "text/csv" in rc.headers.get("content-type", "")
    text = rc.content.decode("utf-8-sig")
    assert "tipo" in text.splitlines()[0]
    assert "Aceite" in text
    assert "EXM-U" in text
