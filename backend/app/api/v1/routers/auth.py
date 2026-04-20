"""Login y usuario actual."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.deps import DbSession
from app.api.v1.deps_auth import get_current_active_user
from app.core.security import create_access_token, verify_password
from app.crud import usuario as crud_usuario
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, Token, UsuarioMe

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(session: DbSession, body: LoginRequest) -> Token:
    """Emite JWT si email/contraseña son válidos."""
    user = await crud_usuario.obtener_usuario_por_email(session, body.email)
    if user is None or not user.activo:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )
    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )
    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)


@router.get("/me", response_model=UsuarioMe)
async def me(current: Usuario = Depends(get_current_active_user)) -> UsuarioMe:
    """Perfil del usuario autenticado."""
    return UsuarioMe.model_validate(current)
