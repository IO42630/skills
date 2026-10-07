# Implementation note

`rename_account.py` is intended as `accounts.rename_account` and uses native relative imports, a frozen dataclass, typed repository injection, and the existing `find`/`save` methods. It replaces the immutable account and returns the repository's saved result; missing accounts raise `NotFoundError(account_id)`.

The selected reference supplies only the keyword-only `rename_to` naming idiom, not its store or concurrency architecture. The supplied name is preserved exactly, including leading/trailing whitespace, as explicitly requested instead of the guideline's usual stripping. No inputs or unrelated code were changed, and no dependencies were installed.

Direct runtime validation was blocked by the available Python interpreter's lack of support for the fixture's existing `Account | None` annotation, which requires Python 3.10+. No tests or graders were inspected.