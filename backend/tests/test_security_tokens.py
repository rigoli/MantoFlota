"""Hash y JWT (core.security)."""

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_password_hash_roundtrip() -> None:
    raw = "Secr3t-Password"
    h = get_password_hash(raw)
    assert verify_password(raw, h)
    assert not verify_password("other", h)


def test_jwt_encode_decode() -> None:
    get_settings.cache_clear()
    token = create_access_token(subject="99", claims={"extra": "x"})
    payload = decode_access_token(token)
    assert payload["sub"] == "99"
    assert payload["extra"] == "x"


def test_jwt_sin_claims_extra() -> None:
    """Rama ``if claims`` falsa en ``create_access_token``."""
    get_settings.cache_clear()
    token = create_access_token(subject="7")
    payload = decode_access_token(token)
    assert payload["sub"] == "7"
    assert "extra" not in payload
