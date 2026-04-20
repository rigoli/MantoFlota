"""Router API versión 1."""

from fastapi import APIRouter

from app.api.v1.routers import auth, dashboard, mantenimientos, unidades

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(dashboard.router)
api_router.include_router(unidades.router)
api_router.include_router(mantenimientos.router)
