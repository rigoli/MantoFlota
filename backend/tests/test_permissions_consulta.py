"""403 cuando el rol no puede mutar datos."""

from types import SimpleNamespace

import pytest

from app.api.v1.deps_auth import get_current_active_user
from app.main import app
from app.models.enums import EstadoUnidad, RolUsuario


@pytest.fixture
def client_consulta_only(client):
    """Mismo cliente pero usuario con rol consulta."""

    async def _fake():
        return SimpleNamespace(
            id=2,
            email="consulta@t",
            nombre="C",
            rol=RolUsuario.consulta,
            activo=True,
            hashed_password="x",
        )

    app.dependency_overrides[get_current_active_user] = _fake
    yield client


@pytest.mark.asyncio
async def test_consulta_no_puede_crear_unidad(client_consulta_only):
    body = {
        "numero_economico": "X-1",
        "placas": "P-1",
        "marca": "M",
        "modelo": "M",
        "anio": 2020,
        "tipo_vehiculo": "T",
        "kilometraje_actual": 0,
        "estado": EstadoUnidad.activa.value,
    }
    r = await client_consulta_only.post("/api/v1/unidades", json=body)
    assert r.status_code == 403


@pytest.mark.asyncio
async def test_consulta_puede_leer_unidades(client_consulta_only):
    r = await client_consulta_only.get("/api/v1/unidades")
    assert r.status_code == 200
