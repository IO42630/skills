# Teaching Evaluations

- `evals.json` defines content and workflow scenarios; it is not an executable test runner.
- Run each scenario in an isolated teaching workspace rather than the skill's source directory.
    - Paths in `files` are relative to the repository root.
    - Copy listed files from `fixtures/workspace/` while preserving paths below that directory.
    - Start scenarios with empty `files` lists in an empty workspace.
    - Keep outputs separate so one scenario cannot influence another.
- The fixture represents earlier sessions with a superseded belief and an unresolved empty-list misconception.
    - Case 4 checks review, lesson sizing, asset reuse, and restraint before new evidence arrives.
    - Case 5 supplies new evidence to check record supersession and an unconfirmed mission change.
- Run case 6 with normal skill routing to assess the invocation boundary.
    - Forcing the skill on only tests response compliance, not whether it activates appropriately.
- Inspect case 7's generated artifact in a browser rather than grading accessibility from prose alone.
    - Check `file://` loading with networking disabled.
    - Check keyboard navigation, focus visibility, and text contrast.
    - Check readable exercises and feedback with JavaScript disabled.
    - Check narrow-screen layout, reduced-motion behavior, and print preview.
- Check case 8's export alone, without the fixture's asset directory.
- Record unavailable checks as unverified rather than treating them as passes.