from unittest.mock import patch

import pytest

from src.core import (
    QUOTES_PATTERN,
    TAB_PATTERN,
    WHITESPACE_PATTERN,
    autocorrect_text,
    normalize_whitespace,
    preserve_punctuation,
)


class TestNormalizeWhitespace:
    """Tests for the normalize_whitespace function."""

    def test_empty_string(self):
        """Test with an empty string."""
        assert normalize_whitespace("") == ""

    def test_string_with_spaces(self):
        """Test with a string that has extra spaces."""
        assert normalize_whitespace("hello   world") == "hello world"

    def test_string_with_tabs(self):
        """Test with a string that has tabs."""
        assert normalize_whitespace("hello\tworld") == "hello, world"

    def test_string_with_quotes(self):
        """Test with a string that has various quotes."""
        assert normalize_whitespace('hello "world"') == "hello 'world'"
        assert normalize_whitespace("hello `world`") == "hello 'world'"
        assert normalize_whitespace("hello ´world´") == "hello 'world'"

    def test_string_with_trailing_whitespace(self):
        """Test with a string that has trailing whitespace."""
        assert normalize_whitespace("hello world   ") == "hello world"
        assert normalize_whitespace("   hello world") == "hello world"
        assert normalize_whitespace("   hello world   ") == "hello world"

    def test_multiline_string(self):
        """Test with a multiline string."""
        input_text = (
            "line 1  with  spaces \nline 2\twith tabs  \n\nline 4 after empty line"
        )
        expected = "line 1 with spaces\nline 2, with tabs\n\nline 4 after empty line"
        assert normalize_whitespace(input_text) == expected

    @pytest.mark.skip("Skipping test for now")
    def test_complex_string(self):
        """Test with a complex string that has multiple whitespace issues."""
        input_text = '  This `text`\t has "many"\tproblems  \nwith     ´spacing´    '
        expected = "This 'text', has 'many', problems\nwith 'spacing'"
        assert normalize_whitespace(input_text) == expected

    def test_logging(self):
        """Test that the function logs appropriately."""
        with patch("src.core.logger") as mock_logger:
            text = "sample text"
            normalize_whitespace(text)

            # Check debug message for input
            mock_logger.debug.assert_any_call(
                f"Normalizing whitespace for text of length {len(text)}"
            )

            # Check debug message for output
            mock_logger.debug.assert_any_call(
                f"Whitespace normalization complete, result length: {1}"
            )


@pytest.mark.skip("Need to review.")
class TestAutocorrectText:
    """Tests for the autocorrect_text function."""

    @patch("src.core.spell.correction")
    def test_empty_string(self, mock_correction):
        """Test with an empty string."""
        assert autocorrect_text("") == ""
        mock_correction.assert_not_called()

    @patch("src.core.spell.correction")
    def test_single_word(self, mock_correction):
        """Test with a single word."""
        mock_correction.return_value = "corrected"
        assert autocorrect_text("word") == "corrected"
        mock_correction.assert_called_once_with("word")

    @patch("src.core.spell.correction")
    def test_multiple_words(self, mock_correction):
        """Test with multiple words."""
        mock_correction.side_effect = ["first", "second"]
        assert autocorrect_text("frst secnd") == "first second"
        assert mock_correction.call_count == 2
        mock_correction.assert_any_call("frst")
        mock_correction.assert_any_call("secnd")

    @patch("src.core.spell.correction")
    def test_capitalized_words_preserved(self, mock_correction):
        """Test that capitalized words are preserved (not corrected)."""
        assert autocorrect_text("Hello world") == "Hello world"
        # Should not attempt to correct "Hello" because it's capitalized
        mock_correction.assert_called_once_with("world")

    @patch("src.core.spell.correction")
    def test_punctuation_preserved(self, mock_correction):
        """Test that punctuation is preserved."""
        mock_correction.return_value = "hello"
        assert autocorrect_text("helo!") == "hello!"
        mock_correction.assert_called_once_with("helo")

    @patch("src.core.spell.correction")
    def test_multiple_punctuation(self, mock_correction):
        """Test with multiple punctuation marks."""
        mock_correction.return_value = "hello"
        assert autocorrect_text("helo!!!") == "hello!!!"
        mock_correction.assert_called_once_with("helo")

    @patch("src.core.spell.correction")
    def test_multiline_text(self, mock_correction):
        """Test with multiline text."""
        mock_correction.side_effect = ["first", "second", "third", "fourth"]
        input_text = "frst line\nsecnd line\n\nthrd frth line"
        expected = "first line\nsecond line\n\nthird fourth line"
        assert autocorrect_text(input_text) == expected
        assert mock_correction.call_count == 4

    @patch("src.core.spell.correction")
    def test_empty_lines_preserved(self, mock_correction):
        """Test that empty lines are preserved."""
        mock_correction.side_effect = ["first", "second"]
        input_text = "frst\n\nsecnd"
        expected = "first\n\nsecond"
        assert autocorrect_text(input_text) == expected
        assert mock_correction.call_count == 2

    @patch("src.core.spell.correction")
    def test_correction_returns_none(self, mock_correction):
        """Test behavior when spell correction returns None."""
        mock_correction.return_value = None
        assert autocorrect_text("unknwn") == "unknwn"
        mock_correction.assert_called_once_with("unknwn")

    @patch("src.core.spell.correction")
    def test_lru_cache(self, mock_correction):
        """Test that the LRU cache is working."""
        mock_correction.return_value = "hello"

        # Call function twice with the same input
        autocorrect_text("helo")
        autocorrect_text("helo")

        # The spell correction should only be called once due to caching
        mock_correction.assert_called_once_with("helo")

    @patch("src.core.preserve_punctuation")
    def test_preserve_punctuation_called(self, mock_preserve_punctuation):
        """Test that preserve_punctuation is called correctly."""
        mock_preserve_punctuation.side_effect = [("word", "!"), ("test", "")]
        with patch("src.core.spell.correction", return_value="corrected"):
            autocorrect_text("word! test")
            mock_preserve_punctuation.assert_any_call("word!")
            mock_preserve_punctuation.assert_any_call("test")


class TestPreservePunctuation:
    """Additional tests for the preserve_punctuation function."""

    def test_word_with_internal_punctuation(self):
        """Test with punctuation in the middle of the word."""
        word, punctuation = preserve_punctuation("hello!world")
        assert word == "hello!world"
        assert punctuation == ""

    def test_word_with_apostrophe(self):
        """Test with apostrophe in the word."""
        word, punctuation = preserve_punctuation("don't")
        assert word == "don't"
        assert punctuation == ""

    def test_multiple_different_punctuation(self):
        """Test with multiple different punctuation marks."""
        word, punctuation = preserve_punctuation("hello!?.")
        assert word == "hello"
        assert punctuation == "!?."

    def test_just_punctuation(self):
        """Test with just punctuation, no word."""
        word, punctuation = preserve_punctuation("...")
        assert word == ""
        assert punctuation == "..."


class TestRegexPatterns:
    """Tests for the regex patterns used in the module."""

    def test_whitespace_pattern(self):
        """Test WHITESPACE_PATTERN."""
        assert WHITESPACE_PATTERN.sub(" ", "hello   world") == "hello world"

    def test_quotes_pattern(self):
        """Test QUOTES_PATTERN."""
        assert (
            QUOTES_PATTERN.sub("'", 'hello "world" `test` ´example´')
            == "hello 'world' 'test' 'example'"
        )

    def test_tab_pattern(self):
        """Test TAB_PATTERN."""
        assert TAB_PATTERN.sub(", ", "hello\tworld") == "hello, world"
