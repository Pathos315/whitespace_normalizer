from unittest.mock import MagicMock, patch

import pytest

from src.log import Logger, get_logger


@pytest.mark.skip
@patch("src.log.os.makedirs")
@patch("src.log.logging.getLogger")
def test_logger_initialization(mock_get_logger, mock_makedirs):
    """Test Logger initialization."""
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    logger = Logger(
        log_dir="test_logs", max_files=5, max_size=2048, log_name="test_log"
    )

    # Verify log directory creation
    mock_makedirs.assert_called_once_with("test_logs", exist_ok=True)

    # Verify logger setup
    mock_get_logger.assert_called_once_with("test_log")
    assert logger.logger == mock_logger
    assert logger.log_dir.name == "test_logs"
    assert logger.max_files == 5
    assert logger.max_size == 2048
    assert logger.log_name == "test_log"


@pytest.mark.skip
@patch("src.log.RotatingFileHandler")
@patch("src.log.logging.StreamHandler")
@patch("src.log.logging.Formatter")
def test_logger_setup_handler(
    mock_formatter, mock_stream_handler, mock_rotating_handler
):
    """Test setup of the rotating file handler."""
    mock_formatter_instance = MagicMock()
    mock_formatter.return_value = mock_formatter_instance

    logger = Logger(
        log_dir="test_logs", max_files=3, max_size=1024, log_name="test_log"
    )
    logger.setup_handler()

    # Verify rotating file handler setup
    mock_rotating_handler.assert_called_once_with(
        filename="test_logs/test_log.log", maxBytes=1024, backupCount=2
    )
    mock_rotating_handler_instance = mock_rotating_handler.return_value
    mock_rotating_handler_instance.setFormatter.assert_called_once_with(
        mock_formatter_instance
    )

    # Verify stream handler setup
    mock_stream_handler.assert_called_once()
    mock_stream_handler_instance = mock_stream_handler.return_value
    mock_stream_handler_instance.setFormatter.assert_called_once_with(
        mock_formatter_instance
    )

    # Verify handlers added to logger
    assert mock_rotating_handler_instance in logger.logger.handlers
    assert mock_stream_handler_instance in logger.logger.handlers


@patch("src.log.logging.getLogger")
def test_logger_methods(mock_get_logger):
    """Test logging methods (debug, info, warning, error, critical)."""
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    logger = Logger(log_dir="test_logs", log_name="test_log")

    # Test debug
    logger.debug("Debug message")
    mock_logger.debug.assert_called_once_with("Debug message")

    # Test info
    logger.info("Info message")
    mock_logger.info.assert_called_once_with("Info message")

    # Test warning
    logger.warning("Warning message")
    mock_logger.warning.assert_called_once_with("Warning message")

    # Test error
    logger.error("Error message")
    mock_logger.error.assert_called_once_with("Error message")

    # Test critical
    logger.critical("Critical message")
    mock_logger.critical.assert_called_once_with("Critical message")


@patch("src.log.Logger")
def test_get_logger(mock_logger_class):
    """Test get_logger function."""
    mock_logger_instance = MagicMock()
    mock_logger_class.return_value = mock_logger_instance

    logger = get_logger(
        log_dir="test_logs",
        max_files=4,
        max_size=4096,
        log_name="test_log",
        level="DEBUG",
        format_str="%(message)s",
    )

    # Verify Logger instance creation
    mock_logger_class.assert_called_once_with(
        log_dir="test_logs",
        max_files=4,
        max_size=4096,
        log_name="test_log",
        level="DEBUG",
        format_str="%(message)s",
    )
    assert logger == mock_logger_instance
