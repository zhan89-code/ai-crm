from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://crm_user:GVvMAwptKlakh3Uz9fMvlaCB66JsugMu@dpg-d8tqdfv7f7vs73ffg0tg-a.oregon-postgres.render.com:5432/ai_crm_m70n"

def get_settings():
    return Settings()
