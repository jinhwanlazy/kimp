"""Notification management for the kimchi premium tracker."""

import asyncio
import math
from pathlib import Path
from kimp.notifiers.telegram import Telegram
from kimp.notifiers.ntfy import Ntfy
from kimp.config import config
from kimp.logging_config import logger


class NotificationState:
    """Track the last notification grid to prevent duplicate alerts."""

    def __init__(self, state_file: Path | None = None):
        """
        Initialize notification state manager.

        Args:
            state_file: Path to state file (defaults to data_dir/.notification_state)
        """
        self.state_file = state_file or (config.data_dir / ".notification_state")

    def get_last_grid(self) -> float | None:
        """
        Get the last notified grid point.

        Returns:
            Last grid point or None if not set
        """
        if not self.state_file.exists():
            return None
        try:
            content = self.state_file.read_text().strip()
            return float(content) if content else None
        except (ValueError, IOError) as e:
            logger.error(f"Failed to read notification state: {e}")
            return None

    def set_last_grid(self, grid: float) -> None:
        """
        Save the last notified grid point.

        Args:
            grid: Grid point to save
        """
        try:
            self.state_file.parent.mkdir(exist_ok=True, parents=True)
            self.state_file.write_text(str(grid))
            logger.debug(f"Saved notification state: {grid}")
        except IOError as e:
            logger.error(f"Failed to save notification state: {e}")


def calculate_grid(premium: float, interval: float | None = None) -> float:
    """
    Calculate the grid point for a given premium.
    Returns the lower bound of the interval the premium falls into.

    Args:
        premium: Premium percentage
        interval: Grid interval (defaults to config.notification_interval)

    Returns:
        Grid point (lower bound of interval)

    Examples:
        -1.0 to -0.5 (exclusive) -> -1.0
        -0.5 to 0.0 (exclusive) -> -0.5
        0.0 to 0.5 (exclusive) -> 0.0
        0.5 to 1.0 (exclusive) -> 0.5
    """
    if interval is None:
        interval = config.notification_interval
    return math.floor(premium / interval) * interval


async def check_and_notify(premium: float, interval: float | None = None) -> None:
    """
    Check if premium crossed a grid interval and send notifications.

    Only notifies when crossing to the next grid point (0.5% intervals by default).
    Prevents duplicate notifications until the next grid is crossed.
    Runs all notifications in parallel and succeeds even if some fail.

    Args:
        premium: Current premium percentage
        interval: Grid interval (defaults to config.notification_interval)
    """
    if interval is None:
        interval = config.notification_interval

    current_grid = calculate_grid(premium, interval)
    state = NotificationState()
    last_grid = state.get_last_grid()

    # First run or grid changed
    if last_grid is None or current_grid != last_grid:
        state.set_last_grid(current_grid)

        # Only notify if not the first run
        if last_grid is not None:
            message = f"🚨 Kimchi Premium Alert\n\nPremium: {premium:.2f}%\nGrid: {current_grid:.1f}%"

            logger.info(f"Premium crossed grid: {last_grid:.1f}% → {current_grid:.1f}%")

            # Initialize notifiers
            telegram = Telegram()
            ntfy = Ntfy()

            # Send notifications in parallel with independent error handling
            results = await asyncio.gather(
                telegram.send(message),
                ntfy.send(message),
                return_exceptions=True
            )

            # Log results
            success_count = sum(1 for r in results if r is True)
            logger.info(f"Notifications sent: {success_count}/{len(results)} successful")
