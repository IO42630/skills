# Implementation note

`RenameAccountAction` follows the module's frozen dataclass, typed repository, native relative imports, immutable replacement, and repository `find`/`save` conventions. Missing accounts raise `NotFoundError(account_id)`; successful execution returns the repository's saved account.

The selected reference supplies the keyword-only `rename_to` naming idiom, not its storage or concurrency architecture. The supplied name is preserved exactly, including whitespace, as explicitly requested instead of the project's usual stripping rule.

Only the two requested output files were written. Inputs were unchanged; no tests were inspected or run, no dependencies were installed, and there were no scope deviations.