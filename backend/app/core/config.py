from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://crm_user:crm_pass@localhost:5432/ai_crm"

@lru_cache
def get_settings() -> Settings:
    return Settings()
