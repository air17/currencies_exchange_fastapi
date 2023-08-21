from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.models.base import Base
from config import settings

engine = create_async_engine(
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
async_session_maker = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)


async def create_all_tables():
    """Creates all tables. Unnecessary if using alembic."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
