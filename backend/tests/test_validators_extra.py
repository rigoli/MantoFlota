"""Más ramas de validadores."""

import pytest

from app.validators import leer_decimal, leer_entero, leer_texto


def test_leer_texto_opcional():
    assert leer_texto("", obligatorio=False) == ""


def test_leer_entero_desde_int():
    assert leer_entero(5) == 5


def test_leer_decimal_desde_decimal():
    from decimal import Decimal

    d = leer_decimal(Decimal("10.5"), "x")
    assert d == Decimal("10.5")


def test_leer_decimal_invalido():
    with pytest.raises(ValueError):
        leer_decimal("no-es-numero", "x")
