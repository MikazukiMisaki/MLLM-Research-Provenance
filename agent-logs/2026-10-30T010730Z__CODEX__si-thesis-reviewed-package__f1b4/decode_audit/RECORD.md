# SI-U1 evaluation decoding metadata and static interface audit

Status: READ_ONLY_METADATA_CHECK; no scientific execution. Review checkout: SI-U1 evaluator commit `8532275932dabddc498c23a2b6d9a045647542f0` as observed locally. The actual event ledger belongs to the completed run `c2356bbda2b44159a333e7c9d24fc2d4`; its 526,169,989 bytes were streamed and SHA256 `6146bb79faeb572c3674ff9ba907fac4be25eff4c2bd161a3d7cf3156d81c96e` matches the independently accepted analysis. Only event type, operation, arm, decoding flags and generated-token counts were aggregated; no prompt, response string, task identity or result was emitted or saved.

## Actual recorded metadata

The metadata script identified all 5,001 completed generation entries: A 1,713, B 1,661, C 1,627. Every recorded entry had `do_sample=false`, `thinking=false`, `max_new_tokens=16`, and adapter_mode equal to its arm; zero violations. Each recorded generation had five tokens according to its recorded count (min=max=5). These are observations of recorded event fields and a pinned ledger hash, not an independent GPU execution or evidence about unrecorded external calls.

## Pinned execution interface

In the local evaluator source SHA256 `d399ffa95c109b5b83195d3639f24261b7a63a62c1b3fe7c18d59ae695ae037a`, the code validates the decoding flags and cap, forms a public projection and parses a selected ID against the environment's current admissible-action map. An unselected action leads to `selection_failure` and success 0; a horizon timeout also leads to 0, whereas a truncated result raises an error and interrupts the comparison. Terminal success requires `state.done and state.reward > 0`. The runtime source SHA256 `c247df8e1ac8985dc569b67c4ab3f3e2efceef1b837973e861a085a95fd3b2bc` calls generation with the output cap and `do_sample=False`. The public projection source SHA256 `2d7b05d5c230cb45c2ad90c7507c11a5c76ce52f7335548c46a48d78e8842239` calls the P0 prompt renderer; `src/sft/protocol.py` has a four-transition history window and an indexed admissible action list. Code inspection is not equivalent to re-execution; the actual event metadata and prior independent validation provide additional evidence that the live run adhered to the recorded interface.

## Limitations and verification

This is not a complete journal replay, proof of all causality or task validity, a preflight or permission to re-run. It does not verify tokenizer and package closure, the prior training processes or model weights. Use previously accepted supervisor, results and package bindings for those claims, not this small metadata check. Source code was only read and no project modules were imported. `audit_decode_metadata.py` used the standard-library JSON parser and SHA256, printed only aggregates, and completed exit 0; count and mismatch assertions passed. The immutable old ledger and original worktrees were not changed.
