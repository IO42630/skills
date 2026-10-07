"""Load settings from a local UTF-8 JSON file."""

import json
from os import PathLike
from typing import Any, Union


def load_settings(path: Union[str, PathLike[str]]) -> dict[str, Any]:
    """Return the JSON object at path, rejecting other top-level values."""
    with open(path, "r", encoding="utf-8") as settings_file:
        settings = json.load(settings_file)

    if not isinstance(settings, dict):
        raise ValueError("Settings must be a JSON object.")

    return settings