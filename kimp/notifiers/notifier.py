"""Base notifier interface."""

from abc import ABC, abstractmethod


class Notifier(ABC):
    """Base class for notification services."""

    @abstractmethod
    async def send(self, message: str) -> bool:
        """
        Send a notification message.

        Args:
            message: Message to send

        Returns:
            True if successful, False otherwise
        """
        pass
