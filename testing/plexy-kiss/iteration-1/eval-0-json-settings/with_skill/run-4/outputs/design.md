# Settings loader design

`load_settings(path)` directly opens a local file as UTF-8 and uses the standard
library's `json.load`. A context manager closes the file even when parsing fails.
The only additional validation requires a top-level dictionary; nested JSON
values remain unchanged. Other top-level values raise `ValueError`.

Filesystem and parsing exceptions are not caught or wrapped, preserving native
`FileNotFoundError` and `json.JSONDecodeError` diagnostics. No alternate sources,
configuration modes, caching, or extra dependencies are needed for current callers.