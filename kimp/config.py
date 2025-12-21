"""Configuration management for the kimchi premium tracker."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class AppConfig(BaseSettings):
    """Application configuration."""

    # Reference coins to track
    reference_coins: list[str] = Field(
        default=["BTC", "ETH", "XRP"],
        description="Cryptocurrency coins to track for premium calculation"
    )

    # Notification settings
    notification_interval: float = Field(
        default=0.5,
        description="Grid interval for notifications in percentage"
    )

    # Data storage
    data_dir: Path = Field(
        default=Path("pages"),
        description="Directory to store CSV data files"
    )

    # Telegram notification settings
    telegram_bot_token: str | None = Field(
        default=None,
        env="TELEGRAM_BOT_TOKEN",
        description="Telegram bot token for notifications"
    )

    telegram_chat_id: str | None = Field(
        default=None,
        env="TELEGRAM_CHAT_ID",
        description="Telegram chat ID for notifications"
    )

    # Ntfy notification settings
    ntfy_topic: str | None = Field(
        default=None,
        env="NTFY_TOPIC",
        description="Ntfy topic for notifications"
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        env="LOG_LEVEL",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )


# Global config instance
config = AppConfig()
