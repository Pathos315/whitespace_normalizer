"""
A whitespace normalizing application for
use in conjunction with Frontline IEP Direct and Frontline 504.
"""

import re
import tkinter as tk
from tkinter import scrolledtext, ttk
from log import get_logger

import pyperclip
from spellchecker import SpellChecker
from typing import NoReturn
from functools import lru_cache


logger = get_logger()
spell = SpellChecker()
logger.debug("SpellChecker initialized")

# Global pre-compiled regex patterns
WHITESPACE_PATTERN = re.compile(r" +")
QUOTES_PATTERN = re.compile(r"[\"`´]")
TAB_PATTERN = re.compile(r"\t")


def normalize_whitespace(text: str) -> str:
    """
    Splits the text into lines, strips all trailing whitespace, regularizes all quote glyphs, and rejoins it.

    Args:
        text (str): Input text, which likely has irregular spacing or quotation marks

    Returns:
        str: A cleaned body of text with normalized whitespaces and quotes.
    """
    logger.debug(f"Normalizing whitespace for text of length {len(text)}")

    # Process all operations in a single pass
    normalized_lines = [
        TAB_PATTERN.sub(
            ", ", QUOTES_PATTERN.sub("'", WHITESPACE_PATTERN.sub(" ", line.strip()))
        )
        for line in text.splitlines()
    ]

    logger.debug(
        f"Whitespace normalization complete, result length: {len(normalized_lines)}"
    )
    return "\n".join(normalized_lines)


@lru_cache(maxsize=10000)
def autocorrect_text(text: str) -> str:
    """
    Autocorrect misspelled words in a text using pyspellchecker while preserving paragraphs.

    Args:
        text (str): The input text to correct

    Returns:
        str: The corrected text with paragraphs preserved
    """
    # Split the text into lines to preserve structure
    lines = text.splitlines()

    corrected_lines = []

    for line in lines:
        # Skip empty lines but preserve them in the output
        if not line.strip():
            corrected_lines.append("")
            continue

        # Split the line into words
        words = line.split()

        # Corrected words list
        corrected_words = []

        for word in words:
            # Preserve punctuation
            word, punctuation = preserve_punctuation(word)

            # Skip correction for capitalized words (likely proper nouns)
            if word and word[0].isupper():
                corrected_words.append(word + punctuation)
                continue

            # Skip empty strings
            if not word:
                continue

            # Get the corrected word
            corrected = spell.correction(word)

            # Add back punctuation
            if corrected:
                corrected_words.append(corrected + punctuation)
            else:
                corrected_words.append(word + punctuation)

        # Join the corrected words back into a line
        corrected_line = " ".join(corrected_words)
        corrected_lines.append(corrected_line)

    # Join the lines back together with newlines
    return "\n".join(corrected_lines)


def preserve_punctuation(word: str) -> tuple[str, str]:
    punctuation = ""
    while word and word[-1] in '.,:;!?()[]{}""\'':
        punctuation = word[-1] + punctuation
        word = word[:-1]
    return word, punctuation


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
        COLUMN_CONFIG = [1, 0, 1]
        ROW_CONFIG = [0, 1, 0, 0]

        for i, weight in enumerate(COLUMN_CONFIG):
            self.root.columnconfigure(i, weight=weight)

        for i, weight in enumerate(ROW_CONFIG):
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


def main():
    """Creates and runs the application."""
    logger.info("Starting WhitespaceNormalizer application")
    try:
        root = tk.Tk()
        app = WhitespaceNormalizerApp(root)
        logger.info("Entering main application loop")
        root.mainloop()
    except Exception as e:
        logger.critical(f"Application crashed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
