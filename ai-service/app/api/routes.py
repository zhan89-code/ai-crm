from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.models.schemas import ScoreRequest, ScoreResponse, ModelStatus
from app.services.scoring import scoring_engine
from app.services.model_registry import registry
from app.core.config import settings
import pandas as pd

router = APIRouter(prefix="/api/v1")

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@router.post("/score")
async def score_leads(request: ScoreRequest, x_api_key: Optional[str] = Header(None)):
    await verify_api_key(x_api_key)
    df = pd.DataFrame([lead.dict() for lead in request.leads])
    results = scoring_engine.predict(df)
    return {"results": results, "model_version": scoring_engine.version}

@router.get("/model/status")
async def model_status(x_api_key: Optional[str] = Header(None)):
    await verify_api_key(x_api_key)
    active = registry.get_active()
    if not active:
        return {"status": "no_model", "version": "none"}
    return {"status": "active", **active}

@router.post("/model/retrain")
async def trigger_retrain(x_api_key: Optional[str] = Header(None)):
    await verify_api_key(x_api_key)
    return {"status": "training_queued", "message": "Retraining started"}
