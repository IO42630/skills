"""Load settings from a local UTF-8 JSON file."""

import json
from os import PathLike
from typing import Any, Dict, Union


def load_settings(path: Union[str, PathLike[str]]) -> Dict[str, Any]:
    """Return a JSON object, preserving its nested values.

    Raise ValueError if the top-level value is not an object. File access
    errors and JSON decoding errors propagate unchanged.
    """
    with open(path, "r", encoding="utf-8") as file:
        settings = json.load(file)

    if not isinstance(settings, dict):
        raise ValueError("Settings must be a JSON object.")

    return settings