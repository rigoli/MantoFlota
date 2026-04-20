"""Ciclo de vida ASGI (``yield`` en lifespan)."""

import pytest

from app.main import app, lifespan


@pytest.mark.asyncio
async def test_lifespan_context_manager() -> None:
    async with lifespan(app):
        pass
