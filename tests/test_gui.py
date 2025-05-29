import tkinter
from unittest.mock import patch

import pytest

from src.gui import WhitespaceNormalizerApp


@pytest.fixture
def app():
    """Fixture to create the app instance."""
    root = tkinter.Tk()
    app = WhitespaceNormalizerApp(root)
    return app


def test_app_initialization(app):
    """Test if the app initializes correctly."""
    assert app.root.title() == "Whitespace Normalizer"


@pytest.mark.skip("Skipping test for now")
@patch("src.gui.normalize_whitespace", return_value="normalized text")
@patch("src.gui.autocorrect_text", return_value="autocorrected text")
@patch("src.gui.pyperclip.copy")
def test_normalize_and_copy_without_autocorrect(
    mock_copy, mock_autocorrect, mock_normalize, app
):
    """Test normalize_and_copy without autocorrect."""
    app.input_text.insert("1.0", "   test text   ")
    app.autocorrect_var.set(False)

    app.normalize_and_copy()

    mock_normalize.assert_called_once_with("   test text   ")
    mock_autocorrect.assert_not_called()
    mock_copy.assert_called_once_with("normalized text")
    assert app.output_text.get("1.0", tkinter.END).strip() == "normalized text"
    assert app.status_label.cget("text") == "Text normalized and copied to clipboard"


@pytest.mark.skip("Skipping test for now")
@patch("src.gui.normalize_whitespace", return_value="normalized text")
@patch("src.gui.autocorrect_text", return_value="autocorrected text")
@patch("src.gui.pyperclip.copy")
def test_normalize_and_copy_with_autocorrect(
    mock_copy, mock_autocorrect, mock_normalize, app
):
    """Test normalize_and_copy with autocorrect."""
    app.input_text.insert("1.0", "   test text   ")
    app.autocorrect_var.set(True)

    app.normalize_and_copy()

    mock_normalize.assert_called_once_with("   test text   ")
    mock_autocorrect.assert_called_once_with("normalized text")
    mock_copy.assert_called_once_with("autocorrected text")
    assert app.output_text.get("1.0", tkinter.END).strip() == "autocorrected text"
    assert (
        app.status_label.cget("text")
        == "Text normalized with autocorrect and copied to clipboard"
    )


@patch("src.gui.pyperclip.copy")
def test_copy_to_clipboard_success(mock_copy, app):
    """Test copy_to_clipboard when it succeeds."""
    app.copy_to_clipboard("test text")
    mock_copy.assert_called_once_with("test text")
    assert app.status_label.cget("text") == ""


@patch("src.gui.pyperclip.copy", side_effect=Exception("Clipboard error"))
def test_copy_to_clipboard_failure(mock_copy, app):
    """Test copy_to_clipboard when it fails."""
    app.copy_to_clipboard("test text")
    mock_copy.assert_called_once_with("test text")
    assert "Error: Failed to copy to clipboard" in app.status_label.cget("text")


@patch("src.gui.tk.Tk.destroy")
@patch("src.gui.exit")
def test_close_application(mock_exit, mock_destroy, app):
    """Test close_application."""
    app.close_application()
    mock_destroy.assert_called_once()
    mock_exit.assert_called_once()
