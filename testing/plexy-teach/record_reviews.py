#!/usr/bin/env python3
"""Materialize the parent's explicit, non-blinded inspection decisions for the two repeat rounds."""

import argparse
import json

from grade_runs import CONFIGS, EVAL_DIR, ROOT, RUNS, grade

REVIEWS = {
    3: {
        "with_skill": {
            1: [
                (True, "Lines 79–96 trace A waiting at 2, B returning 7, A adding 7 then 1, and A returning 10; the local totals are explicitly separate."),
                (True, "The worked input [2, [3, 4], 1] has four integer leaves and one child call; lines 60–70 need only a loop and list type check."),
                (True, "Lines 63–72 display the full function with return after the loop; lines 101–103 explain [] returning 0. Line 145 limits inputs to finite cycle-free integer lists and warns about recursion depth. The function passes nine executable checks."),
                (True, "Lines 107–137 require covering the code, recalling the rule, and tracing [4, [1, [2]], [], 3]; feedback tracks 2 → 3 → 10 returns and identifies wrong return destinations, resets, and premature stopping."),
                (True, "All practice, next-use guidance, and later recall stay with integers and nested lists. Cycles and extreme depth are limits, not additional exercises."),
                (True, "The header budgets 1/4/4/1 minutes across idea, example, practice, and takeaway. The four main sections use one small worked input, two core tasks, and no required anecdotes or application setup."),
                (True, "Lines 96–99 explain that returning alone does not update the parent and a bare call yields only 3; practice asks for each caller's before/after subtotal rather than a definition of recursion."),
            ],
            2: [
                (True, "Lines 77–86 show the parent holding 2, the child computing and returning 7, and the pending += using that value to produce 9."),
                (True, "The worked [2, [3, 4]] has three integer leaves and one child; no framework, filesystem, parser, or setup is introduced."),
                (True, "Lines 65–74 give the full loop and recursive accumulation. Lines 87–89 explain empty and flat stopping cases and return indentation; lines 64 and 137 state finite cycle-free integer-list scope and depth limits. Nine executable checks pass."),
                (True, "Lines 106–127 require recalling the mechanism, tracing [1, [2, 3], 4], explaining continuation to 4, and checking an empty child; feedback shows child 5, parent 6 then 10, not just the final answer."),
                (True, "Transfer and later recall only alter integers, empty lists, and nesting. Other types and extreme depth are identified as outside the example."),
                (True, "The header allocates 1/4/2/2/1 minutes to five focused sections. One two-call trace, a missing-addition diagnosis, and short changed-input practice need no unrelated content."),
                (True, "Lines 93–102 distinguish a child calculating 7 from the parent discarding it and returning 2. The learner must explain both separate local results and the parent's addition."),
            ],
            3: [
                (True, "Lines 75–87 explicitly trace parent 2, child 7, return to parent, and 2 + 7 = 9; the parent changes its own result with +=."),
                (True, "The sole worked input [2, [3, 4]] uses three leaves and one child. The example stays entirely in Python number-and-list operations."),
                (True, "Lines 60–68 show the complete aggregation function; lines 89–91 explain zero-iteration [] and finite descent. Line 136 states type and recursion-depth limitations. All nine executable inputs pass."),
                (True, "Lines 95–118 instruct covering the function, retrieving the rule, and tracing [1, [2, []], 3]; feedback gives return order 0 → 2 → 6, parent totals, and explanations for losing the final 3 or double-counting."),
                (True, "All changed inputs, error diagnosis, immediate practice, and delayed recall stay within numbers, empty lists, and nested lists."),
                (True, "Four sections are budgeted 2/3/4/1 minutes. The two-call explanation and three short practice tasks are focused, with no compulsory history, curiosity anchors, or nine-part template."),
                (True, "The learner has to explain immediate return destinations, separate local totals, loop continuation, and the lost-result bug; lines 125–129 distinguish running a child from adding its answer."),
            ],
        },
        "without_skill": {
            1: [
                (True, "Trace table lines 108–117 shows C returning 4 to B, B adding 3 + 4 and returning 7 to A, then A adding 2 + 7 and continuing to 5 for 14."),
                (True, "The worked [2, [3, [4]], 5] has four leaves and two nested child calls, still a small list-only example without external machinery."),
                (True, "Lines 70–87 expose the recursive accumulation, return after the loop, empty-list zero, and finite non-circular scope. Line 58 excludes other containers and extreme depth. Nine executable checks pass."),
                (True, "Practice [1, [2, []], 3] asks for four intermediate checkpoints; lines 160–175 require filling the function without looking back and tracing [4, [1, [2]], 3], with an explanation of counting each leaf once."),
                (True, "Fresh traces, empty-child checks, missing-addition and early-return diagnoses all use the same number-and-list model."),
                (True, "Five sections have a 0–10-minute route, one compact trace table, and short prediction/reconstruction tasks. No compulsory unrelated stories or setup. This is a fuller exercise set, but the core remains plausibly ten minutes."),
                (True, "Lines 121–127 explain the immediate caller, and lines 178–192 test discarded returns, early return, and independent empty children; correct totals alone are not the lesson's entire substance."),
            ],
            2: [
                (True, "Trace rows 117–125 show C returning 4 to B, B adding to 3 and returning 7 to A, and A adding to 2 then continuing to 1 for 10."),
                (True, "The worked [2, [3, [4]], 1] uses four leaves and two child calls. The introductory flat loop is expressly limited to flat lists, not presented as the nested solution."),
                (True, "Lines 80–100 show the complete recursive function, return placement, [] returning 0, and finite number/list non-circular scope. Lines 65–73 correctly explain the flat intro's TypeError on nested lists. The recursive function passes nine executable inputs."),
                (True, "Changed inputs [4, [1, 2], 3] and [-2, [5, [], [1]], 3] require child and parent returns; lines 179–183 explicitly retrieve an explanation of the pause/add/resume mechanism, with corrective feedback."),
                (True, "Practice and repair only use numeric leaves, nesting, empty children, and the same function. Optional scratch textareas introduce no new programming model."),
                (True, "Five sections run 0–1, 1–3, 3–6, 6–8, and 8–10 minutes. The flat-loop bridge is brief, and the core includes no application setup, history, or mandated teaching template."),
                (True, "Lines 170–183 ask why a bare call yields only 3, repair the missing +=, and reconstruct the caller's mechanism in words rather than restating a self-call definition."),
            ],
            3: [
                (True, "Trace rows 119–125 show C returning 4, B adding it to 3 then adding 1 and returning 8, and A adding 8 to 2 then 5 to return 15."),
                (True, "The worked [2, [3, [4], 1], 5] has five leaves and two child calls. No external setup or unfamiliar application is needed."),
                (True, "Lines 79–103 show the two-line child assignment/addition, final return, empty-list zero, and finite non-self-containing input scope. Line 204 adds the depth limit. The complete recursive function passes nine executable inputs; the ??? block is an explicitly unfinished exercise."),
                (True, "Lines 143–163 ask for fresh returns from [1, [2, [3]], []] and [[[-2]], 5], then lines 192–196 retrieve the mechanism without looking back. Feedback distinguishes adding zero from replacing a parent's total."),
                (True, "Fresh inputs, code reconstruction, and early-return diagnosis remain within numeric nested lists. The optional notes box is explicitly not a Python runner or saved state."),
                (True, "Five main sections allocate 0–1, 1–3, 3–6, 6–8, and 8–10 minutes. The worked example and practice stay focused; no compulsory anecdotes, frameworks, or nine-section scaffold."),
                (True, "The learner explains paused local state, immediate return destinations, continuation after child return, and why a repeated whole-input call fails to progress; it is not only a recursion definition."),
            ],
        },
    },
    4: {
        "with_skill": {
            1: [
                (True, "Lines 75–88 show parent total 2, child return 7 assigned to child_total, and the parent's next addition producing 9; returning alone is explicitly not an update to parent state."),
                (True, "The worked [2, [3, 4]] has three integer leaves and one child, and the two-line return/use form adds no external machinery."),
                (True, "Lines 61–71 display the complete recursive function and return after the loop. Lines 90–92 explain empty and flat stopping behavior; lines 48 and 139 state finite integer-list/no-cycle and depth limitations. Nine executable inputs pass."),
                (True, "Practice covers the trace, recalls the parent's action, and requires a fresh chain for [2, [5, [1]], 3]. Feedback identifies returns 1 then 6, outer totals 2 → 8 → 11, and the immediate receiver of each return."),
                (True, "The lost-answer diagnosis, empty-child boundary, learner-created input, and later recall all stay with integer leaves and lists."),
                (True, "Four sections budget 1/4/3/2 minutes for idea, trace, two core practice tasks, and takeaway/boundary. No compulsory history or unrelated examples are added."),
                (True, "Lines 115–127 require distinguishing a child failing to run from its result being discarded and repairing the branch; practice makes the return-to-addition connection observable."),
            ],
            2: [
                (True, "Table rows 89–95 show the parent keeping 2 while the child accumulates 7, then the parent receiving and adding 7 to return 9. Lines 99–101 name the exact pending +=."),
                (True, "Worked [2, [3, 4]] uses three integer leaves and one child. Only an explained list type check is needed beyond the learner's loops and returns."),
                (True, "Lines 68–76 show the complete aggregation and final return; lines 102–104 explain [] zero and finite descent. Lines 67 and 151 define finite non-circular integer lists, modest depth, and no general validation. Nine executable inputs pass."),
                (True, "Lines 109–130 ask to cover the code, explain the addition, and trace [1, [2, []], 3] with separate caller totals; feedback details empty 0, child 2, and parent 1 → 3 → 6 plus loop continuation."),
                (True, "Transfer, missing-addition repair, immediate practice, and next-day recall only use integers and nested lists. Cycles/depth remain stated limitations."),
                (True, "The header budgets 2/4/3/1 minutes across four main sections, with one two-call worked trace and three focused tasks. There is no obligatory historical or application scaffolding."),
                (True, "Lines 139–145 require diagnosing a discarded 7, repairing +=, and finding the first divergence in each call's subtotal; the lesson directly tests how the total is built."),
            ],
            3: [
                (True, "Rows 87–92 explicitly show the child returning 7 to a parent waiting at 2, the resumed statement behaving as subtotal += 7, and the parent returning 9."),
                (True, "The worked [2, [3, 4]] has three integer leaves and one child; no filesystem, parsing, object hierarchy, or framework appears."),
                (True, "Lines 71–78 display complete aggregation with the final return. Lines 98–100 explain integer and empty-list stopping cases; lines 65 and 141 state finite non-self-containing inputs and recursion-depth limitations. Nine executable inputs pass."),
                (True, "Lines 105–121 require memory retrieval and tracing [1, [2, [3]], []] with returns 3, 5, 0, and 6; feedback checks the outer subtotal before/after the empty child and warns against simply flattening mentally."),
                (True, "The deeper trace, discarded-result diagnosis, and delayed [4, [1, []]] recall all stay in the taught integer/list model."),
                (True, "Four core sections follow a six-minute explanation, three-minute practice, one-minute retrieval route. The optional later-review reveal adds no compulsory unrelated content."),
                (True, "Lines 130–134 distinguish computation from collection and explain that replacing a subtotal would lose earlier numbers; return chains, not reading or final numbers, are proposed as evidence of understanding."),
            ],
        },
        "without_skill": {
            1: [
                (True, "Rows 107–115 show C returning 4 to B, B adding it to 3 then 1 and returning 8, and A adding to 2 then 5 to return 15."),
                (True, "The worked [2, [3, [4], 1], 5] has five leaves and two child calls. A brief flat-loop bridge and static work-card analogy do not require external setup."),
                (True, "Lines 67–88 show the full recursive aggregation, return outside the loop, [] returning 0, and finite numbers/lists without self-containment. No general-purpose arbitrary-input claim is made. Nine executable inputs pass."),
                (True, "Lines 129–144 require fresh returns for [1, [2, [3]], 4] and an empty-child check, explaining the final 4; lines 151–173 reconstruct code without looking and retrieve the pause/use/continue mechanism."),
                (True, "All transfer, code reconstruction, and early-return diagnosis remain numeric nested-list tasks; no dictionaries, performance work, or unfamiliar libraries are required."),
                (True, "Five sections budget 0–1, 1–3, 3–6, 6–8, and 8–10 minutes. The core is a small static trace and short exercises, without compulsory unrelated history or curiosity anchors."),
                (True, "Lines 119–124 require tracking simultaneous separate totals and the receiver of C's return. Changed-input feedback explains continuation and an exit explanation ties return values to the caller's update."),
            ],
            2: [
                (True, "Rows 130–135 show C returning 4 to B, B computing 3 + 4 and returning 7 to A, and A computing 2 + 7 then adding 5 to return 14."),
                (True, "Worked [2, [3, [4]], 5] uses four leaves and two nested child calls. The introductory flat function is a small prerequisite bridge and is expressly not the nested-list solution."),
                (True, "Lines 80–106 show full recursive accumulation, final return, [] zero, finite non-circular input scope, and recursion-depth limits. The recursive function passes nine executable inputs; selecting the earlier flat intro was a test-extractor error, not a lesson bug."),
                (True, "Practice [-1, [2, [], [3]], 4] asks for four call returns and shows 0, 3, 5, and 8 with additions. The learner recalls item versus items and gives an explanation plus a fresh exit prediction for [[], [6], -2]."),
                (True, "Negative leaves, empty children, branch reconstruction, and return-placement diagnosis stay in the same model. Type/cycle limits are scope notes, not extension projects."),
                (True, "Five sections span 0–1, 1–3, 3–6, 6–9, and 9–10 minutes. The flat bridge is brief, the trace has six rows, and practice has three short focused checks."),
                (True, "Lines 162–175 test progress into item instead of repeated items and why early return loses later inputs. Lines 185–196 require explaining the caller's pause, subtotal addition, and stopping behavior."),
            ],
            3: [
                (True, "Rows 121–128 show separate call subtotals, C returning 4 to B, B adding to 3 and returning 7, and A adding to 2 then continuing to 5 for 14; static frames reinforce the same state."),
                (True, "Worked [2, [3, [4]], 5] uses four leaves and two child calls. Call frames are explained as the separate workspaces already shown, not as additional tooling."),
                (True, "Lines 85–104 expose the complete function, final return, [] zero, finite integer/float nested-list scope, and cycle/depth exclusions. The 'at any depth' contract at line 84 is qualified by the explicit depth limitation at 104. Nine executable inputs pass."),
                (True, "Practice [1, [2, 3], [], 4] asks for the waiting total, child return, parent update, and empty-child behavior. Lines 175–205 retrieve the branch without looking and trace [[], [6, [-2, 1]], 3] with a -1 → 5 → 8 return chain."),
                (True, "All transfer remains numeric nested lists; frames/stack describe the taught calls, and other types are excluded rather than turned into new tasks."),
                (True, "Six main sections allocate 0–1, 1–3, 3–6, 6–8, 8–9, and 9–10 minutes. This is the fullest new lesson but its core is still one small trace, short predictions, branch retrieval, and a fresh numeric input; no mandatory history or nine-section scaffold."),
                (True, "Lines 184–193 distinguish discarding a return, replacing a subtotal, and accumulating correctly. The final check demands intermediate returns and reasons for stopping, not merely a self-call definition."),
            ],
        },
    },
}


