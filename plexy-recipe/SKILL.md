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
    - Read `.agents/recipes/cookbook.md` when it exists.
    - When present, follow its project-specific recipe structure and naming conventions.
    - Compare relevant recipes by concept. Revise one only when asked or authorized; otherwise report a duplicate.
    - For a new concept, follow the cookbook's section structure and category hierarchy.
        - If the cookbook is missing, derive its conventions from existing recipes and the project.
        - Create it before writing the new recipe.
        - Specify required and optional recipe sections.
        - Define a concise, category-first naming hierarchy.
    - Keep a table with `keyword`, `weight`, and `scope` columns for filename terms.
        - For a new cookbook, generate the initial table from project conventions for the user to review and edit.
        - For an authorized update that needs a missing table, create a draft for user review.
        - Treat the table as user-maintained after creation and preserve the user's edits.
        - Give broader groups higher weights than narrower concerns, types, or topics.
        - Sort table rows by descending weight, then alphabetically by keyword for equal weights.
        - Order filename keywords by descending weight; order equal weights alphabetically.
        - For example, these project-specific weights produce `recipe-backend-testing-resource.md`:

          | keyword | weight | scope |
          | --- | --- | --- |
          | backend | 30 | Backend code |
          | testing | 20 | Tests |
          | resource | 10 | Resources |

        - Include every filename keyword in the table.
        - For a missing term, propose a row for the user to add; edit the table only with explicit authorization.
        - Preserve established weights; ask if a new term's placement cannot be inferred.
    - Use `recipe-<category>-<subcategory>-<topic>.md` when each category adds useful meaning.
        - For example, prefer `recipe-frontend-angular-zoneless.md` over `recipe-zoneless-angular.md`.
        - Use lowercase kebab case without a sequence number for new recipes.
    - If that filename already exists for a different concept, choose a more specific, descriptive slug.
    - Preserve existing filenames, including recipes that already have sequence numbers.
    - Keep the collection flat unless existing directories or stable categories justify a tree.
    - Keep category chains concise and searchable.
    - Reuse established prefixes such as `frontend` or `backend`.
    - Omit categories that add no useful distinction; cross-cutting recipes need not encode every category.
    - Treat the cookbook as conventions, not an exhaustive recipe catalog.
    - Update cookbook rules only when an authorized change to the conventions is needed.
    - Create or revise the cookbook on its own only when the user explicitly requests it.
    - If a separate index exists, update its relevant entry as part of an authorized recipe addition or rename.
    - Create `.agents/recipes/` only when a new recipe or an explicitly requested cookbook needs it.
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
    - Read `.agents/recipes/cookbook.md` when it exists.
    - Treat it as guidance, not a recipe or complete catalog.
    - Create a missing cookbook only when authoring a recipe or when the user explicitly requests it.
2. Find candidates by concept and read the best match, including assumptions, limits, and checks.
    - Search filenames and contents; do not rely on one prefix or category to find a recipe.
    - Search recursively when the collection already uses subdirectories.
    - Verify cookbook or index suggestions through filename and content search.
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
    - Confirm every filename keyword is in the cookbook and ordered by descending weight.
    - Re-read the saved recipe and report its path.
