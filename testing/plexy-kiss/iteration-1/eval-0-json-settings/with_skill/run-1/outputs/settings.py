"""Load settings from a local UTF-8 JSON file."""

import json


def load_settings(path) -> dict:
    """Return a JSON object, letting file and JSON parsing errors propagate.

    Raise ValueError if the top-level JSON value is not an object.
    """
    with open(path, "r", encoding="utf-8") as settings_file:
        settings = json.load(settings_file)

    if not isinstance(settings, dict):
        raise ValueError("Settings must be a JSON object")

    return settings