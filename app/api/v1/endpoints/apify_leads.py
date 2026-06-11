from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, func, nulls_last, select
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, require_leads_access
from app.models.apify_lead import ApifyLead
from app.schemas.apify_lead import ApifyLeadListResponse

router = APIRouter(dependencies=[Depends(require_leads_access)])

DEFAULT_LIMIT = 2000
MAX_LIMIT = 2000


@router.get("", response_model=ApifyLeadListResponse)
def list_apify_leads(
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=1,
        le=MAX_LIMIT,
        description="Cantidad de registros a devolver (máximo 2000)",
    ),
    db: Session = Depends(get_db_session),
) -> ApifyLeadListResponse:
    rows = db.scalars(
        select(ApifyLead)
        .where(
            ApifyLead.flujo.isnot(None),
            func.length(func.trim(ApifyLead.flujo)) > 0,
        )
        .order_by(nulls_last(desc(ApifyLead.creado_en)), desc(ApifyLead.id))
        .limit(limit)
    ).all()

    return ApifyLeadListResponse(items=rows, limit=limit, count=len(rows))
