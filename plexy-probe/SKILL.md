---
name: plexy-probe
description: >
  Run an adaptive, one-question-at-a-time probe that sharpens a plan, design, or decision and records
  each question and answer in `.agents/probes/probe-NN_slug.md`.
  Use when the user asks for a probe, says "probe me", "probe this", "let's probe", "start a probe",
  or asks to continue or end a probe; also for a relentless interview that stress-tests their thinking.
  Do not use for technical investigation of a system ("probe the endpoint") or ordinary plan mentions.
---

# plexy-probe

- Treat the probe as a design tree: each answer opens or closes branches.
- Ask one question at a time, adapting each question to the answers already given.
- Ask only questions whose prerequisites are settled and whose answers can change the outcome.
- Record the probe in a per-probe file so it survives context loss and can be resumed.
- Let the user stop with `end probe`; close with a shared-understanding summary.

## Boundaries

- This skill interviews the user about a decision; it does not investigate a system.
    - "Probe the endpoint" is ordinary debugging, not a probe session.
- Ask about the work, not the user's confidence, mood, or personality.
- Read code, plans, and references to ask better questions; do not edit them during the probe.
    - Answer a mid-probe question, then return to the interview.

## Open the probe

- Name the subject: the plan, design, or decision to sharpen.
- State the goal in one line: what the probe must settle.
    - If the subject is too vague to name, ask one opening question first.
    - Create the file as soon as the subject is nameable; record that exchange as Q1.
        - If the opening question came first, create the file immediately after the answer.
- Keep one goal per probe; split unrelated subjects into separate probes.
- Derive a short lowercase kebab-case slug from the subject.
- Create `.agents/probes/` at the target project root if it does not exist.
- Number the file from the highest existing `probe-NN_*.md`.
    - Use `probe-01_<slug>.md` for the first probe; zero-pad to two digits.
    - Match a wider existing width; never reuse an existing path.
    - Reuse the existing file when the user resumes a probe.
    - If an open probe already covers the same subject, offer to resume it.
    - If the user asks to continue a probe and several are open, ask which one first.
- Write the header and the first question before asking it.
- Tell the user the file path once, then keep the interview in chat.
    - Say: `Probing <subject>. One question at a time. Reply "end probe" to stop.`
- Keep secrets out of the file; record that a constraint exists, not its value.

### Probe file

Use this template. Replace each placeholder with real content or "None" as you go.
Leave the outcome empty until close; never leave template text in the final file.
Update the file before asking the next question.

```markdown
# Probe: <subject>

- Status: open
- Started: <YYYY-MM-DD>
- Goal: <decision or understanding the probe must settle>
- Subject: <plan, design, decision, or reference>

## Decisions

- **D1** — <settled decision>. <reason, when not obvious>

## Transcript

### Q1 — <title>

- **Question:** <question body, including the realistic choices>
- **Recommended:** <answer>
- **Answer:** <the user's answer, quoted or summarized>
- **Effect:** <what it settled, changed, or unblocked>

## Open branches

- <unsettled decision and what it blocks>

## Assumptions

- <assumption made without asking, and why it is safe>

## Outcome

- **Settled:** <one line per decision, or "none">
- **Unsettled:** <open branches, or "none">
- **Next:** <action and whether it is confirmed>
```

- Add a decision only after the user answers or delegates it.
- Keep each D entry to one line; the transcript holds the reasoning.
- Mark decisions the user delegated as assumptions, not as their choices.
- Keep the transcript faithful; summarize long answers without changing their meaning.
- Never record a question you did not ask or an answer the user did not give.
- When a settled decision changes, revise its D entry and note the change in the transcript.
    - Do not create a duplicate decision for the same branch.

## Ask one question

- Choose the unblocked question whose answer changes the most later questions.
    - A question that depends on an open question waits.
    - Prefer scope, architecture, safety, and cost over naming and formatting.
    - Skip facts, preferences, and details that do not change the outcome.
- Check the file before asking; do not re-ask a settled decision.
- Ask exactly one question per turn.
- Do not hide sub-questions inside one question.
- Format it like this:

```markdown
**Q2 — <title>**
<question body, including the realistic choices>

**Recommended:** <answer>. <one-line reason>.
```

Example:

```markdown
**Q1 — Where does the probe stop?**
Should the probe settle the storage choice only, or also the migration path?

**Recommended:** Storage only. The migration can be probed separately once the store is fixed.
```

- Phrase the question as a decision the user can accept or reject.
    - Fact question: "What breaks without the cache?"
    - Decision question: "Should we add the cache before a measured symptom exists?"
- Word the question so replying `yes` accepts the recommendation.
- Give a recommendation even when the user may disagree; a concrete default is easier to correct.
    - If you have no defensible default, say what is missing and ask for it.
