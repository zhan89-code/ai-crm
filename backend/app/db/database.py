from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings

class Base(DeclarativeBase):
    pass
import os

settings = get_settings()
# Force the internal DB URL
DATABASE_URL = "postgresql+asyncpg://crm_user:GVvMAwptKlakh3Uz9fMvlaCB66JsugMu@dpg-d8tqdfv7f7vs73ffg0tg-a.oregon-postgres.render.com:5432/ai_crm_m70n"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={'ssl': 'require'}
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.create_all)
        pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
