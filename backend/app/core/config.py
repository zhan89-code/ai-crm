from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str

@lru_cache
def get_settings() -> Settings:
    return Settings()
