# Design

`load_settings(path)` opens a local file with explicit UTF-8 encoding, parses it
with the standard library's `json.load`, and validates that the top-level value
is a dictionary. Nested objects, arrays, and scalar values remain unchanged.

The context manager closes the file even if parsing fails. Missing-file errors
and `json.JSONDecodeError` propagate without wrapping, retaining their native
diagnostics. Valid JSON with a non-object root raises `ValueError`.

The helper supports string and path-like local paths. It has no additional data
sources, modes, configuration, dependencies, or abstraction layers because
current callers do not need them. Type annotations support Python 3.9 or newer.