"""Upbit exchange client."""

from kimp.exchanges.exchange import Exchange
from kimp.types import Pair


class Upbit(Exchange):
    """Upbit cryptocurrency exchange."""

    def __init__(self):
        """Initialize Upbit exchange."""
        super().__init__("Upbit", "https://api.upbit.com/v1")

    @staticmethod
    def get_symbol(pair: Pair) -> str:
        """
        Get Upbit market symbol from pair.

        Args:
            pair: Trading pair

        Returns:
            Upbit market symbol (e.g., KRW-BTC)
        """
        return f"{pair.quote}-{pair.base}"

    async def get_price(self, pair: Pair) -> float:
        """
        Get current price for a trading pair.

        Args:
            pair: Trading pair

        Returns:
            Current price in quote currency
        """
        symbols = self.get_symbol(pair)
        res = await self.get('ticker', markets=symbols)
        return float(res[0]['trade_price'])
