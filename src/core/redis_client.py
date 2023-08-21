import json
from functools import wraps
from typing import Any

from redis.asyncio import ConnectionPool, Redis
from fastapi import BackgroundTasks

from config import settings

redis_connection_pool = ConnectionPool(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True
)


async def redis_set_value(redis: Redis, key: str, value: Any, expire: int | None):
    """Sets data in redis."""
    value_json = json.dumps(value)
    await redis.set(name=key, value=value_json, ex=expire)


async def redis_get_value(redis: Redis, key: str, expire: int | None) -> Any:
    """Gets data from redis."""
    value: str | None = await redis.getex(key, ex=expire)
    if value:
        return json.loads(value)
    return None


def cache_result(expire: int | None = settings.REDIS_CACHE_EXPIRE):
    """
    Caches the result of a function in redis.

    Add redis and background_tasks arguments to the function call for caching to work.
    """

    def decorator(f):
        @wraps(f)
        async def wrapper(*arg, background_tasks: BackgroundTasks = None, redis: Redis = None, **kwargs):
            if redis and background_tasks:
                key = "".join(arg)
                value = await redis_get_value(redis, key, expire)
                if not value:
                    value = await f(*arg, **kwargs)
                    background_tasks.add_task(redis_set_value, redis=redis, key=key, value=value, expire=expire)
                return value
            else:
                return await f(*arg, **kwargs)

        return wrapper

    return decorator
