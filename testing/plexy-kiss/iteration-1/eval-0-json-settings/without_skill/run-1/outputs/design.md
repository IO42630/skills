# Design

`load_settings(path)` accepts a local string or path-like filename and reads it
with explicit UTF-8 encoding. The standard library's `json.load` preserves nested
objects, arrays, and scalar values; only the root must be a dictionary.

A non-object root raises `ValueError`. Filesystem errors and malformed-JSON
diagnostics propagate unchanged, including `FileNotFoundError` and
`json.JSONDecodeError`. A context manager closes the file on success or failure.
No alternate sources, modes, defaults, or configuration framework are needed.