# Implementation note

`RenameAccountAction` follows the account module's frozen dataclass, typed repository, immutable replacement, and relative-import conventions. It uses `find` and `save`, raises the existing `NotFoundError(account_id)` for a missing account, and returns the saved account.

The selected reference supplies the keyword-only `rename_to` naming idiom, not its execution architecture. The explicit task requirement overrides normal name stripping: leading/trailing whitespace is preserved exactly.

Only the two requested output files were written; inputs were unchanged. No dependencies were installed, and no tests, graders, evaluation metadata, reports, or other runs were inspected or executed.