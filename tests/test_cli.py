"""Integration tests between the CLI and the pre-processing logic."""

import pytest
from click.testing import CliRunner

from src.cli import cli


@pytest.fixture
def runner():
    """CliRunner shared by all the tests."""
    return CliRunner()


def test_clean_remove_missing(runner):
    result = runner.invoke(cli, ["clean", "remove-missing", "1", "", "nan", "3"])
    assert result.exit_code == 0
    assert result.output.strip() == "['1', '3']"


def test_clean_fill_missing(runner):
    result = runner.invoke(
        cli, ["clean", "fill-missing", "1", "", "3", "--fill-value", "9"]
    )
    assert result.exit_code == 0
    assert result.output.strip() == "['1', '9', '3']"


def test_numeric_normalize(runner):
    result = runner.invoke(cli, ["numeric", "normalize", "1", "2", "3"])
    assert result.exit_code == 0
    assert result.output.strip() == "[0.0, 0.5, 1.0]"


def test_numeric_standardize(runner):
    result = runner.invoke(cli, ["numeric", "standardize", "1", "1"])
    assert result.exit_code == 0
    assert result.output.strip() == "[0.0, 0.0]"


def test_numeric_clip(runner):
    result = runner.invoke(
        cli,
        [
            "numeric",
            "clip",
            "--min-value",
            "0",
            "--max-value",
            "1",
            "--",
            "-1",
            "0.5",
            "2",
        ],
    )
    assert result.exit_code == 0
    assert result.output.strip() == "[0.0, 0.5, 1.0]"


def test_numeric_to_int(runner):
    result = runner.invoke(cli, ["numeric", "to-int", "1", "2.7", "abc"])
    assert result.exit_code == 0
    assert result.output.strip() == "[1, 2]"


def test_numeric_log(runner):
    result = runner.invoke(cli, ["numeric", "log", "--", "1", "-5"])
    assert result.exit_code == 0
    assert result.output.strip() == "[0.0]"


def test_text_tokenize(runner):
    result = runner.invoke(cli, ["text", "tokenize", "Hello, World!"])
    assert result.exit_code == 0
    assert result.output.strip() == "hello world"


def test_text_remove_punctuation(runner):
    result = runner.invoke(cli, ["text", "remove-punctuation", "Hi! You?"])
    assert result.exit_code == 0
    assert result.output.strip() == "Hi You"


def test_text_remove_stopwords(runner):
    result = runner.invoke(
        cli, ["text", "remove-stopwords", "The cat is black", "-s", "the", "-s", "is"]
    )
    assert result.exit_code == 0
    assert result.output.strip() == "cat black"


def test_struct_shuffle(runner):
    args = ["struct", "shuffle", "1", "2", "3", "4", "--seed", "42"]
    first = runner.invoke(cli, args)
    second = runner.invoke(cli, args)
    assert first.exit_code == 0
    assert first.output == second.output


def test_struct_flatten(runner):
    result = runner.invoke(cli, ["struct", "flatten", "1,2", "3"])
    assert result.exit_code == 0
    assert result.output.strip() == "['1', '2', '3']"


def test_struct_unique(runner):
    result = runner.invoke(cli, ["struct", "unique", "1", "2", "2", "1"])
    assert result.exit_code == 0
    assert result.output.strip() == "['1', '2']"
