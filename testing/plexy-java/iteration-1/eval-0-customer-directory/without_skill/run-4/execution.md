# Execution record

## Inputs consulted

Only these fixture files were read, relative to the project root:

- `testing/plexy-java/fixtures/customer-directory/pom.xml`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/model/Customer.java`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/service/CustomerDirectory.java`

No skill files were consulted or applied. No graders, tests, other runs, eval definitions, or benchmark results were read. No fixture, grading, or report files were edited.

## Changes

- Saved complete Maven and Java source files under `outputs/`, preserving the source layout, packages, class names, public method names, and argument types at JVM erasure. The map parameter is now generically typed as `Map<String, Customer>`.
- Preserved the supplied map by reference; loading updates that same map and duplicate ids replace existing entries.
- Made lookup absence explicit with `Optional<Customer>` and typed the display result as `List<String>`. Display strings remain sorted lexicographically in `Name (id)` form.
- Rejected a null directory map. Customer constructors and setters reject null or blank ids and names while preserving valid text and mutability.
- Removed suppression of file-read exceptions. UTF-8 reads propagate `IOException`; malformed or blank-field rows produce descriptive `IOException` messages including their one-based line number.
- Preserved the complete POM unchanged, including Java 17, UTF-8, and both existing dependencies.

## Tool usage

Inspection and artifact generation used three `get_file_structure` attempts (all reported unavailable), three successful `open` calls, two `multi_tool_use.parallel` wrapper calls, and one `apply_patch` call saving all four artifacts: nine calls including wrappers. This count excludes final submission.

No commands, tests, builds, or dependency downloads were run. No timing or token measurements were available or invented.

## Caveats

- Compilation and grading are deferred to the parent; no execution-based validation was performed.
- Lookup callers must now handle `Optional<Customer>`.
- CSV retains the supplied simple first-comma split behavior, not quoted or multiline CSV parsing. Empty or blank rows are invalid; remaining commas are part of the name.
- Loading is incremental: valid rows preceding a malformed row remain in the supplied map. The supplied map must support mutation for loading.