# Settings loader design

`load_settings(path)` opens a local file with explicit UTF-8 decoding and uses
the standard-library JSON parser. It returns the parsed dictionary directly,
preserving nested objects, arrays, and scalar values without conversion.

A single top-level type check rejects non-object JSON with `ValueError`.
No exceptions are caught or wrapped, so missing-file and malformed-JSON
diagnostics remain native. The context manager closes the file even when
parsing fails. There are no dependencies, alternate sources, or extra modes.