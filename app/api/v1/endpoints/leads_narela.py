from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, nulls_last, select
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, require_leads_access
from app.models.lead_narela import LeadNarela
from app.schemas.lead_narela import (
    DismissMensajeBasuraRequest,
    LeadNarelaListResponse,
    LeadNarelaRead,
)
from app.utils.mensaje_basura import remove_mensaje_basura_at_index

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
        select(LeadNarela)
        .where(LeadNarela.estado.isnot(None))
        .order_by(nulls_last(desc(LeadNarela.creado_en)), desc(LeadNarela.id))
        .limit(limit)
    ).all()

    return LeadNarelaListResponse(items=rows, limit=limit, count=len(rows))


@router.patch("/{lead_id}/mensaje-basura/dismiss", response_model=LeadNarelaRead)
def dismiss_mensaje_basura(
    lead_id: int,
    payload: DismissMensajeBasuraRequest,
    db: Session = Depends(get_db_session),
) -> LeadNarelaRead:
    lead = db.get(LeadNarela, lead_id)
    if lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead no encontrado",
        )

    try:
        lead.mensaje_basura = remove_mensaje_basura_at_index(
            lead.mensaje_basura,
            payload.message_index,
        )
    except IndexError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Índice de mensaje inválido",
        ) from exc

    db.commit()
    db.refresh(lead)
    return lead
