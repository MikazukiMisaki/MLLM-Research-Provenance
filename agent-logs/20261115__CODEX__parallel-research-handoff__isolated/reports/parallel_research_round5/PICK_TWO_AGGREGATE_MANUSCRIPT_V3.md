# From the first placement to the second: selected opportunities, action presentation, and immediate outcomes

**V3 current-code clarification.** V3 retains V2 and adds a partial description of a currently visible opportunity-selection function; its historic execution binding and helper semantics are unverified. A [limited independent text review](PICK_TWO_AGGREGATE_MANUSCRIPT_V3_INSERTION_INDEPENDENT_TEXT_REVIEW_V1.md) checked the insertion against static notes, not the historic run or data. No numerical research values were recomputed.

**Aggregate-based working draft, V2 background, for restricted local review.** V2 preserved V1, added a related-work discussion and implemented wording changes recommended in the [limited V1 text review](PICK_TWO_AGGREGATE_MANUSCRIPT_V1_INDEPENDENT_TEXT_REVIEW_V1.md); a [limited V2 check](PICK_TWO_AGGREGATE_MANUSCRIPT_V2_INSERTION_INDEPENDENT_TEXT_REVIEW_V1.md) compares the changes with existing reviews but does not verify the underlying data or original papers. This is an exploratory account of previously exposed development results, not a held-out evaluation or a preregistered confirmation. All numerical statements below are transcribed from the named reports; this drafting exercise did not independently check the original tasks, states, executions, parsing, or replay records. The identity of the original four-condition protocol and any further applicable conditions remain unconfirmed; a default-path candidate has not been opened or authenticated. This draft does not incorporate or resolve the paused task-weighting analysis, and is not authorization to distribute the draft or its sources.

## Abstract

Tasks involving two objects offer a useful setting for separating whether an opportunity was recorded, which action was selected, and what followed an action. In 30 previously consumed development trajectories, the source reports a first-object opportunity in 29 tasks and a second-object exact-destination opportunity in ten. All 29 recorded first placements were immediate. At the ten selected second-opportunity states, the historical next action was `look`; three trajectories subsequently completed the anchored placement within recorded follow-up, and seven were censored at the recorded end. A reported reset, single-step comparison at those selected states recorded immediate task completion after fixed exact placement in 10/10 and after `look` in 0/10. Separately, a fixed four-condition presentation study reports different choice marginals when action rows and identifiers are varied. The observations concern selected development states and distinct observation windows. They do not establish that `look` precludes later completion, that an interface change improves final success, or a general explanation for the first–second distinction. [S1, S2, S3]

## 1. Research questions

The practical question is why recorded behavior places a first object immediately yet does not immediately select the second object's exact placement in a set of identified opportunities. This formulation does not assume that the two roles were randomly assigned or that an unobserved opportunity was impossible. We ask:

1. Under the previously reported opportunity predicates and observation windows, what first- and second-object opportunities and subsequent actions were recorded?
2. At selected second-opportunity states, how do reported immediate outcomes under two fixed next actions differ from what the historical trajectories later recorded?
3. In a separate fixed presentation study, how do reported exact-placement choices vary with row order and action identifiers, and what can marginal counts establish about within-state choice changes?

These are complementary descriptive questions. They do not form a single causal chain or a population estimate. The role comparison, historical follow-up, reset comparison, and four-condition choice study have different selection and measurement conditions. [S1, S2, S3, S4]

## 2. Materials and measurement

### 2.1 Historical opportunities and follow-up

The historical material consists of 30 previously consumed two-object development trajectories. According to the aggregate account, the reported rules identified first-object opportunities in 29 tasks and second-object exact-destination opportunities in ten. The recorded windows and reported predicates define what was detected: failure to observe an opportunity is not evidence that it could not occur. First- and second-object roles refer to different selected states, and the aggregate reports do not establish random role assignment or independent panels. [S1, S2]

For the selected second-opportunity states, the next historical action and the subsequent recorded follow-up are distinct observations. The follow-up ends at the recorded end; trajectories censored there cannot be treated as demonstrated permanent failures. Separately, the aggregate account describes a reset-and-replay single-step comparison at those selected states. It compares a fixed exact-placement action with `look` on the **immediate** recorded outcome. It is not a full-trajectory comparison of alternative policies, and this description does not claim that an external independent team reproduced the reset. The predicates, identities, reset and replay execution, and completeness of the underlying records have not been independently checked for this draft. [S1, S2]

### 2.1.1 Current-code candidate and historical-method gap

