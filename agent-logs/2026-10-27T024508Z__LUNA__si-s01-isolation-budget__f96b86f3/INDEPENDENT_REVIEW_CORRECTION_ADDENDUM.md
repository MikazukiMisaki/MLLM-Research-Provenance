# Independent-review correction addendum

Append-only clarification; prior frozen files remain unchanged. No new metadata, task payload, raw result, or project code was read for this note.

1. **Current runtime status:** `NOT_TESTED`. A96 did load the model and complete 96 source tasks under the explicitly adopted `SHARED_CONTAINER_CUDA_V1` accounting policy, with resource ownership recorded as `UNPROVEN_NOT_ASSERTED`. The older CUDA identity observation remains historical; by itself it neither negates A96 nor reinstates a strict PID-to-GPU proof requirement absent a newly adopted protocol. This note makes no claim about present GPU load or future runtime readiness.

2. **Recipe and token-budget scope:** The C24 limitation applies to the older fixed recipe; it does not by itself veto the candidate 17-failure / five-late-anchor mechanism design. The 18,939,904-token theoretical ceiling versus 16M arose only in the optional three-arm arithmetic scenario in `BUDGET_CANDIDATES.json`; it is not evidence that the current minimum candidate requires that amount or has a budget contradiction. The earlier 16M value is the prior source protocol's cap, not automatically a cap or authorization for a new design.

3. **Historical versus fresh comparison:** Lack of a fresh CONTINUE arm is not an automatic bar to a causal comparison. Historical P0 behavior may be reusable if a frozen comparability contract establishes the relevant initialization, state, public inputs, policy/model/runtime identity, and execution semantics. Matching public state alone is insufficient; a fresh CONTINUE call alone also does not prove hidden simulator/RNG equivalence. Whether historical evidence satisfies that contract remains to be established, and no arm is mandated by this note.

These corrections change no evidence, design selection, budget, execution status, or authorization.
