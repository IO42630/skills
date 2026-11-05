---
name: plexy-sheep
description: >
  Keep changes native to an existing codebase. Use whenever implementing or reviewing a project change where
  local conventions matter, especially when considering unfamiliar syntax, APIs, dependencies, markup attributes,
  or abstractions. Gather comparable production examples, prefer established idioms, and ask before introducing
  a materially novel construct unless the user explicitly authorizes it. Do not use for standalone code with no
  repository conventions to preserve.
---

# plexy-sheep

- Make the requested change fit the codebase rather than adding an agent's preferred constructs.
- Treat repository precedent as evidence, not as a rigid quota or a reason to repeat unsafe behavior.
- Keep exploration focused on the affected code and its closest comparable examples.

## Workflow

1. Identify the requested behavior and explicit constraints.
    - Separate required behavior from implementation suggestions or incidental examples.
    - Note any construct, library, attribute, or abstraction the change may introduce.
2. Inspect local precedent before choosing an implementation.
    - Start in the affected module and nearby production code.
    - Compare examples that solve a similar problem in a similar context.
    - Check tests when they clarify contracts or expected behavior.
    - Do not turn the task into a repository-wide convention audit.
3. Prefer established idioms when they satisfy the requirement.
    - Reuse existing helpers, syntax, libraries, and component patterns where they fit.
    - Do not add a new construct merely because it is familiar or convenient.
4. Judge whether the evidence establishes a convention.
    - Aim for four or five independent, comparable production examples.
    - Treat this as a contextual evidence threshold, not a raw text-match count.
    - Count distinct use sites, not repeated copies of one implementation.
    - Give nearby examples more weight than unrelated uses elsewhere in the repository.
    - Exclude generated, vendored, copied, test-only, and exceptional edge-case code.
    - Fewer examples may still be useful evidence, but do not present weak evidence as a firm convention.
5. Treat consistent omission as evidence too.
    - Compare ordinary cases with ordinary cases before applying an exceptional constraint broadly.
    - If comparable fields consistently omit an optional attribute, do not add it based on one special case.
    - Do not infer a rule from generated duplicates or repeated copies of the same source.
6. Handle necessary novelty explicitly.
    - If an established idiom cannot meet the requirement, state the gap and why a new construct is needed.
    - Ask for approval before introducing a material departure when the user has not authorized it.
    - A clear requirement can authorize a novel mechanism when that mechanism is necessary to fulfill it.
    - Ask about unresolved choices, such as a new dependency, when the requirement does not settle them.
    - Never imitate a precedent that is unsafe, incorrect, or incompatible with the requested behavior.
7. Implement and verify only the requested change.
    - Use focused tests or checks that cover the behavior and relevant boundaries.
    - Briefly report the precedent used, the evidence strength, and any approved departure.

## Evidence examples

- Five independent production call sites of a helper for the same purpose support reusing that helper.
- Five generated copies of one call site do not establish five independent precedents.
- One exceptional field limit does not establish a limit for ordinary fields.
- Repeated omission of a field limit on comparable forms is useful evidence against adding one by default.
- A required behavior with no safe local precedent may justify novelty after the user approves the approach.

## Review before delivery

- Confirm the implementation meets the explicit behavior and preserves relevant project conventions.
- Confirm evidence came from comparable use sites rather than accidental text frequency.
- Confirm any material new construct was necessary and authorized.
- Report weak evidence or unresolved choices instead of inventing a repository rule.