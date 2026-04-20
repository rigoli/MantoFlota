"""Panel de inicio — resumen operativo."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.deps import DbSession
from app.api.v1.deps_auth import get_current_active_user
from app.crud import dashboard as crud_dash
from app.models.usuario import Usuario
from app.schemas.dashboard import DashboardInicio

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

CurrentUser = Annotated[Usuario, Depends(get_current_active_user)]


@router.get("/inicio", response_model=DashboardInicio)
async def obtener_resumen_inicio(session: DbSession, _: CurrentUser) -> DashboardInicio:
    """Próximos mantenimientos sugeridos y unidades en taller."""
    return await crud_dash.resumen_inicio(session)
