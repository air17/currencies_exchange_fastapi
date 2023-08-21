import httpx
from httpx import Response

from core.redis_client import cache_result


@cache_result()
async def get_rates(
    date: str, base: str = "USD", currencies: list[str] | None = None
) -> dict[str, float]:
    """
    Returns all rates.

    Add redis and background_tasks arguments to the function call for caching to work.

    Args:
        date: Date in ISO format.
        base: Base currency.
        currencies: List of currencies to return (optional).

    Returns:
        Dictionary of rates for each available currency. Format: {"currency": rate}
    """
    url = f"https://api.exchangerate.host/{date}?base={base}"
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


@cache_result()
async def get_rate_for_currency(
    currency: str, date: str, base: str = "USD"
) -> dict[str, float]:
    """
    Returns rate for currency.

    Add `redis` and `background_tasks` arguments to the function call for caching to work.

    Args:
        currency: Currency to return.
        date: Date in ISO format.
        base: Base currency.

    Returns:
        Currency rate dictionary. Format: {"currency": rate}.

    Raises:
        ValueError: If currency value is not found for given date.
    """
    rates = await get_rates(date, base, [currency])
    value = rates.get(currency)
    if value is None:
        raise ValueError(f"Currency {currency} not found")
    return {currency: value}
