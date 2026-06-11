from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, func, nulls_last, select
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, require_leads_access
from app.models.lead_narela import LeadNarela
from app.schemas.lead_narela import LeadNarelaListResponse

router = APIRouter(dependencies=[Depends(require_leads_access)])

DEFAULT_LIMIT = 2000
MAX_LIMIT = 2000


@router.get("", response_model=LeadNarelaListResponse)
def list_leads_narela(
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=1,
        le=MAX_LIMIT,
        description="Cantidad de registros a devolver (máximo 500)",
    ),
    db: Session = Depends(get_db_session),
) -> LeadNarelaListResponse:
    rows = db.scalars(
        select(LeadNarela)
        .where(
            LeadNarela.situacion.isnot(None),
            func.length(func.trim(LeadNarela.situacion)) > 0,
        )
        .order_by(nulls_last(desc(LeadNarela.creado_en)), desc(LeadNarela.id))
        .limit(limit)
    ).all()

    return LeadNarelaListResponse(items=rows, limit=limit, count=len(rows))
