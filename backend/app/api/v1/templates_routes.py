from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.schemas import EmailTemplateCreate, EmailTemplateRead
from app.models.models import EmailTemplate, User

router = APIRouter(prefix="/templates", tags=["templates"])

@router.get("/")
async def list_templates(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select, func
    query = select(EmailTemplate).where(EmailTemplate.tenant_id == current_user.tenant_id, EmailTemplate.deleted_at.is_(None))
    if category:
        query = query.where(EmailTemplate.category == category)
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    query = query.offset((page - 1) * page_size).limit(page_size).order_by(EmailTemplate.created_at.desc())
    result = await db.execute(query)
    items = result.scalars().all()
    return {"items": items, "total": total or 0, "page": page, "page_size": page_size, "total_pages": (total or 0 + page_size - 1) // page_size}

@router.get("/{template_id}")
async def get_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select
    result = await db.execute(select(EmailTemplate).where(EmailTemplate.id == template_id, EmailTemplate.tenant_id == current_user.tenant_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Template not found")
    return item

@router.post("/")
async def create_template(
    data: EmailTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = EmailTemplate(**data.model_dump(), tenant_id=current_user.tenant_id, created_by=current_user.id)
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item

@router.put("/{template_id}")
async def update_template(
    template_id: str,
    data: EmailTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select
    result = await db.execute(select(EmailTemplate).where(EmailTemplate.id == template_id, EmailTemplate.tenant_id == current_user.tenant_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Template not found")
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    await db.flush()
    return item

@router.delete("/{template_id}")
async def delete_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select
    from datetime import datetime
    result = await db.execute(select(EmailTemplate).where(EmailTemplate.id == template_id, EmailTemplate.tenant_id == current_user.tenant_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Template not found")
    item.deleted_at = datetime.utcnow()
    await db.flush()
    return {"ok": True}
