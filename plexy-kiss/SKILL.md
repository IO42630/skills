---
name: plexy-kiss
description: >
  Keep solutions readable, maintainable, and no more complex than the actual requirements justify.
  Use when designing, implementing, refactoring, or reviewing code, scripts, or automation workflows.
  Trigger especially on "keep it simple", "KISS", "overengineered", "too many layers", "DRY",
  or requests for precise abstractions without speculative features, configuration, concurrency, or frameworks.
---

# plexy-kiss

- Build the requested solution, not the larger system it could become.
- Control solution scope and complexity, not investigation effort or whose coding style to follow.
- Minimize maintenance burden, not lines, files, dependencies, or abstractions independently.

## Keep the actual workflow visible

- Use the user's requirements and the project's existing constraints as the definition of done.
- Do not invent future variants, scale targets, or operating modes.
- Keep the main flow easy to follow in execution order.
- Prefer direct logic when it remains readable.
- Give functions and classes clear names for meaningful responsibilities.
- Keep edits within the requested scope instead of folding in unrelated cleanup.

## Make abstractions precise

- Extract a shared concept or a responsibility that makes current logic easier to understand.
- Apply `DRY` to shared knowledge that must change together.
    - Do not merge unrelated logic merely because it looks similar.
    - A little duplication can be cheaper than coupling independent concepts.
- Require a present purpose for interfaces, wrappers, and architectural layers.
    - A single implementation is not automatically wrong if a real contract requires the interface.
    - "We might need it later" is not a requirement unless that extension is part of the task.
- Omit structure whose removal would not hurt correctness, readability, or an established contract.

## Make capabilities earn their place

- Add configuration only for variation that actual callers need.
- Add concurrency, caching, or other optimizations only for a demonstrated need or explicit performance target.
- Prefer existing tools when they adequately solve the problem.
- Judge dependencies by their total maintenance cost rather than their count.
    - An established library can remove more complexity than hand-written replacement code.
- Handle real failure modes at the appropriate boundary.
    - Catch errors for recovery, cleanup, boundary translation, or missing actionable context.
    - Let diagnostic native errors propagate when the caller can already use them.
    - Preserve the original cause when translating an error.
    - Avoid defensive checks for states that established invariants make impossible.

## Keep the correctness floor

- Preserve required validation, security controls, cleanup, and data integrity.
- Retain structure required by governing guidelines or established project contracts.
- Allow complexity justified by explicit requirements or consequential failures.
- Do not turn simplicity into a ban on classes, dependencies, or multiple files.

## Calibration

- A browser automation should open, read, solve, submit, and repeat when that is the requested workflow.
    - Do not add a worker pool, background service, or configurable command-line interface without a requirement.
- A one-off JSON reader needs a direct library call, not a configurable processor framework.
- A payment retry needs duplicate-charge protection even if that makes the implementation larger.
- A loader explicitly required to support several sources may warrant an interface.