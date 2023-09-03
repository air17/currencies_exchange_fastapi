from abc import ABC, abstractmethod
from functools import wraps

import httpx
from fastapi import BackgroundTasks
from httpx import Response
from pydantic import PastDate
from redis.asyncio import Redis

from config import settings
from core.redis_client import redis_get_value, redis_set_value


def cache_result(expire: int | None = settings.REDIS_CACHE_EXPIRE):
    """Caches the result of a class method using redis."""

    def decorator(f):
        @wraps(f)
        async def wrapper(self, *args, **kwargs):
            if self.redis is not None:
                key = str(args) + str(kwargs)
                value = await redis_get_value(self.redis, key, expire)
                if not value:
                    value = await f(self, *args, **kwargs)
                    if self.background_tasks is not None:
                        self.background_tasks.add_task(
                            redis_set_value, redis=self.redis, key=key, value=value, expire=expire
                        )
                    else:
                        await redis_set_value(redis=self.redis, key=key, value=value, expire=expire)
                return value
            else:
                return await f(self, *args, **kwargs)
        return wrapper
    return decorator


class BaseClient(ABC):
    """Base client for exchange rate providers."""

    def __init__(self, redis: Redis | None = None, background_tasks: BackgroundTasks | None = None):
        self.redis = redis
        self.background_tasks = background_tasks

    @abstractmethod
    async def get_rates(self, date: PastDate | None = None, base: str = "USD", currencies: list[str] | None = None) -> dict[str, float]:
        """
        Returns all rates.

        Args:
            date: Date for which to return rate.
            base: Base currency.
            currencies: List of currencies to return (optional).

        Returns:
            Dictionary of rates for each available currency.
            Format: {"currency": rate}
        """
        raise NotImplementedError()

    @cache_result()
    async def get_rate_for_currency(self, currency: str, date: PastDate | None = None, base: str = "USD") -> dict[str, float]:
        """
        Returns rate for currency.

        Add `redis` and `background_tasks` arguments to the function call for caching to work.

        Args:
            currency: Currency to return.
            date: Date for which to return rate.
            base: Base currency.

        Returns:
            Currency rate dictionary.
            Format: {"currency": rate}.

        Raises:
            ValueError: If currency value is not found for given date.
        """
        rates = await self.get_rates(date, base, [currency])
        value = rates.get(currency)
        if value is None:
            raise ValueError(f"Currency {currency} not found")
        return {currency: value}


class ExchangeRateHostClient(BaseClient):
    """A client for "exchangerate.host" exchange rate API."""

    @cache_result()
    async def get_rates(self, date: PastDate | None = None, base: str = "USD", currencies: list[str] | None = None) -> dict[str, float]:
        url = f"https://api.exchangerate.host/{self.format_date(date)}?base={base}"
        if currencies:
            url += f"&symbols={','.join(currencies)}"
        async with httpx.AsyncClient() as client:
            response: Response = await client.get(url)
        if response.is_error:
            raise httpx.HTTPError(f"HTTP error: {response.status_code}")
        response_data = response.json()
        if response_data["success"] is False:
            raise httpx.HTTPError(f"API error: {response_data}")
        return response_data["rates"]

    @staticmethod
    def format_date(date: PastDate | None) -> str:
        """Formats date for "exchangerate.host" API"""
        return date.isoformat() if date else "latest"
