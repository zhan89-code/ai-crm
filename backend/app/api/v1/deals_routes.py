
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.db.database import get_db
from app.models.models import Deal, User
from app.schemas.schemas import DealCreate, DealRead, DealStageUpdate, PaginatedResponse
from app.core.auth import get_current_user

router = APIRouter(prefix="/deals", tags=["Deals"])


@router.get("", response_model=PaginatedResponse)
async def list_deals(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    stage: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Deal).where(Deal.tenant_id == current_user.tenant_id, Deal.deleted_at.is_(None))
    if stage:
        query = query.where(Deal.stage == stage)
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar()
    query = query.offset((page - 1) * page_size).limit(page_size).order_by(Deal.created_at.desc())
    result = await db.execute(query)
    deals = result.scalars().all()
    return PaginatedResponse(
        items=[DealRead.model_validate(d) for d in deals],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=DealRead, status_code=201)
async def create_deal(data: DealCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    deal = Deal(**data.model_dump(), tenant_id=current_user.tenant_id)
    db.add(deal)
    await db.commit()
    await db.refresh(deal)
    return deal


@router.get("/{deal_id}", response_model=DealRead)
async def get_deal(deal_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Deal).where(Deal.id == deal_id, Deal.tenant_id == current_user.tenant_id, Deal.deleted_at.is_(None)))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.put("/{deal_id}", response_model=DealRead)
async def update_deal(deal_id: UUID, data: DealCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Deal).where(Deal.id == deal_id, Deal.tenant_id == current_user.tenant_id, Deal.deleted_at.is_(None)))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(deal, k, v)
    await db.commit()
    await db.refresh(deal)
    return deal


@router.patch("/{deal_id}/stage", response_model=DealRead)
async def update_deal_stage(deal_id: UUID, data: DealStageUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Deal).where(Deal.id == deal_id, Deal.tenant_id == current_user.tenant_id, Deal.deleted_at.is_(None)))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.stage = data.stage
    if data.probability is not None:
        deal.probability = data.probability
    if data.actual_close is not None:
        deal.actual_close = data.actual_close
    await db.commit()
    await db.refresh(deal)
    return deal


@router.delete("/{deal_id}", status_code=204)
async def delete_deal(deal_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Deal).where(Deal.id == deal_id, Deal.tenant_id == current_user.tenant_id, Deal.deleted_at.is_(None)))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    from datetime import datetime
    deal.deleted_at = datetime.utcnow()
    await db.commit()
