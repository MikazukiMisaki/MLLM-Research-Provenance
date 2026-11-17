# Independent descriptive trajectory recount

Scope: the original interrupted fixed-product run, four pre-used, related authored DEV tasks, not an accepted confirmatory comparison. No model, CUDA or environment was invoked. Raw logs and task material were not modified. The scripted output contains only anonymized aggregate information and SHA-256 digests of the raw worker/owner event files. It is not evidence of task independence or a population success-rate estimate.

| Case / arm | Recorded final win | Actions / returned generations | Input / output token IDs | Action types |
|---|---:|---:|---:|---|
| A / P0 | false | 50 / 50 | 13,175 / 250 | 25 look, 25 examine |
| A / candidate | false | 50 / 50 | 13,175 / 250 | 25 look, 25 examine |
| B / P0 | true | 9 / 9 | 2,936 / 45 | 2 look, 3 go, 2 take, 2 move |
| B / candidate | true | 11 / 11 | 3,546 / 55 | 4 look, 3 go, 2 take, 2 move |
| C / P0 | false | 50 / 50 | 18,021 / 250 | see aggregate |
| C / candidate | **UNKNOWN** | 28 / 29 | 10,370 / 145 | see aggregate |
| D / both | not run | — | — | — |

Output token counts include stop/EOS IDs when recorded; input counts are recorded full sequence length minus generated IDs, not character counts or separate prefill billing. Every listed arm has one returned reset, environment construction and initialization, model load and materialization. For C candidate, the owner journal has 29 step reservations but only 28 returned; the 29th is **unknown**, not zero. The 29th generation did return. C candidate lacks a final result and may not be counted as either success or failure. These records reproduce 199 returned generations, 198 returned steps and 61,223/995 input/output token IDs across all six started arms.

Case A: the 50 action strings match position-for-position; both alternate look/examine for the entire 50-step horizon. All 100 parser statuses are selected. This supports an observed repetitive behavior in one particular task, not a causal diagnosis or evidence of general policy behavior. Case B: both initial public records match; the first action divergence is step 3, where P0 goes and candidate looks. Both later win; candidate uses two additional generations/steps and 610 input and 10 output token IDs. A also has matching public initial records; these matches do not establish identical hidden state. Positional action equality after divergence is not a state-aligned behavioral comparison.

Both complete pairs agree on success, so the observed difference on these two is zero (one success and one failure for each arm). Their exposure, relatedness, selection, tiny sample, interrupted broader roster, earlier materialization budget deviation and unresolved prospective stop-token contract preclude a causal or generalization claim. We cannot infer that single-source training raises or lowers task success; case B cost difference is descriptive only. The candidate in C has no complete initial-public-result record, so this script makes no pairwise initial-state claim for C.

## Forward question

A testable hypothesis is that a *fixed offline* self-improvement training set containing verified positive demonstrations of progressing beyond repeated observation or non-progress states reduces repeated-action trajectories and improves final native task success relative to an otherwise matched fixed P0 or training control. These data identify a behavior worth testing; they do not establish the cause of the loop or validate the proposed intervention. A prospective comparison should lock the data provenance, product identities, exact prompt/parser/termination contract, task roster and order, both-arm resource budget, native win definition, missing-outcome handling and analyses before running. Match training compute and data quantity for a training-content control where feasible. The primary endpoint is complete-task native success on prespecified tasks; repetition frequency and generation/step cost are secondary. Previously used and related DEV cases remain exploratory; independent-task claims require independent tasks and appropriate power. Avoid post-hoc changes to the frozen baseline, runtime selector or recovery semantics.

Method: `python analyze.py > aggregate_v2.json`; no raw action strings or task descriptions are exported. Raw input digests and per-operation reservations/returns appear in that JSON. The two input sources of truth are worker `dev_decision_committed`/`generation_returned`/`fixed_product_arm_result` and supervisor `operation_reserved`/`operation_returned`. An earlier `aggregate.json` is a retained draft whose category `other` includes move; `aggregate_v2.json` is the final classification.

Files SHA-256: `analyze.py` `48c2347b6995856a02ff695a156c4ae563fe7d2a34d28f14c2f5251e7d941f74`; `aggregate_v2.json` `141f4526e37ea1d97e653fb9361c6719cec72dd8aa7b1e2e7ee573fa82ab0472`.
