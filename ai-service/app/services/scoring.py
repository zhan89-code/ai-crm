import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional
from app.core.config import settings

class LeadScoringEnsemble:
    def __init__(self):
        self.model = None
        self.version = "0.1.0"
        self._loaded = False

    def load(self):
        model_path = Path(settings.MODEL_PATH) / "ensemble_v1.joblib"
        if model_path.exists():
            data = joblib.load(model_path)
            self.model = data["model"]
            self.version = data.get("version", "0.1.0")
            self._loaded = True
        else:
            self._loaded = False

    def predict(self, df: pd.DataFrame) -> list[dict]:
        if not self._loaded or self.model is None:
            return [{"score": 0.5, "tier": "B", "confidence": 0.0} for _ in range(len(df))]
        features = self._extract_features(df)
        scores = self.model.predict_proba(features)[:, 1]
        results = []
        for score in scores:
            if score >= 0.8:
                tier = "S"
            elif score >= 0.6:
                tier = "A"
            elif score >= 0.4:
                tier = "B"
            else:
                tier = "C"
            results.append({"score": float(score), "tier": tier, "confidence": abs(score - 0.5) * 2})
        return results

    def _extract_features(self, df: pd.DataFrame) -> np.ndarray:
        feature_cols = ["email_opened", "email_clicked", "website_visits", "pages_per_visit", "time_on_site", "form_submissions", "days_since_first_touch", "engagement_score"]
        available = [c for c in feature_cols if c in df.columns]
        return df[available].fillna(0).values

scoring_engine = LeadScoringEnsemble()
