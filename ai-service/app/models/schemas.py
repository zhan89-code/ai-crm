from pydantic import BaseModel
from typing import Optional

class LeadFeatures(BaseModel):
    source: str
    industry: Optional[str] = None
    company_size: Optional[str] = None
    email_opened: int = 0
    email_clicked: int = 0
    website_visits: int = 0
    pages_per_visit: float = 0.0
    time_on_site: float = 0.0
    form_submissions: int = 0
    days_since_first_touch: int = 0
    engagement_score: float = 0.0

class ScoreRequest(BaseModel):
    leads: list[LeadFeatures]

class ScoreResponse(BaseModel):
    lead_index: int
    score: float
    tier: str
    confidence: float

class ModelStatus(BaseModel):
    model_version: str
    last_trained: str
    accuracy: float
    f1_score: float
    total_predictions: int
