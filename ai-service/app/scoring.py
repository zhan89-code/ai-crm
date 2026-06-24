
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class LeadScoringService:
    def __init__(self):
        self.model_version = "v1.0.0"
        self.weights = {"xgboost": 0.5, "elasticnet": 0.3, "dnn": 0.2}

    def score_lead(self, features: Dict[str, Any]) -> Dict[str, Any]:
        xgb_score = self._xgboost_predict(features)
        en_score = self._elasticnet_predict(features)
        dnn_score = self._dnn_predict(features)
        ensemble = (
            self.weights["xgboost"] * xgb_score
            + self.weights["elasticnet"] * en_score
            + self.weights["dnn"] * dnn_score
        )
        calibrated = self._platt_calibrate(ensemble)
        tier = self._score_to_tier(calibrated)
        factors = self._compute_shap_factors(features)
        return {
            "score": round(calibrated, 4),
            "tier": tier,
            "factors": factors,
            "model_version": self.model_version,
            "scored_at": datetime.utcnow().isoformat(),
        }

    def _xgboost_predict(self, features: Dict[str, Any]) -> float:
        return 0.75

    def _elasticnet_predict(self, features: Dict[str, Any]) -> float:
        return 0.68

    def _dnn_predict(self, features: Dict[str, Any]) -> float:
        return 0.71

    def _platt_calibrate(self, raw_score: float) -> float:
        A, B = -4.0, 4.0
        return 1.0 / (1.0 + np.exp(A * raw_score + B))

    def _score_to_tier(self, score: float) -> str:
        if score >= 0.8:
            return "A"
        elif score >= 0.6:
            return "B"
        elif score >= 0.4:
            return "C"
        return "D"

    def _compute_shap_factors(self, features: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {"feature": "company_size", "impact": 0.15, "value": features.get("company_size")},
            {"feature": "email_engagement", "impact": 0.12, "value": features.get("email_opens")},
            {"feature": "website_visits", "impact": 0.08, "value": features.get("website_visits")},
        ]

    def compute_psi(self, reference: np.ndarray, current: np.ndarray, n_bins: int = 10) -> float:
        bins = np.linspace(min(reference.min(), current.min()), max(reference.max(), current.max()), n_bins + 1)
        ref_hist = np.histogram(reference, bins=bins)[0] / len(reference)
        cur_hist = np.histogram(current, bins=bins)[0] / len(current)
        ref_hist = np.clip(ref_hist, 1e-6, None)
        cur_hist = np.clip(cur_hist, 1e-6, None)
        psi = np.sum((cur_hist - ref_hist) * np.log(cur_hist / ref_hist))
        return float(psi)


scoring_service = LeadScoringService()
