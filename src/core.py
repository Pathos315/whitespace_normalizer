"""
A whitespace normalizing application for
normalizing whitespaces, which can optionally autocorrect spelling errors in the text.
"""

import re
from functools import lru_cache

from spellchecker import SpellChecker

from src.log import get_logger

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
    """
    Separates trailing punctuation from a given word.
    This function takes a string `word` and extracts any trailing punctuation
    characters (e.g., '.', ',', ':', ';', '!', '?', '(', ')', '[', ']', '{', '}',
    '"', '\'') from the end of the word. It returns a tuple containing the word
    without the trailing punctuation and the extracted punctuation.

    Args:
        word (str): The input word from which trailing punctuation will be separated.

    Returns:
        tuple[str, str]: A tuple where the first element is the word without trailing
        punctuation, and the second element is the extracted punctuation.
    """

    punctuation = ""
    while word and word[-1] in '.,:;!?()[]{}""\'':
        punctuation = word[-1] + punctuation
        word = word[:-1]
    return word, punctuation
