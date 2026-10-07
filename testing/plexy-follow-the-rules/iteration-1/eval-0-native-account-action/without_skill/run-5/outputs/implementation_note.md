Implemented `RenameAccountAction` for the future `accounts.rename_account` module using native relative imports, a frozen dataclass, and a typed repository field. It looks up the account, raises `NotFoundError(account_id)` when absent, replaces the immutable account's name, and returns `repository.save(...)`.

The keyword-only `rename_to` follows the selected reference's naming idiom without adopting its execution architecture. Leading and trailing whitespace are preserved exactly, as explicitly requested rather than following the project's usual stripping convention.

Only the two requested output files were written. Inputs were left unchanged; no dependencies were installed, and no tests or grading were inspected or run. No scope deviations.