A [limited static inspection](PICK_TWO_OPPORTUNITY_METHOD_STATIC_ACCESS_RECORD_V1.md) of the currently visible `select_first_opportunity` function and an [independent source check](PICK_TWO_OPPORTUNITY_STATIC_METHOD_INDEPENDENT_REVIEW_V1.md) describe part of a candidate selection rule. The function scans recorded public decisions in order, processes the current observation before testing, and returns on the first matching opportunity before applying that decision's subsequent operation update. Among the visible checks, it requires an existing first-placed instance with supported current placement, a different instance in both the maintained `held` and `taken` records, and a matching legal move to the same concrete destination; matching commands are sorted and the first is selected. The evidence state is not an independently verified physical state: for example, an absent location entry alone does not clear `held`. Missing or malformed action information is treated separately rather than automatically proving that an opportunity was absent.

These are partial facts about the **current code**, not a certified definition of the historical panel. Observation-wrapper and operation-confirmation semantics, inputs, task eligibility, and the exact executed historical bytes were not verified. The initial static inspection returned development-seed constants before stopping, and the independent review returned additional source lines beyond its assigned function; both access records describe their limits. Neither check opened task contents or establishes whether an unobserved opportunity was impossible. Existing access restrictions and stop rules remain unchanged; neither inspection authorizes further source or input access.

### 2.2 Four-condition action-presentation study

A separate report describes 20 opportunity states from ten previously consumed tasks: ten first-object and ten second-object states. Within each role it reports the same states across the four conditions below. The action-label vocabulary and commands were unchanged, row reversal and ID–command assignment were independently reconstructed, and each condition used its own numeric ID map for decoding, according to the report. Neither the states nor the one fixed SHA label permutation were selected using this batch's responses; the question itself was informed by previous outcomes. The source's use of the word “public” does not itself authorize distribution or establish protected-task exclusion. [S4]

| Condition | Row order | ID assignment |
|---|---|---|
| C1 | Original | Original |
| C2 | Original | Fixed hash-permuted |
| C3 | Reversed | Original |
| C4 | Reversed | Fixed hash-permuted |

The report classifies outputs as exact placement, `look`, other valid, or invalid, and uses ten as the denominator per role and condition, retaining invalid outputs in that denominator. It reports reproduction of 40/40 old-condition ID/command choices and raw-text matches, and an independent CPU reader's authentication and reparse of 80 recorded calls; these are historical source claims, not a fresh verification by this draft. [S4]

The factorial panel should not be assumed to be identical to the historical or reset comparison panel merely because the role labels are related. Its fixed permutation and selected states do not establish effects over arbitrary permutations or environments. Although conditions are structured as a row-order by ID-assignment diagnostic, the presented aggregate counts alone do not establish a general context-independent position or identifier mechanism. [S1, S3, S4]

## 3. Results

### 3.1 Recorded opportunities and two follow-up windows

All 29 recorded first placements were immediate. At the ten selected second-opportunity states, the historical next action was `look`. Within historical recorded follow-up, three trajectories later completed the anchored placement and seven were censored at the recorded end. In the separate reported reset single-step comparison at those selected states, immediate task completion was 10/10 following fixed exact placement and 0/10 following `look`. [S1, S2]

These statements answer different questions. A selected command is not itself evidence that it was executed successfully; immediate completion after a forced next action is not a full-trajectory outcome under a policy. The 0/10 immediate result after `look` does not show that a subsequent completion could never occur; three historical trajectories were reported to complete the anchored placement later. Nor do the seven censored trajectories establish that later completion was impossible. The results do not estimate how often second-object opportunities occur outside the recorded panel. [S1, S2]

### 3.2 Reported presentation-condition marginals

The following table transcribes the source's four category counts. Each row refers to ten states in the named role; the conditions reuse states within role. [S4]

| Role | Condition | Exact placement | `look` | Other valid | Invalid |
|---|---|---:|---:|---:|---:|
| First object | C1 | 10 | 0 | 0 | 0 |
| First object | C2 | 10 | 0 | 0 | 0 |
| First object | C3 | 1 | 0 | 9 | 0 |
| First object | C4 | 7 | 0 | 3 | 0 |
| Second object | C1 | 0 | 10 | 0 | 0 |
| Second object | C2 | 0 | 10 | 0 | 0 |
| Second object | C3 | 1 | 8 | 1 | 0 |
| Second object | C4 | 0 | 10 | 0 | 0 |

These are selection categories, not executed outcomes. In particular, `look` and other-valid choices are different categories: a binary indicator for exact placement combines them as non-exact-placement and does not reveal whether the underlying non-placement command stayed the same. The categories do not identify the full commands within other-valid or validate parsing, state matching, execution, or later success. [S1, S4]

### 3.3 What the published marginals permit about within-state changes

A subsequent post-result CPU analysis used the eight reported exact-placement marginals, not individual task identities or state-level choices. It defines a change as a difference between two conditions in a state's binary label for selection of that role's exact-placement command. Assuming the source correctly reports the same ten states within each role and correctly parsed labels, the first-object C1–C3 marginal pair implies exactly nine such changes; C3–C4 permits either six or eight. These are the feasible values reported by the analysis, not a reconstruction of the missing state-level joint record. The source explicitly notes that feasible endpoints for different pairs need not all be simultaneously attainable in one four-condition joint table. [S3]

