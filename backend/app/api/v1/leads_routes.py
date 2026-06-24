
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.db.database import get_db
from app.models.models import Lead, Contact, User
from app.schemas.schemas import LeadCreate, LeadRead, LeadScoreResponse, PaginatedResponse
from app.core.auth import get_current_user

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("", response_model=PaginatedResponse)
async def list_leads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    min_score: float = Query(None, ge=0, le=1),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Lead).where(Lead.tenant_id == current_user.tenant_id, Lead.deleted_at.is_(None))
    if status:
        query = query.where(Lead.status == status)
    if min_score is not None:
        query = query.where(Lead.score >= min_score)
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar()
    query = query.offset((page - 1) * page_size).limit(page_size).order_by(Lead.score.desc().nullslast())
    result = await db.execute(query)
    leads = result.scalars().all()
    return PaginatedResponse(
        items=[LeadRead.model_validate(l) for l in leads],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=LeadRead, status_code=201)
async def create_lead(data: LeadCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    contact_result = await db.execute(select(Contact).where(Contact.id == data.contact_id, Contact.tenant_id == current_user.tenant_id))
    if not contact_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Contact not found")
    lead = Lead(**data.model_dump(), tenant_id= current_user.tenant_id)
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead


@router.get("/{lead_id}", response_model=LeadRead)
async def get_lead(lead_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lead).where(Lead.id == lead_id, Lead.tenant_id == current_user.tenant_id, Lead.deleted_at.is_(None)))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.post("/{lead_id}/score", response_model=LeadScoreResponse)
async def score_lead(lead_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lead).where(Lead.id == lead_id, Lead.tenant_id == current_user.tenant_id, Lead.deleted_at.is_(None)))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    from datetime import datetime
    from decimal import Decimal
    lead.score = Decimal("0.7500")
    lead.score_label = "B"
    lead.score_factors = {"top_positive": ["company_size", "email_opens"], "top_negative": ["no_website"]}
    lead.scored_at = datetime.utcnow()
    lead.model_version = "v1.0.0"
    await db.commit()
    return LeadScoreResponse(
        lead_id=lead.id, score=0.75, tier="B",
        factors=[{"feature": "company_size", "impact": 0.3}, {"feature": "email_opens", "impact": 0.2}],
        model_version="v1.0.0", scored_at=lead.scored_at,
    )


@router.post("/{lead_id}/convert", response_model=LeadRead)
async def convert_lead(lead_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lead).where(Lead.id == lead_id, Lead.tenant_id == current_user.tenant_id, Lead.deleted_at.is_(None)))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = "converted"
    await db.commit()
    return lead
