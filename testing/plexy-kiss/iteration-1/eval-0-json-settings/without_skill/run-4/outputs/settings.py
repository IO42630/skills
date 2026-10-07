"""Load settings from a local UTF-8 JSON file."""

from __future__ import annotations

import json
from os import PathLike
from typing import Any


def load_settings(path: str | PathLike[str]) -> dict[str, Any]:
    """Return the JSON object at path, preserving its nested values.

    Raise ValueError if the top-level JSON value is not an object.
    FileNotFoundError and json.JSONDecodeError propagate unchanged.
    """
    with open(path, "r", encoding="utf-8") as settings_file:
        settings = json.load(settings_file)

    if not isinstance(settings, dict):
        raise ValueError("Settings must be a top-level JSON object")

    return settings