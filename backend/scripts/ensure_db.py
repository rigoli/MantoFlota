#!/usr/bin/env python3
"""Crea las bases ``mantoflota`` y ``mantoflota_test`` si no existen (MAMP MySQL)."""

from __future__ import annotations

import sys
from pathlib import Path

# Permite importar ``app`` al ejecutar desde ``backend/``
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pymysql  # noqa: E402
from sqlalchemy.engine.url import make_url  # noqa: E402

from app.core.config import Settings  # noqa: E402


def ensure_databases() -> None:
    """Ejecuta ``CREATE DATABASE IF NOT EXISTS`` en utf8mb4."""
    settings = Settings()  # type: ignore[call-arg]
    url = make_url(settings.database_url_sync)
    port = url.port or 3306
    conn = pymysql.connect(
        host=url.host or "localhost",
        port=int(port),
        user=url.username or "root",
        password=url.password or "",
        charset="utf8mb4",
    )
    try:
        with conn.cursor() as cur:
            for name in ("mantoflota", "mantoflota_test"):
                cur.execute(
                    (
                        "CREATE DATABASE IF NOT EXISTS `{}` "
                        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                    ).format(name)
                )
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    ensure_databases()
    print("Bases mantoflota / mantoflota_test verificadas.")
