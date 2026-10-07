# Settings loader

`load_settings(path)` accepts a local string or path-like file path. It opens
the file as UTF-8 and uses the standard-library JSON decoder, preserving nested
objects, arrays, and scalar values without transformation. A context manager
closes the file even when decoding fails.

Only a top-level object is accepted; other JSON values raise `ValueError`.
Filesystem and decoding exceptions are not caught or replaced, preserving native
`FileNotFoundError` and `json.JSONDecodeError` diagnostics. No additional data
sources, operating modes, dependencies, or configuration abstractions are needed.