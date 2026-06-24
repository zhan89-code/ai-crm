# AI Lead Scoring Pipeline Architecture

## Overview
Ensemble model combining XGBoost, ElasticNet, and a small DNN. Runs as a separate Python microservice (FastAPI) with scheduled retraining via APScheduler and async task queue via Celery + Redis.

## Architecture

[CRM API] --score request--> [AI Service /predict]
                                   |
[PostgreSQL] --features--> [Feature Store] --batch--> [Model Trainer]
                                   |                       |
                                   v                       v
                            [Predictions]          [Model Registry]
                                                           |
                                                    [S3/MinIO]

## Feature Engineering Pipeline

### Feature Categories
1. Demographic (10 features):
   company_size_encoded, industry_encoded, revenue_log, job_seniority_score, company_age_days
2. Behavioral (15 features):
   page_views_7d/30d/90d, content_downloads, pricing_page_visits, email_opens/clicks/replies, meeting_count, webinar_attended
3. Engagement Velocity (12 features):
   open_rate_delta_7d_30d, click_rate_delta_7d_30d, engagement_momentum, recency_days
4. External/Enrichment (8 features):
   has_tech_stack, funding_recent, hiring_signal, social_sentiment_score, clearbit_enriched

### Transformations
1. Numeric: StandardScaler for linear models, raw for XGBoost
2. Categorical: One-hot encoding (top 50 per category, OTHER bucket)
3. Missing: IterativeImputer (BayesianRidge estimator)
4. Skewed: log1p transform for revenue, page_views
5. Feature engineering: velocity deltas, ratios, interaction terms (70 total features)

### Feature Store
- Materialized feature vectors in PostgreSQL (updated hourly via Celery task)
- Feature metadata in JSON schema (versioned)
- Online serving via direct DB query (< 10ms)
- Feature importance tracking per model version

## Model Ensemble

### Model 1: XGBoost (primary, weight 0.5)
- Hyperparameters tuned via Optuna (50 trials)
- Key params: max_depth=6, learning_rate=0.05, n_estimators=500, subsample=0.8
- Handles non-linear interactions + built-in feature importance

### Model 2: ElasticNet (secondary, weight 0.3)
- L1/L2 regularization: alpha=0.01, l1_ratio=0.5
- Provides stable linear baseline, interpretable coefficients

### Model 3: DNN (tertiary, weight 0.2)
- Architecture: Input(70) -> Dense(128,ReLU) -> Dropout(0.3) -> Dense(64,ReLU) -> Dense(32,ReLU) -> Dense(1,Sigmoid)
- Training: Adam optimizer, batch_size=64, epochs=100, early stopping (patience=10)
- Framework: PyTorch

### Blending and Calibration
- Weighted average: final = 0.5*xgb + 0.3*en + 0.2*dnn
- Calibration: Platt scaling (logistic regression on validation set)
- Output: probability 0.0-1.0 mapped to score 0-100 (integer)

### Tier Assignment
- A-Tier: 80-100 (immediate outreach, < 1hr SLA)
- B-Tier: 60-79 (priority follow-up, < 24hr)
- C-Tier: 40-59 (nurture sequence)
- D-Tier: 0-39 (long-term drip or DQ)

## Inference Flow

1. CRM receives lead/lead update
2. CRM publishes event to Redis queue: channel="lead.updated"
3. Celery worker picks up event, fetches features from Feature Store
4. Run ensemble prediction (target < 200ms p95)
5. Write score + SHAP factors back to leads table
6. If score crosses tier threshold, publish event to trigger email sequence
7. Update SHAP explanations in lead.score_factors (top 3 pos/neg)

## Model Operations

### Training Schedule (APScheduler)
- Weekly full retrain: Sunday 2 AM UTC (90-day rolling window)
- Triggered retrain: If PSI > 0.2 detected on daily monitoring
- Champion/Challenger: New model trained alongside current, 10% traffic split

### Drift Detection
- Daily: Calculate PSI of score distribution vs. training baseline
- Threshold: PSI > 0.2 triggers automatic retrain
- Also monitor precision@top20% degradation

### Evaluation Thresholds
- AUC-ROC >= 0.80
- Precision@Top20% >= 0.60
- Expected Calibration Error (ECE) <= 0.05
- Cross-week AUC variance < 0.02

### Champion/Challenger (A/B Testing)
- New model trained alongside current production model
- 10% of scoring routed to challenger
- Promote challenger if AUC improves by >= 0.02 over 2 weeks
- All experiments logged to model_experiments table

### Explainability (SHAP)
- Pre-computed per prediction: TreeSHAP for XGBoost component
- Stored as JSON: { positive: [{feature, value, contribution}], negative: [...] }
- Displayed in UI as waterfall chart in LeadDetailSheet

## Infrastructure
- AI service runs in Docker container (separate from main API)
- Model artifacts stored in S3/MinIO (versioned by model version)
- Async scoring via Celery workers (horizontal scaling)
- Feature store in shared PostgreSQL (materialized hourly)
- Health endpoint: GET /health returns DB connection + last retrain timestamp

## AI Service API Endpoints
- POST /predict - Single lead scoring (real-time, < 200ms)
- POST /predict/batch - Bulk scoring (async, returns job_id)
- GET /metrics - Current model performance metrics
- POST /retrain - Trigger manual retrain
- GET /retrain/{job_id} - Training job status