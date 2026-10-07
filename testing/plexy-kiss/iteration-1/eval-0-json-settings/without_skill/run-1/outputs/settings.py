"""Load JSON settings from a local file."""

import json
from os import PathLike
from typing import Any, Dict, Union


def load_settings(path: Union[str, PathLike[str]]) -> Dict[str, Any]:
    """Read a UTF-8 JSON object, preserving nested values.

    Raise ValueError for a non-object root. FileNotFoundError and
    json.JSONDecodeError propagate unchanged.
    """
    with open(path, "r", encoding="utf-8") as source:
        settings = json.load(source)

    if not isinstance(settings, dict):
        raise ValueError("Settings must be a JSON object at the top level")

    return settings