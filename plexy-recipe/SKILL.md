---
name: plexy-recipe
description: >
  Capture a code pattern from project code, supplied snippets, or a described concept as a self-contained,
  reusable Markdown recipe under .agents/recipes/ using names such as recipe-foo-bar.md.
  Find, explain, and apply existing recipes
  when the user asks to look in recipes or implement something using them. Trigger whenever the user asks to
  document, preserve, generalize, save, look up, or use a code pattern as a recipe, even without saying
  "recipe". Do not trigger for ordinary code changes unless recipe capture or use is requested.
---

# plexy-recipe

- Turn concrete code patterns into concise guides that work for both people and future agents.
- Reuse existing recipes to implement requested changes without treating recipes as unquestionable authority.
- Keep one self-contained Markdown file per distinct concept.

## Choose the workflow

- Use the authoring workflow when the user asks to capture, document, generalize, or save a pattern.
- Use the application workflow when the user asks to find, explain, or implement a pattern from recipes.
- Do not create or update a recipe as a side effect of ordinary implementation work.
- If the requested pattern or target project is unclear, ask only for information that blocks a useful result.

## Author a recipe

1. Identify the target project's root directory.
    - Save in that project's `.agents/recipes/`, not beside this skill.
2. Gather the smallest useful evidence for the pattern.
    - Inspect the supplied code or named source files.
    - Check relevant callers, tests, contracts, and project conventions when they affect the pattern.
    - Use the user's description only when it is sufficient; otherwise ask for missing evidence.
3. Establish the pattern before writing instructions.
    - State the problem it solves and when it fits; introduce only the mental model needed to follow it.
    - Trace a concrete input through the mechanism to its observable outcome in causal order.
    - Explain why a step or ordering matters when omitting it could change the result.
    - Separate reusable invariants from project choices, assumptions, dependencies, and optional adaptations.
    - Distinguish observed behavior, recommendations, and unresolved concerns.
    - When sources conflict, check current implementation, tests, or configuration and state any remaining uncertainty.
4. Check for an existing recipe before choosing a filename.
    - Compare relevant recipes by concept. Revise one only when asked or authorized; otherwise report a duplicate.
    - For a new concept, use `recipe-<lowercase-kebab-case-slug>.md` without a sequence number.
    - If that filename already exists for a different concept, choose a more specific, descriptive slug.
    - Preserve existing filenames, including recipes that already have sequence numbers.
    - Prefer a flat collection unless the project already has useful directories or stable categories justify them.
    - Keep slugs concise and searchable; use established prefixes such as `frontend` or `backend` when helpful.
    - Avoid encoding every category in a filename; recipes can cover cross-cutting concepts.
    - If an index exists, update its relevant entry as part of an authorized recipe addition or rename.
    - Create `.agents/recipes/` only when a new recipe is needed.
5. Teach the pattern at its natural scale.
    - Use a complete, representative example that connects the input, key wiring or decision, and outcome.
    - Keep a simple pattern short; add detail or examples only for branches that change behavior.
    - Make examples syntactically coherent and source-faithful. Label pseudocode and project-specific choices.
    - Keep one concept per recipe and enough context to use it without the chat or source file.

### Recipe content

- Choose only useful sections, such as purpose, fit, mechanism, example, limits, checks, or sources.
- Connect important steps to their reason and likely failure; make checks demonstrate observable behavior.
- Cut repeated explanations and incidental detail before unique reasoning, evidence, assumptions, invariants, or edges.
- Cite inspected paths and symbols, but keep the essential guidance in the recipe itself.
- Omit irrelevant details and secrets. Do not endorse unsafe or accidental behavior as a recommendation.
    - Explain the risk and ask before preserving a questionable pattern.

## Find and apply a recipe

1. Resolve `.agents/recipes/` from the target project root, not this skill's fixtures.
2. Find candidates by concept and read the best match, including assumptions, limits, and checks.
    - Search filenames and contents; do not rely on one prefix or category to find a recipe.
    - Search recursively when the collection already uses subdirectories.
    - Treat an index as a navigation aid, not a complete catalog; verify matches through search.
    - If none fits, ask whether to create one or proceed without it.
3. Inspect target code and tests; compare contracts with the recipe and adapt names and structure.
    - Surface material conflicts or missing prerequisites before implementation.
4. Implement only the requested behavior; update the recipe only when separately asked.
5. Run focused checks or relevant tests and report the recipe, adaptations, and unresolved issues.

## Review before delivery

- Check that a reader can explain the pattern's fit, trace its mechanism, identify adaptations, and verify its result.
- Check that the example is complete enough for the concept.
    - Compression should remove repetition, not essential context.
- Check source provenance, uncertainty labels, authorized path, and filename.
    - Re-read the saved recipe and report its path.