- Record the question in the transcript when you ask it.
- Wait for the answer; do not add a second question to the same turn.

### Handle the answer

- Record the answer, then update decisions, assumptions, and open branches.
- Recompute the next question from the updated tree; do not follow a pre-written script.
- If the user replies `yes`, record the recommendation as the answer.
- If the user says `no` without naming an alternative, ask one clarifying question before moving on.
- If an answer is too vague to settle the branch, ask one clarifying question; do not record a guess.
- Record the user's choice even when you disagree; state the risk once, then move on.
- Do not praise or grade answers; record them and continue.
- Do not recap the whole probe after each answer; the file holds it.
- If the answer is `I don't know` or `you decide`:
    - Take the recommendation and mark it as an assumption, or
    - mark the branch open and move to an independent one, or
    - resolve it with a fact-finding step when the answer is discoverable.
    - Never stall the probe on a question the user cannot answer.
    - Do not re-ask a declined question in different words.
- If the user answers several questions at once, record them all and continue from the updated tree.
- If the user asks you something mid-probe, answer it first, then resume with one probe question.
- If the user replies `end probe` or clearly asks to end the probe, treat it as a command, not an answer.
    - Close immediately; mark the current question as unanswered.
    - If the same message also answers it, record the answer before closing.

### Facts versus decisions

- A probe question is a decision the user owns: scope, intent, constraints, trade-offs.
- A fact is something you can look up: file contents, current behavior, measurements, documentation.
- Find facts before asking.
    - Read the file, search the repo, check the documentation, or dispatch a subagent.
    - Ask the user only for context that exists only in their head or outside the workspace.
- If a fact is unavailable, ask for that one fact and record it as context.
    - Then ask the decision it informs; do not turn the probe into a fact questionnaire.
- Do not ask the user to confirm a fact you can verify.
- If a lookup is slow, say what you are checking and ask an independent question while it runs.
    - Fold the fact in when it lands.

## Close the probe

- Close when the user ends the probe, the goal is settled, or the next question would not change the outcome.
- If the user signals impatience or the probe has run long, offer to close with the decisions so far.
- Update the file first:
    - Set `Status: ended` and add `Ended: <YYYY-MM-DD>`.
    - Fill the outcome; move anything unresolved to open branches.
    - Record `Confirmed: <YYYY-MM-DD>` only after the user confirms the summary.
- Then give a compact summary in chat:

```markdown
## Probe closed — <subject>

- **Settled:**
    - <decision, or "none">
- **Assumptions:** <assumptions that could change the plan, or "none">
- **Open:** <unsettled branches and what they risk, or "none">
- **Next:** <the action you propose>

Confirm this matches your understanding before I proceed.
```

- Keep the chat summary to what changes the next action; the file holds the full record.
- Confirm once at the end, not after every answer.
- Do not implement, write the plan, or change code before the user confirms the summary.
    - A probe is a thinking tool, not an execution trigger.
    - If the original request already authorized action after the probe, still ask once for confirmation.
- If the user ended early, name what is still unknown and how it could change the result.
    - Do not fill gaps with guesses; list them as open branches.
- After confirmation, act on the settled decisions and leave the file as the record.

## Resume a probe

- Read the probe file before asking anything.
- Continue from the first unresolved branch; do not re-ask settled questions.
- If a new answer contradicts a settled decision, record the change and revisit only its dependents.
- If the user names a probe, use that file.
- If the probe is ended and the user wants to continue, reopen the same file.
    - Set `Status: open`, remove `Ended` and `Confirmed`, and clear the old outcome.
    - The transcript keeps the history.
- Do not create a second file for the same probe.
- If no probe is open, say so instead of inventing one.

## What to probe

Use these branches to find high-value questions, not as a checklist.
Ask one only when its answer can change the outcome.

- **Outcome:** What observable result makes this a success?
- **Scope:** What is explicitly out of scope?
- **Constraints:** Which limits are real: time, compatibility, security, cost, operations?
- **Failure and blast radius:** What would make it wrong or unsafe, and who or what does it hit?
- **Alternatives:** What is the next-best option, and what would make it win?
- **Reversibility:** What is the cost of being wrong, and how would we undo it?
- **Evidence:** How will we know it worked?
- **Disconfirmation:** What evidence would change your mind?

## Why

- One question at a time lets each answer refine the next question; a batch round cannot.
- A per-probe file survives context loss, makes the interview auditable, and lets the user resume.
- A recommendation keeps the probe moving and gives the user something concrete to accept or correct.
- Asking only outcome-changing questions respects the user's time and prevents interrogation drift.
- `end probe` keeps the user in control; the summary makes the cost of stopping visible.
