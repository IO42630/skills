# Settings loader design

`load_settings(path)` opens a local file with explicit UTF-8 decoding and uses
the standard library's `json.load` to preserve nested dictionaries, lists, and
scalar values. It validates only that the top-level result is a dictionary,
raising `ValueError` for every other JSON value.

The context manager closes the file even when parsing fails. No exception
wrapping is needed: missing files retain `FileNotFoundError`, and malformed JSON
retains `json.JSONDecodeError` with its original location diagnostics. Other
filesystem and decoding errors also propagate naturally.

The single function follows the current local-file workflow directly. There are
no additional sources, modes, configuration layers, or third-party dependencies.