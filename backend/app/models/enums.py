"""Enumeraciones de dominio."""

import enum


class EstadoUnidad(str, enum.Enum):
    """Estado operativo de la unidad en el sistema."""

    activa = "activa"
    taller = "taller"
    baja = "baja"


class RolUsuario(str, enum.Enum):
    """Rol de acceso a la API."""

    administrador = "administrador"
    operador = "operador"
    consulta = "consulta"
