---
name: plexy-markdown
description: >
  Write and edit Markdown as tight bullets — one statement per bullet, sub-bullets for sub-statements, lines under 120 chars. 
  Use whenever creating or editing any .md file (README, docs, ADR, notes, changelog, PR body) 
  or when the user asks for concise, scannable, or well-structured Markdown.
---

# plexy-markdown

Tight Markdown scans fast and diffs clean. Put one idea per line; nest the rest.

## The format

- **One statement per bullet.**
    - A statement is a single claim, step, fact, or rule.
    - If a bullet joins two ideas with "and", "then", "which", or a dash, split it.
- **Sub-statements become sub-bullets.**
    - Nest to show structure: the parent names the thing, children describe it.
    - Two or three levels is plenty; deeper means the structure is wrong.
- **Keep every line under 120 characters.**
    - The cap is a readability budget, not a formatting rule.
    - Break at clause boundaries into sub-bullets before wrapping a line.
- **Be concise.**
    - Cut words that don't change meaning (very, really, in order to, it should be noted).
    - Drop filler headings and empty transitions.

## What it looks like

Bad — one long bullet mixing several ideas:

> The deploy pipeline builds the image, pushes to the registry, updates the manifest, and verifies the pods.

Good — parent plus children:

```markdown
- The deploy pipeline has four stages.
    - Build the image.
    - Push it to the registry.
    - Update the manifest to trigger a rollout.
    - Verify the pods are healthy.
```

Bad — dash-chained fragments:

> - The service is fast - it caches responses - and it retries on failure.

Good:

> - The service is fast.
>   - It caches responses.
>   - It retries on failure.

## Where the rules bend

- **Code blocks, tables, frontmatter, and URLs are exempt.**
    - You can't wrap code, a URL, or a table cell without breaking it.
    - Let those lines run long rather than corrupt them.
- **Never delete content to hit the width.**
    - Restructure into sub-bullets; a genuinely long single statement may stand.
- **Don't rewrite prose the user didn't ask you to touch.**
    - Apply the style to what you write or edit, not to unrelated files.
- **Keep the document's existing structure.**
    - Don't collapse headings, tables, or ordered steps just to use bullets.

## Optional: enforcing the rules in-file

The skill travels with the agent; a file does not. To hold agents that lack this skill,
prepend this marker to the file:

```markdown
[//]: # (AI AGENT RULES - DO NOT EDIT - START)
[//]: # (- use bulletpoints for statements, and sub-bulletpoints for sub-statements)
[//]: # (- dont string statements together using dashes, especially if lengthy)
[//]: # (- be concise, always reduce non-informative noise)
[//]: # (AI AGENT RULES - DO NOT EDIT - END)
```

- Add it only when the user asks to guard or enforce a file.
- Don't prepend it to every Markdown file by default — it is noise in most.
- Keep the marker in sync with this skill when the rules change.

## Why

- One idea per line lets a reader skim the first words and know the shape.
- Short lines survive narrow terminals and side-by-side diffs.
- Sub-bullets carry parent-to-detail relationships that prose hides.
- Tight bullets cost fewer tokens and dodge merge conflicts on every edit.
