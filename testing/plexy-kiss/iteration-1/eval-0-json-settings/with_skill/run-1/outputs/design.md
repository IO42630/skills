# Design

`load_settings(path)` directly opens a local file as UTF-8 and parses it with
the standard library's `json.load`. A context manager closes the file even
when parsing fails. The only additional validation requires a dictionary at
the top level; nested JSON values are preserved without transformation.

Non-object JSON raises `ValueError`. File and parsing errors are not caught,
so callers retain native `FileNotFoundError` and `json.JSONDecodeError`
diagnostics. No additional sources, operating modes, dependencies, or
abstraction layers are needed for the current local-file workflow.