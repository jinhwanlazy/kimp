"""Telegram notifier implementation."""

import aiohttp
from .notifier import Notifier
from kimp.config import config
from kimp.logging_config import logger


class Telegram(Notifier):
    """Telegram Bot API notifier."""

    def __init__(self):
        """Initialize Telegram notifier."""
        self.token = config.telegram_bot_token
        self.chat_id = config.telegram_chat_id

    async def send(self, message: str) -> bool:
        """
        Send notification via Telegram Bot API.

        Args:
            message: Message to send

        Returns:
            True if successful, False otherwise
        """
        if not self.token or not self.chat_id:
            logger.debug("Telegram credentials not configured, skipping")
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                }) as resp:
                    if resp.status == 200:
                        logger.info("Telegram notification sent successfully")
                        return True
                    else:
                        logger.warning(f"Telegram notification failed with status {resp.status}")
                        return False
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False
