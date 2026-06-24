from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MODEL_PATH: str = "/app/models"
    API_KEY: str = "dev-key-change-in-prod"
    LOG_LEVEL: str = "INFO"

settings = Settings()
