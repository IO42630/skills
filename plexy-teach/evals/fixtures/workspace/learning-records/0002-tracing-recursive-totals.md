# Tracing recursive totals

- Status: active
- Insight: The learner can trace totals for non-empty nested lists but thinks every list needs a first leaf value.
- Evidence: Correctly traced `[2, [3]]` to `5`, then said `[]` is invalid because there is nothing to recurse on.
- Implication: Teach empty-list termination next without repeating the basic non-empty trace.
- Predecessor: [Separate loops for every nesting depth](0001-hard-coded-depth.md).