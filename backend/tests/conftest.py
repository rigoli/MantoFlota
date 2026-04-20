"""Configuración pytest: motor async por prueba (evita conflicto de event loops)."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.db.session import get_db

os.environ.setdefault(
    "DATABASE_URL_ASYNC",
    os.environ.get(
        "TEST_DATABASE_URL_ASYNC",
        "mysql+asyncmy://root:root@localhost:8889/mantoflota_test",
    ),
)
os.environ.setdefault(
    "DATABASE_URL_SYNC",
    os.environ.get(
        "TEST_DATABASE_URL_SYNC",
        "mysql+pymysql://root:root@localhost:8889/mantoflota_test",
    ),
)
os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000")
os.environ.setdefault(
    "JWT_SECRET_KEY",
    "pytest-jwt-secret-key-must-be-long-enough-for-hs256-tests",
)

from app.core.config import get_settings  # noqa: E402

get_settings.cache_clear()

from app.api.v1.deps_auth import get_current_active_user  # noqa: E402
from app.main import app  # noqa: E402
from app.models.enums import RolUsuario  # noqa: E402


@pytest_asyncio.fixture
async def engine():
    """Nuevo motor y tablas por prueba (aislado y mismo loop que el test)."""
    url = os.environ["DATABASE_URL_ASYNC"]
    eng = create_async_engine(
        url,
        echo=False,
        poolclass=NullPool,
    )
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()


@pytest_asyncio.fixture
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    async with factory() as sess:
        yield sess


@pytest_asyncio.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def _fake_admin():
        class _U:
            id = 1
            email = "pytest@local"
            nombre = "Pytest"
            rol = RolUsuario.administrador
            activo = True
            hashed_password = "x"

        return _U()

    async def _get_db():
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

    app.dependency_overrides[get_db] = _get_db
    app.dependency_overrides[get_current_active_user] = _fake_admin
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
