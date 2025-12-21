"""Naver exchange rate client."""

from kimp.exchanges.exchange import Exchange
from kimp.types import Pair


class Naver(Exchange):
    """Naver exchange rate API."""

    def __init__(self):
        """Initialize Naver exchange rate client."""
        super().__init__(
            "Naver",
            "https://m.search.naver.com/p/csearch/content/qapirender.nhn?key=calculator&pkid=141&q=%ED%99%98%EC%9C%A8&where=m&u1=keb&u6=standardUnit&u7=0&u3=USD&u4=KRW&u8=down&u2=1",
        )

    async def get_price(self, pair: Pair) -> float:
        """
        Get USD/KRW exchange rate from Naver.

        Args:
            pair: Must be USD/KRW

        Returns:
            USD/KRW exchange rate

        Raises:
            ValueError: If pair is not USD/KRW or rate not found
        """
        if pair.base != "USD" or pair.quote != "KRW":
            raise ValueError("Only USD/KRW pair is supported")
        data = await self.get()
        for item in data.get("country", []):
            if item.get("currencyUnit") == "원":
                return float(item.get("value", "0").replace(",", ""))
        raise ValueError(f"KRW rate not found from {data}")
