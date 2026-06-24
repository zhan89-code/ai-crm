from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings
import asyncio
import logging
import os

logger = logging.getLogger(__name__)

settings = get_settings()

# Use the environment variable directly to avoid Pydantic issues
db_url = os.environ.get('DATABASE_URL', settings.DATABASE_URL)

logger.info(f'Using DATABASE_URL: {db_url.split('@')[0].split(':')[0]}:***@{db_url.split('@')[1] if '@' in db_url else 'unknown'}')

# Handle SSL args manually for safer connection
connect_args = {'ssl': 'require'}

# Clean URL for SQLAlchemy if it contains query params
base_url = db_url.split('?')[0]
if base_url.startswith('postgresql://'):
    base_url = base_url.replace('postgresql://', 'postgresql+asyncpg://', 1)

engine = create_async_engine(
    base_url,
    echo=False,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args=connect_args
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

class Base(DeclarativeBase):
    pass

async def init_db():
    max_retries = 10
    for attempt in range(max_retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info('Database tables created successfully')
            return
        except Exception as e:
            wait = 2 ** attempt
            if wait > 30: wait = 30
            logger.warning(f'DB connection attempt {attempt + 1} failed: {e}. Retrying in {wait}s...')
            await asyncio.sleep(wait)
