# SI-P3 v2 source-first candidate — paper budget and stop ledger

**Not executable; collection remains `NO_GO_NOW`.** This is a paper-only restatement of the reviewed v2 candidate. It creates no schedule, seed table, gate, argv, run identity, output directory, or clearance.

## Incremental acquisition budget (future-only, not authorized)

The adopted A96 identities and family quotas remain fixed at 35/26/16/9/10. At the maximum planned horizon of 50:

| Phase | Generations | Environment operations, including reset | Generated-token upper bound |
|---|---:|---:|---:|
| Source-only A96 | 4,800 | 4,896 = 4,800 actions + 96 resets | 76,800 = 4,800 × 16 |
| Remaining branch stage if reached | 4,416 = 192 teacher + 4,224 suffix | 4,896 = 480 prefix-replay actions + 96 teacher actions + 4,224 suffix actions + 96 replay resets | 72,960 = 96 × (40 + 16) + 4,224 × 16 |
| Full source-first ceiling | 9,216 | 9,792 | 149,760 |

Source-first means all 96 sources are durably complete before any branch/replay/teacher work. It does not mean “free screening”: source-only may consume 4,800 generations, 4,896 environment operations, and 76,800 output tokens. At every phase, actual early terminal/stop conditions can reduce use; none of the ceilings is a forecast of completion.

Additional proposed hard caps are at most 16,000,000 aggregate input tokens and at most 4 allocated GPU-device-hours. They are hard stops, not claims that the campaign fits. The paper arithmetic's per-call envelope is 75,497,472 input tokens across the full 9,216-call ceiling; that is a loose ceiling and is not compatible with promising completion under the stricter 16M aggregate cap. Actual prompt lengths, runtime, and GPU allocation are not observed for this future workload. A budget interruption is a technical/budget STOP, not a normal source failure or structural no-go.

For any future measurement, device-hours must be accumulated from monotonic per-device allocation intervals, summing elapsed seconds per uniquely identified allocated GPU UUID and dividing by 3,600. Wall time alone is not device-hours; multiplying wall time by an assumed device count is not evidence. A trusted UUID and process/host ownership mapping is currently absent, so the 4-device-hour cap is not yet auditable/enforceable in the present execution context.

## Source-only futility checks and stop semantics

After all 96 source units are normally complete and evidence is sealed, compute the frozen, conservative reachable set E from the actual after-action-5 snapshot, nonterminal/nontruncated state, complete nonempty ordered map, and valid source closure. Missing/contradictory evidence is `INTEGRITY/TECHNICAL STOP`, not exclusion from E and not a failure label. An incomplete source unit has `Y0=NA`.

Before any branch phase, the design can stop as `COMPLETE_SOURCE96_STRUCTURAL_NO_GO` only if an immutable necessary upper bound cannot meet every predeclared floor:

- E: at least 72 total, and family minima 22/17/10/6/7;
- E with source outcome Y0=0 (upper bound for C): at least 24 total, and family minima 9/6/4/2/3;
- E with Y0=1 (upper bound for neutral): at least 24 total, and family minima 9/6/4/2/3.

If this structural stop occurs, teacher outcomes remain `NA` with `TEACHER_NOT_RUN_SOURCE_FUTILITY`; this is not a completed paired acquisition or evidence that C is zero. If the bounds pass, the result is only `SOURCE_UPPER_BOUNDS_NOT_FUTILE`, not a GO. A future separately authorized branch stage would process all preassigned eligible E tasks, including source successes, once each; never only failures. No top-up, task replacement, added 384, redrawing, threshold relaxation, or automatic continuation is allowed.

## Cost categories that must remain separate

- **Historical science:** 5,142 model generations and 7,949 reset-inclusive environment operations. The earlier 177 generations / 342 operations are already included in those totals and must not be added again.
- **Prior engineering CUDA probe:** independently recorded allocated device-time was 0.0066242038 device-hours; the probe stopped at the CUDA identity guard before 8B/P0 weights, model generation, or environment operations. This is engineering cost, not an increment to the historical scientific totals and not proof of model memory/latency fit.
- **Pure identity diagnostic:** its recorded one-byte tensor observation was a separate consumed engineering diagnostic; it is not a model load or science run. No repeat is authorized.
- **Future A96 acquisition:** the ceilings above are hypothetical and have no execution release.
- **Future training:** unbudgeted and unauthorized. Historical S120/collator evidence is not training exposure.
- **Future evaluation:** the reserved 600 identities are task-disjoint TRAIN metadata, not held-out evidence. The coordinator's planning note estimates up to 90,000 generations for a later A/B/C evaluation; that work is not funded or authorized here. No evaluation budget should be silently charged to the 4-device-hour engineering/acquisition cap.

## Readiness and scientific interpretation

Current trusted-host/PID mapping is blocked: the only recorded SSH attempt to `sdxsrv03` returned 255 with publickey/password authentication failure; no remote host, source, GPU table, or PID namespace was observed. Locally `/proc/1/ns/pid` was permission-denied and a trusted host PID mapping was not established. Do not retry SSH, relax the foreign-process guard, or infer ownership from a process count. A future route would need to be an already authorized host-native session or independently trusted host/container PID+UID+start-time mapping visible alongside NVML; none is presently evidenced as usable.

Even if the recipe is later constructible, C−A is the complete S120+new-C training package, while C−B is a matched-pool/adoption contrast, not an isolated proof that failure awareness causes improvement. Fixed d=5 first-action distillation is not adaptive stopping. Recipe constructibility and learning efficacy are separate decisions. Present status: no trusted execution route, no new collection, no training/evaluation authority.

