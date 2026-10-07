# Design

`load_settings(path)` accepts a local file path, opens it explicitly as UTF-8,
and uses the standard-library JSON decoder. A context manager closes the file
on both success and failure. The decoded dictionary is returned unchanged,
preserving nested objects, arrays, and scalar values; an empty object is valid.

Only the top-level type is validated: non-object JSON raises `ValueError`.
No exceptions are caught or wrapped, so missing files retain their native
`FileNotFoundError` and malformed JSON retains its `json.JSONDecodeError`
diagnostics. No alternate sources, modes, dependencies, or configuration
abstractions are needed.