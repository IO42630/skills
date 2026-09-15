# skills

A collection of AI agent skills compatible with [skills.sh](https://skills.sh/) and the `skills` CLI.

## Available Skills

### [`plexy-do-less`](./plexy-do-less/SKILL.md)

Biases agents toward the smallest correct action: answer or edit directly, skip repo-wide scans, tangents, and preamble.

### [`plexy-markdown`](./plexy-markdown/SKILL.md)

Formats Markdown as tight bullets: one statement per bullet, sub-bullets for sub-statements, lines under 120 chars.

## Installation

Install a skill via the `skills` CLI:

```bash
# Install to your current project
npx skills add IO42630/skills@plexy-do-less

# Or install globally for your agents
npx skills add IO42630/skills@plexy-do-less -g
```

## One-off Usage (without installing)

```bash
npx skills use IO42630/skills@plexy-markdown
```
