import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = os.environ.get('DATABASE_URL')

@lru_cache
def get_settings() -> Settings:
    return Settings()
