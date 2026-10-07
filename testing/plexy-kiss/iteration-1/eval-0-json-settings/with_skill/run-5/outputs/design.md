# Settings loader design

`load_settings(path)` opens a local file as UTF-8, decodes it with the standard-library `json.load`, and validates that the root is a dictionary. Nested objects, arrays, and scalar values remain as decoded; no flattening, defaults, or coercion is applied.

The context manager closes the file even when decoding fails. Non-object roots raise `ValueError`; filesystem and JSON decoding errors propagate without wrapping, retaining their native diagnostics.

The helper accepts a string or filesystem path object. One direct function is sufficient for the current local-file workflow; no source abstraction, operating modes, configuration framework, or external dependencies are needed.