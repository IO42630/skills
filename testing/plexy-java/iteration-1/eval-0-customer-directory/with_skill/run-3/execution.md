### Inputs consulted

- `testing/plexy-java/fixtures/customer-directory/pom.xml`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/model/Customer.java`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/service/CustomerDirectory.java`

### Skill consulted

- `/Users/ivan.olexyn/home/ws-github/io42630/skills/plexy-java/SKILL.md`, read first and used as task instructions.
- No other skills, tests, graders, runs, evaluation definitions, or benchmark results were read.

### Changes

- Saved complete source files and the unchanged Maven configuration under `outputs/`; dependencies and Java 17 release remain unchanged.
- Replaced manual value-object boilerplate with Lombok `@Data` and `@RequiredArgsConstructor`, preserving mutable fields, accessors, and the two-string constructor.
- Added Lombok `@NonNull` to constructor-required fields. The scoped `outputs/lombok.config` selects `JDK` null checks so generated constructors and setters use `Objects.requireNonNull`; configuration lookup stops at the output root.
- Kept the supplied map by reference and used `Map<String, Customer>` and `List<String>` instead of raw types. The constructor's argument remains `Map` at erasure.
- Changed `findById(String)` to return `Optional<Customer>` for explicit absence.
- Retained naturally sorted `Name (id)` display strings and UTF-8 loading into the same map.
- Removed the swallowed `IOException`; file-read failures propagate through the existing declared exception. Rows without a separating comma produce an observable `IOException`.
- Replaced wildcard imports, grouped imports, used inferred local types where obvious, and split chained calls and multiple arguments across lines.

### Validation and caveats

- Artifact generation only: no commands, tests, builds, dependency fetches, or timing/token measurements were performed.
- Compilation and grading remain the parent's responsibility. Keep `outputs/lombok.config` with the sources for the specified generated null checks.
- CSV retains the fixture's simple first-comma split: no header or quoted-field parser is added. Empty field values remain allowed. Duplicate ids overwrite previous entries; successful earlier rows remain loaded if a later row is malformed.
- Constructor validation rejects null required arguments; the map is not copied or audited for pre-existing invalid entries.
- All writes are confined to this run directory; fixture and grading files are unchanged.

### Tool counts

Through the artifact-creation call, seven individual tool invocations were made: four `open_entire_file`, two `get_file_structure` attempts (both reported unavailable), and one `apply_patch`. Two `multi_tool_use.parallel` orchestration calls wrapped five of the individual invocations. No shell or IDE-execution tools were called. Final submission is not included in these counts. Elapsed time and token usage are unavailable and are not estimated.