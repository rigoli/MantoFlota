"""Validación de esquemas de mantenimiento."""

from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.mantenimiento import MantenimientoCreate, MantenimientoUpdate


def test_fecha_iso():
    m = MantenimientoCreate(
        tipo="T",
        fecha_servicio="2026-04-19",
        kilometraje=1,
        costo=1,
        proveedor="P",
        responsable="R",
    )
    assert m.fecha_servicio.year == 2026


def test_fecha_invalida():
    with pytest.raises(ValidationError):
        MantenimientoCreate(
            tipo="T",
            fecha_servicio="no-fecha",
            kilometraje=1,
            costo=1,
            proveedor="P",
            responsable="R",
        )


def test_fecha_servicio_como_date():
    d = date(2026, 3, 15)
    m = MantenimientoCreate(
        tipo="T",
        fecha_servicio=d,
        kilometraje=1,
        costo=1,
        proveedor="P",
        responsable="R",
    )
    assert m.fecha_servicio == d


def test_create_fecha_servicio_tipo_invalido():
    with pytest.raises(TypeError, match="fecha_servicio"):
        MantenimientoCreate(
            tipo="T",
            fecha_servicio=12345,
            kilometraje=1,
            costo=1,
            proveedor="P",
            responsable="R",
        )


def test_update_fecha_servicio_vacia_string():
    u = MantenimientoUpdate(fecha_servicio="")
    assert u.fecha_servicio is None


def test_update_fecha_servicio_invalida():
    with pytest.raises(TypeError, match="fecha_servicio"):
        MantenimientoUpdate.model_validate({"fecha_servicio": 99})
