"""
Pytest configuration and shared fixtures.
"""

import os
import sys
import tkinter as tk
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

# Add the src directory to the path so tests can import from it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def root():
    """Fixture that provides a Tkinter root window."""
    # Create the Tk instance inside the test file
    root = tk.Tk()
    # Set a standard size for all GUI tests
    root.geometry("800x500")
    yield root
    # Clean up properly
    root.destroy()


@pytest.fixture
def mock_logger():
    """Mock the logger to avoid writing to files during tests."""
    # Create a mock logger object
    mock_log = MagicMock()

    # Add all the required methods to the mock
    for method in ["debug", "info", "warning", "error", "critical"]:
        setattr(mock_log, method, MagicMock())

    # Patch the module to use our mock
    with patch("src.log.logger", mock_log):
        yield mock_log


@pytest.fixture
def sample_text_fixtures():
    """Create sample text fixtures for testing."""
    return {
        "regular": "This is a regular text without any special whitespace.",
        "with_spaces": "This   text   has   extra   spaces.",
        "with_tabs": "This\ttext\thas\ttabs.",
        "mixed": "This  text\thas both  spaces\tand\ttabs.",
        "with_quotes": 'This text has "different" `quotes` and "more quotes".',
        "multiline": "Line 1 with  spaces\nLine 2\twith tabs\n\nLine 4 after empty line",
        "with_spelling": "This text has misspelled wrds.",
    }


@pytest.fixture
def test_data_dir():
    """Return a Path object pointing to the test data directory."""
    test_dir = Path(__file__).parent / "test_data"

    # Create the directory if it doesn't exist
    test_dir.mkdir(exist_ok=True)

    return test_dir


@pytest.fixture
def create_test_file(test_data_dir):
    """Create a temporary test file with given content."""

    def _create_file(filename, content):
        file_path = test_data_dir / filename
        with open(file_path, "w") as f:
            f.write(content)
        return file_path

    return _create_file


def pytest_configure(config):
    """Add custom markers to the pytest configuration."""
    config.addinivalue_line("markers", "gui: mark test as requiring GUI functionality")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow")
