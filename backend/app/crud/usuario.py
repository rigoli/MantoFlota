"""CRUD usuarios."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import RolUsuario
from app.models.usuario import Usuario


async def obtener_usuario_por_id(session: AsyncSession, usuario_id: int) -> Usuario | None:
    """Usuario por id."""
    res = await session.execute(select(Usuario).where(Usuario.id == usuario_id))
    return res.scalar_one_or_none()


async def obtener_usuario_por_email(session: AsyncSession, email: str) -> Usuario | None:
    """Usuario por email (normalizado minúsculas)."""
    email_norm = email.strip().lower()
    res = await session.execute(select(Usuario).where(Usuario.email == email_norm))
    return res.scalar_one_or_none()


async def crear_usuario(
    session: AsyncSession,
    *,
    email: str,
    hashed_password: str,
    nombre: str,
    rol: RolUsuario,
    activo: bool = True,
) -> Usuario:
    """Inserta usuario."""
    u = Usuario(
        email=email.strip().lower(),
        hashed_password=hashed_password,
        nombre=nombre.strip(),
        rol=rol,
        activo=activo,
    )
    session.add(u)
    await session.flush()
    return u
