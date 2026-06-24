
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.db.database import get_db
from app.models.models import Contact, User
from app.schemas.schemas import ContactCreate, ContactRead, PaginatedResponse
from app.core.auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get("", response_model=PaginatedResponse)
async def list_contacts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    tag: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Contact).where(Contact.tenant_id == current_user.tenant_id, Contact.deleted_at.is_(None))
    if search:
        query = query.where(
            (Contact.first_name.ilike(f"%{search}%")) |
            (Contact.last_name.ilike(f"%{search}%")) |
            (Contact.email.ilike(f"%{search}%")) |
            (Contact.company.ilike(f"%{search}%"))
        )
    if tag:
        query = query.where(Contact.tags.contains([tag]))
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar()
    query = query.offset((page - 1) * page_size).limit(page_size).order_by(Contact.created_at.desc())
    result = await db.execute(query)
    contacts = result.scalars().all()
    return PaginatedResponse(
        items=[ContactRead.model_validate(c) for c in contacts],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=ContactRead, status_code=201)
async def create_contact(data: ContactCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    contact = Contact(**data.model_dump(), tenant_id=current_user.tenant_id)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


@router.get("/{contact_id}", response_model=ContactRead)
async def get_contact(contact_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contact).where(Contact.id == contact_id, Contact.tenant_id == current_user.tenant_id, Contact.deleted_at.is_(None)))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactRead)
async def update_contact(contact_id: UUID, data: ContactCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contact).where(Contact.id == contact_id, Contact.tenant_id == current_user.tenant_id, Contact.deleted_at.is_(None)))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(contact, k, v)
    await db.commit()
    await db.refresh(contact)
    return contact


@router.delete("/{contact_id}", status_code=204)
async def delete_contact(contact_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contact).where(Contact.id == contact_id, Contact.tenant_id == current_user.tenant_id, Contact.deleted_at.is_(None)))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    from datetime import datetime
    contact.deleted_at = datetime.utcnow()
    await db.commit()
