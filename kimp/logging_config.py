"""Logging configuration for the kimchi premium tracker."""

import logging
import sys
from kimp.config import config


def setup_logging() -> logging.Logger:
    """
    Set up logging configuration.

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("kimp")
    logger.setLevel(getattr(logging, config.log_level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, config.log_level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


# Global logger instance
logger = setup_logging()
