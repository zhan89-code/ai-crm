import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from pathlib import Path

def train_ensemble(data_path: str, model_path: str):
    df = pd.read_csv(data_path)
    feature_cols = ["email_opened", "email_clicked", "website_visits", "pages_per_visit", "time_on_site", "form_submissions", "days_since_first_touch", "engagement_score"]
    X = df[feature_cols].fillna(0)
    y = df["converted"]
    model = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X, y)
    scores = cross_val_score(model, X, y, cv=5, scoring="f1")
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "version": "1.0.0", "metrics": {"f1": float(scores.mean())}}, model_path)
    print(f"Model saved. F1: {scores.mean():.4f}")

if __name__ == "__main__":
    train_ensemble("/data/training.csv", "/app/models/ensemble_v1.joblib")
