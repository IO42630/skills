---
name: plexy-markdown-update
description: >
  Make focused Markdown updates when the user explicitly asks to update an existing file. Natural forms include
  "update this doc" and "I'm updating this page." Do not trigger for rewrite, edit, revision, or correction requests
  unless the user asks for an update. Prefer small, clear edits that preserve meaning and useful structure.
---

# plexy-markdown-update

- Keep updates accurate, concise, and easy to review.
- Prefer local edits; accuracy, completeness, and explicit requests take priority over diff size.

## When to apply

- Trigger only when the user explicitly asks to update an existing Markdown file.
  "Update this doc" and "I'm updating this page" are examples.
- A rewrite, edit, revision, correction, or creation request alone does not trigger this skill.
  Follow the requested approach without imposing its update workflow.
- If an update also requests a rewrite or restructure, honor it within the requested scope.

## Update existing Markdown

1. Read the target and enough surrounding content to understand its structure.
2. Map requested changes to existing text.
    - Replace outdated claims in place and add new facts near related content.
3. Edit locally, then make a light editorial pass.
    - Remove filler and repetition; clarify awkward wording and improve scanability when small edits help.
    - Preserve accurate meaning and useful detail; leave clear wording alone.
    - Prefer local replacements and a few focused lines; this is a preference, not a quota.
    - Preserve the existing structure and format where practical; restructure only when requested or needed.
4. Review the diff before delivery.
    - Remove superseded claims even when that makes the diff larger.
    - Check that changes serve the request, clarity, or correctness.
    - Check the edited area for grammar, links, and consistent lists or tables.

## Use with plexy-markdown

- Apply `plexy-markdown` to added or substantially rewritten text.
- Preserve the established format; don't reflow or convert untouched text just to apply the style.

## Examples

- Fact change: `This repo uses Jest.` → `This repo uses Vitest.`
- Prefer the direct replacement over `Testing is done via Vitest.`

- New fact: change `Jest` to `Vitest` and add a nearby sentence that browser tests use Playwright.
- Avoid replacing the whole testing section or leaving conflicting claims.

- Light edit: `This guide explains the process in a simple way.` → `This guide explains the process clearly.`