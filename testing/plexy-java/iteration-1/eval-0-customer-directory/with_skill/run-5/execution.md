# Execution record

## Inputs consulted

- `testing/plexy-java/fixtures/customer-directory/pom.xml`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/model/Customer.java`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/service/CustomerDirectory.java`

## Skill consulted

- `/Users/ivan.olexyn/home/ws-github/io42630/skills/plexy-java/SKILL.md`, read first.
- No other skills, tests, graders, runs, evaluations, or benchmark results were read.

## Changes

- Saved the complete Maven file with the original Java 17 settings and both dependencies unchanged.
- Replaced handwritten customer boilerplate with Lombok `@Data`; retained mutable fields, the two-string constructor, and existing accessor names. Null ids and names are rejected in construction and mutation.
- Used Lombok `@RequiredArgsConstructor` and a non-null, typed map field for the directory. The supplied map is retained, not copied.
- Added `outputs/lombok.config` to make Lombok generate `java.util.Objects.requireNonNull` checks and keep configuration local to these artifacts.
- Changed lookup to `Optional<Customer>` and display results to `List<String>`, retaining sorted `Name (id)` rendering.
- Retained UTF-8 loading into the original map, removed silent I/O failure handling, and report rows missing the comma separator with `IOException` rather than an indexing failure.
- Replaced wildcard imports and raw types, used obvious local-variable inference, and formatted chains and multi-argument calls per the skill.

## Tool usage

Through the artifact-writing call, seven individual tool invocations were issued: four `open`, two `get_file_structure`, and one `apply_patch`. Both structure calls reported that the action was unavailable; direct reads of the permitted source files supplied the needed content. Two `parallel` wrapper invocations dispatched the independent reads and structure requests. The final delivery invocation is not included in these counts.

## Validation and caveats

- Artifact-generation only: no terminal commands, builds, tests, dependency fetches, or timing/token measurements were performed.
- All writes are within this run directory. Fixture and parent-owned grading/report files are untouched.
- Parent compilation/grading remains pending; include `outputs/lombok.config` with the generated project so null checks use the configured JDK implementation.
- Parsing retains the original first-comma split semantics; quoted CSV is not added. If a malformed row follows valid rows, earlier rows remain in the supplied map.