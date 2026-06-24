
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.models import ModelRegistry, User
from app.core.auth import get_current_user, require_role

router = APIRouter(prefix="/ai", tags=["AI/ML"])


@router.get("/model/status")
async def get_model_status(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ModelRegistry).where(ModelRegistry.is_active == True).order_by(ModelRegistry.created_at.desc()).limit(1)
    )
    model = result.scalar_one_or_none()
    if not model:
        return {"status": "no_model", "message": "No active model deployed"}
    return {
        "status": "active",
        "version": model.version,
        "metrics": model.metrics,
        "training_date": model.training_date.isoformat(),
        "feature_count": len(model.feature_list) if model.feature_list else 0,
    }


@router.post("/model/retrain", status_code=202)
async def trigger_retrain(current_user: User = Depends(require_role("admin")), db: AsyncSession = Depends(get_db)):
    return {"status": "retrain_triggered", "message": "Model retraining has been queued"}
