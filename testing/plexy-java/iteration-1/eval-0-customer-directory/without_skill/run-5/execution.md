# Execution record

## Inputs consulted

Only these fixture files were read, relative to the project root:

- `testing/plexy-java/fixtures/customer-directory/pom.xml`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/model/Customer.java`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/service/CustomerDirectory.java`

No skill files were consulted or applied. No grader, tests, other runs, evaluations, or benchmark results were read. All writes are confined to this run directory; fixture and parent-owned files remain untouched.

## Changes

- Saved the complete Maven file unchanged, retaining Java 17, UTF-8, and both existing dependencies.
- Kept Customer mutable, preserving its constructor, getters, and setters. Reject null and blank id/name values in the constructor and setters, and provide equality and hash codes based on both fields.
- Replaced raw collections with `Map<String, Customer>` and `List<String>`. The map constructor argument remains a Map and is retained directly, not copied; null maps are rejected.
- Changed `findById(String)` to return `Optional<Customer>` so absence is explicit.
- Preserved naturally sorted display strings in the form `Name (id)`.
- Preserved UTF-8 loading into the supplied map and last-row-wins behavior for duplicate ids. File-read exceptions now propagate; malformed rows produce an IOException with their one-based row number.

## Validation and caveats

Artifact generation only: no commands, tests, builds, application executions, or dependency fetches were performed. Compilation and grading are left to the parent; no passing results are claimed.

CSV input is deliberately limited to two unquoted comma-separated fields, without headers or quoted-field support. Empty or blank fields and extra columns are rejected; nonblank field text is preserved without trimming. Loading is not transactional: valid earlier rows remain in the map if a later row is malformed. Customers remain mutable; changing their ids does not re-key the supplied map, and changing either field changes their hash code. Caller-supplied map entries are not copied or normalized.

## Tool accounting

- Three `get_file_structure` calls were attempted, all returning unavailable.
- Three `open` calls successfully read the permitted input files.
- Two parallel-wrapper calls grouped those six inspection calls.
- One `apply_patch` call creates the three complete output files and this execution record.
- These counts cover artifact generation and exclude the final submission call.

No timing or token measurements were collected or estimated.