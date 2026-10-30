# R19 methods draft — revision 2

Status: revised following independent review; independent re-review pending. Original draft SHA-256 `6a2a22297fe8296293e0de318468fa22fd2cc1e05048bd64afd30c46246cc985` remains unchanged. Four targeted corrections:

1. Add all protocol eligibility conditions: at least five remaining environment actions at the original prefix, verified exact replay, one executed recovery action, and its nonterminal resulting state. Explicitly identify the resulting cohort as post-intervention conditioned. These rules are in frozen `/home/lizening/wt-r19-recovery-duration-v1/R19_PROTOCOL.md` SHA-256 `7668d7fa5422ad6ad7d3affc72b2e573ec19aae53314198fc14b46dc74c9a3d9`, section Population and Sampling. Note the five-action threshold is evaluated **before** the first recovery action, not after it.
2. State five K conditions and four prespecified K2–K5 versus K1 contrasts. The machine-readable frozen protocol `r19_recovery_duration_v1.json` SHA-256 `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122` lists the four comparisons.
3. Characterize the 29 diagnostic cases as unsupported or ambiguous and coverage-only; do not claim every one lacks a mapping. Actual G4 summary `/home/lizening/research-notes/agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923/future_g4_report/summary.json` SHA-256 `6ff56b7e9bc31c29bc9afd0c3ceea43c4fdf53b2addb29d3ce9f2c5e99b5d3c4` reports `unsupported_or_ambiguous_count=29` and `coverage_only_count=29`.
4. Specify that the task actor resumes only when the resulting state is nonterminal; a terminal state ends the episode. Frozen protocol `R19_PROTOCOL.md` sections 25 and 33–35 describe the terminal and handoff behavior.

No values, original evidence, scientific code, provenance index or runtime were modified; no model, CUDA, ALFWorld or formal analyzer was called. Source for the remaining numeric claims is the previous draft's separate `EVIDENCE_MAP.md` and its hash-bound aggregate recount.
