"""Data models for the kimchi premium tracker."""

from dataclasses import dataclass


@dataclass
class PriceData:
    """Individual coin price data from exchanges."""

    coin: str
    upbit_price: float
    binance_price: float
    est_usd_krw: float


@dataclass
class PremiumData:
    """Calculated kimchi premium data."""

    timestamp: float
    usd_krw: float
    est_usd_krw: float
    premium: float

    def to_csv_row(self) -> str:
        """Convert to CSV row format."""
        return f"{self.timestamp},{self.usd_krw},{self.est_usd_krw},{self.premium}\n"

    @classmethod
    def csv_header(cls) -> str:
        """Return CSV header."""
        return "timestamp,usd_krw,est_usd_krw,premium\n"
