"""Data pre-processing functions for lists of values and text."""

import math
import random
import re


def _is_missing(value):
    """Return True if the value is considered missing (None, '' or nan)."""
    if value is None or value == "":
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    if isinstance(value, str) and value.strip().lower() == "nan":
        return True
    return False


def remove_missing(values):
    """Remove missing values (None, '' and nan) from a list."""
    return [v for v in values if not _is_missing(v)]


def fill_missing(values, fill_value=0):
    """Replace missing values in a list with the given fill value."""
    return [fill_value if _is_missing(v) else v for v in values]


def remove_duplicates(values):
    """Return the unique values of a list, keeping their original order."""
    unique = []
    for v in values:
        if v not in unique:
            unique.append(v)
    return unique


def normalize(values, new_min=0.0, new_max=1.0):
    """Normalize numerical values to [new_min, new_max] with min-max scaling."""
    old_min, old_max = min(values), max(values)
    if old_max == old_min:
        return [new_min for _ in values]
    scale = (new_max - new_min) / (old_max - old_min)
    return [new_min + (v - old_min) * scale for v in values]


def standardize(values):
    """Standardize numerical values with the z-score: (x - mean) / std."""
    mean = sum(values) / len(values)
    std = math.sqrt(sum((v - mean) ** 2 for v in values) / len(values))
    if std == 0:
        return [0.0 for _ in values]
    return [(v - mean) / std for v in values]


def clip(values, min_value, max_value):
    """Clip numerical values to the range [min_value, max_value]."""
    return [min(max(v, min_value), max_value) for v in values]


def to_integers(values):
    """Convert strings to integers, excluding non-numerical values."""
    result = []
    for v in values:
        try:
            result.append(int(float(v)))
        except (ValueError, TypeError):
            continue
    return result


def log_transform(values):
    """Apply the natural logarithm to the positive values of a list."""
    return [math.log(v) for v in values if v > 0]


def tokenize(text):
    """Split text into lower-cased words made of alphanumeric characters."""
    return " ".join(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def remove_punctuation(text):
    """Keep only alphanumeric characters and spaces."""
    return re.sub(r"[^a-zA-Z0-9 ]", "", text)


def remove_stopwords(text, stopwords):
    """Lower-case the text and remove the given stop-words."""
    stop = {w.lower() for w in stopwords}
    return " ".join(w for w in text.lower().split() if w not in stop)


def flatten(list_of_lists):
    """Flatten a list of lists into a single list."""
    return [item for sublist in list_of_lists for item in sublist]


def shuffle(values, seed=None):
    """Return a shuffled copy of the list; the seed makes it reproducible."""
    shuffled = list(values)
    random.Random(seed).shuffle(shuffled)
    return shuffled
