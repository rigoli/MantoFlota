"""Validadores auxiliares."""

import pytest

from app.models.enums import EstadoUnidad
from app.validators import (
    leer_entero,
    leer_estado_unidad,
    leer_texto,
    parse_fecha_dd_mm_yyyy,
)


def test_leer_texto_vacio():
    with pytest.raises(ValueError):
        leer_texto("", obligatorio=True)


def test_leer_entero_invalido():
    with pytest.raises(ValueError):
        leer_entero("abc")


def test_parse_fecha_ok():
    d = parse_fecha_dd_mm_yyyy("19/04/2026")
    assert d.year == 2026 and d.month == 4 and d.day == 19


def test_parse_fecha_mala():
    with pytest.raises(ValueError):
        parse_fecha_dd_mm_yyyy("99/99/2026")


def test_estado_ok():
    assert leer_estado_unidad("activa") == EstadoUnidad.activa


def test_estado_malo():
    with pytest.raises(ValueError):
        leer_estado_unidad("xyz")
