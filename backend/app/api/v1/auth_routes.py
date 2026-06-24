
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.models import User, Tenant
from app.schemas.schemas import UserCreate, UserRead, UserLogin, TokenResponse, TenantCreate, TenantRead
from app.core.auth import hash_password, verify_password, create_access_token, create_refresh_token, decode_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TenantRead, status_code=201)
async def register(data: TenantCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Tenant).where(Tenant.slug == data.slug))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Tenant slug already exists")
    tenant = Tenant(name=data.name, slug=data.slug, plan=data.plan)
    db.add(tenant)
    await db.flush()
    user = User(
        email=f"admin@{data.slug}.local",
        password_hash=hash_password("changeme123"),
        full_name="Admin",
        role="admin",
        tenant_id=tenant.id,
    )
    db.add(user)
    await db.commit()
    return tenant


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email, User.deleted_at.is_(None)))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_access_token(user.id, user.tenant_id, user.role)
    refresh = create_refresh_token(user.id, user.tenant_id)
    user.last_login_at = __import__("datetime").datetime.utcnow()
    await db.commit()
    return TokenResponse(access_token=access, refresh_token=refresh, expires_in=3600)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    from uuid import UUID
    user_id = UUID(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id, User.deleted_at.is_(None)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    access = create_access_token(user.id, user.tenant_id, user.role)
    new_refresh = create_refresh_token(user.id, user.tenant_id)
    return TokenResponse(access_token=access, refresh_token=new_refresh, expires_in=3600)


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
