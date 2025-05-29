import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from unittest.mock import ANY, MagicMock, patch

import pytest

from src.gui import WhitespaceNormalizerApp


@pytest.fixture
def app_with_real_tk():
    """Create an app with a real Tk root for widget testing."""
    try:
        # Create a real Tk instance
        root = tk.Tk()

        # Make the window not visible
        root.withdraw()

        with patch("src.gui.logger", autospec=True):
            app = WhitespaceNormalizerApp(root)
            yield app
            # Clean up
            root.destroy()
    except tk.TclError:
        # Skip test if Tk can't be initialized (e.g., in CI environment)
        pytest.skip("Cannot initialize Tk - test requires a display")


@pytest.mark.skip("Need to review.")
class TestWidgetProperties:
    """Tests for widget properties and configurations."""

    def test_input_text_properties(self, app_with_real_tk: WhitespaceNormalizerApp):
        """Test properties of the input text widget."""
        app = app_with_real_tk
        # Check if input_text is a ScrolledText widget

        assert isinstance(app.input_text, ScrolledText)
        assert app.input_text.cget("wrap") == "word"
        assert app.input_text.cget("wrap") == "word"

        # Check grid placement
        grid_info = app.input_text.grid_info()
        assert grid_info["row"] == "1"
        assert grid_info["column"] == "0"

    def test_output_text_properties(self, app_with_real_tk: WhitespaceNormalizerApp):
        app = app_with_real_tk
        assert isinstance(app.output_text, ScrolledText)
        assert app.output_text.cget("wrap") == "word"
        assert app.output_text.cget("wrap") == "word"

        # Check grid placement
        grid_info = app.output_text.grid_info()
        assert grid_info["row"] == "1"
        assert grid_info["column"] == "2"

    def test_autocorrect_checkbox_properties(
        self, app_with_real_tk: WhitespaceNormalizerApp
    ):
        """Test properties of the autocorrect checkbox."""
        app = app_with_real_tk
        # Check if autocorrect_checkbox is a ttk.Checkbutton

        assert isinstance(app.autocorrect_checkbox, ttk.Checkbutton)
        assert isinstance(app.autocorrect_checkbox, ttk.Checkbutton)

        # Check text property
        text = app.autocorrect_checkbox.cget("text")
        assert text == "Enable Autocorrect"

        # Check variable binding
        assert app.autocorrect_var.get() is False  # Default should be False

    def test_status_label_properties(self, app_with_real_tk: WhitespaceNormalizerApp):
        """Test properties of the status label."""
        app = app_with_real_tk
        assert isinstance(app.status_label, ttk.Label)
        assert isinstance(app.status_label, ttk.Label)

        # Initially, the status label should be empty
        assert app.status_label.cget("text") == ""

        # Check grid placement
        grid_info = app.status_label.grid_info()
        assert grid_info["row"] == "2"
        assert int(grid_info["columnspan"]) >= 3


@pytest.mark.skip("Need to review.")
@pytest.mark.parametrize("autocorrect_enabled", [True, False])
class TestInteractiveFlow:
    """Tests for interactive flow with the widgets."""

    @patch("src.gui.normalize_whitespace")
    @patch("src.gui.autocorrect_text")
    @patch("src.gui.pyperclip.copy")
    def test_text_flow(
        self,
        mock_copy,
        mock_autocorrect,
        mock_normalize,
        app_with_real_tk: WhitespaceNormalizerApp,
        autocorrect_enabled,
    ):
        """Test the flow of text through the application."""
        app = app_with_real_tk

        # Set up mock return values
        mock_normalize.return_value = "normalized text"
        mock_autocorrect.return_value = "corrected text"

        # Set text in input widget
        app.input_text.delete("1.0", tk.END)
        app.input_text.insert("1.0", "input   text with   spaces")

        # Set autocorrect checkbox
        app.autocorrect_var.set(autocorrect_enabled)

        # Trigger normalization
        app.normalize_and_copy()

        # Check that normalize_whitespace was called
        mock_normalize.assert_called_once_with("input   text with   spaces")

        # Check if autocorrect was called based on checkbox state
        if autocorrect_enabled:
            mock_autocorrect.assert_called_once_with("normalized text")
            mock_copy.assert_called_once_with("corrected text")

            # Check output text content
            assert app.output_text.get("1.0", "end-1c") == "corrected text"

            # Check status label
            assert "with autocorrect" in app.status_label.cget("text")
        else:
            mock_autocorrect.assert_not_called()
            mock_copy.assert_called_once_with("normalized text")

            # Check output text content
            assert app.output_text.get("1.0", "end-1c") == "normalized text"

            # Check status label
            assert "with autocorrect" not in app.status_label.cget("text")


