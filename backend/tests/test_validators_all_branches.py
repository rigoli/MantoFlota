"""Cobertura de ramas en ``app/validators`` y esquemas de mantenimiento."""

from datetime import date

import pytest

from app.models.enums import EstadoUnidad
from app.schemas.mantenimiento import MantenimientoCreate, MantenimientoUpdate
from app.validators import (
    leer_decimal,
    leer_entero,
    leer_estado_unidad,
    leer_texto,
    parse_fecha_dd_mm_yyyy,
)


def test_leer_texto_none_obligatorio():
    with pytest.raises(ValueError):
        leer_texto(None, obligatorio=True)


def test_leer_texto_none_opcional():
    assert leer_texto(None, obligatorio=False) == ""


def test_leer_entero_none():
    with pytest.raises(ValueError):
        leer_entero(None)


def test_leer_entero_string_vacia():
    with pytest.raises(ValueError):
        leer_entero("   ")


def test_parse_fecha_segmento_vacio():
    with pytest.raises(ValueError):
        parse_fecha_dd_mm_yyyy("01//2026")


def test_parse_fecha_partes_no_tres():
    with pytest.raises(ValueError):
        parse_fecha_dd_mm_yyyy("01/02")


def test_parse_fecha_int_invalido():
    with pytest.raises(ValueError):
        parse_fecha_dd_mm_yyyy("aa/bb/cc")


def test_parse_fecha_objeto_date():
    d = date(2026, 4, 19)
    assert parse_fecha_dd_mm_yyyy(d) is d


def test_leer_estado_enum_passthrough():
    assert leer_estado_unidad(EstadoUnidad.taller) == EstadoUnidad.taller


def test_leer_estado_none():
    with pytest.raises(ValueError):
        leer_estado_unidad(None)


def test_leer_estado_vacio():
    with pytest.raises(ValueError):
        leer_estado_unidad("   ")


def test_mantenimiento_create_typeerror_fecha():
    with pytest.raises(TypeError):
        MantenimientoCreate(
            tipo="T",
            fecha_servicio=123,  # type: ignore[arg-type]
            kilometraje=1,
            costo=1,
            proveedor="P",
            responsable="R",
        )


def test_mantenimiento_update_fecha_iso():
    u = MantenimientoUpdate(fecha_servicio="2026-04-20")
    assert u.fecha_servicio is not None


def test_mantenimiento_update_fecha_objeto_date():
    d = date(2026, 5, 1)
    u = MantenimientoUpdate(fecha_servicio=d)
    assert u.fecha_servicio == d


def test_mantenimiento_update_fecha_ddmm():
    u = MantenimientoUpdate(fecha_servicio="20/04/2026")
    assert u.fecha_servicio.year == 2026


def test_mantenimiento_update_fecha_typeerror():
    with pytest.raises(TypeError):
        MantenimientoUpdate(fecha_servicio=[])  # type: ignore[arg-type]


def test_leer_decimal_none():
    with pytest.raises(ValueError):
        leer_decimal(None)
