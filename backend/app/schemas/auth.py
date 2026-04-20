"""Esquemas autenticación."""

import re

from pydantic import BaseModel, Field, field_validator

from app.models.enums import RolUsuario

# EmailStr/email-validator rechazan TLD reservados (.local). Los seeds usan *.manto.local.
_LOGIN_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class LoginRequest(BaseModel):
    """Credenciales JSON."""

    email: str
    password: str = Field(min_length=1)

    @field_validator("email")
    @classmethod
    def email_normalizado(cls, v: str) -> str:
        s = v.strip().lower()
        if len(s) > 255 or not _LOGIN_EMAIL_RE.match(s):
            raise ValueError("Correo inválido")
        return s


class Token(BaseModel):
    """Respuesta OAuth2."""

    access_token: str
    token_type: str = "bearer"


class UsuarioMe(BaseModel):
    """Usuario autenticado (sin secreto)."""

    id: int
    email: str
    nombre: str
    rol: RolUsuario

    model_config = {"from_attributes": True}
