---
name: plexy-save
description: >
  Rewrite the repo's root AGENTS.md as a reduced model of the project, and write an independent
  session checkpoint under `.agents/saves/` that captures the current session's goal, decisions,
  changes, state, and next steps, so the session can be restored later.
  Use when the user asks to save or refresh session context, persist the current session,
  rebuild or update AGENTS.md, or hand off work to a fresh session.
  Do not use for ordinary file saves, commits, or a request to summarize one change.
---

# plexy-save

`AGENTS.md` is the repo's durable model; a save is the session's restore point.
They serve different readers and must not be copies of each other.

- Update `AGENTS.md` with the repo model a fresh session needs.
- Write an independent session save under `.agents/saves/`.
- Preserve what is still true; drop what is not.
- Reply in three lines.

## Two artifacts

- **`AGENTS.md`** answers: what is this repo, what are its parts, how do I build and test it?
    - It is read at the start of every session.
    - It is repo-scoped, compressed, and durable.
- **`.agents/saves/save-NN_slug.md`** answers: what was this session doing, what did it decide,
  what changed, and what is left?
    - It is read when the user restores that session.
    - It is session-scoped, concrete, and allowed to be longer.
    - It is not auto-loaded; the user reads it only on restore.
- Do not paste the repo model into the save.
- Do not turn `AGENTS.md` into a session log.
- Cross-reference; never duplicate.

## Boundaries

- Use this for repo-level context saves and session checkpoints, not ordinary file writes or commits.
- Do not invent facts; every sentence must trace to a path, command, version, number, or the conversation.
- Do not copy `.agents/` files into either output; mine them for facts.
- Keep secrets out of the save; record that a constraint exists, not its value.

## 1. Read before writing

- Existing `AGENTS.md` — the starting draft; keep every fact that still holds.
- Existing saves under `.agents/saves/` — the latest checkpoint; reuse facts that still hold.
- Existing `.agents/` files — mine for facts, then ignore.
- Build config that actually exists — `package.json`, `pom.xml`, `build.gradle`, `Cargo.toml`.
    - Never list a command you have not confirmed exists.
- Source tree and domain code — the primary input for the repo model.
    - Explore actively; configs alone give you a skeleton, not the meaning.
- WIP markers — TODOs, uncommitted changes, half-built features, open branches.
- The full conversation of this session — the save's primary input.

## 2. Update AGENTS.md

Use exactly five sections in `AGENTS.md`, in this order.
Let length follow the repo's real size; completeness beats a line cap.
Do not repeat a fact across sections; Contents defines it, History may only reference it.

```markdown
# <project title>

## 1. Overview
## 2. Model
## 3. Contents
## 4. Conventions
## 5. History

### YYYY-MM-DD — topic
```

### Overview

- One or two sentences: what the project is, who it serves, and its stack with versions.
- One line on where the project stands right now.
- Why: a fresh session needs the project's identity and current state before any detail.

### Model

- The domain ontology: core entities, how they relate, invariants, and the vocabulary a developer uses.
- Draw the concept graph, not a story; a fresh session should absorb what the codebase means.
- If there is no real domain (pure infra or config), say so in one line and move on.
- Why: names and relationships are the map that makes the rest of the file navigable.

### Contents

- A semantic inventory of the modules a developer thinks in, not a directory tree.
- Per unit: what it does → what it depends on → current state (done / in-progress / blocked / pending).
- Collapse boilerplate; do not list every file.
- Why: the next session needs to know which unit owns a behavior and what is unfinished.

### Conventions

- Build, test, and lint commands verbatim, each citing where it is defined.
- Style rules — indent, quotes, naming, import order — each citing the config that enforces it.
- Only real patterns and gotchas; drop generic advice.
- Keep machine-specific environment facts out of Conventions; record them in Overview or History.
- Why: unverified commands and generic advice cost the next session time and trust.

### History

- A rewritten digest, not an append-only log; merge old entries and drop stale ones.
- Priority order: anomalies first, then decisions still in force, then open issues.
- Format: `### YYYY-MM-DD — topic`, followed by one-fact bullets.
- Why: history explains the current state; it is not a changelog of everything that happened.

## 3. Write the session save

Use this template. The save is a restore point, not a second repo model.
Its reader is the user resuming this session, not a fresh session exploring the repo.

```markdown
# Save: <session topic>

- Date: <YYYY-MM-DD>
- Repo: <repo root>
- Status: <in-progress | handed-off | done>
- Repo model: `AGENTS.md`

## Goal

- <what the user asked for in this session>
- <success condition, if stated>

## Scope

- <what this session covers>
- <what it explicitly does not cover>

## Context

- <one line on the repo and the part this session touched>
- <constraints and assumptions not obvious from the repo>
- <relevant files, issues, docs, commands>
- <earlier decisions that still shape this work>

## Work and decisions

- <what changed, in order, with file paths>
- **D1** — <decision>. <rationale>
- <alternatives rejected, when they matter for restoring the thread>

## State

- <what works>
- <what is broken or unverified>
- <tests and commands run, with results>
- <uncommitted changes and where they live>

## Open threads

- <what remains>
- <blockers and who or what resolves them>
- <the next concrete action>

## Restore

- Read this file; read `AGENTS.md` for the repo model.
- Start with: <one-line instruction for the resumed session>.
```

- Capture intent, constraints, and decisions that the code cannot show.
- Include exact paths, commands, test results, and uncommitted changes.
- Include what failed or is uncertain; a restore point that hides gaps is a trap.
- Do not paste the five-section repo model; reference `AGENTS.md` instead.
- Make the restore line actionable, not a summary.

### Save numbering

- Create `.agents/saves/` at the repo root if it does not exist.
- Derive a short lowercase kebab-case slug from the session's main topic.
    - Fall back to the repo directory name when the topic is unclear.
- Number the save from the highest existing `save-NN_*.md`.
    - Use `save-01_<slug>.md` for the first save; zero-pad to two digits.
    - Match a wider existing width; never reuse an existing path.
- Create a new save for each checkpoint; update an existing save when the user names it.
    - Do not create a duplicate for the same checkpoint.

## 4. Write and verify

- Write `AGENTS.md` first; it is the durable repo model.
- Write the save second; it records the session, including the repo update.
- If either write fails, stop and report which file is missing.
- Never leave placeholder text in either file.

- Repo check: could a fresh session name the components, their relationships, and what is unfinished,
  from `AGENTS.md` alone?
- Session check: could the user resume this session from the save without the chat transcript?
- Command check: does every command in `AGENTS.md` actually exist?
- Duplication check: does the save avoid pasting the repo model?
- File check: do both files exist, and does the save point to the right `AGENTS.md`?
- Stale check: did you drop anything that is no longer true instead of carrying it forward?

## Reply

Answer in exactly three content lines; no headings or extra notes:

- The files written.
- What changed in `AGENTS.md`.
- What the save captures and what was dropped as stale from `AGENTS.md`.

## Why

- `AGENTS.md` is loaded every session; the save is loaded only on restore, so their lifetimes differ.
- A session save must carry intent and state that the code cannot, or restoring it is guesswork.
- Keeping the save independent stops the repo model from becoming a session log.
- Cross-references keep both artifacts small, truthful, and reviewable.
