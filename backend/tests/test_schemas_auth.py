"""LoginRequest y validación de correo local."""

import pytest
from pydantic import ValidationError

from app.schemas.auth import LoginRequest


def test_login_email_valido_manto_local() -> None:
    m = LoginRequest(email="  Admin@Manto.LOCAL  ", password="x")
    assert m.email == "admin@manto.local"


@pytest.mark.parametrize(
    "email",
    [
        "sin-arroba",
        "@nodominio",
        "user@",
        "user @x.com",
        "a" * 252 + "@x.co",  # >255 caracteres
    ],
)
def test_login_email_invalido(email: str) -> None:
    with pytest.raises(ValidationError):
        LoginRequest(email=email, password="secret")
