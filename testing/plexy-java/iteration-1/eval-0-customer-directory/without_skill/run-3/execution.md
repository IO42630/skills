### Inputs consulted

Only these fixture files were read, relative to the project root:

- `testing/plexy-java/fixtures/customer-directory/pom.xml`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/model/Customer.java`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/service/CustomerDirectory.java`

No skill was consulted or applied. No grader, tests, other runs, evaluations, or benchmark results were read. Fixtures and grading files were not edited; all writes are inside this run directory.

### Changes

- Saved the complete `pom.xml` unchanged, preserving Java 17, UTF-8, and both existing dependencies and versions.
- Kept `Customer` mutable with the original constructor, getters, and setters. Null fields now raise `NullPointerException`; blank fields raise `IllegalArgumentException`. Valid values are preserved without trimming.
- Replaced raw collections with `Map<String, Customer>` and `List<String>`. The directory retains the supplied map, rejects a null map and null existing keys or values, and returns `Optional<Customer>` from `findById`.
- Preserved sorted display strings in the form `Name (id)`.
- Kept explicit UTF-8 loading into the supplied map. File-read failures propagate as `IOException`; malformed rows and blank fields produce an `IOException` identifying the line, with the original validation cause where applicable.

### Caveats and verification

Artifact generation only: no commands, builds, tests, application runs, or dependency fetches were performed. Compilation and grading are left to the parent. Only static inspection of the permitted inputs was performed.

The CSV format is deliberately limited to two unquoted fields per row; there is no header, quoted-field, or embedded-comma support. Duplicate ids overwrite existing entries, matching the original map behavior. A malformed later row can leave earlier rows loaded. The supplied map must be writable for loading, and callers remain responsible for maintaining valid contents when mutating it directly.

### Actual tool calls known at artifact writing

- `get_file_structure`: 3 attempted calls, all reported unavailable and returned no file contents.
- `open_entire_file`: 3 successful calls, one for each permitted input.
- `apply_patch`: 1 call, the call writing these four artifacts.
- `multi_tool_use.parallel`: 2 wrapper calls for the inspection attempts and input reads above.
- Skill, terminal, test, build, and dependency-fetch calls: 0.

These counts include the current artifact-writing invocation but exclude the subsequent final submission. Elapsed time and token usage were not measured and are not reported.