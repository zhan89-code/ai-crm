
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.db.database import get_db
from app.models.models import CRMIntegration, User
from app.schemas.schemas import CRMIntegrationCreate, CRMIntegrationRead
from app.core.auth import get_current_user

router = APIRouter(prefix="/integrations", tags=["CRM Integrations"])


@router.get("", response_model=list[CRMIntegrationRead])
async def list_integrations(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CRMIntegration).where(CRMIntegration.tenant_id == current_user.tenant_id, CRMIntegration.deleted_at.is_(None))
    )
    return result.scalars().all()


@router.post("", response_model=CRMIntegrationRead, status_code=201)
async def create_integration(data: CRMIntegrationCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    integration = CRMIntegration(**data.model_dump(), tenant_id=current_user.tenant_id, created_by=current_user.id)
    db.add(integration)
    await db.commit()
    await db.refresh(integration)
    return integration


@router.post("/{integration_id}/sync", status_code=202)
async def trigger_sync(integration_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CRMIntegration).where(CRMIntegration.id == integration_id, CRMIntegration.tenant_id == current_user.tenant_id))
    integration = result.scalar_one_or_none()
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    from datetime import datetime
    integration.last_sync_at = datetime.utcnow()
    await db.commit()
    return {"status": "sync_triggered", "integration_id": str(integration_id)}
