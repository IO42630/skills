"""Load settings from a local UTF-8 JSON file."""

import json
from os import PathLike
from typing import Any, Union


def load_settings(path: Union[str, PathLike[str]]) -> dict[str, Any]:
    """Return a JSON object, leaving filesystem and JSON errors unchanged.

    Raise ValueError if the file contains a non-object JSON value.
    """
    with open(path, "r", encoding="utf-8") as file:
        settings = json.load(file)

    if not isinstance(settings, dict):
        raise ValueError("Settings must be a JSON object")

    return settings