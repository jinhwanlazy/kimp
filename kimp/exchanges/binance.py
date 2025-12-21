"""Binance exchange client."""

from kimp.exchanges.exchange import Exchange
from kimp.types import Pair


class Binance(Exchange):
    """Binance cryptocurrency exchange."""

    def __init__(
        self,
        name: str = "Binance",
        base_url: str = "https://api.binance.com/api/v3",
    ):
        """
        Initialize Binance exchange.

        Args:
            name: Exchange name
            base_url: Base URL for API
        """
        super().__init__(name, base_url)

    @staticmethod
    def get_symbol(pair: Pair) -> str:
        """
        Get Binance symbol from pair.

        Args:
            pair: Trading pair

        Returns:
            Binance symbol (e.g., BTCUSDT)
        """
        return f"{pair.base}{pair.quote}"

    async def get_price(self, pair: Pair) -> float:
        """
        Get current price for a trading pair.

        Args:
            pair: Trading pair

        Returns:
            Current price in quote currency
        """
        symbol = self.get_symbol(pair)
        res = await self.get("ticker", "price", symbol=symbol)
        return float(res["price"])
