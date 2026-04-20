"""Autenticación JWT y permisos por rol."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import DbSession
from app.core.security import decode_access_token
from app.crud import usuario as crud_usuario
from app.models.enums import RolUsuario
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


async def get_current_user(
    session: DbSession,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Usuario:
    """Resuelve usuario desde Bearer JWT."""
    credentials_exc = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exc
        user_id = int(sub)
    except (JWTError, ValueError, TypeError) as exc:
        raise credentials_exc from exc

    user = await crud_usuario.obtener_usuario_por_id(session, user_id)
    if user is None or not user.activo:
        raise credentials_exc
    return user


async def get_current_active_user(
    user: Annotated[Usuario, Depends(get_current_user)],
) -> Usuario:
    """Usuario activo (alias explícito)."""
    return user


def require_roles(*allowed: RolUsuario):
    """Dependencia: solo roles indicados."""

    async def _check(
        user: Annotated[Usuario, Depends(get_current_active_user)],
    ) -> Usuario:
        if user.rol not in allowed:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail="Permisos insuficientes para esta operación",
            )
        return user

    return _check
