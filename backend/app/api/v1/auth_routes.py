from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.models import User, Tenant
from app.schemas.schemas import UserCreate, UserRead, UserLogin, TokenResponse, TenantCreate, TenantRead
from app.core.auth import hash_password, verify_password, create_access_token, create_refresh_token, decode_token, get_current_user
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRead, status_code=201)async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):    try:        existing = await db.execute(select(User).where(User.email == data.email))        if existing.scalar_one_or_none():            raise HTTPException(status_code=409, detail="Email already registered")        import random, string        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))        tenant = Tenant(id=uuid.uuid4(), name=f"{data.full_name}u0027s Workspace", slug=f"{data.email.split("@")[0]}-{suffix}")        db.add(tenant)        await db.flush()        user = User(email=data.email, password_hash=hash_password(data.password), full_name=data.full_name, tenant_id=tenant.id, role="admin")        db.add(user)        await db.commit()        await db.refresh(user)        return user    except Exception as e:        await db.rollback()        raise HTTPException(status_code=500, detail=str(e))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email, User.deleted_at.is_(None)))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_access_token(user.id, user.tenant_id, user.role)
    refresh = create_refresh_token(user.id, user.tenant_id)
    return TokenResponse(access_token=access, refresh_token=refresh, expires_in=3600)
