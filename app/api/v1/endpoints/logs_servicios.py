from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, require_auth
from app.models.logs_servicio import LogsServicio
from app.schemas.logs_servicio import LogsServicioListResponse
from app.utils.logs_servicio_filters import (
    apply_estado_filter,
    apply_llegada_filter,
    apply_sucursal_filter,
)

router = APIRouter(dependencies=[Depends(require_auth)])

DEFAULT_LIMIT = 500
MAX_LIMIT = 500
PAGE_SIZE_DEFAULT = 100
PAGE_SIZE_MAX = 500


def _escape_ilike(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def _apply_list_filters(
    query,
    *,
    nombre_prestador: str | None,
    fecha_desde: date | None,
    fecha_hasta: date | None,
    sucursal: str | None = None,
    estado: str | None = None,
    llegada: str | None = None,
):
    if nombre_prestador is not None:
        term = nombre_prestador.strip()
        pattern = f"%{_escape_ilike(term)}%"
        query = query.where(LogsServicio.nombre_prestador.ilike(pattern, escape="\\"))

    if fecha_desde is not None:
        query = query.where(LogsServicio.fec_ini >= fecha_desde)

    if fecha_hasta is not None:
        query = query.where(LogsServicio.fec_ini <= fecha_hasta)

    query = apply_sucursal_filter(query, sucursal)
    query = apply_estado_filter(query, estado)
    query = apply_llegada_filter(query, llegada)

    return query


@router.get("", response_model=LogsServicioListResponse)
def list_logs_servicios(
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=1,
        le=MAX_LIMIT,
        description="Cantidad de registros a devolver en la vista reciente (máximo 500)",
    ),
    nombre_prestador: str | None = Query(
        default=None,
        min_length=1,
        max_length=200,
        description="Filtra por nombre de prestador",
    ),
    fecha_desde: date | None = Query(
        default=None,
        description="Fecha de turno (fec_ini) desde, inclusive",
    ),
    fecha_hasta: date | None = Query(
        default=None,
        description="Fecha de turno (fec_ini) hasta, inclusive",
    ),
    sucursal: str | None = Query(
        default=None,
        description="Código de sucursal (ROS, PAR, CBA, BAS, SFE)",
    ),
    estado: str | None = Query(
        default=None,
        description="Estado del servicio (confirmado, cancelado, pendiente, etc.)",
    ),
    llegada: str | None = Query(
        default=None,
        description="Categoría de hora de llegada",
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Número de página (1-based) cuando hay filtros de prestador o fechas",
    ),
    page_size: int = Query(
        default=PAGE_SIZE_DEFAULT,
        ge=1,
        le=PAGE_SIZE_MAX,
        description="Registros por página cuando hay filtros de prestador o fechas",
    ),
    db: Session = Depends(get_db_session),
) -> LogsServicioListResponse:
    has_prestador = nombre_prestador is not None and nombre_prestador.strip() != ""
    has_date_filter = fecha_desde is not None or fecha_hasta is not None

    if fecha_desde is not None and fecha_hasta is not None and fecha_desde > fecha_hasta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fecha_desde no puede ser posterior a fecha_hasta",
        )

    if has_prestador or has_date_filter:
        prestador_term = nombre_prestador.strip() if has_prestador else None

        filtered = _apply_list_filters(
            select(LogsServicio),
            nombre_prestador=prestador_term,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            sucursal=sucursal,
            estado=estado,
            llegada=llegada,
        )
        count_query = _apply_list_filters(
            select(func.count()).select_from(LogsServicio),
            nombre_prestador=prestador_term,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            sucursal=sucursal,
            estado=estado,
            llegada=llegada,
        )

        total = db.scalar(count_query) or 0
        offset = (page - 1) * page_size

        rows = db.scalars(
            filtered.order_by(LogsServicio.id.desc()).offset(offset).limit(page_size)
        ).all()

        return LogsServicioListResponse(
            items=rows,
            limit=page_size,
            count=len(rows),
            total=total,
            page=page,
            page_size=page_size,
        )

    rows = db.scalars(
        select(LogsServicio).order_by(LogsServicio.id.desc()).limit(limit)
    ).all()

    count = len(rows)
    return LogsServicioListResponse(
        items=rows,
        limit=limit,
        count=count,
        total=count,
        page=1,
        page_size=limit,
    )
