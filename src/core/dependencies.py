from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.users import User
from core.repository.users import UserManager
from core.session import async_session_maker
from core.redis_client import redis_connection_pool


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Database session generator."""
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """User CRUD manager."""
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    """DI for UserManager."""
    yield UserManager(user_db)


async def get_redis() -> AsyncGenerator[Redis, None]:
    """DI for Redis."""
    redis_client = Redis(connection_pool=redis_connection_pool)
    yield redis_client
    await redis_client.close()
