from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.core.config import Settings, get_settings
from app.schemas.common import HealthResponse
from app.schemas.logs_servicio import LogsServicioRead

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db_session),
) -> HealthResponse:
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"

    return HealthResponse(
        status="ok" if db_status == "ok" else "degraded",
        app_name=settings.app_name,
        version=settings.app_version,
        database=db_status,
        control_cuentas_login_configured=settings.control_cuentas_login_enabled,
        logs_servicios_llego_a_tiempo="llego_a_tiempo"
        in LogsServicioRead.model_fields,
    )
