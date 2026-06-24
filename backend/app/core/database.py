from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Import models so they register on the correct Base metadata
from app.db.database import Base
from app.models.models import User, Tenant

DATABASE_URL = "postgresql+asyncpg://crm_user:GVvMAwptKlakh3Uz9fMvlaCB66JsugMu@dpg-d8tqdfv7f7vs73ffg0tg-a.oregon-postgres.render.com:5432/ai_crm_m70n"

engine = create_async_engine(DATABASE_URL, echo=False, pool_size=20, max_overflow=10)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
