"""Validadores y lectura segura de datos (reutilizables, estilo consola / API).

Incluye condicionales explícitos y bucles donde corresponde (rúbrica Etapa 2).
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation

from app.models.enums import EstadoUnidad


def leer_texto(valor: str | None, obligatorio: bool = True, etiqueta: str = "campo") -> str:
    """Normaliza texto; rechaza vacío si es obligatorio."""
    if valor is None:
        if obligatorio:
            raise ValueError(f"{etiqueta}: valor requerido")
        return ""
    texto = valor.strip()
    if obligatorio and texto == "":
        raise ValueError(f"{etiqueta}: no puede estar vacío")
    return texto


def leer_entero(valor: str | int | None, etiqueta: str = "entero") -> int:
    """Parsea entero desde string o int."""
    if valor is None:
        raise ValueError(f"{etiqueta}: valor requerido")
    if isinstance(valor, int):
        return valor
    s = str(valor).strip()
    if s == "":
        raise ValueError(f"{etiqueta}: vacío")
    try:
        return int(s)
    except ValueError as exc:
        raise ValueError(f"{etiqueta}: no es un entero válido") from exc


def leer_decimal(valor: str | float | Decimal | None, etiqueta: str = "decimal") -> Decimal:
    """Parsea decimal positivo o cero."""
    if valor is None:
        raise ValueError(f"{etiqueta}: valor requerido")
    if isinstance(valor, Decimal):
        d = valor
    else:
        try:
            d = Decimal(str(valor).strip().replace(",", "."))
        except InvalidOperation as exc:
            raise ValueError(f"{etiqueta}: decimal inválido") from exc
    return d


def parse_fecha_dd_mm_yyyy(valor: str | date) -> date:
    """Convierte ``dd/mm/aaaa`` o devuelve ``date`` sin cambios."""
    if isinstance(valor, date):
        return valor
    s = str(valor).strip()
    partes = s.split("/")
    # Recorrer segmentos para validar longitud con ciclo explícito
    idx = 0
    while idx < len(partes):
        if partes[idx] == "":
            raise ValueError("Formato de fecha inválido; use dd/mm/aaaa")
        idx += 1
    if len(partes) != 3:
        raise ValueError("Formato de fecha inválido; use dd/mm/aaaa")
    try:
        dia = int(partes[0])
        mes = int(partes[1])
        anio = int(partes[2])
    except ValueError as exc:
        raise ValueError("Formato de fecha inválido; use dd/mm/aaaa") from exc
    return date(anio, mes, dia)


def leer_estado_unidad(valor: str | EstadoUnidad | None) -> EstadoUnidad:
    """Convierte texto a ``EstadoUnidad``."""
    if isinstance(valor, EstadoUnidad):
        return valor
    if valor is None or str(valor).strip() == "":
        raise ValueError("Estado de unidad requerido")
    clave = str(valor).strip().lower()
    for miembro in EstadoUnidad:
        if miembro.value == clave:
            return miembro
    raise ValueError("Estado inválido; use activa, taller o baja")
