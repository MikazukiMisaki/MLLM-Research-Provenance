# Reset receipt and paired initial-state handoff

Static code review only: no task content was accessed and no model, environment,
GPU, job or production code was invoked or modified. This describes claims
made by the cited worker, not independently authenticated physical behavior.

## Source bindings

| Source | SHA256 |
|---|---|
| `gate-live/effect_ipc.py` | `046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8` |
| `gate-live/environment_step.py` | `1c2df60c671ab408dfd5738192edd0371db848191a904c77e695dc250ff7b00e` |
| `fixed_product_dev/episode.py` | `06922aed662e84c1366624600c361f64ca7fba1ee93daccf83ff8de7a174a21b` |
| `fixed_product_dev/supervise.py` | `0cc7cd3e5b640c4ddc1652f97236891e09b25b7e09857c99fcdc4c5c0965e307` |
| `src/self_improvement/si_p3/contract.py` | `2d7b05d5c230cb45c2ad90c7507c11a5c76ce52f7335548c46a48d78e8842239` |

`gate-live` is `/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live`;
`fixed_product_dev` is `/home/lizening/research-notes/agent-logs/20261118__CODEX__fixed_product_per_arm__private/runtime/fixed_product_dev`;
`contract.py` is under `/home/lizening/.codex/worktrees/parallel-goal-runtime-9dd`.

## Journal structure and sequence

`episode.py:23–28` invokes `Controller.effect('reset', env.reset, convert)`;
the converter returns the actual nested evidence fields `arm`, `state`,
`gamefile` and `candidate_native_reset`. `EffectOwner.returned` writes and
fsyncs a journal row whose relevant logical shape is:

```json
{"kind":"reset_returned","payload":{"owner_seq":0,"evidence":{"arm":"P0","state":{},"gamefile":"...","candidate_native_reset":{}}}}
```

The sample is schematic: the integer is the actual active ticket, not always
zero; the state and capture must have their real validated structure. The
full row also includes schema, row seq, previous digest, monotonic timestamp
and row digest (`effect_ipc.py:18–33,64–74`). `PublicState.to_dict` supplies
`task_id`, `family`, `goal`, `observation`, `valid_actions` as an ordered list,
`done`, `reward` and `truncated` (`contract.py:124–151`). The native-reset
capture contains `won_batch` and `won_batch_type`, not a full raw native state
(`environment_step.py:30–57`).

The child sends `kind='returned'`, the same `seq`, `operation='reset'`, and a
`receipt_sha256` generated after writing the complete JSON line. The receipt
is SHA256 of that complete line **including newline**, not the row's internal
chain `digest`. A parent intending to use the claim must bind the active reset
ticket to the returned seq/op, validate framing/row chain and line receipt,
extract `payload.evidence.state`, and check the expected types and fields.
The existing generic budget channel does not independently establish native
truth merely by matching the receipt. A journal can contain extra non-effect
events; any receipt lookup must be matched to the actual claimed line and
active operation rather than assume a constant row number.

## Original comparison order

In the cited separate-arm implementation the parent reads the first arm's
completed `fixed_product_arm_result.initial_public` and inserts it as
`previous_initial` in the second worker's SHA-bound config
(`supervise.py:348–371,434–468`). In the second worker,
`episode.py:29–42` checks the reset return shape, captured `won_batch=[false]`,
expected game and nonterminal state, serializes the public initial state and
compares it with `previous_initial`. Only afterwards does line 49 reserve and
perform `model_load`. The parent performs an additional comparison after the
second completed arm; it is not the mechanism performing the pre-load check.
The generic old StageBudgetChannel does not itself extract reset state before
ACK. A new parent-mediated pre-load handshake must be explicitly implemented
and tested; it is not provided by the existing `EffectOwner` wire format.

The reset receipt, captured native envelope and state are all produced inside
the child. A valid hash and state comparison establish consistency of those
claims, not independent proof of native ALFWorld execution or equality of
hidden state. Missing/partial/unmatched receipt or failed comparison should
remain a stop/unknown according to the applicable prospective protocol.
