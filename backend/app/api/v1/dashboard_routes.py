
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.models import Deal, Lead, EmailLog, ModelRegistry, User
from app.schemas.schemas import DashboardSummary
from app.core.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    pipeline_result = await db.execute(
        select(func.count(Deal.id), func.coalesce(func.sum(Deal.amount), 0))
        .where(Deal.tenant_id == current_user.tenant_id, Deal.deleted_at.is_(None))
    )
    pipeline_count, pipeline_value = pipeline_result.one()

    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    leads_today_result = await db.execute(
        select(func.count(Lead.id)).where(Lead.tenant_id == current_user.tenant_id, Lead.created_at >= today)
    )
    leads_week_result = await db.execute(
        select(func.count(Lead.id)).where(Lead.tenant_id == current_user.tenant_id, Lead.created_at >= week_ago)
    )
    avg_score_result = await db.execute(
        select(func.avg(Lead.score)).where(Lead.tenant_id == current_user.tenant_id, Lead.score.isnot(None))
    )
    model_result = await db.execute(
        select(ModelRegistry).where(ModelRegistry.is_active == True).order_by(ModelRegistry.created_at.desc()).limit(1)
    )
    model = model_result.scalar_one_or_none()

    return DashboardSummary(
        pipeline_value=float(pipeline_value or 0),
        pipeline_count=pipeline_count,
        leads_today=leads_today_result.scalar(),
        leads_this_week=leads_week_result.scalar(),
        avg_score=float(avg_score_result.scalar() or 0),
        score_distribution={"A": 0, "B": 0, "C": 0, "D": 0},
        email_metrics={"sent": 0, "open_rate": 0, "click_rate": 0},
        model_health={
            "status": "healthy" if model else "no_model",
            "auc": model.metrics.get("auc", 0) if model else 0,
            "psi": model.metrics.get("psi", 0) if model else 0,
            "last_retrain": model.training_date.isoformat() if model else None,
        },
        recent_activity=[],
    )
