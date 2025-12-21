"""Data storage management for the kimchi premium tracker."""

from datetime import datetime, UTC
from pathlib import Path
from kimp.models import PremiumData
from kimp.config import config
from kimp.logging_config import logger


class CSVStorage:
    """Handle CSV file storage for premium data."""

    def __init__(self, data_dir: Path | None = None):
        """
        Initialize CSV storage.

        Args:
            data_dir: Directory to store CSV files (defaults to config.data_dir)
        """
        self.data_dir = data_dir or config.data_dir

    def save(self, data: PremiumData) -> None:
        """
        Save premium data to CSV file.

        Args:
            data: Premium data to save
        """
        # Ensure data directory exists
        self.data_dir.mkdir(exist_ok=True, parents=True)

        # Get file path for today
        filepath = self._get_filepath()

        # Ensure file exists with header
        self._ensure_file_exists(filepath)

        # Append data
        try:
            with open(filepath, "a") as f:
                f.write(data.to_csv_row())
            logger.info(f"Data saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save data to {filepath}: {e}")
            raise

    def _get_filepath(self) -> Path:
        """Get the CSV file path for today's date."""
        date = datetime.now(UTC).strftime("%Y-%m-%d")
        return self.data_dir / f"{date}.csv"

    def _ensure_file_exists(self, filepath: Path) -> None:
        """
        Ensure CSV file exists with header.

        Args:
            filepath: Path to CSV file
        """
        if not filepath.exists():
            try:
                filepath.write_text(PremiumData.csv_header())
                logger.info(f"Created new CSV file: {filepath}")
            except Exception as e:
                logger.error(f"Failed to create CSV file {filepath}: {e}")
                raise
