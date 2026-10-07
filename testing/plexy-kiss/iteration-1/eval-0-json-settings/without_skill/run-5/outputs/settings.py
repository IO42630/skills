"""Load settings from a local UTF-8 JSON file."""

import json
from os import PathLike
from typing import Any, Union


def load_settings(path: Union[str, PathLike[str]]) -> dict[str, Any]:
    """Return a JSON object, preserving nested values.

    Raise ValueError if the document's top-level value is not an object.
    FileNotFoundError and json.JSONDecodeError propagate unchanged.
    """
    with open(path, "r", encoding="utf-8") as source:
        settings = json.load(source)

    if not isinstance(settings, dict):
        raise ValueError("Settings must be a JSON object")

    return settings