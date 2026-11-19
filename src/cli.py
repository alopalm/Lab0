"""Command line interface for the pre-processing functions."""

import click

from src import preprocessing as pp


def _parse_numbers(values):
    """Convert a tuple of strings into a list of floats."""
    return [float(v) for v in values]


@click.group()
def cli():
    """Command line tool for data pre-processing."""


@cli.group()
def clean():
    """Commands for data cleaning."""


@cli.group()
def numeric():
    """Commands for numerical attributes."""


@cli.group()
def text():
    """Commands for textual information."""


@cli.group()
def struct():
    """Commands for the structure of data."""


# ---------- clean ----------
@clean.command("remove-missing")
@click.argument("values", nargs=-1)
def remove_missing_cmd(values):
    """Remove missing values ('', None, nan).

    Example: cli clean remove-missing 1 "" nan 3
    """
    click.echo(pp.remove_missing(list(values)))


@clean.command("fill-missing")
@click.argument("values", nargs=-1)
@click.option("--fill-value", default="0", help="Value used to fill missing values.")
def fill_missing_cmd(values, fill_value):
    """Fill missing values with a given value.

    Example: cli clean fill-missing 1 "" nan 3 --fill-value 9
    """
    click.echo(pp.fill_missing(list(values), fill_value))


# ---------- numeric ----------
@numeric.command("normalize")
@click.argument("values", nargs=-1)
@click.option("--new-min", default=0.0, type=float, help="Minimum of the new range.")
@click.option("--new-max", default=1.0, type=float, help="Maximum of the new range.")
def normalize_cmd(values, new_min, new_max):
    """Normalize numbers with min-max scaling.

    Example: cli numeric normalize 1 2 3 --new-min 0 --new-max 10
    """
    click.echo(pp.normalize(_parse_numbers(values), new_min, new_max))


@numeric.command("standardize")
@click.argument("values", nargs=-1)
def standardize_cmd(values):
    """Standardize numbers with the z-score.

    Example: cli numeric standardize 1 2 3
    """
    click.echo(pp.standardize(_parse_numbers(values)))


@numeric.command("clip")
@click.argument("values", nargs=-1)
@click.option("--min-value", default=0.0, type=float, help="Minimum value to clip.")
@click.option("--max-value", default=1.0, type=float, help="Maximum value to clip.")
def clip_cmd(values, min_value, max_value):
    """Clip numbers to a range.

    Example: cli numeric clip --min-value 0 --max-value 1 -- -1 0.5 2
    """
    click.echo(pp.clip(_parse_numbers(values), min_value, max_value))


@numeric.command("to-int")
@click.argument("values", nargs=-1)
def to_int_cmd(values):
    """Convert values to integers, dropping non-numerical ones.

    Example: cli numeric to-int 1 2.7 abc
    """
    click.echo(pp.to_integers(list(values)))


@numeric.command("log")
@click.argument("values", nargs=-1)
def log_cmd(values):
    """Apply the logarithm to the positive numbers.

    Example: cli numeric log 1 10 100
    """
    click.echo(pp.log_transform(_parse_numbers(values)))


# ---------- text ----------
@text.command("tokenize")
@click.argument("text_input")
def tokenize_cmd(text_input):
    """Tokenize text into lower-cased alphanumeric words.

    Example: cli text tokenize "Hello, World!"
    """
    click.echo(pp.tokenize(text_input))


@text.command("remove-punctuation")
@click.argument("text_input")
def remove_punctuation_cmd(text_input):
    """Keep only alphanumeric characters and spaces.

    Example: cli text remove-punctuation "Hello, World!"
    """
    click.echo(pp.remove_punctuation(text_input))


@text.command("remove-stopwords")
@click.argument("text_input")
@click.option(
    "--stopwords",
    "-s",
    multiple=True,
    default=("the", "a", "an", "is"),
    help="Stop-word to remove (repeat the option for several).",
)
def remove_stopwords_cmd(text_input, stopwords):
    """Remove stop-words from the text (lower-cased).

    Example: cli text remove-stopwords "The cat is black" -s the -s is
    """
    click.echo(pp.remove_stopwords(text_input, list(stopwords)))


# ---------- struct ----------
@struct.command("shuffle")
@click.argument("values", nargs=-1)
@click.option("--seed", default=None, type=int, help="Seed for reproducibility.")
def shuffle_cmd(values, seed):
    """Shuffle a list of values.

    Example: cli struct shuffle 1 2 3 4 --seed 42
    """
    click.echo(pp.shuffle(list(values), seed))


@struct.command("flatten")
@click.argument("lists", nargs=-1)
def flatten_cmd(lists):
    """Flatten a list of lists given as comma-separated groups.

    Example: cli struct flatten 1,2 3,4 5
    """
    click.echo(pp.flatten([group.split(",") for group in lists]))


@struct.command("unique")
@click.argument("values", nargs=-1)
def unique_cmd(values):
    """Remove duplicated values.

    Example: cli struct unique 1 2 2 3 1
    """
    click.echo(pp.remove_duplicates(list(values)))


if __name__ == "__main__":
    cli()