The bounds do not count changes among non-placement commands and do not establish action execution, understanding, long-term success, or a mechanism. The selected role panels should not be treated as randomized role assignments or independent samples without additional design evidence; the condition pairs reuse states. This is a consequence of already exposed marginals, not a new observation or a held-out test. [S1, S3]

## 4. Interpretation and limits

The historical results are consistent with a gap between a recorded second opportunity and immediate selection of its exact-placement command in this selected panel. The reset comparison addresses immediate outcomes of two specified actions at selected states. The presentation study addresses output choices under four specified displays. They should be read side by side, not joined into a per-task causal explanation. In particular, neither the first-versus-second role difference nor the display-associated choice marginals establish why the model behaved as recorded or what would happen under a new distribution of tasks. [S1–S4]

The historical opportunity rules, selection and observation windows, underlying state identities, parsers, action executions, and immediate outcome measurements require primary-record verification. Source reports are not an independent audit of these records. Different model calls, repeated conditions and selected states may share dependencies, and no independent-population generalization is warranted from the displayed counts. The task-weighted analysis remains paused after its recorded resource-control deviation; this draft does not treat it as reproduced, completed, or supporting evidence. [S1, S3, S4]

## 5. Related work

[Li et al. (2026)](https://arxiv.org/abs/2610.18579v1) pair factual probes with action choices on frozen decision states and include probes for the number of objects already placed in two-object tasks. [Zhu et al. (2026)](https://arxiv.org/abs/2609.40111v2) compare proposed corrections with original-action retries from matched checkpoints where replay is supported. Neither two-object state probes nor matched action replay was introduced by this study. Our narrow descriptive focus is a previously exposed selected opportunity panel, the reported immediate consequences of two fixed actions, and a separate presentation diagnostic. The studies differ in selection, measurement and outcome windows; prior results do not validate our historical records or support a shared mechanism. These descriptions are based on the [limited primary-source review](RECOVERY_RELATED_WORK_TWO_PAPER_SOURCE_CHECK_V1.md); their implementations and data were not audited here.

[Koul et al. (2026)](https://aclanthology.org/2026.findings-acl.1743/) also study identifier representation and item ordering in database and tool selection. Their tasks and measurements differ from the reported four-condition action-choice diagnostic, and their work is not an independent replication of these results; see the [source-specific note](ACTION_INTERFACE_NEARBY_2026_PRIMARY_LITERATURE_V1.md). This positioning does not claim a comprehensive literature search.

## 6. Reproducibility and audit scope

The summary-only bounds report describes a producer and an independently authored checking program, both with recorded exit code zero, and a checker that reports 12 rows and synthetic binary-mask checks. The original execution's exit codes were subsequently transcribed by the coordinator rather than saved as independent witnessed receipts; resource figures were worker self-reports. The later same-machine fresh-directory run is reported to match reference result lines, with coordinator-transcribed exit statuses and worker self-reported resources. That local repeat checks the supplied scripts and conditional aggregate computation in that setting; it does not validate the input marginals, original state identities or model execution, establish repeatability across platforms, or constitute third-party or external-machine reproduction. Costs not independently measured remain unknown. [S1, S3]

The original four-condition protocol has not been confirmed. A default-path candidate has been identified but not opened or authenticated; its identity and any further applicable conditions remain unresolved. This does not assert that a preregistration existed, nor that no additional conditions exist. No automatic retry of the previously exhausted full-model rerun is implied by this draft. [S3]

## Sources

- **S1:** [Cross-direction quantitative evidence supplement V6](CROSS_DIRECTION_QUANTITATIVE_EVIDENCE_SUPPLEMENT_V6.md), first/second opportunity section and reproducibility notes.
- **S2:** [Direction 2 observation-window replacement](DIRECTION_2_OBSERVATION_WINDOW_REPLACEMENT_V1.md), proposed replacement text.
- **S3:** [Four-condition exact-placement choice bounds](PICK_TWO_CHOICE_CHANGE_SHARP_BOUNDS_RESULTS_V1.md), reported feasible values, execution record and limitations.
- **S4:** [Fixed row-order × ID-assignment diagnostic](../pick_two_display_factorial_round4/RESULTS.md), lines 1–18 only.

## Drafting access record

The V1 author wrote the draft from the four named sources above; S4 access was limited to lines 1–18. The complete S1, S2 and S3 texts were displayed, including their cross-direction or resource-limit context. The branch name was checked. No other manuscript text, original tasks, cases, raw states, JSON, protected archive, or paused three-category manual-inference record was consulted during V1 drafting. No research values were calculated, model or environment run, or source data validated during drafting. V2 additionally incorporates the limited V1 text review and named literature notes and source links; V3 references the separately recorded current-code inspection and independent check. This access record concerns these drafting actions, not previous authors or reviews; neither the V1 review nor subsequent changes certify underlying source data or execution.
