import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger:
    """
    A custom logger that maintains a maximum of 3 log files.
    When the current log file reaches its maximum size, the oldest log is deleted
    and a new log file is created.
    """

    def __init__(
        self,
        log_dir="logs",
        max_files=3,
        max_size=1024 * 1024,
        log_name="application",
        level=logging.INFO,
        format_str="%(asctime)s - %(levelname)s - %(message)s",
    ):
        """
        Initialize the RotatingLogs logger.

        Args:
            log_dir (str): Directory where log files will be stored
            max_files (int): Maximum number of log files to maintain
            max_size (int): Maximum size of each log file in bytes
            log_name (str): Base name for log files
            level (int): Logging level
            format_str (str): Format string for log messages
        """
        self.log_dir = Path(log_dir)
        self.max_files = max_files
        self.max_size = max_size
        self.log_name = log_name
        self.level = level
        self.format_str = format_str

        # Create log directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)

        # Set up logger
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(self.level)

        # Remove any existing handlers to avoid duplicates
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Set up rotating file handler
        self.setup_handler()

    def setup_handler(self):
        """Set up the rotating file handler."""
        log_file = self.log_dir / f"{self.log_name}.log"

        # Create a rotating file handler
        handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=self.max_size,
            backupCount=self.max_files
            - 1,  # -1 because the main log file counts as one
        )

        # Set formatter
        formatter = logging.Formatter(self.format_str)
        handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(handler)

        # Add a console handler if desired
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Log an error message."""
        self.logger.error(message)

    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)


def get_logger(
    log_dir="logs",
    max_files=3,
    max_size=1024 * 1024,
    log_name="application",
    level=logging.INFO,
    format_str="%(asctime)s - %(levelname)s - %(message)s",
):
    """
    Get a configured RotatingLogs instance.

    Args:
        log_dir (str): Directory where log files will be stored
        max_files (int): Maximum number of log files to maintain
        max_size (int): Maximum size of each log file in bytes
        log_name (str): Base name for log files
        level (int): Logging level
        format_str (str): Format string for log messages

    Returns:
        RotatingLogs: A configured logger instance
    """
    return Logger(
        log_dir=log_dir,
        max_files=max_files,
        max_size=max_size,
        log_name=log_name,
        level=level,
        format_str=format_str,
    )
