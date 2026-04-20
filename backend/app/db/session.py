"""Sesión async y motor SQLAlchemy."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import Settings, get_settings


def create_engine_and_session(settings: Settings | None = None):
    """Crea motor async y factory de sesiones."""
    cfg = settings or get_settings()
    engine = create_async_engine(
        cfg.database_url_async,
        echo=False,
        pool_pre_ping=True,
    )
    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    return engine, session_factory


_engine = None
_session_factory = None


def get_engine_session_factory():
    """Lazy init para tests que parchean settings."""
    global _engine, _session_factory
    if _engine is None or _session_factory is None:
        _engine, _session_factory = create_engine_and_session()
    return _engine, _session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependencia FastAPI: sesión con commit al finalizar la petición."""
    _, factory = get_engine_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
