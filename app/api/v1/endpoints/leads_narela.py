from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, require_leads_access
from app.models.lead_narela import LeadNarela
from app.schemas.lead_narela import LeadNarelaListResponse

router = APIRouter(dependencies=[Depends(require_leads_access)])

DEFAULT_LIMIT = 500
MAX_LIMIT = 500


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
        select(LeadNarela).order_by(LeadNarela.id.desc()).limit(limit)
    ).all()

    return LeadNarelaListResponse(items=rows, limit=limit, count=len(rows))
