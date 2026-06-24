from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import router
from app.services.scoring import scoring_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    scoring_engine.load()
    yield

app = FastAPI(title="AI Scoring Service", version="0.1.0", lifespan=lifespan)
app.include_router(router)
