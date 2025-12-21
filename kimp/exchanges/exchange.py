"""Base exchange class."""

from kimp.utils.api_client import APIClient
from kimp.types import Pair


class Exchange(APIClient):
    """Base class for cryptocurrency exchanges."""

    def __init__(self, name: str, base_url: str):
        """
        Initialize exchange.

        Args:
            name: Exchange name
            base_url: Base URL for API
        """
        super().__init__(name, base_url)

    async def get_price(self, pair: Pair) -> float:
        """
        Get price for a trading pair.

        Args:
            pair: Trading pair (e.g., BTC/KRW)

        Returns:
            Current price

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("This method should be overridden by subclasses")


