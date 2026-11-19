"""Unit tests for the pre-processing logic."""

import math

import pytest

from src import preprocessing as pp


@pytest.fixture
def numbers():
    """List of numbers shared by several tests."""
    return [1.0, 2.0, 3.0, 4.0, 5.0]


def test_remove_missing():
    assert pp.remove_missing([1, None, "", float("nan"), "nan", 2]) == [1, 2]


@pytest.mark.parametrize(
    "fill_value, expected",
    [(0, [1, 0, 0, 2]), (-1, [1, -1, -1, 2]), ("x", [1, "x", "x", 2])],
)
def test_fill_missing(fill_value, expected):
    assert pp.fill_missing([1, None, "", 2], fill_value) == expected


def test_fill_missing_default():
    assert pp.fill_missing([None, 3]) == [0, 3]


@pytest.mark.parametrize(
    "values, expected",
    [([1, 2, 2, 3], [1, 2, 3]), (["a", "a"], ["a"]), ([], [])],
)
def test_remove_duplicates(values, expected):
    assert pp.remove_duplicates(values) == expected


def test_normalize_default(numbers):
    assert pp.normalize(numbers) == [0.0, 0.25, 0.5, 0.75, 1.0]


@pytest.mark.parametrize(
    "new_min, new_max, expected",
    [(0, 10, [0, 2.5, 5, 7.5, 10]), (-1, 1, [-1, -0.5, 0, 0.5, 1])],
)
def test_normalize_range(numbers, new_min, new_max, expected):
    assert pp.normalize(numbers, new_min, new_max) == pytest.approx(expected)


def test_normalize_constant():
    assert pp.normalize([3, 3, 3]) == [0.0, 0.0, 0.0]


def test_standardize(numbers):
    result = pp.standardize(numbers)
    assert sum(result) / len(result) == pytest.approx(0.0)
    std = math.sqrt(sum(r**2 for r in result) / len(result))
    assert std == pytest.approx(1.0)


def test_standardize_constant():
    assert pp.standardize([2, 2]) == [0.0, 0.0]


def test_clip(numbers):
    assert pp.clip(numbers, 2, 4) == [2, 2, 3, 4, 4]


def test_to_integers():
    assert pp.to_integers(["1", "2.7", "abc", "-3"]) == [1, 2, -3]


def test_log_transform():
    assert pp.log_transform([1, math.e, -2, 0]) == pytest.approx([0.0, 1.0])


def test_tokenize():
    assert pp.tokenize("Hello, World! 123") == "hello world 123"


def test_remove_punctuation():
    assert pp.remove_punctuation("Hi! How are you?") == "Hi How are you"


def test_remove_stopwords():
    assert pp.remove_stopwords("The cat IS black", ["the", "is"]) == "cat black"


def test_flatten():
    assert pp.flatten([[1, 2], [3], []]) == [1, 2, 3]


def test_shuffle_reproducible(numbers):
    assert pp.shuffle(numbers, seed=42) == pp.shuffle(numbers, seed=42)
    assert sorted(pp.shuffle(numbers, seed=42)) == numbers
