"""Main entry point for the kimchi premium tracker."""

import asyncio
from kimp.premium_calculator import PremiumCalculator
from kimp.data_storage import CSVStorage
from kimp.notification_manager import check_and_notify
from kimp.logging_config import logger


async def main() -> None:
    """
    Main application entry point.

    Calculates kimchi premium, saves data, and sends notifications.
    """
    try:
        # Calculate premium
        logger.info("Starting kimchi premium calculation...")
        calculator = PremiumCalculator()
        premium_data = await calculator.calculate()

        # Save data
        logger.info("Saving data to CSV...")
        storage = CSVStorage()
        storage.save(premium_data)

        # Send notifications if threshold crossed
        logger.info("Checking notification thresholds...")
        await check_and_notify(premium_data.premium)

        logger.info("Completed successfully")

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
