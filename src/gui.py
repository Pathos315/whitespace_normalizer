import tkinter as tk
from tkinter import scrolledtext, ttk
from typing import NoReturn

import pyperclip

from src.core import autocorrect_text, normalize_whitespace
from src.log import logger

logger.debug("Logger initialized for GUI module")


class WhitespaceNormalizerApp:
    """
    A widget to normalize whitespaces.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Whitespace Normalizer")
        self.root.geometry("800x500")

        # Configure the grid layout
        self._configure_layout()

        # Create widgets
        self._create_widgets()

    def _configure_layout(self):
        """Configure the responsive grid layout."""
        # Make rows and columns expand properly
        column_config = [1, 0, 1]
        row_config = [0, 1, 0, 0]

        for i, weight in enumerate(column_config):
            self.root.columnconfigure(i, weight=weight)

        for i, weight in enumerate(row_config):
            self.root.rowconfigure(i, weight=weight)

    def _create_widgets(self):
        """
        Creates the overall layout of the application.
        """
        # Input label
        input_label = ttk.Label(self.root, text="Input Text:")
        input_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

        # Output label
        output_label = ttk.Label(self.root, text="Normalized Text:")
        output_label.grid(row=0, column=2, sticky="w", padx=10, pady=(10, 0))

        # Input text area
        self.input_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.input_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Button frame in the middle
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=1, padx=5, pady=10)

        # Add checkbox for autocorrect toggle
        self.autocorrect_var = tk.BooleanVar(value=False)
        self.autocorrect_checkbox = ttk.Checkbutton(
            button_frame, text="Enable Autocorrect", variable=self.autocorrect_var
        )
        self.autocorrect_checkbox.pack(pady=5)

        # Normalize button
        normalize_button = ttk.Button(
            button_frame, text="Normalize >", command=self.normalize_and_copy, width=15
        )
        normalize_button.pack(pady=10)

        # Output text area
        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.output_text.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.status_label = ttk.Label(self.root, text="")
        self.status_label.grid(row=2, column=0, columnspan=3, pady=5)

        # Close button
        close_frame = ttk.Frame(self.root)
        close_frame.grid(row=3, column=0, columnspan=3, pady=10)

        close_button = ttk.Button(
            close_frame, text="Close", command=self.close_application, width=15
        )
        close_button.pack()
        logger.debug("All widgets created successfully")

    def close_application(self) -> NoReturn:
        """Closes the application."""
        logger.info("Closing application...")
        self.root.destroy()
        exit()

    def normalize_and_copy(self):
        """
        Gets the input text, removes all trailing whitespaces,
        copies it to the clipboard, and produces it as output text."
        """
        # Get input text
        input_text = self.input_text.get("1.0", tk.END)

        # Normalize text
        normalized_text = normalize_whitespace(input_text)

        # Apply autocorrect if enabled
        if self.autocorrect_var.get():
            logger.info("Autocorrect enabled, applying spell correction")
            normalized_text = autocorrect_text(normalized_text)
            self.status_label.config(
                text="Text normalized with autocorrect and copied to clipboard"
            )
        else:
            logger.info("Autocorrect disabled")
            self.status_label.config(text="Text normalized and copied to clipboard")

        self.copy_to_clipboard(normalized_text)

        # Update output text
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", normalized_text)

        # Make sure status update is displayed
        self.root.update_idletasks()

    def copy_to_clipboard(self, normalized_text):
        try:
            pyperclip.copy(normalized_text)
            logger.info("Text copied to clipboard successfully")
        except Exception as e:
            logger.error(f"Failed to copy to clipboard: {e}")
            self.status_label.config(text="Error: Failed to copy to clipboard")
