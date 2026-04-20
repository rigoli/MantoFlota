"""Aplicación FastAPI MantoFlota."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida: arranque y apagado."""
    yield


settings = get_settings()

app = FastAPI(
    title="MantoFlota API",
    description="Control de mantenimiento preventivo — Etapa 2",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list or ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health():
    """Comprobación rápida del servicio."""
    return {"status": "ok", "service": "mantoflota"}
