---
name: plexy-markdown-update
description: >
  Preserve wording and structure only when the user explicitly asks to update an existing Markdown file, including
  natural forms such as "update this doc" or "I'm updating this page." Do not trigger for requests to rewrite, edit,
  revise, or correct Markdown without explicitly asking for an update. For updates, make the smallest accurate, locally
  traceable edits; avoid unrelated rewriting or reformatting. Pair with plexy-markdown for authored text without
  retrofitting untouched content.
---

# plexy-markdown-update

- Keep updates easy to review by preserving text that remains accurate and useful.
- Minimize unnecessary diff; accuracy, completeness, and explicit user requests take priority.

## When to apply

- Apply this skill only when the user explicitly asks to update an existing Markdown file.
  Natural forms such as "update this doc" and "I'm updating this page" count.
- Rewrite, edit, revision, correction, and creation requests do not trigger this skill unless the user explicitly asks
  to update an existing Markdown file.
  Follow the user's requested approach without imposing its diff-preserving workflow.
- If an update request also asks for a restructure or rewrite, honor that request and keep the rewrite scoped.

## Update existing Markdown

1. Read the relevant content and enough surrounding structure to understand its context.
2. Map the requested changes to existing text.
    - Keep accurate, relevant text unchanged.
    - Replace stale or incorrect claims where they already appear.
    - Add genuinely new facts near the related content.
    - Restructure only when requested or needed for correctness or clarity.
3. Edit the smallest meaningful spans.
    - Prefer a local word or phrase replacement when it preserves meaning and grammar.
    - Preserve sentence wording and order when only a fact or term has changed.
    - Add a focused line or list item instead of rewriting a nearby paragraph.
    - Keep headings, paragraph boundaries, list style, and table structure where practical.
    - Renumber only when a list's membership or order changes.
4. Do not keep outdated text merely to make the diff smaller.
    - Remove or replace a superseded claim when leaving it would create a contradiction.
    - Make surrounding edits only as large as needed for a correct, readable result.
5. Preserve unrelated formatting and content.
    - Do not reflow, reorder, rename, or restyle sections outside the requested change.
    - Do not run broad formatting over a document just to reduce line lengths.
6. Review the focused diff before delivery.
    - Check that each changed line maps to a requested fact or a necessary correction.
    - Confirm untouched content remains intact and stale claims do not remain contradictory.
    - Check grammar, links, list structure, and table consistency in the edited area.

## Use with plexy-markdown

- Use `plexy-markdown` guidance for text you add or substantially rewrite.
- Do not convert existing prose into bullets solely to apply that formatting style.
- Preserve the document's established format unless the user requests a style change.

## Examples

- Before: `This repo uses Jest.`
- New finding: the repo now uses Vitest.
- Prefer: `This repo uses Vitest.`
- Avoid: `Testing is done via Vitest.`
- The direct replacement preserves the sentence and makes the changed fact obvious.

- Before: `Unit tests run with Jest.`
- New finding: unit tests use Vitest, and browser tests still use Playwright.
- Prefer: change `Jest` to `Vitest` and add a nearby sentence about Playwright.
- Avoid: replacing the whole testing section or appending a conflicting Vitest claim.

- A larger rewrite is appropriate when the user explicitly requests a new structure.
- Keep that rewrite scoped; leave unrelated sections and accurate facts alone.