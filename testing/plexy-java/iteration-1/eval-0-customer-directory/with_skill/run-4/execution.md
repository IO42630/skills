# Execution

## Inputs consulted

- `/Users/ivan.olexyn/home/ws-github/io42630/skills/plexy-java/SKILL.md` (task instructions).
- `testing/plexy-java/fixtures/customer-directory/pom.xml`.
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/model/Customer.java`.
- `testing/plexy-java/fixtures/customer-directory/src/main/java/example/service/CustomerDirectory.java`.

No other skills, fixture files, tests, graders, other runs, evaluation files, or benchmark results were read.

## Changes

- Saved complete Maven configuration with the existing Java 17 settings and unchanged dependencies.
- Replaced manual customer boilerplate with Lombok-generated mutable accessors, an all-arguments constructor, value-object methods, and a builder. Null ids and names fail in constructors and setters.
- Used Lombok's required-arguments constructor for the directory and retained the supplied map rather than copying it. A null map fails during construction.
- Added `outputs/lombok.config` with JDK null-check generation, so Lombok uses `Objects.requireNonNull` for required constructor parameters. Configuration lookup stops at this output project.
- Used explicit imports and parameterized collections. Missing lookups return `Optional.empty()`; display strings remain naturally sorted `Name (id)` strings.
- Kept UTF-8 reads and inserts into the original map. File-read exceptions propagate; rows lacking the comma separator produce an `IOException` identifying the one-based row number.
- Kept parsing limited to the existing first-comma split: no header handling, trimming, or quoted-field interpretation was added. Duplicate ids replace existing entries. Loading is not transactional: a malformed later row can leave earlier rows inserted.

## Tool accounting

Artifact-generation calls: one `open_entire_file` for the skill, three `get_file_structure` attempts (all unavailable), three `open` calls for the allowed inputs, and one `apply_patch` call creating the artifacts. Two `multi_tool_use.parallel` calls dispatched the structure attempts and input reads. These counts exclude the final submission call.

No terminal commands, tests, builds, or dependency fetches were run, as requested. Compilation and behavioral grading remain for the parent. No timing or token measurements were available or fabricated.

All writes were restricted to `testing/plexy-java/iteration-1/eval-0-customer-directory/with_skill/run-4/`.