# Settings loader design

`load_settings(path)` reads a local file with explicit UTF-8 encoding and uses
the standard library JSON decoder. It accepts string and path-like paths and
returns the decoded dictionary without transforming nested values.

Only the top-level object requirement is validated; other valid JSON values at
the top level raise `ValueError`. No exceptions are wrapped, preserving native
`FileNotFoundError` and `json.JSONDecodeError` diagnostics. A context manager
closes the file even when decoding fails.

The helper requires Python 3.9 or newer and has no third-party dependencies.
There are no alternate sources, modes, defaults, caching, or schema rules.