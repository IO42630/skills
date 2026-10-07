# Implementation note

`RenameAccountAction` follows the native frozen-dataclass action pattern and uses relative imports for its future location at `accounts.rename_account`. It reads with `repository.find`, raises `NotFoundError(account_id)` when missing, and saves an immutable replacement, returning the repository's saved account.

The keyword-only `rename_to` parameter follows the selected reference's naming idiom without adopting its execution architecture. The supplied name is preserved exactly, including surrounding whitespace, as explicitly requested instead of the usual stripping convention.

Inputs were left unchanged. No tests, grading, dependency installation, or unrelated migration was performed.