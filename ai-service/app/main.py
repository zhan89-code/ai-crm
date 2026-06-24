
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List
from app.scoring import scoring_service

app = FastAPI(title="AI Scoring Service", version="0.1.0")


class ScoreRequest(BaseModel):
    lead_id: str
    features: Dict[str, Any]


class ScoreResponse(BaseModel):
    lead_id: str
    score: float
    tier: str
    factors: List[Dict[str, Any]]
    model_version: str
    scored_at: str


@app.post("/score", response_model=ScoreResponse)
async def score_lead(request: ScoreRequest):
    result = scoring_service.score_lead(request.features)
    return ScoreResponse(lead_id=request.lead_id, **result)


@app.get("/health")
async def health():
    return {"status": "healthy", "model_version": scoring_service.model_version}
