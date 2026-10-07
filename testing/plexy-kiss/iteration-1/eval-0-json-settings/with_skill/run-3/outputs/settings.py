"""Load settings from a local UTF-8 JSON file."""

import json
from os import PathLike
from typing import Any, Dict, Union


def load_settings(path: Union[str, PathLike[str]]) -> Dict[str, Any]:
    """Return a JSON object, preserving nested values and native read errors.

    Raise ValueError if the JSON document's top-level value is not an object.
    FileNotFoundError and json.JSONDecodeError propagate unchanged.
    """
    with open(path, "r", encoding="utf-8") as file:
        settings = json.load(file)

    if not isinstance(settings, dict):
        raise ValueError("Settings must be a top-level JSON object")

    return settings