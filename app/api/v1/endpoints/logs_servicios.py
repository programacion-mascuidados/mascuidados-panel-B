from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, require_auth
from app.models.logs_servicio import LogsServicio
from app.schemas.logs_servicio import LogsServicioListResponse

router = APIRouter(dependencies=[Depends(require_auth)])

DEFAULT_LIMIT = 500
MAX_LIMIT = 500
PRESTADOR_HISTORY_MAX = 10_000


def _escape_ilike(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


@router.get("", response_model=LogsServicioListResponse)
def list_logs_servicios(
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=1,
        le=MAX_LIMIT,
        description="Cantidad de registros a devolver (máximo 500)",
    ),
    nombre_prestador: str | None = Query(
        default=None,
        min_length=1,
        max_length=200,
        description="Filtra por nombre de prestador y devuelve su historial completo",
    ),
    db: Session = Depends(get_db_session),
) -> LogsServicioListResponse:
    if nombre_prestador is not None:
        term = nombre_prestador.strip()
        if not term:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="nombre_prestador no puede estar vacío",
            )

        pattern = f"%{_escape_ilike(term)}%"
        rows = db.scalars(
            select(LogsServicio)
            .where(LogsServicio.nombre_prestador.ilike(pattern, escape="\\"))
            .order_by(LogsServicio.id.desc())
            .limit(PRESTADOR_HISTORY_MAX)
        ).all()

        count = len(rows)
        return LogsServicioListResponse(items=rows, limit=count, count=count)

    rows = db.scalars(
        select(LogsServicio).order_by(LogsServicio.id.desc()).limit(limit)
    ).all()

    return LogsServicioListResponse(items=rows, limit=limit, count=len(rows))