@pytest.mark.skip("Need to review.")
class TestButtonCallbacks:
    """Tests for button callbacks."""

    @patch("src.gui.WhitespaceNormalizerApp.normalize_and_copy")
    def test_normalize_button_callback(self, mock_normalize_method):
        """Test that the normalize button's callback is correct."""
        with patch("tkinter.Tk") as mock_tk:
            with patch("tkinter.ttk.Button") as mock_button:
                with patch("src.gui.logger", autospec=True):
                    # Create a spy for the Button constructor
                    def capture_button_args(*args, **kwargs):
                        """Capture the arguments passed to the Button constructor."""
                        capture_button_args = MagicMock()
                        capture_button_args.called_with = (args, kwargs)
                        return MagicMock()

                    mock_button.side_effect = capture_button_args

                    # Create the app
                    app = WhitespaceNormalizerApp(mock_tk.return_value)

                    # Find the normalize button call
                    normalize_button_call = None
                    for _, kwargs in mock_button.call_args_list:
                        if "text" in kwargs and kwargs["text"] == "Normalize >":
                            normalize_button_call = kwargs
                            break

                    assert normalize_button_call is not None

                    # Call the command callback
                    normalize_button_call["command"]()

                    # Verify the normalize_and_copy method was called
                    mock_normalize_method.assert_called_once()

    @patch("src.gui.WhitespaceNormalizerApp.close_application")
    def test_close_button_callback(self, mock_close_method):
        """Test that the close button's callback is correct."""
        with patch("tkinter.Tk") as mock_tk:
            with patch("tkinter.ttk.Button") as mock_button:
                with patch("src.gui.logger", autospec=True):
                    # Create a spy for the Button constructor
                    def capture_button_args(*args, **kwargs):
                        capture_button_args = MagicMock()
                        capture_button_args.called_with = (args, kwargs)
                        return MagicMock()

                    mock_button.side_effect = capture_button_args

                    # Create the app
                    app = WhitespaceNormalizerApp(mock_tk.return_value)

                    # Find the close button call
                    close_button_call = None
                    for _, kwargs in mock_button.call_args_list:
                        if "text" in kwargs and kwargs["text"] == "Close":
                            close_button_call = kwargs
                            break

                    assert close_button_call is not None

                    # Call the command callback
                    close_button_call["command"]()

                    # Verify the close_application method was called
                    mock_close_method.assert_called_once()


@pytest.mark.skip("Need to review.")
class TestGridLayout:
    """Tests for grid layout configuration."""

    def test_root_grid_configuration(self):
        """Test the root's grid configuration."""
        with patch("tkinter.Tk") as mock_tk:
            mock_root = mock_tk.return_value

            with patch("src.gui.logger", autospec=True):
                app = WhitespaceNormalizerApp(mock_root)

                # Check that columnconfigure was called for all 3 columns
                assert mock_root.columnconfigure.call_count == 3

                # Check weights for columns
                column_weights = [
                    call_args[0][1]
                    for call_args in mock_root.columnconfigure.call_args_list
                ]
                # Expected pattern: first and last columns with weight 1, middle with weight 0
                assert column_weights == [1, 0, 1]

                # Check that rowconfigure was called for all 4 rows
                assert mock_root.rowconfigure.call_count == 4

                # Check weights for rows
                row_weights = [
                    call_args[0][1]
                    for call_args in mock_root.rowconfigure.call_args_list
                ]
                # Expected pattern: row 1 (index 1) with weight 1, others with weight 0
                assert row_weights[1] == 1
                assert row_weights[0] == 0
                assert row_weights[2] == 0
                assert row_weights[3] == 0
