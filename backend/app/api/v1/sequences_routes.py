
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.db.database import get_db
from app.models.models import EmailSequence, EmailSequenceStep, EmailTemplate, User
from app.schemas.schemas import EmailSequenceCreate, EmailSequenceRead, EmailTemplateCreate, EmailTemplateRead, PaginatedResponse
from app.core.auth import get_current_user

router = APIRouter(prefix="/sequences", tags=["Email Sequences"])


@router.get("/templates", response_model=PaginatedResponse)
async def list_templates(
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
):
    query = select(EmailTemplate).where(EmailTemplate.tenant_id == current_user.tenant_id, EmailTemplate.deleted_at.is_(None))
    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return PaginatedResponse(
        items=[EmailTemplateRead.model_validate(t) for t in result.scalars().all()],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("/templates", response_model=EmailTemplateRead, status_code=201)
async def create_template(data: EmailTemplateCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    tpl = EmailTemplate(**data.model_dump(), tenant_id=current_user.tenant_id, created_by=current_user.id)
    db.add(tpl)
    await db.commit()
    await db.refresh(tpl)
    return tpl


@router.get("", response_model=PaginatedResponse)
async def list_sequences(
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
):
    query = select(EmailSequence).where(EmailSequence.tenant_id == current_user.tenant_id, EmailSequence.deleted_at.is_(None))
    if status:
        query = query.where(EmailSequence.status == status)
    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return PaginatedResponse(
        items=[EmailSequenceRead.model_validate(s) for s in result.scalars().all()],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=EmailSequenceRead, status_code=201)
async def create_sequence(data: EmailSequenceCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    seq_data = data.model_dump(exclude={"steps"})
    seq = EmailSequence(**seq_data, tenant_id=current_user.tenant_id, created_by=current_user.id)
    db.add(seq)
    await db.flush()
    for i, step_data in enumerate(data.steps):
        step = EmailSequenceStep(sequence_id=seq.id, step_order=i, **step_data)
        db.add(step)
    await db.commit()
    await db.refresh(seq)
    return seq


@router.get("/{sequence_id}", response_model=EmailSequenceRead)
async def get_sequence(sequence_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmailSequence).where(EmailSequence.id == sequence_id, EmailSequence.tenant_id == current_user.tenant_id, EmailSequence.deleted_at.is_(None)))
    seq = result.scalar_one_or_none()
    if not seq:
        raise HTTPException(status_code=404, detail="Sequence not found")
    return seq


@router.post("/{sequence_id}/enroll", status_code=204)
async def enroll_contact(sequence_id: UUID, contact_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmailSequence).where(EmailSequence.id == sequence_id, EmailSequence.tenant_id == current_user.tenant_id))
    seq = result.scalar_one_or_none()
    if not seq:
        raise HTTPException(status_code=404, detail="Sequence not found")
    seq.entry_count += 1
    await db.commit()
