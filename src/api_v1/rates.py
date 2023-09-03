from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import PastDate
from redis.asyncio import Redis

from core.authentication import current_active_user
from core.dependencies import get_redis
from core.exchange_providers import ExchangeRateHostClient
from core.models.users import User
from utils import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/")
async def get_all_rates(
    background_tasks: BackgroundTasks,
    date: PastDate | None = None,
    redis: Redis = Depends(get_redis),
    _: User = Depends(current_active_user),
) -> dict[str, float]:
    """Returns all rates."""
    exchange_client = ExchangeRateHostClient(redis=redis, background_tasks=background_tasks)
    return await exchange_client.get_rates(date)


@router.get("/{currency}")
async def get_currency_rate(
    currency: str,
    background_tasks: BackgroundTasks,
    date: PastDate | None = None,
    _: User = Depends(current_active_user),
    redis: Redis = Depends(get_redis),
) -> dict[str, float]:
    """Returns rate for a given currency."""
    exchange_client = ExchangeRateHostClient(redis=redis, background_tasks=background_tasks)
    try:
        return await exchange_client.get_rate_for_currency(currency, date)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
