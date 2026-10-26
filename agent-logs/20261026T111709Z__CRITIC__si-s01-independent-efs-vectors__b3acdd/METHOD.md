# Independent SI-S01 source upper-bound acceptance vectors

This package is synthetic design material, not a software PASS or a scientific execution release. Only the adopted protocol was read. No project module, runtime, tokenizer, model, environment, CUDA, network or test runner was invoked.

The builder uses literal N=[35,26,16,9,10], E floors=[22,17,10,6,7], F/S floors=[9,6,4,2,3] and totals72/24/24. Each case has hand-specified E/F/S arrays and expected status. Its stdlib checks only establish internal arithmetic and constructibility, not production correctness.

For each family, character j in slot_modes_by_family_local_index gives the mode of zero-based family-local slot j in a later synthetic Plan. There are exactly96 slots per case. The adapter may supply fake canonical identities, but must not select real A96 identities or read new task bodies.

Modes:
- N: normal success at action1; no S5.
- S: first five actions are nonterminal, with a nonempty action map at S5; seal S5 before generation6; action6 succeeds and terminates. Terminating at action5 would be ineligible and is intentionally forbidden.
- F: first five actions produce a valid S5; seal it before generation6; the sixth generation is rejected by the real frozen P0 parser and executes no action. This is a normal source failure, not a technical exception. Keep the valid S5.

All YT are NA. An S outcome is source success, not teacher success. All cases complete96 normal source dispositions and may therefore be sealed before necessary-condition classification. Projected call counts refer only to later software fixtures, not calls performed in this task.

Seven cases test exact E72/F24 acceptance, E71, F23, S23, and separately sufficient totals with one E/F/S family deficit. F/S family minima each sum to24: the F23 and S23 cases necessarily also have a family deficit. Those two total checks cannot be isolated while preserving all family minima.

A later independent reviewer can load the JSON, construct the synthetic boundary behavior, run the real production collector/auditor, and compare the returned status, per-family E/F/S, normal_sources=96, source_phase_sealed=true, allYT=NA and physical call counts. No production import is required to read this oracle. Production need not return the explanatory violation labels.

The expected NOT_FUTILE result says only that source necessary upper bounds are not violated. It does not establish Q, C24, a constructible training recipe or learning efficacy. Real rendering/token counts and hardware timing require their own evidence and are deliberately unspecified here.
