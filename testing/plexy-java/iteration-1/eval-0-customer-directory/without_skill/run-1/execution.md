# Execution record

## Inputs consulted

Only these fixture files were read, relative to the project root:

- `testing/plexy-java/fixtures/customer-directory/pom.xml`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/model/Customer.java`
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/service/CustomerDirectory.java`

No skill was consulted or applied. No grader, tests, other runs, evaluations, or benchmark results were read. The fixtures were not modified. All writes are confined to this run directory.

## Changes

- Saved the complete Maven file with the original Java 17 settings and dependencies unchanged.
- Kept `Customer` mutable, with the same constructor, getters, and setters. Constructor and setter inputs now reject null or blank IDs and names without trimming valid text.
- Replaced raw map/list types and wildcard imports with typed collections and explicit imports. The directory retains and updates the supplied map rather than copying it; a null map is rejected immediately.
- Changed `findById(String)` to return `Optional<Customer>` for explicit absence.
- Preserved sorted display strings in the form `Name (id)`.
- Kept UTF-8 loading, propagated file-read `IOException`s, and added descriptive line-numbered `IOException`s for missing or blank CSV fields. A null path is rejected explicitly.

## Verification and caveats

Artifact generation only. No commands, tests, builds, application launches, or dependency fetching were performed. Compilation and grading are left to the parent.

CSV parsing retains the original first-comma separator behavior: the remainder is the name. Quoted CSV fields are not decoded. Duplicate IDs overwrite existing entries. Loading is not transactional: valid earlier rows remain in the supplied map if a later row is malformed. The caller must supply a mutable map with correctly typed entries; external map modifications remain visible.

## Tool usage

Artifact-generation calls, including the call writing this record and excluding final delivery:

- `open_entire_file`: 3 calls, one per permitted input.
- `multi_tool_use.parallel`: 1 wrapper call for those independent reads.
- `apply_patch`: 1 call creating the three output files and this record.
- Skill reads, commands, searches, builds, and test executions: 0.

No measured timing or token usage is available; none is claimed.