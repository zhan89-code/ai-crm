from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings
import asyncio
import logging

logger = logging.getLogger(__name__)

settings = get_settings()

db_url = settings.DATABASE_URL
# Ensure ssl=require or sslmode=require is handled if not present in the URL
if 'sslmode=' not in db_url and 'ssl=' not in db_url:
    prefix = '?' if '?' not in db_url else '&'
    db_url += f'{prefix}ssl=require'

# Force conversion to asyncpg
if db_url.startswith('postgresql://'):
    db_url = db_url.replace('postgresql://', 'postgresql+asyncpg://', 1)

engine = create_async_engine(
    db_url,
    echo=False,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={'ssl': 'require'}
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
