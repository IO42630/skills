# Account module conventions

- Actions are frozen dataclasses with a typed `repository: AccountRepository` field.
- Use the dataclass-generated constructor; do not hand-write injection boilerplate.
- Name the action entry point `execute`.
- Models are immutable; use `dataclasses.replace` for updates rather than mutating stored instances.
- Read and write through the existing repository methods.
- Missing accounts raise the existing `NotFoundError(account_id)`; do not invent another error contract.
- Account names normally have leading/trailing whitespace stripped before saving.
- Match neighboring imports, type annotations, and four-space indentation.
- Keep changes local to the requested action; no framework, dependency, or concurrency changes.