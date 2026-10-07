# Execution record

## Inputs consulted

Only these fixture files were read, relative to the project root:

- `testing/plexy-java/fixtures/customer-directory/pom.xml`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/model/Customer.java`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/service/CustomerDirectory.java`

No skill was consulted or applied. No graders, tests, other runs, evaluation definitions, or benchmark results were read. Fixture and grading files were not modified.

## Artifacts and changes

- `outputs/pom.xml`: complete copy retaining Java 17, UTF-8, and both original dependencies unchanged.
- `outputs/src/main/java/example/model/Customer.java`: retains mutable id/name fields, constructor, getters, and setters; rejects null or blank field values without trimming valid values. Adds field-based equality, hash code, and a diagnostic string representation.
- `outputs/src/main/java/example/service/CustomerDirectory.java`: uses typed collections while retaining the supplied map by reference; rejects a null map; returns `Optional<Customer>` for lookup; returns naturally sorted `Name (id)` strings; loads UTF-8 rows into the same map and propagates file-read failures. Malformed rows produce an `IOException` with the line number and, for invalid fields, the underlying cause. Null lookup ids and paths fail explicitly.

Packages, class names, existing public method names, and argument types are retained. The constructor's map type is parameterized without changing its erased argument type. The lookup return type intentionally changes to make absence explicit.

## Tool accounting

Before artifact creation, there were six individual tool invocations: three `get_file_structure` attempts (all unavailable) and three successful `open` calls. Those were dispatched through two parallel-wrapper calls. All four artifacts are written together in one `apply_patch` invocation. These counts exclude final delivery; wrapper calls are reported separately from individual tool invocations.

No commands, tests, builds, dependency downloads, or IDE executions were performed. No timing or token measurements were collected or estimated.

## Validation limits and behavior

Artifacts were reviewed against the three supplied inputs only; compilation and grading are left to the parent. CSV handling retains the original simple first-comma split, not quoted CSV parsing: remaining commas belong to the name. Blank or malformed rows fail rather than being silently skipped. Duplicate ids overwrite earlier values, and existing map entries are otherwise retained. Loading is incremental: valid earlier rows remain in the supplied map if a later row is invalid. Supplied map contents remain caller-managed. Because customers are mutable and have value-based hash codes, they should not be mutated while used as hash-based collection keys.