# Final clarification addendum

This addendum clarifies two statements in the prior summary. The original frozen records are unchanged. No GPU, model, or environment checks were run for this clarification.

1. **Historical model/runtime evidence:** A96 did load the model under the shared-GPU accounting contract and completed all 96 source tasks; a real engineering preflight also previously exited 0. The earlier UUID probe failure and unresolved local-PID-to-GPU ownership mapping remain historical limitations, but should not be read as meaning every recent engineering action stopped before weight loading. Current GPU load and present-day future-run feasibility have not been rechecked; past success does not establish current readiness.

2. **Input-token arithmetic:** `18,939,904` is the conservative theoretical product of the candidate generation count and an assumed per-call ceiling of 8,192 input tokens. It is not a forecast of actual consumption or a claim that a future run necessarily needs more than 16 million tokens. The 16M figure belongs to the prior source protocol's hard cap; it is neither an automatically applicable cap nor an authorization for a future pilot. Any new experiment requires a separately reviewed and authorized budget.

This clarification does not change the conditional scenario arithmetic, select cases, authorize execution, or establish current runtime readiness.
