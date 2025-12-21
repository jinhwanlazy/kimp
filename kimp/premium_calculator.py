"""Premium calculation logic for the kimchi premium tracker."""

import asyncio
import time
from kimp.models import PremiumData, PriceData
from kimp.exchanges.upbit import Upbit
from kimp.exchanges.binance import Binance
from kimp.exchanges.naver import Naver
from kimp.types import Pair
from kimp.config import config
from kimp.logging_config import logger


class PremiumCalculator:
    """Calculate kimchi premium from exchange prices."""

    def __init__(self):
        self.upbit = Upbit()
        self.binance = Binance()
        self.naver = Naver()

    async def calculate(self) -> PremiumData:
        """
        Calculate the current kimchi premium.

        Returns:
            PremiumData with calculated premium

        Raises:
            Exception: If price fetching fails for all coins
        """
        timestamp = time.time()

        # Fetch all prices in parallel
        logger.info("Fetching prices from exchanges...")
        try:
            async with asyncio.TaskGroup() as tg:
                naver_task = tg.create_task(self._fetch_naver_rate())
                upbit_tasks = {
                    coin: tg.create_task(self._fetch_upbit_price(coin))
                    for coin in config.reference_coins
                }
                binance_tasks = {
                    coin: tg.create_task(self._fetch_binance_price(coin))
                    for coin in config.reference_coins
                }
        except Exception as e:
            logger.error(f"Failed to fetch prices: {e}")
            raise

        # Get Naver USD/KRW rate
        naver_usd_krw = naver_task.result()
        if naver_usd_krw is None:
            raise ValueError("Failed to fetch Naver USD/KRW rate")

        logger.info(f"Naver USD/KRW: {naver_usd_krw}")

        # Calculate estimated USD/KRW from each coin
        price_data_list: list[PriceData] = []
        est_usd_krw_values: list[float] = []

        for coin in config.reference_coins:
            upbit_price = upbit_tasks[coin].result()
            binance_price = binance_tasks[coin].result()

            if upbit_price is not None and binance_price is not None:
                est_usd_krw = upbit_price / binance_price
                est_usd_krw_values.append(est_usd_krw)

                price_data = PriceData(
                    coin=coin,
                    upbit_price=upbit_price,
                    binance_price=binance_price,
                    est_usd_krw=est_usd_krw
                )
                price_data_list.append(price_data)

                logger.info(
                    f"{coin}: Upbit={upbit_price} KRW, "
                    f"Binance={binance_price} USDT, "
                    f"Est. USD/KRW={est_usd_krw:.2f}"
                )
            else:
                logger.warning(f"Skipping {coin} due to missing price data")

        if not est_usd_krw_values:
            raise ValueError("No valid price data available for premium calculation")

        # Calculate average estimated USD/KRW
        est_usd_krw_avg = sum(est_usd_krw_values) / len(est_usd_krw_values)
        logger.info(f"Average estimated USD/KRW: {est_usd_krw_avg:.2f}")

        # Calculate premium
        premium = self._calculate_premium(est_usd_krw_avg, naver_usd_krw)
        logger.info(f"Kimchi premium: {premium:.2f}%")

        return PremiumData(
            timestamp=timestamp,
            usd_krw=naver_usd_krw,
            est_usd_krw=est_usd_krw_avg,
            premium=premium
        )

    async def _fetch_naver_rate(self) -> float | None:
        """Fetch USD/KRW rate from Naver."""
        try:
            return await self.naver.get_price(Pair("USD", "KRW"))
        except Exception as e:
            logger.error(f"Failed to fetch Naver USD/KRW rate: {e}")
            return None

    async def _fetch_upbit_price(self, coin: str) -> float | None:
        """Fetch coin price from Upbit."""
        try:
            return await self.upbit.get_price(Pair(coin, "KRW"))
        except Exception as e:
            logger.error(f"Failed to fetch Upbit {coin}/KRW price: {e}")
            return None

    async def _fetch_binance_price(self, coin: str) -> float | None:
        """Fetch coin price from Binance."""
        try:
            return await self.binance.get_price(Pair(coin, "USDT"))
        except Exception as e:
            logger.error(f"Failed to fetch Binance {coin}/USDT price: {e}")
            return None

    @staticmethod
    def _calculate_premium(est_usd_krw: float, naver_usd_krw: float) -> float:
        """
        Calculate the premium percentage.

        Args:
            est_usd_krw: Estimated USD/KRW from crypto exchanges
            naver_usd_krw: Actual USD/KRW from Naver

        Returns:
            Premium percentage
        """
        return (est_usd_krw - naver_usd_krw) / naver_usd_krw * 100
