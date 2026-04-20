"""Configuración CORS."""

import os

from app.core.config import Settings, get_settings


def test_cors_origins_list_vacio(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL_ASYNC",
        os.environ.get(
            "DATABASE_URL_ASYNC",
            "mysql+asyncmy://root:root@localhost:8889/mantoflota_test",
        ),
    )
    monkeypatch.setenv(
        "DATABASE_URL_SYNC",
        os.environ.get(
            "DATABASE_URL_SYNC",
            "mysql+pymysql://root:root@localhost:8889/mantoflota_test",
        ),
    )
    monkeypatch.setenv("CORS_ORIGINS", "")
    get_settings.cache_clear()
    assert Settings().cors_origins_list == []


def test_cors_origins_list_ignora_segmentos_vacios(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL_ASYNC",
        os.environ.get(
            "DATABASE_URL_ASYNC",
            "mysql+asyncmy://root:root@localhost:8889/mantoflota_test",
        ),
    )
    monkeypatch.setenv(
        "DATABASE_URL_SYNC",
        os.environ.get(
            "DATABASE_URL_SYNC",
            "mysql+pymysql://root:root@localhost:8889/mantoflota_test",
        ),
    )
    monkeypatch.setenv(
        "CORS_ORIGINS",
        "http://localhost:3000, ,http://otro.local,   ",
    )
    get_settings.cache_clear()
    assert Settings().cors_origins_list == [
        "http://localhost:3000",
        "http://otro.local",
    ]
