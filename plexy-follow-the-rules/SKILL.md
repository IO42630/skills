---
name: plexy-follow-the-rules
description: >
  Follow the user's guidelines, reference style, and established project idioms instead of the agent's defaults.
  Use when writing, editing, or reviewing code under project conventions, explicit preferences, or supplied examples.
  Trigger especially on complaints about ignored libraries, annotations, naming, structure, or error-handling conventions.
---

# plexy-follow-the-rules

- Make code feel native to the user's project.
- Control whose conventions guide the implementation, not how much system to build.
- Consistency reduces the work required to understand and maintain a change.

## Identify the governing conventions

- Respect the governing instruction hierarchy.
- Within the permitted choices, use this order of evidence.
    - Explicit task requirements and user preferences.
    - References the user designates as the target style.
    - Established conventions in the affected project or module.
- Treat other user-selected projects as style evidence, not architectures to transplant wholesale.
- Do not guess the user's style from unrelated projects or the agent's preferred stack.

## Turn guidance into implementation choices

- Read the applicable project guidelines.
- Examine relevant reference code for concrete idioms.
    - Naming and formatting.
    - Responsibility boundaries and file organization.
    - Libraries, annotations, and boilerplate-reduction tools.
    - Error handling and testing patterns.
- Match these choices in the changed code rather than matching only whitespace.
- Reuse established tools when they express the intended design more clearly.
    - Avoid hand-written boilerplate when the intended convention already supplies it.
    - Confirm that the tool is available or explicitly requested before relying on it.
- Leave unrelated code unchanged unless the task includes a style migration.

## Resolve conflicts honestly

- Follow a clear explicit preference over an inferred convention when it is compatible with governing constraints.
- Ask a focused question when equally applicable guidance conflicts in a way that materially changes the solution.
- Explain a concrete incompatibility rather than silently substituting the agent's preferred approach.
- Preserve correctness, security, and established contracts when adapting examples.
- Do not treat obsolete or incidental details in a reference as requirements.

## Calibration

- Match a selected project's naming idiom without importing its worker pool or deployment architecture.
- Follow local error-handling conventions rather than replacing them with a generic custom exception scheme.
