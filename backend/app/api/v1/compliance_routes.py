from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.schemas import DSARRequestCreate, DSARRequestResponse
from app.models.models import DSARRequest, User

router = APIRouter(prefix="/compliance", tags=["compliance"])

@router.get("/dsar")
async def list_dsar(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select, func
    query = select(DSARRequest).where(DSARRequest.tenant_id == current_user.tenant_id)
    if status:
        query = query.where(DSARRequest.status == status)
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    query = query.offset((page - 1) * page_size).limit(page_size).order_by(DSARRequest.created_at.desc())
    result = await db.execute(query)
    items = result.scalars().all()
    return {"items": items, "total": total or 0, "page": page, "page_size": page_size, "total_pages": (total or 0 + page_size - 1) // page_size}

@router.post("/dsar")
async def create_dsar(
    data: DSARRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    req = DSARRequest(**data.model_dump(), tenant_id=current_user.tenant_id, status="pending")
    db.add(req)
    await db.flush()
    await db.refresh(req)
    return req

@router.put("/dsar/{request_id}")
async def update_dsar(
    request_id: str,
    data: DSARRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select
    result = await db.execute(select(DSARRequest).where(DSARRequest.id == request_id, DSARRequest.tenant_id == current_user.tenant_id))
    req = result.scalar_one_or_none()
    if not req:
        raise HTTPException(status_code=404, detail="DSAR request not found")
    for k, v in data.model_dump().items():
        setattr(req, k, v)
    await db.flush()
    return req