def main(iteration_number):
    eval_dir = ROOT / f"iteration-{iteration_number}" / EVAL_DIR.name
    expectations = json.loads((eval_dir / "eval_metadata.json").read_text())["assertions"]
    frozen = json.loads((ROOT / "iteration-2" / EVAL_DIR.name / "eval_metadata.json").read_text())["assertions"]
    if expectations != frozen:
        raise ValueError("These recorded reviews apply only to the unchanged iteration 2 rubric.")
    pending = []
    for config in CONFIGS:
        for number in RUNS:
            run_dir = eval_dir / config / f"run-{number}"
            decisions = REVIEWS[iteration_number][config][number]
            if len(decisions) != len(expectations):
                raise ValueError("Every frozen expectation needs an explicit decision.")
            review = {"expectations": [
                {"text": text, "passed": passed, "evidence": evidence}
                for text, (passed, evidence) in zip(expectations, decisions)
            ]}
            grade((run_dir / "outputs/lesson.html").read_text(), expectations, review)
            path = run_dir / "content_review.json"
            if path.exists():
                raise RuntimeError(f"Refusing to overwrite an existing review: {path}")
            pending.append((path, review))
    for path, review in pending:
        path.write_text(json.dumps(review, indent=2) + "\n")
    print(f"Recorded six explicit content reviews for iteration {iteration_number}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iteration", type=int, choices=[3, 4], required=True)
    args = parser.parse_args()
    main(args.iteration)