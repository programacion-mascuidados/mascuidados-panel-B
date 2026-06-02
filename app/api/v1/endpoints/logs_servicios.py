from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, require_auth
from app.models.logs_servicio import LogsServicio
from app.schemas.logs_servicio import LogsServicioListResponse

router = APIRouter(dependencies=[Depends(require_auth)])

DEFAULT_LIMIT = 500
MAX_LIMIT = 500


@router.get("", response_model=LogsServicioListResponse)
def list_logs_servicios(
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=1,
        le=MAX_LIMIT,
        description="Cantidad de registros a devolver (máximo 500)",
    ),
    db: Session = Depends(get_db_session),
) -> LogsServicioListResponse:
    rows = db.scalars(
        select(LogsServicio).order_by(LogsServicio.id.desc()).limit(limit)
    ).all()

    return LogsServicioListResponse(items=rows, limit=limit, count=len(rows))
