# Lab0 – Fundamentals of Continuous Integration

Data pre-processing library with a Click CLI, linted with pylint, formatted with black and tested with pytest.

## Setup
```bash
uv sync
```

## Usage
```bash
uv run python -m src.cli --help
uv run python -m src.cli clean remove-missing 1 "" nan 3
uv run python -m src.cli numeric normalize 1 2 3 --new-min 0 --new-max 10
uv run python -m src.cli text remove-stopwords "The cat is black" -s the -s is
uv run python -m src.cli struct shuffle 1 2 3 4 --seed 42
```
Negative numbers must go after `--`: `uv run python -m src.cli numeric clip -- -1 0.5 2`

## Quality checks
```bash
uv run python -m pylint src/*.py
uv run black src/*.py
uv run python -m pytest -v --cov=src
```
