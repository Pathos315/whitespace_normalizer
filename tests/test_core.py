import pytest

from src.core import preserve_punctuation


def test_preserve_punctuation_no_punctuation():
    word, punctuation = preserve_punctuation("hello")
    assert word == "hello"
    assert punctuation == ""


def test_preserve_punctuation_single_punctuation():
    word, punctuation = preserve_punctuation("hello!")
    assert word == "hello"
    assert punctuation == "!"


def test_preserve_punctuation_multiple_punctuation():
    word, punctuation = preserve_punctuation("hello!!!")
    assert word == "hello"
    assert punctuation == "!!!"


def test_preserve_punctuation_middle_punctuation():
    word, punctuation = preserve_punctuation("he!llo")
    assert word == "he!llo"
    assert punctuation == ""


def test_preserve_punctuation_empty_string():
    word, punctuation = preserve_punctuation("")
    assert word == ""
    assert punctuation == ""


def test_preserve_punctuation_only_punctuation():
    word, punctuation = preserve_punctuation("!!!")
    assert word == ""
    assert punctuation == "!!!"
