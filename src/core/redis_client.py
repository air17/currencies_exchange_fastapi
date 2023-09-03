import json
from typing import Any

from redis.asyncio import ConnectionPool, Redis

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
