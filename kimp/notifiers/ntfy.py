"""Ntfy notifier implementation."""

import aiohttp
from .notifier import Notifier
from kimp.config import config
from kimp.logging_config import logger


class Ntfy(Notifier):
    """Ntfy.sh notifier."""

    def __init__(self):
        """Initialize Ntfy notifier."""
        self.topic = config.ntfy_topic

    async def send(self, message: str) -> bool:
        """
        Send notification via ntfy.sh.

        Args:
            message: Message to send

        Returns:
            True if successful, False otherwise
        """
        if not self.topic:
            logger.debug("NTFY_TOPIC not configured, skipping")
            return False

        url = f"https://ntfy.sh/{self.topic}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=message.encode("utf-8")) as resp:
                    if resp.status == 200:
                        logger.info("ntfy notification sent successfully")
                        return True
                    else:
                        logger.warning(f"ntfy notification failed with status {resp.status}")
                        return False
        except Exception as e:
            logger.error(f"Failed to send ntfy notification: {e}")
            return False
