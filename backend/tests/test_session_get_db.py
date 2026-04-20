"""Cobertura de ``get_db``."""

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import get_settings


@pytest.mark.asyncio
async def test_get_db_async_for(monkeypatch):
    import app.db.session as session_mod

    url = get_settings().database_url_async
    eng = create_async_engine(url, echo=False, poolclass=NullPool)
    factory = async_sessionmaker(eng, class_=AsyncSession, expire_on_commit=False)

    monkeypatch.setattr(
        session_mod,
        "get_engine_session_factory",
        lambda: (eng, factory),
    )

    from app.db.session import get_db

    n = 0
    async for sess in get_db():
        n += 1
        await sess.execute(text("SELECT 1"))
    assert n == 1

    await eng.dispose()
