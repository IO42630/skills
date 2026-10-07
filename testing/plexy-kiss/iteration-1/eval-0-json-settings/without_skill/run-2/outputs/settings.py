"""Load settings from a local UTF-8 JSON file."""

import json
from os import PathLike
from typing import Any, Union


def load_settings(path: Union[str, PathLike[str]]) -> dict[str, Any]:
    """Return a JSON object, preserving its nested values.

    File access and JSON decoding errors propagate unchanged. A non-object
    top-level value raises ValueError.
    """
    with open(path, "r", encoding="utf-8") as settings_file:
        settings = json.load(settings_file)

    if not isinstance(settings, dict):
        raise ValueError("Settings JSON must contain an object at the top level.")

    return settings